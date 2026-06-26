# Script 89: Energy Breakdown

import matplotlib.pyplot as plt

labels = ["Lighting", "HVAC", "Machines"]
values = list(map(float, input("Enter consumption values: ").split()))

plt.pie(values, labels=labels, autopct='%1.1f%%')
plt.title("Energy Consumption")
plt.show()
