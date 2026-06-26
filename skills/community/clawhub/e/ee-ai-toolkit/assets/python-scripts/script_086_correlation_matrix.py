# Script 86: Correlation Matrix

import pandas as pd

data = {
    "Load": [100, 120, 140, 160],
    "Voltage": [220, 225, 230, 228],
    "Temperature": [25, 27, 30, 32]
}

df = pd.DataFrame(data)

print(df.corr())
