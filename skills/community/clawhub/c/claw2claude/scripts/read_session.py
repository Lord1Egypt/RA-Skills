#!/usr/bin/env python3
"""Safely read a field from the session file, avoiding shell variable interpolation risks.
Usage: read_session.py <session_file> <field>
"""
import sys
import json

if len(sys.argv) < 3:
    print("", end="")
    sys.exit(0)

session_file = sys.argv[1]
field = sys.argv[2]

try:
    with open(session_file, encoding="utf-8") as f:
        data = json.load(f)
    print(data.get(field, ""), end="")
except Exception:
    print("", end="")
