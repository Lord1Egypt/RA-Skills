# Script 84: Anomaly Detection

import numpy as np

data = np.array(list(map(float, input("Enter values: ").split())))

mean = np.mean(data)
std = np.std(data)

threshold = 2 * std

anomalies = data[np.abs(data - mean) > threshold]

print("Anomalies:", anomalies)
