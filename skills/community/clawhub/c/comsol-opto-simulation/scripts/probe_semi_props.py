#!/usr/bin/env python3
"""Probe COMSOL SemiconductorMaterialModel property names."""
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
VENDOR_DIR = SKILL_DIR / "vendor" / "site-packages"
if str(VENDOR_DIR) not in sys.path:
    sys.path.insert(0, str(VENDOR_DIR))

import mph
client = mph.start()
model = client.create('probe_model')
jm = model.java
comp = jm.component().create('comp1', True)
geom = comp.geom().create('geom1', 2)
rect = geom.feature().create('r1', 'Rectangle')
rect.set('size', ['1000[nm]', '100[nm]'])
geom.run()

semi = comp.physics().create('semi', 'Semiconductor', 'geom1')
mm = semi.create('mat1', 'SemiconductorMaterialModel')
mm.selection().set([1])

# List all available properties
print("=== SemiconductorMaterialModel properties ===")
for prop in mm.properties():
    print(prop)

# Try to list via feature names
print("\n=== Feature names ===")
for tag in mm.feature().tags():
    print(tag)

print("\n=== Direct property access attempts ===")
for key in ['Eg0', 'Eg', 'Chi0', 'Chi', 'mun0', 'mun', 'mup0', 'mup',
            'Nc0', 'Nc', 'Nv0', 'Nv', 'epsilonr', 'relpermittivity']:
    try:
        val = mm.get(key)
        print(f"  {key}: {val}")
    except Exception as e:
        print(f"  {key}: ERROR - {e}")

client.clear()
