# Script 54: Breaker Selection

load_current = float(input("Load Current (A): "))

breaker = load_current * 1.25

print(f"Recommended Breaker Rating ≈ {breaker:.2f} A")
