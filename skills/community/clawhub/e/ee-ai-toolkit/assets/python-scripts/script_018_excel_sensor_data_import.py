# Script 18: Excel Data Import

import pandas as pd

file = input("Enter Excel file name: ")

try:
    df = pd.read_excel(file)
    print(df.head())
except:
    print("Error loading Excel file.")
