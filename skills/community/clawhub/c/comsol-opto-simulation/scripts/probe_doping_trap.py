#!/usr/bin/env python3
"""Probe COMSOL SemiconductorMaterialModel for doping parameters and TrapAssistedRecombination."""
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
VENDOR_DIR = SKILL_DIR / "vendor" / "site-packages"
if str(VENDOR_DIR) not in sys.path:
    sys.path.insert(0, str(VENDOR_DIR))

import mph
client = mph.start()
model = client.create('probe_doping2')
jm = model.java
comp = jm.component().create('comp1', True)
geom = comp.geom().create('geom1', 2)
rect = geom.feature().create('r1', 'Rectangle')
rect.set('size', ['1000[nm]', '100[nm]'])
geom.run()

semi = comp.physics().create('semi', 'Semiconductor', 'geom1')
mm = semi.create('mat1', 'SemiconductorMaterialModel')
mm.selection().set([1])

print("=== SemiconductorMaterialModel properties ===")
for prop in mm.properties():
    print(f"  {prop}")

print("\n=== Testing doping-related SET ===")
for key in ['Nd', 'Na', 'ND', 'NA', 'Ndoping', 'Nadoping', 
            'donor_concentration', 'acceptor_concentration',
            'Nd_cm3', 'Na_cm3', 'n_doping', 'p_doping']:
    try:
        mm.set(key, '1e16')
        print(f"  {key}: OK")
    except Exception as e:
        err = str(e)
        if '未知参数' in err or 'Unknown' in err:
            print(f"  {key}: UNKNOWN")
        else:
            print(f"  {key}: ERROR - {err[:100]}")

# Test TrapAssistedRecombination
print("\n=== Testing TrapAssistedRecombination properties ===")
trap = semi.create('trap1', 'TrapAssistedRecombination')
trap.selection().set([1])
for prop in trap.properties():
    print(f"  {prop}")

print("\n=== Testing TrapAssistedRecombination SET ===")
for key in ['taun', 'taup', 'tau_n', 'tau_p', 'Et', 'Etrap', 
            'capture_cross_section_n', 'capture_cross_section_p',
            'Cn', 'Cp', 'ctn', 'ctp']:
    try:
        trap.set(key, '1e-9')
        print(f"  {key}: OK")
    except Exception as e:
        err = str(e)
        if '未知参数' in err or 'Unknown' in err:
            print(f"  {key}: UNKNOWN")
        else:
            print(f"  {key}: ERROR - {err[:100]}")

client.clear()
