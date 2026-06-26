#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Probe COMSOL boundary structure after finalization."""
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

# Test with union
fin.set('action', 'union')
geom.run()

print("=== UNION finalization ===")
print(f"Number of domains: {geom.getNDomains()}")
print(f"Number of boundaries: {geom.getNBoundaries()}")

# Try to access domain and boundary info
print(f"\nTrying to access domain info...")
try:
    obj = geom.object('fin')
    print(f"  Object 'fin' exists: True")
    print(f"  Object type: {type(obj)}")
    
    # Try to get domain names
    try:
        domains = obj.getDomainNames()
        print(f"  Domain names: {domains}")
    except Exception as e:
        print(f"  getDomainNames FAILED: {e}")
    
    # Try to get boundary names
    try:
        boundaries = obj.getBoundaryNames()
        print(f"  Boundary names: {boundaries}")
    except Exception as e:
        print(f"  getBoundaryNames FAILED: {e}")
        
except Exception as e:
    print(f"  Object 'fin' access FAILED: {e}")

# Test with assembly
client.remove(model)
model2 = client.create("test2")
jm2 = model2.java
comp2 = jm2.component().create("comp1", True)
geom2 = comp2.geom().create("geom1", 2)

r1b = geom2.feature().create('r1', 'Rectangle')
r1b.set("size", ["1000[nm]", "100[nm]"])
r1b.set("pos", ["0[nm]", "0[nm]"])

r2b = geom2.feature().create('r2', 'Rectangle')
r2b.set("size", ["1000[nm]", "100[nm]"])
r2b.set("pos", ["0[nm]", "100[nm]"])

fin2 = geom2.feature('fin')
fin2.set('action', 'assembly')
geom2.run()

print("\n=== ASSEMBLY finalization ===")
print(f"Number of domains: {geom2.getNDomains()}")
print(f"Number of boundaries: {geom2.getNBoundaries()}")

try:
    obj2 = geom2.object('fin')
    print(f"  Object 'fin' exists: True")
    try:
        domains2 = obj2.getDomainNames()
        print(f"  Domain names: {domains2}")
    except Exception as e:
        print(f"  getDomainNames FAILED: {e}")
    try:
        boundaries2 = obj2.getBoundaryNames()
        print(f"  Boundary names: {boundaries2}")
    except Exception as e:
        print(f"  getBoundaryNames FAILED: {e}")
except Exception as e:
    print(f"  Object 'fin' access FAILED: {e}")

client.remove(model2)
print("\nDone.")
