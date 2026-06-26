#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Probe COMSOL fin feature properties - v2."""
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
print(f"fin type: {fin.getType()}")
print(f"fin tag: {fin.tag()}")
print(f"fin properties: {list(fin.properties())}")

# Try to get input selection
for sel_name in ['input', 'selinput', 'sel', 'selection', 'obj']:
    try:
        sel = fin.selection(sel_name)
        print(f"  selection('{sel_name}') OK - entities: {sel.entities()}")
    except Exception as e:
        print(f"  selection('{sel_name}') FAILED: {e}")

# Check if fin has input property
for prop in ['input', 'selinput', 'sel']:
    try:
        val = fin.get(prop)
        print(f"  get('{prop}') = {val}")
    except Exception as e:
        print(f"  get('{prop}') FAILED: {e}")

geom.run()
print(f"\nGeometry built successfully.")
print(f"Number of domains: {geom.getNDomains()}")
print(f"Number of boundaries: {geom.getNBoundaries()}")

# Check the built geometry
print(f"\nDomain tags: {list(geom.getDomainTags())}")
print(f"Boundary tags: {list(geom.getBoundaryTags())}")

client.remove(model)
print("Done.")
