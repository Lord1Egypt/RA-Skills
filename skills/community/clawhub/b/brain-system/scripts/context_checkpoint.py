#!/usr/bin/env python3
"""Create a compact external context checkpoint for long conversations.
No network calls. Writes a timestamped markdown checkpoint from known state files.
"""
from pathlib import Path
from datetime import datetime
import json

ws = Path('/root/.openclaw/workspace')
out_dir = ws / 'context-checkpoints'
out_dir.mkdir(exist_ok=True)
ts = datetime.now().strftime('%Y-%m-%d-%H%M%S')
out = out_dir / f'checkpoint-{ts}.md'

parts = []
parts.append(f'# Context Checkpoint {ts}\n')
parts.append('## Purpose\nExternal compact memory to reduce context-window pressure. Load this before continuing long-running work if chat context is compacted or stale.\n')

for rel in [
    'skills/brain-system/state/brain-state.json',
    'skills/server-body-ops/state/authority.json',
    'TOOLS.md',
    'memory/2026-05-15.md',
]:
    p = ws / rel
    if not p.exists():
        continue
    txt = p.read_text(errors='replace')
    if rel.endswith('.json'):
        try:
            txt = json.dumps(json.loads(txt), ensure_ascii=False, indent=2)
        except Exception:
            pass
    if len(txt) > 12000:
        txt = txt[-12000:]
        txt = '[truncated: kept tail]\n' + txt
    parts.append(f'## {rel}\n```\n{txt}\n```\n')

out.write_text('\n'.join(parts), encoding='utf-8')
print(out)
