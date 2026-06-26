# Script 43: Voltage Profile

import matplotlib.pyplot as plt

voltages = list(map(float, input("Enter bus voltages: ").split()))

plt.plot(voltages, marker='o')
plt.xlabel("Bus Number")
plt.ylabel("Voltage (p.u.)")
plt.title("Voltage Profile")
plt.grid()
plt.show()
