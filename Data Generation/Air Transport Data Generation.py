#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import streamlit as st
import airportsdata as ad
import numpy as np
from geopy.distance import geodesic
import requests
import pandas as pd
from datetime import datetime
import random
from datetime import datetime


iata_lst = []
airports = ad.load('IATA')
for x in airports:

    iata_lst.append(airports[x]['iata'])
    
src_code = []
dest_code = []
for i in iata_lst:
    for j in iata_lst:
        src_code.append(i)
        dest_code.append(j)
 
date_lst = []
crud = []
def crude():
    api_key = "XGKR1V3H9D2KVG77"
    api_url = "https://www.alphavantage.co/query"
    function = "TIME_SERIES_DAILY_ADJUSTED"
    symbol = "CL" #Crude Oil price
    outputsize = "full" 
    payload = {'function': function, 'symbol': symbol, 'apikey': api_key, 'outputsize': outputsize}
    response = requests.get(api_url, params=payload)
    data = response.json()
    df = pd.DataFrame.from_dict(data['Time Series (Daily)'], orient='index')
    df.columns = ['open', 'high', 'low', 'close', 'adjusted_close', 'volume', 'dividend_amount', 'split_coefficient']
    df = df.apply(pd.to_numeric)
    df.drop(['high','low', 'close', 'adjusted_close', 'volume', 'dividend_amount', 'split_coefficient'],axis = 1,inplace = True)
    df['date'] = df.index
    df = df[:1000]
    for x in range(0,len(df['date'])):
        date_lst.append(df['date'][x])
        crud.append(df['open'][x])
    return date_lst,crud



x,y = crude()

date_lst_final = []
crud_final = []
wt = []
#print(random.choice(crude()))
i=0
while i<41977441:
    i+=1
    num = random.randrange(1000)
    date_lst_final.append(x[num])
    crud_final.append(y[num])
    wt.append(random.randrange(50))


final_df = pd.DataFrame(list(zip(date_lst_final,wt,src_code,dest_code,crud_final)),columns=["Date","Weight of Package","Source Airport", "Destination Airport","Crude Oil Price"])


dist = []
airports = ad.load('IATA')
for i in range(0,len(final_df['Source Airport'])):
    src_lat = airports[final_df["Source Airport"][i]]['lat']
    src_lon = airports[final_df["Source Airport"][i]]['lon']
    dest_lat = airports[final_df["Destination Airport"][i]]['lat']
    dest_lon = airports[final_df["Destination Airport"][i]]['lon']
    dist.append(geodesic((src_lat,src_lon), (dest_lat,dest_lon)).km)
    
final_df['Distance'] = dist



final_df.to_csv("Sheet1.csv")


    




