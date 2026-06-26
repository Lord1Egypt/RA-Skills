# Script 83: Harmonic Plot

import matplotlib.pyplot as plt

harmonics = list(map(float, input("Enter harmonic magnitudes: ").split()))

orders = list(range(1, len(harmonics)+1))

plt.bar(orders, harmonics)
plt.xlabel("Harmonic Order")
plt.ylabel("Magnitude")
plt.title("Harmonic Spectrum")
plt.show()
