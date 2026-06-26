#!/usr/bin/env python3
"""Lightweight local brain-system maintenance tick.
Reads brain-state.json, prints pending prospective memory and strongest nerves.
No network calls, no destructive actions.
"""
import json
from pathlib import Path

base = Path(__file__).resolve().parents[1]
state_path = base / "state" / "brain-state.json"
state = json.loads(state_path.read_text())
print(f"brain-state version={state.get('version')} rhythm={state.get('activeRhythm')} mode={state.get('activeMode')}")
print("top fast nerves:")
for nerve in sorted(state.get("fastNerves", []), key=lambda n: n.get("weight", 0), reverse=True)[:5]:
    flag = "myelinated" if nerve.get("myelinated") else "learning"
    print(f"- {nerve['id']} weight={nerve.get('weight')} {flag}: {nerve.get('trigger')}")
pending = state.get("prospectiveMemory", [])
print(f"pending prospective items: {len(pending)}")
for item in pending[:10]:
    print(f"- {item}")
