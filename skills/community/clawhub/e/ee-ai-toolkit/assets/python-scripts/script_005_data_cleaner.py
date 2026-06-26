# Script 5: Data Cleaner

import pandas as pd

data = {
    "Voltage": [220, None, 230, 225],
    "Current": [10, 12, None, 11]
}

df = pd.DataFrame(data)

# Fill missing values
df = df.fillna(df.mean())

print("Cleaned Data:")
print(df)
