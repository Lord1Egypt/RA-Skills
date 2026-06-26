# Script 12: Signal Plotter

import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0, 1, 100)
signal = 230 * np.sin(2 * np.pi * 50 * t)

plt.plot(t, signal)
plt.xlabel("Time (s)")
plt.ylabel("Voltage (V)")
plt.title("AC Signal (50 Hz)")
plt.show()
