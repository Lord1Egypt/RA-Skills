#!/usr/bin/env python3
"""Probe COMSOL SemiconductorMaterialModel for electron affinity and mobility."""
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
VENDOR_DIR = SKILL_DIR / "vendor" / "site-packages"
if str(VENDOR_DIR) not in sys.path:
    sys.path.insert(0, str(VENDOR_DIR))

import mph
client = mph.start()
model = client.create('probe_model3')
jm = model.java
comp = jm.component().create('comp1', True)
geom = comp.geom().create('geom1', 2)
rect = geom.feature().create('r1', 'Rectangle')
rect.set('size', ['1000[nm]', '100[nm]'])
geom.run()

semi = comp.physics().create('semi', 'Semiconductor', 'geom1')
mm = semi.create('mat1', 'SemiconductorMaterialModel')
mm.selection().set([1])

# Get all properties and filter for chi/affinity
print("=== All properties ===")
for prop in mm.properties():
    if 'chi' in prop.lower() or 'aff' in prop.lower() or 'ea' in prop.lower() or 'ref' in prop.lower():
        print(f"  {prop}")

print("\n=== Testing Chi variants ===")
for key in ['Chi0', 'Chi', 'chi0', 'chi', 'EA0', 'EA', 'ea0', 'ea',
            'ElectronAffinity', 'electron_affinity', 'affinity']:
    try:
        mm.set(key, '4.0')
        print(f"  {key}: OK")
    except Exception as e:
        err = str(e)
        if '未知参数' in err or 'Unknown' in err or 'not found' in err.lower():
            print(f"  {key}: UNKNOWN")
        else:
            print(f"  {key}: ERROR - {err[:100]}")

# Also test mobility variants
print("\n=== Testing mobility variants ===")
for key in ['mun', 'mup', 'mu_n', 'mu_p', 'mu_e', 'mu_h',
            'mobility_n', 'mobility_p', 'MobilityElectron', 'MobilityHole']:
    try:
        mm.set(key, '100')
        print(f"  {key}: OK")
    except Exception as e:
        err = str(e)
        if '未知参数' in err or 'Unknown' in err:
            print(f"  {key}: UNKNOWN")
        else:
            print(f"  {key}: ERROR - {err[:100]}")

client.clear()
