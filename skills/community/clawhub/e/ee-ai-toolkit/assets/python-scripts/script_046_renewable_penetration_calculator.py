# Script 46: Renewable Penetration

renewable = float(input("Renewable Power (MW): "))
total = float(input("Total Generation (MW): "))

penetration = (renewable / total) * 100

print(f"Renewable Penetration = {penetration:.2f}%")
