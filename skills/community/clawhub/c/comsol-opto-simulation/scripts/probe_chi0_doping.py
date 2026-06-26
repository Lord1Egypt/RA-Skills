#!/usr/bin/env python3
"""Probe COMSOL chi0 and doping setup."""
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
VENDOR_DIR = SKILL_DIR / "vendor" / "site-packages"
if str(VENDOR_DIR) not in sys.path:
    sys.path.insert(0, str(VENDOR_DIR))

import mph
client = mph.start()
model = client.create('probe_chi_doping')
jm = model.java
comp = jm.component().create('comp1', True)
geom = comp.geom().create('geom1', 2)
rect = geom.feature().create('r1', 'Rectangle')
rect.set('size', ['1000[nm]', '100[nm]'])
geom.run()

semi = comp.physics().create('semi', 'Semiconductor', 'geom1')
mm = semi.create('mat1', 'SemiconductorMaterialModel')
mm.selection().set([1])

print("=== Testing chi0 (lowercase) ===")
for key in ['chi0', 'Chi0', 'CHI0']:
    try:
        mm.set(key, '4.0[eV]')
        print(f"  {key}: OK")
    except Exception as e:
        err = str(e)
        if '未知参数' in err or 'Unknown' in err:
            print(f"  {key}: UNKNOWN")
        else:
            print(f"  {key}: ERROR - {err[:100]}")

# Test material doping
print("\n=== Testing material doping properties ===")
mat = comp.material().create('mat2', 'Common')
mat.selection().set([1])
pg = mat.propertyGroup('def')

for key in ['donor_concentration', 'acceptor_concentration', 
            'Nd', 'Na', 'ND', 'NA', 'n_doping', 'p_doping',
            'numberdensitydonor', 'numberdensityacceptor',
            'donor_number_density', 'acceptor_number_density']:
    try:
        pg.set(key, '1e16[1/cm^3]')
        print(f"  {key}: OK")
    except Exception as e:
        err = str(e)
        if '未知参数' in err or 'Unknown' in err or 'not found' in err.lower():
            print(f"  {key}: UNKNOWN")
        else:
            print(f"  {key}: ERROR - {err[:100]}")

client.clear()
