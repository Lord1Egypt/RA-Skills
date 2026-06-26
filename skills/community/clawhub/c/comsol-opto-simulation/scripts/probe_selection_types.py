#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Probe available selection types in COMSOL."""
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

# Try different selection types
selection_types = [
    'Box', 'Explicit', 'Adjacent', 'Ball', 'Cylinder', 'Disk',
    'Complement', 'Difference', 'Intersection', 'Union',
    'EdgeSelection', 'BoundarySelection', 'DomainSelection'
]

for sel_type in selection_types:
    try:
        tag = f'test_{sel_type.lower()}'
        sel = geom.selection().create(tag, sel_type)
        print(f"  {sel_type}: OK (tag={tag})")
        geom.selection().remove(tag)
    except Exception as e:
        print(f"  {sel_type}: FAILED - {str(e)[:80]}")

client.remove(model)
print("Done.")
