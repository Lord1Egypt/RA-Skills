# Script 82: Voltage Trend Analyzer

import matplotlib.pyplot as plt

voltages = list(map(float, input("Enter voltage values: ").split()))

plt.plot(voltages)
plt.xlabel("Time")
plt.ylabel("Voltage (V)")
plt.title("Voltage Trend")
plt.grid()
plt.show()
