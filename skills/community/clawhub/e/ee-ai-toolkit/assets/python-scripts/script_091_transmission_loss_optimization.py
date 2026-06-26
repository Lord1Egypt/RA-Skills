# Script 91: Loss Optimization

import numpy as np

currents = np.array([100, 90, 80, 70])
R = 0.5

losses = currents**2 * R

for i, l in zip(currents, losses):
    print(f"Current {i} A -> Loss {l:.2f} W")

best = currents[np.argmin(losses)]
print("Optimal Current for Minimum Loss:", best)
