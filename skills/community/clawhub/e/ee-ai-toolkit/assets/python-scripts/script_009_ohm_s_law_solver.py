# Script 9: Ohm's Law

def ohms_law(V=None, I=None, R=None):
    if V is None:
        return I * R
    elif I is None:
        return V / R
    elif R is None:
        return V / I

print("Solve Ohm's Law")

V = float(input("Enter Voltage (or 0 if unknown): "))
I = float(input("Enter Current (or 0 if unknown): "))
R = float(input("Enter Resistance (or 0 if unknown): "))

if V == 0:
    print("Voltage =", ohms_law(None, I, R))
elif I == 0:
    print("Current =", ohms_law(V, None, R))
elif R == 0:
    print("Resistance =", ohms_law(V, I, None))
