# Script 37: Series & Parallel Resistance

import math

choice = input("Series or Parallel (s/p): ").lower()

values = list(map(float, input("Enter resistances (space separated): ").split()))

if choice == "s":
    result = sum(values)
elif choice == "p":
    result = 1 / sum(1/r for r in values)

print(f"Equivalent Resistance = {result:.2f} Ohm")
