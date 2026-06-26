# Script 36: Cable Sizing

I = float(input("Load Current (A): "))

if I < 20:
    size = "2.5 mm²"
elif I < 40:
    size = "6 mm²"
elif I < 70:
    size = "10 mm²"
else:
    size = "16 mm² or higher"

print("Recommended Cable Size:", size)
