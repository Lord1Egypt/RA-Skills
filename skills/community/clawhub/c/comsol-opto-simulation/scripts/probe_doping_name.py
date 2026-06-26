#!/usr/bin/env python3
"""Probe COMSOL Semiconductor features for doping."""
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
VENDOR_DIR = SKILL_DIR / "vendor" / "site-packages"
if str(VENDOR_DIR) not in sys.path:
    sys.path.insert(0, str(VENDOR_DIR))

import mph
client = mph.start()
model = client.create('probe_doping')
jm = model.java
comp = jm.component().create('comp1', True)
geom = comp.geom().create('geom1', 2)
rect = geom.feature().create('r1', 'Rectangle')
rect.set('size', ['1000[nm]', '100[nm]'])
geom.run()

semi = comp.physics().create('semi', 'Semiconductor', 'geom1')

print("=== Testing doping feature names ===")
for name in ['Doping', 'DonorDoping', 'AcceptorDoping', 'DopingDistribution',
             'DopantDistribution', 'ImpurityDistribution', 'Dopant']:
    try:
        feat = semi.create(f'test_{name}', name)
        print(f"  {name}: OK")
    except Exception as e:
        err = str(e)
        if '未知特征' in err or 'Unknown' in err:
            print(f"  {name}: UNKNOWN")
        else:
            print(f"  {name}: ERROR - {err[:100]}")

client.clear()
