#!/usr/bin/env python3
"""Probe COMSOL SemiconductorMaterialModel for reference energy / electron affinity."""
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
VENDOR_DIR = SKILL_DIR / "vendor" / "site-packages"
if str(VENDOR_DIR) not in sys.path:
    sys.path.insert(0, str(VENDOR_DIR))

import mph
client = mph.start()
model = client.create('probe_model4')
jm = model.java
comp = jm.component().create('comp1', True)
geom = comp.geom().create('geom1', 2)
rect = geom.feature().create('r1', 'Rectangle')
rect.set('size', ['1000[nm]', '100[nm]'])
geom.run()

semi = comp.physics().create('semi', 'Semiconductor', 'geom1')
mm = semi.create('mat1', 'SemiconductorMaterialModel')
mm.selection().set([1])

# Try reference energy related
print("=== Testing reference energy variants ===")
for key in ['Eref_sb', 'Eref', 'Eref_sb_mat', 'eref', 'E0', 'Vref',
            'Phiref', 'phiref', 'Phi0', 'phi0', 'WF', 'wf',
            'WorkFunction', 'work_function']:
    try:
        mm.set(key, '4.0')
        print(f"  {key}: OK")
    except Exception as e:
        err = str(e)
        if '未知参数' in err or 'Unknown' in err:
            print(f"  {key}: UNKNOWN")
        else:
            print(f"  {key}: ERROR - {err[:120]}")

# Also try to read description of known properties
print("\n=== Property descriptions ===")
for prop in ['Eg0', 'epsilonr', 'mun', 'mup']:
    try:
        desc = mm.propDescription(prop)
        print(f"  {prop}: {desc}")
    except Exception as e:
        print(f"  {prop}: no desc - {e}")

client.clear()
