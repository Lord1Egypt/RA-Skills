#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Probe COMSOL Box selection with correct entity dimension setup."""
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

# Set entity dimension using JInt
sel_top.set('entitydim', JInt(1))  # 1 = edges in 2D
print(f"\nset entitydim=1 (JInt): OK")

# Try to get entities
try:
    ents = list(sel_top.entities())
    print(f"  entities(): {ents}")
except Exception as e:
    print(f"  entities() FAILED: {e}")

try:
    ents = list(sel_top.entities(JInt(1)))  # dimension 1
    print(f"  entities(JInt(1)): {ents}")
except Exception as e:
    print(f"  entities(JInt(1)) FAILED: {e}")

# Check all properties and their values
print("\nSelection property values:")
for prop in sel_top.properties():
    try:
        val = sel_top.getString(prop)
        print(f"  {prop} = {val}")
    except Exception as e:
        try:
            val = sel_top.getInt(prop)
            print(f"  {prop} = {val} (int)")
        except Exception:
            try:
                val = sel_top.getDouble(prop)
                print(f"  {prop} = {val} (double)")
            except Exception:
                print(f"  {prop} = <could not read>")

# Try with inputent
print("\nTrying inputent property:")
sel_top.set('inputent', 'all')
try:
    ents = list(sel_top.entities())
    print(f"  entities() after inputent='all': {ents}")
except Exception as e:
    print(f"  FAILED: {e}")

client.remove(model)
print("\nDone.")
