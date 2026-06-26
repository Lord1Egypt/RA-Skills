# Script 48: Smart Meter Aggregator

import pandas as pd

data = {
    "Hour": range(1, 6),
    "Load": [100, 120, 110, 130, 140]
}

df = pd.DataFrame(data)

total = df["Load"].sum()
average = df["Load"].mean()

print("Total Load =", total)
print("Average Load =", average)
