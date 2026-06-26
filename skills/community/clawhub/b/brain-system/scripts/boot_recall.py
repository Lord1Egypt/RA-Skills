#!/usr/bin/env python3
"""Boot recall: compactly load pinned memory, latest checkpoint, brain state, server authority, and task queue."""
from pathlib import Path
import json, glob
ws = Path('/root/.openclaw/workspace')
items = [
    'memory/DO_NOT_FORGET.md',
    'skills/brain-system/state/brain-state.json',
    'skills/server-body-ops/state/authority.json',
    'skills/brain-system/state/task-queue.json',
    'TOOLS.md',
]
print('# BOOT RECALL')
for rel in items:
    p = ws / rel
    if not p.exists():
        continue
    txt = p.read_text(errors='replace')
    if rel.endswith('.json'):
        try: txt = json.dumps(json.loads(txt), ensure_ascii=False, indent=2)
        except Exception: pass
    if len(txt) > 6000: txt = '[tail only]\n' + txt[-6000:]
    print(f'\n## {rel}\n```\n{txt}\n```')
ckpts = sorted(glob.glob(str(ws / 'context-checkpoints' / 'checkpoint-*.md')))
if ckpts:
    p = Path(ckpts[-1]); txt = p.read_text(errors='replace')
    print(f'\n## latest checkpoint: {p.name}\n```\n{txt[-6000:]}\n```')
