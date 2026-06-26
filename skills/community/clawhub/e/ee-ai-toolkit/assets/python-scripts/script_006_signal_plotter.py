# Script 6: Signal Plotter

import matplotlib.pyplot as plt

time = [0, 1, 2, 3, 4]
voltage = [220, 225, 230, 228, 227]

plt.plot(time, voltage)
plt.xlabel("Time")
plt.ylabel("Voltage (V)")
plt.title("Voltage Signal")
plt.show()
