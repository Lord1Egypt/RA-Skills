#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Probe COMSOL Box selection setup for boundaries."""
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
VENDOR_DIR = SKILL_DIR / "vendor" / "site-packages"
if str(VENDOR_DIR) not in sys.path:
    sys.path.insert(0, str(VENDOR_DIR))

import mph

client = mph.start()
model = client.create("test")
jm = model.java
comp = jm.component().create("comp1", True)
geom = comp.geom().create("geom1", 2)

# Create two rectangles
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

# Create Box selection at component level
sel_top = comp.selection().create('sel_top', 'Box')
sel_top.set('xmin', '0[nm]')
sel_top.set('xmax', '1000[nm]')
sel_top.set('ymin', '199[nm]')
sel_top.set('ymax', '201[nm]')
sel_top.set('condition', 'inside')

# Need to set the geometric entity level for the selection
print(f"\nSelection properties: {list(sel_top.properties())}")

# Try to set entity dimension
for dim_prop in ['entitydim', 'geomdim', 'dimension']:
    try:
        sel_top.set(dim_prop, 1)  # 1 = edges/boundaries in 2D
        print(f"  set {dim_prop}=1: OK")
    except Exception as e:
        print(f"  set {dim_prop}=1: FAILED - {e}")

# Try to set geometry
for geom_prop in ['geom', 'geometry']:
    try:
        sel_top.set(geom_prop, 'geom1')
        print(f"  set {geom_prop}='geom1': OK")
    except Exception as e:
        print(f"  set {geom_prop}='geom1': FAILED - {e}")

# Try to get entities
try:
    ents = list(sel_top.entities())
    print(f"\n  entities: {ents}")
except Exception as e:
    print(f"\n  entities FAILED: {e}")

try:
    ents = list(sel_top.entities(1))  # dimension 1
    print(f"  entities(1): {ents}")
except Exception as e:
    print(f"  entities(1) FAILED: {e}")

client.remove(model)
print("\nDone.")
