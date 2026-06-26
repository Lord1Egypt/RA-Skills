# Script 60: Single-Line Data

equipment = []

n = int(input("Number of components: "))

for i in range(n):
    name = input("Component name: ")
    rating = input("Rating: ")
    equipment.append((name, rating))

print("\nSingle-Line Data:")
for item in equipment:
    print(f"{item[0]} - {item[1]}")
