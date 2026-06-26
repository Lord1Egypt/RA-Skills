# Script 2: Load Forecasting

import numpy as np
from sklearn.linear_model import LinearRegression

# Sample data
days = np.array([1, 2, 3, 4, 5]).reshape(-1, 1)
load = np.array([400, 420, 450, 470, 500])

model = LinearRegression()
model.fit(days, load)

prediction = model.predict([[6]])

print(f"Predicted Load for Day 6: {prediction[0]:.2f} MW")
