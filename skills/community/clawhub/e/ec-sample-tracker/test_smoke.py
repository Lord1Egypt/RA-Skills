#!/usr/bin/env python3
import sys, importlib.util
spec = importlib.util.spec_from_file_location('ec_sample_tracker', 'ec-sample-tracker.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

mod.init_db()
print("✅ DB initialized")

import argparse

# Fake args for each command
class Obj:
    def __init__(self, **kw):
        self.__dict__.update(kw)

# Test add
mod.cmd_add(Obj(
    name="NiFe-LDH/NF-2026-042",
    synthesis_date="2026-04-20",
    method="hydrothermal",
    precursors="Ni(NO3)2,Fe(NO3)3,urea",
    substrate="Ni foam",
    load=2.1,
    reaction="OER",
    tags="NiFe-LDH,hydrothermal,batch-42",
    storage="fridge-4",
    owner="xray",
    notes="Test sample for OER stability",
    status="active"
))

mod.cmd_list(Obj(status=None, reaction=None, storage=None, synth_after=None, synth_before=None, tag=None, limit=None))
print("✅ list OK")

mod.cmd_status(Obj())
print("✅ status OK")

print("\n✅ All smoke tests passed")
