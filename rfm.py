import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("data.csv", encoding= 'unicode_escape')
df.head

df.apply(lambda x :sum(x.isnull())/len(x), axis=0)

df['date'] = [x.split(' ')[0] for x in df["InvoiceDate"]]
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.to_period('M')
df[['date', 'month']]

R_value = df.groupby('CustomerID')['date'].max()
R_value = (df['date'].max() - R_value).dt.days
F_value = df.groupby('CustomerID')['InvoiceNo'].nunique()
df['amount'] = df['Quantity'] * df['UnitPrice']
M_value = df.groupby('CustomerID')['InvoiceNo'].nunique()
M_value = df.groupby('CustomerID')['amount'].sum()
R_bins = [0, 30, 90, 180, 360, 720]
F_bins = [1, 2, 5, 10, 20, 5000]
M_bins = [0, 500, 2000, 5000, 10000, 200000]
R_score = pd.cut(R_value, R_bins, labels=[5,4,3,2,1], right=False)
F_score = pd.cut(F_value, F_bins, labels=[1,2,3,4,5], right=False)
M_score = pd.cut(M_value, M_bins, labels=[1,2,3,4,5], right=False)

rfm = pd.concat([R_score, F_score, M_score], axis=1)
rfm.rename(columns={'date': 'R_score', 'InvoiceNo': 'F_score', 'amount': 'M_score'}, inplace=True)
rfm['R_score'] = rfm['R_score'].astype('float')
rfm['F_score'] = rfm['F_score'].astype('float')
rfm['M_score'] = rfm['M_score'].astype('float')
rfm.describe()

rfm['R'] = np.where(rfm['R_score'] > 3.82, '高', '低')
rfm['F'] = np.where(rfm['F_score'] > 2.03, '高', '低')
rfm['M'] = np.where(rfm['M_score'] > 1.89, '高', '低')
rfm

rfm['RFM'] = rfm['R'] + rfm['F'] + rfm['M']

def rfm2grade(x):
    if x == '高高高':
        return 'VIP'
    elif x == "高低高":
        return 'High Value Customer'
    elif x == "低高高":
        return 'Medium Value Customer'
    elif x == '低低高':
        return 'Lost Customer'
    elif x == "高高低":
        return 'Medium Value Customer'
    else:
        return 'Low Value Customer'

rfm['Customer_segment'] = rfm['RFM'].apply(rfm2grade)
rfm

rfm['Customer_segment'].value_counts().plot(kind='pie',
                                            figsize=(15, 9),
                                            autopct='%.1f%%',
                                            title='RFM',
                                            textprops={'fontsize': 8},
                                            subplots=True)
plt.legend(loc=2, bbox_to_anchor=(1.05, 1.0), borderaxespad=0)