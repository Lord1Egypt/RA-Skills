#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Probe COMSOL fin feature properties."""
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
print(f"fin tags: {list(fin.tags())}")
print(f"fin properties: {list(fin.properties())}")

# Try setting using selection
print("\nTrying to set input selection...")
try:
    fin.selection('input').set(['r1', 'r2'])
    print("  input.set OK")
except Exception as e:
    print(f"  input.set FAILED: {e}")

# Try alternative property names
try:
    fin.set('input', ['r1', 'r2'])
    print("  set('input') OK")
except Exception as e:
    print(f"  set('input') FAILED: {e}")

try:
    fin.set('selinput', ['r1', 'r2'])
    print("  set('selinput') OK")
except Exception as e:
    print(f"  set('selinput') FAILED: {e}")

# Check if there's a selection method
print("\nChecking selection methods...")
for sel_name in ['input', 'selinput', 'sel', 'selection']:
    try:
        sel = fin.selection(sel_name)
        print(f"  selection('{sel_name}') OK")
    except Exception as e:
        print(f"  selection('{sel_name}') FAILED: {e}")

geom.run()
print("\nGeometry built successfully.")
print(f"Number of domains: {geom.getNDomains()}")
print(f"Number of boundaries: {geom.getNBoundaries()}")

client.remove(model)
print("Done.")
