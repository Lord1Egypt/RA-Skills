#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Probe COMSOL selection via model.java.selection()."""
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

# Try creating selections at model level
print("Creating selections at model level:")
try:
    sel = jm.selection().create('sel_test', 'Explicit')
    print("  Explicit: OK")
    jm.selection().remove('sel_test')
except Exception as e:
    print(f"  Explicit: FAILED - {e}")

try:
    sel = jm.selection().create('sel_test2', 'Box')
    print("  Box: OK")
    jm.selection().remove('sel_test2')
except Exception as e:
    print(f"  Box: FAILED - {e}")

# Try component-level selection
comp = jm.component().create("comp1", True)
geom = comp.geom().create("geom1", 2)

print("\nCreating selections at component level:")
try:
    sel = comp.selection().create('sel_test', 'Explicit')
    print("  Explicit: OK")
    comp.selection().remove('sel_test')
except Exception as e:
    print(f"  Explicit: FAILED - {e}")

try:
    sel = comp.selection().create('sel_test2', 'Box')
    print("  Box: OK")
    comp.selection().remove('sel_test2')
except Exception as e:
    print(f"  Box: FAILED - {e}")

# Create geometry
r1 = geom.feature().create('r1', 'Rectangle')
r1.set("size", ["1000[nm]", "100[nm]"])
r1.set("pos", ["0[nm]", "0[nm]"])

r2 = geom.feature().create('r2', 'Rectangle')
r2.set("size", ["1000[nm]", "100[nm]"])
r2.set("pos", ["0[nm]", "100[nm]"])

fin = geom.feature('fin')
fin.set('action', 'union')
geom.run()

print(f"\nGeometry built:")
print(f"  Domains: {geom.getNDomains()}")
print(f"  Boundaries: {geom.getNBoundaries()}")

# Try using mph API to access model
print(f"\nmph model: {model}")
print(f"  components: {model.components()}")

client.remove(model)
print("\nDone.")
