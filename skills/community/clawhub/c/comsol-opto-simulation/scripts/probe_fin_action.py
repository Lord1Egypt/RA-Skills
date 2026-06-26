#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Probe COMSOL fin action property."""
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

# Create two adjacent rectangles
r1 = geom.feature().create('r1', 'Rectangle')
r1.set("size", ["1000[nm]", "100[nm]"])
r1.set("pos", ["0[nm]", "0[nm]"])

r2 = geom.feature().create('r2', 'Rectangle')
r2.set("size", ["1000[nm]", "100[nm]"])
r2.set("pos", ["0[nm]", "100[nm]"])

fin = geom.feature('fin')
print(f"fin properties: {list(fin.properties())}")

# Try setting action property
for action_val in ['union', 'assembly', 'formunion']:
    try:
        fin.set('action', action_val)
        print(f"  set action='{action_val}' OK")
    except Exception as e:
        print(f"  set action='{action_val}' FAILED: {e}")

# Try to read current action value
try:
    action_val = fin.getString('action')
    print(f"  Current action: {action_val}")
except Exception as e:
    print(f"  getString('action') FAILED: {e}")

try:
    action_val = fin.propertyString('action')
    print(f"  Current action (propertyString): {action_val}")
except Exception as e:
    print(f"  propertyString('action') FAILED: {e}")

geom.run()
print(f"\nAfter setting action=union:")
print(f"Number of domains: {geom.getNDomains()}")
print(f"Number of boundaries: {geom.getNBoundaries()}")

client.remove(model)
print("Done.")
