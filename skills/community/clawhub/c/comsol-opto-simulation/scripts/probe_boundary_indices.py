#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Probe COMSOL all boundary indices."""
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
VENDOR_DIR = SKILL_DIR / "vendor" / "site-packages"
if str(VENDOR_DIR) not in sys.path:
    sys.path.insert(0, str(VENDOR_DIR))

import mph
from jpype import JInt

client = mph.start()
model = client.create("test")
jm = model.java
comp = jm.component().create("comp1", True)
geom = comp.geom().create("geom1", 2)

# Create two rectangles stacked: r1 at y=[0,100], r2 at y=[100,200]
r1 = geom.feature().create('r1', 'Rectangle')
r1.set("size", ["1000[nm]", "100[nm]"])
r1.set("pos", ["0[nm]", "0[nm]"])

r2 = geom.feature().create('r2', 'Rectangle')
r2.set("size", ["1000[nm]", "100[nm]"])
r2.set("pos", ["0[nm]", "100[nm]"])

fin = geom.feature('fin')
fin.set('action', 'union')
geom.run()

print(f"Geometry: {geom.getNDomains()} domains, {geom.getNBoundaries()} boundaries")

# Test boundary selections
boundary_tests = [
    ("bottom", '0[nm]', '1000[nm]', '-1[nm]', '1[nm]'),
    ("internal", '0[nm]', '1000[nm]', '99[nm]', '101[nm]'),
    ("top", '0[nm]', '1000[nm]', '199[nm]', '201[nm]'),
    ("left", '-1[nm]', '1[nm]', '-1[nm]', '201[nm]'),
    ("right", '999[nm]', '1001[nm]', '-1[nm]', '201[nm]'),
]

results = {}
for name, xmin, xmax, ymin, ymax in boundary_tests:
    sel = comp.selection().create(f'sel_{name}', 'Box')
    sel.set('xmin', xmin)
    sel.set('xmax', xmax)
    sel.set('ymin', ymin)
    sel.set('ymax', ymax)
    sel.set('condition', 'inside')
    sel.set('entitydim', JInt(1))
    
    ents = list(sel.entities())
    results[name] = ents
    print(f"  {name}: boundaries {ents}")
    comp.selection().remove(f'sel_{name}')

# Also test with larger boxes that might capture multiple boundaries
print("\nTesting side boundaries separately:")
side_tests = [
    ("left_only", '-1[nm]', '1[nm]', '0[nm]', '100[nm]'),   # left side of r1
    ("right_only", '999[nm]', '1001[nm]', '0[nm]', '100[nm]'), # right side of r1
    ("left_r2", '-1[nm]', '1[nm]', '100[nm]', '200[nm]'),    # left side of r2
    ("right_r2", '999[nm]', '1001[nm]', '100[nm]', '200[nm]'), # right side of r2
]

for name, xmin, xmax, ymin, ymax in side_tests:
    sel = comp.selection().create(f'sel_{name}', 'Box')
    sel.set('xmin', xmin)
    sel.set('xmax', xmax)
    sel.set('ymin', ymin)
    sel.set('ymax', ymax)
    sel.set('condition', 'inside')
    sel.set('entitydim', JInt(1))
    
    ents = list(sel.entities())
    print(f"  {name}: boundaries {ents}")
    comp.selection().remove(f'sel_{name}')

client.remove(model)
print("\nDone.")
