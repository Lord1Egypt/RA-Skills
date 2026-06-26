#!/usr/bin/env python3
"""Probe COMSOL SemiconductorMaterialModel property SET methods."""
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
VENDOR_DIR = SKILL_DIR / "vendor" / "site-packages"
if str(VENDOR_DIR) not in sys.path:
    sys.path.insert(0, str(VENDOR_DIR))

import mph
client = mph.start()
model = client.create('probe_model2')
jm = model.java
comp = jm.component().create('comp1', True)
geom = comp.geom().create('geom1', 2)
rect = geom.feature().create('r1', 'Rectangle')
rect.set('size', ['1000[nm]', '100[nm]'])
geom.run()

semi = comp.physics().create('semi', 'Semiconductor', 'geom1')
mm = semi.create('mat1', 'SemiconductorMaterialModel')
mm.selection().set([1])

# Test SET for each property
print("=== Testing SET methods ===")
for key in ['Eg0', 'Chi0', 'mun0', 'mup0', 'Nc0', 'Nv0', 'epsilonr',
            'Eg', 'Chi', 'mun', 'mup', 'Nc', 'Nv']:
    try:
        mm.set(key, '1')
        print(f"  {key}: OK")
    except Exception as e:
        err = str(e)
        if '未知参数' in err or 'Unknown' in err:
            print(f"  {key}: UNKNOWN PARAMETER")
        else:
            print(f"  {key}: ERROR - {err[:80]}")

client.clear()
