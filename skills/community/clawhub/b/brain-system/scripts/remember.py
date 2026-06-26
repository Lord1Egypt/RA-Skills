#!/usr/bin/env python3
"""Append a durable pinned memory to memory/DO_NOT_FORGET.md and today's daily log."""
from pathlib import Path
from datetime import datetime
import sys

text = " ".join(sys.argv[1:]).strip()
if not text:
    print("Usage: remember.py <important fact/rule>", file=sys.stderr)
    raise SystemExit(2)
ws = Path('/root/.openclaw/workspace')
today = datetime.now().strftime('%Y-%m-%d')
entry = f"- {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} — {text}\n"
for rel in ['memory/DO_NOT_FORGET.md', f'memory/{today}.md']:
    p = ws / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('a', encoding='utf-8') as f:
        f.write('\n' + entry if p.stat().st_size else entry)
print('remembered:', text)
