# Script 88: Substation Monitoring

import matplotlib.pyplot as plt

load = [100, 110, 105, 115, 120]
voltage = [220, 222, 219, 221, 223]

plt.plot(load, label="Load")
plt.plot(voltage, label="Voltage")

plt.legend()
plt.title("Substation Monitoring")
plt.show()
