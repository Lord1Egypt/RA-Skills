# Script 56: Transformer Sizing

load_kw = float(input("Load (kW): "))
pf = float(input("Power Factor: "))

kva = load_kw / pf

print(f"Required Transformer Size ≈ {kva:.2f} kVA")
