#!/usr/bin/env python3
"""Print compact core memory files for session recovery."""
from pathlib import Path
ws = Path('/root/.openclaw/workspace')
files = [
    'memory/DO_NOT_FORGET.md',
    'skills/brain-system/state/brain-state.json',
    'skills/server-body-ops/state/authority.json',
    'TOOLS.md',
]
for rel in files:
    p = ws / rel
    if p.exists():
        print(f'\n===== {rel} =====')
        txt = p.read_text(errors='replace')
        print(txt[-8000:] if len(txt) > 8000 else txt)
PY = None
