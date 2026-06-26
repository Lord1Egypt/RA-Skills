# Script 94: Battery Dispatch

load = [50, 80, 120, 90]
threshold = 100

for i, l in enumerate(load):
    if l > threshold:
        print(f"Hour {i}: Discharge Battery")
    else:
        print(f"Hour {i}: Charge Battery")
