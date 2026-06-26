# Script 16: JSON Loader

import json

file = input("Enter JSON file name: ")

try:
    with open(file, 'r') as f:
        data = json.load(f)
        print("Circuit Parameters:")
        print(data)
except:
    print("Error loading file.")
