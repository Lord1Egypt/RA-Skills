# Script 11: CSV Data Reader

import pandas as pd

file = input("Enter CSV file name: ")

try:
    df = pd.read_csv(file)
    print("Data Preview:")
    print(df.head())

    print("\nSummary:")
    print(df.describe())
except:
    print("Error reading file.")
