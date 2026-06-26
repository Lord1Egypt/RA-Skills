#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Probe COMSOL selection timing."""
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

# Create rectangles
r1 = geom.feature().create('r1', 'Rectangle')
r1.set("size", ["1000[nm]", "100[nm]"])
r1.set("pos", ["0[nm]", "0[nm]"])

r2 = geom.feature().create('r2', 'Rectangle')
r2.set("size", ["1000[nm]", "100[nm]"])
r2.set("pos", ["0[nm]", "100[nm]"])

# Try creating selection BEFORE geom.run()
print("Creating selections BEFORE geom.run():")
try:
    sel_top = geom.selection().create('sel_top', 'Box')
    sel_top.set('xmin', '0[nm]')
    sel_top.set('xmax', '1000[nm]')
    sel_top.set('ymin', '199[nm]')
    sel_top.set('ymax', '201[nm]')
    sel_top.set('condition', 'inside')
    print("  sel_top (Box): OK")
except Exception as e:
    print(f"  sel_top (Box): FAILED - {e}")

fin = geom.feature('fin')
fin.set('action', 'union')

# Try creating selection after fin but before run
print("\nCreating selections after fin but before run:")
try:
    sel_bottom = geom.selection().create('sel_bottom', 'Box')
    sel_bottom.set('xmin', '0[nm]')
    sel_bottom.set('xmax', '1000[nm]')
    sel_bottom.set('ymin', '-1[nm]')
    sel_bottom.set('ymax', '1[nm]')
    sel_bottom.set('condition', 'inside')
    print("  sel_bottom (Box): OK")
except Exception as e:
    print(f"  sel_bottom (Box): FAILED - {e}")

geom.run()
print("\nAfter geom.run():")
print(f"  Number of domains: {geom.getNDomains()}")
print(f"  Number of boundaries: {geom.getNBoundaries()}")

# Try using mph API to get info
print("\nmph API exploration:")
try:
    # Try to get selections
    sel_tags = list(geom.selection().tags())
    print(f"  Selection tags: {sel_tags}")
except Exception as e:
    print(f"  Getting selection tags FAILED: {e}")

client.remove(model)
print("\nDone.")
