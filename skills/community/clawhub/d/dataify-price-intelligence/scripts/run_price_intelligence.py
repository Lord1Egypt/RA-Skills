#!/usr/bin/env python3
import os
import sys

RUNTIME = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "dataify-task-operations", "scripts"))
if RUNTIME not in sys.path:
    sys.path.insert(0, RUNTIME)
from business_workflow import run

if __name__ == "__main__":
    raise SystemExit(run("price"))
