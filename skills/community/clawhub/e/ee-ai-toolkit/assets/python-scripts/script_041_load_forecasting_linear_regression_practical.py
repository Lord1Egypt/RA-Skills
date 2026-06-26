# Script 41: Load Forecasting

import numpy as np
from sklearn.linear_model import LinearRegression

# Example historical data
hours = np.array(range(1, 11)).reshape(-1, 1)
load = np.array([100, 120, 130, 150, 170, 160, 180, 200, 210, 220])

model = LinearRegression()
model.fit(hours, load)

future_hour = int(input("Enter next hour to predict: "))
prediction = model.predict([[future_hour]])

print(f"Predicted Load = {prediction[0]:.2f} MW")
