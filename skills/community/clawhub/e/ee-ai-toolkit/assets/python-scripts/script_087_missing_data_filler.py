# Script 87: Missing Data Filler

import pandas as pd
import numpy as np

data = [100, 120, None, 140, None, 160]

series = pd.Series(data)

filled = series.interpolate()

print("Filled Data:")
print(filled)
