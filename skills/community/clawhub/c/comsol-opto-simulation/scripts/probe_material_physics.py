#!/usr/bin/env python3
"""Test if SemiconductorMaterialModel reads electronaffinity from material."""
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
VENDOR_DIR = SKILL_DIR / "vendor" / "site-packages"
if str(VENDOR_DIR) not in sys.path:
    sys.path.insert(0, str(VENDOR_DIR))

import mph
client = mph.start()
model = client.create('probe_model6')
jm = model.java
comp = jm.component().create('comp1', True)
geom = comp.geom().create('geom1', 2)
rect = geom.feature().create('r1', 'Rectangle')
rect.set('size', ['1000[nm]', '100[nm]'])
geom.run()

# Create material with electronaffinity
mat = comp.material().create('mat1', 'Common')
mat.selection().set([1])
pg = mat.propertyGroup('def')
pg.set('electronaffinity', '4.5[eV]')
pg.set('bandgap', '1.1[eV]')
pg.set('relpermittivity', '12')

# Create semiconductor physics
semi = comp.physics().create('semi', 'Semiconductor', 'geom1')
mm = semi.create('mat1_model', 'SemiconductorMaterialModel')
mm.selection().set([1])

# Set only mobility and DOS in physics model
mm.set('mun', '1000[cm^2/(V*s)]')
mm.set('mup', '500[cm^2/(V*s)]')
mm.set('Nc', '1e19[1/cm^3]')
mm.set('Nv', '1e19[1/cm^3]')
mm.set('epsilonr', '12')

print("=== Material assigned, physics model created ===")
print("  electronaffinity in material: 4.5 eV")
print("  bandgap in material: 1.1 eV")
print("  Physics model: mun=1000, mup=500, Nc=1e19, Nv=1e19, epsilonr=12")

# Try to build study and solve to see if COMSOL accepts this
study = jm.study().create('std1')
stat = study.feature().create('stat1', 'Stationary')
stat.set('useinitsol', 'off')

mesh = comp.mesh().create('mesh1')
mesh.feature().create('size1', 'Size')
mesh.feature('size1').set('hauto', '5')
mesh.run()

print("\n=== Attempting solve... ===")
try:
    study.run()
    print("  SOLVE: OK")
except Exception as e:
    err = str(e)
    if '未知参数' in err or 'Unknown' in err:
        print(f"  SOLVE: FAILED - {err[:200]}")
    else:
        print(f"  SOLVE: ERROR - {err[:200]}")

client.clear()
