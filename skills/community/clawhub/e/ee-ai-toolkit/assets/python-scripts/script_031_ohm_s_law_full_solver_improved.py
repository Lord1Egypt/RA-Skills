# Script 31: Ohm’s Law Solver (Improved)

def solve_ohms(V=None, I=None, R=None):
    if V is None:
        return I * R
    elif I is None:
        return V / R
    elif R is None:
        return V / I

V = float(input("Voltage (0 if unknown): "))
I = float(input("Current (0 if unknown): "))
R = float(input("Resistance (0 if unknown): "))

if V == 0:
    print("Voltage =", solve_ohms(None, I, R))
elif I == 0:
    print("Current =", solve_ohms(V, None, R))
elif R == 0:
    print("Resistance =", solve_ohms(V, I, None))
