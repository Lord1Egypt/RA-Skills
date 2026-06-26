# Script 40: Parameter Sweep

import numpy as np
import matplotlib.pyplot as plt

V = 230
I = np.linspace(1, 50, 50)

P = V * I

plt.plot(I, P)
plt.xlabel("Current (A)")
plt.ylabel("Power (W)")
plt.title("Power vs Current")
plt.show()
