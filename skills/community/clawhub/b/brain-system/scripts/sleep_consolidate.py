#!/usr/bin/env python3
"""Sleep consolidation: summarize current durable state into a compact daily consolidation note."""
from pathlib import Path
from datetime import datetime
import json, glob
ws = Path('/root/.openclaw/workspace')
out_dir = ws / 'memory' / 'consolidations'
out_dir.mkdir(parents=True, exist_ok=True)
today = datetime.now().strftime('%Y-%m-%d')
out = out_dir / f'{today}.md'
sections = [f'# Sleep Consolidation {today}\n']
for rel in ['memory/DO_NOT_FORGET.md', 'skills/brain-system/state/brain-state.json', 'skills/server-body-ops/state/authority.json', 'skills/brain-system/state/task-queue.json']:
    p = ws / rel
    if p.exists():
        txt = p.read_text(errors='replace')
        if len(txt) > 4000: txt = '[tail only]\n' + txt[-4000:]
        sections.append(f'## {rel}\n```\n{txt}\n```\n')
ckpts = sorted(glob.glob(str(ws / 'context-checkpoints' / 'checkpoint-*.md')))
if ckpts:
    sections.append(f'## Latest checkpoint\n- {ckpts[-1]}\n')
out.write_text('\n'.join(sections), encoding='utf-8')
print(out)
