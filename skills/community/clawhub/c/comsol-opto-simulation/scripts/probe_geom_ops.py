#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Probe COMSOL geometry operations."""
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

# List available feature types
print("Available geometry feature types:")
# Try creating some common features
features_to_test = ['Rectangle', 'Circle', 'Union', 'FormUnion', 'FormAssembly', 'CompositeUnion', 'Difference', 'Intersection']

for feat in features_to_test:
    try:
        tag = f"test_{feat.lower()}"
        f = geom.feature().create(tag, feat)
        print(f"  {feat}: OK (tag={tag})")
        geom.feature().remove(tag)
    except Exception as e:
        print(f"  {feat}: FAILED - {e}")

# Check specifically for 'fin' feature
print("\nChecking if 'fin' already exists:")
print(f"  geom.feature().tags(): {list(geom.feature().tags())}")

client.remove(model)
print("Done.")
