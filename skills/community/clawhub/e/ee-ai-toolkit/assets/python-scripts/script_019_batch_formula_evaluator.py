# Script 19: Batch Calculations

import numpy as np

voltages = np.array([220, 230, 240])
currents = np.array([10, 12, 11])

power = voltages * currents

print("Power values:", power)
