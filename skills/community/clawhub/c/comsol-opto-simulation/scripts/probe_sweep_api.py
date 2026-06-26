#!/usr/bin/env python3
"""Probe COMSOL study sweep API."""
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
VENDOR_DIR = SKILL_DIR / "vendor" / "site-packages"
if str(VENDOR_DIR) not in sys.path:
    sys.path.insert(0, str(VENDOR_DIR))

import mph
client = mph.start()
model = client.create('probe_sweep')
jm = model.java

study = jm.study().create('std1')
stat = study.feature().create('stat1', 'Stationary')

print("=== StudyFeature methods ===")
for attr in dir(stat):
    if not attr.startswith('_'):
        print(f"  {attr}")

print("\n=== Testing sweep creation ===")
try:
    sweep = study.feature().create('sweep1', 'AuxiliarySweep')
    print("  study.feature().create('sweep1', 'AuxiliarySweep'): OK")
except Exception as e:
    print(f"  study.feature().create: ERROR - {e}")

try:
    sweep = stat.create('sweep1', 'AuxiliarySweep')
    print("  stat.create('sweep1', 'AuxiliarySweep'): OK")
except Exception as e:
    print(f"  stat.create: ERROR - {e}")

client.clear()
