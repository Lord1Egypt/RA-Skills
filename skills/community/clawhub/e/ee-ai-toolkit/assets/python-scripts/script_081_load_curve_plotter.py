# Script 81: Load Curve Plotter

import matplotlib.pyplot as plt

loads = list(map(float, input("Enter hourly load values: ").split()))

plt.plot(loads, marker='o')
plt.xlabel("Time (Hour)")
plt.ylabel("Load (MW)")
plt.title("Load Curve")
plt.grid()
plt.show()
