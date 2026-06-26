#!/usr/bin/env python3
"""Probe COMSOL parametric sweep setup."""
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
VENDOR_DIR = SKILL_DIR / "vendor" / "site-packages"
if str(VENDOR_DIR) not in sys.path:
    sys.path.insert(0, str(VENDOR_DIR))

import mph
client = mph.start()
model = client.create('probe_parametric')
jm = model.java

study = jm.study().create('std1')

print("=== Testing Parametric creation ===")
try:
    param = study.feature().create('param1', 'Parametric')
    print("  study.feature().create('param1', 'Parametric'): OK")
    param.set('pname', 'V_bias')
    param.set('plist', '-1,-0.5,0,0.5,1')
    print("  param.set plist: OK")
except Exception as e:
    print(f"  Parametric: ERROR - {e}")

print("\n=== Testing Stationary with Parametric ===")
try:
    stat = study.feature().create('stat1', 'Stationary')
    print("  stat1 created")
    # Try to add parametric to study, not to stat
    param = study.feature().create('param1', 'Parametric')
    param.set('pname', 'V_bias')
    param.set('plist', '-1,-0.5,0,0.5,1')
    print("  Parametric sweep on study: OK")
except Exception as e:
    print(f"  ERROR - {e}")

client.clear()
