#!/usr/bin/env python3
"""Probe COMSOL material propertyGroup for electron affinity."""
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
VENDOR_DIR = SKILL_DIR / "vendor" / "site-packages"
if str(VENDOR_DIR) not in sys.path:
    sys.path.insert(0, str(VENDOR_DIR))

import mph
client = mph.start()
model = client.create('probe_model5')
jm = model.java
comp = jm.component().create('comp1', True)
geom = comp.geom().create('geom1', 2)
rect = geom.feature().create('r1', 'Rectangle')
rect.set('size', ['1000[nm]', '100[nm]'])
geom.run()

# Create material
mat = comp.material().create('mat1', 'Common')
mat.selection().set([1])
pg = mat.propertyGroup('def')

print("=== Material propertyGroup properties ===")
for prop in pg.properties():
    print(f"  {prop}")

print("\n=== Testing material properties for semiconductor ===")
for key in ['electronaffinity', 'electron_affinity', 'EA', 'ea', 'chi', 'Chi',
            'bandgap', 'Eg', 'relpermittivity', 'permeability']:
    try:
        pg.set(key, '4.0')
        print(f"  {key}: OK")
    except Exception as e:
        err = str(e)
        if '未知参数' in err or 'Unknown' in err or 'not found' in err.lower():
            print(f"  {key}: UNKNOWN")
        else:
            print(f"  {key}: ERROR - {err[:120]}")

# Also test Semiconductor module material model again with Eref_sb
print("\n=== Testing Eref_sb as electron affinity substitute ===")
semi = comp.physics().create('semi', 'Semiconductor', 'geom1')
mm = semi.create('mat2', 'SemiconductorMaterialModel')
mm.selection().set([1])

for key in ['Eref_sb', 'Eref_sb_mat']:
    try:
        mm.set(key, '4.0[eV]')
        print(f"  {key} with unit: OK")
    except Exception as e:
        err = str(e)
        print(f"  {key} with unit: ERROR - {err[:120]}")

client.clear()
