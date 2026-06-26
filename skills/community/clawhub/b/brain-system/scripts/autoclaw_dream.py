#!/usr/bin/env python3
"""AutoClaw dream system: offline simulation and rehearsal from durable memory.
It does not execute actions; it generates next-time playbooks and fast-nerve candidates.
"""
from pathlib import Path
from datetime import datetime
import json, re
ws=Path('/root/.openclaw/workspace')
out_dir=ws/'memory'/'dreams'; out_dir.mkdir(parents=True, exist_ok=True)
ts=datetime.now().strftime('%Y-%m-%d-%H%M%S')
texts=[]
for rel in ['memory/DO_NOT_FORGET.md', f"memory/{datetime.now().strftime('%Y-%m-%d')}.md", 'skills/brain-system/state/brain-state.json', 'skills/server-body-ops/state/authority.json']:
    p=ws/rel
    if p.exists(): texts.append((rel,p.read_text(errors='replace')[-8000:]))
content='\n'.join(f'## {r}\n{t}' for r,t in texts)
# Deterministic lightweight rehearsal prompts/checklists, not LLM-generated dreams.
playbooks=[]
if '/v1' in content: playbooks.append('Relay issue rehearsal: check baseUrl includes /v1 before model/provider conclusions.')
if 'server body' in content.lower() or 'serverBody' in content: playbooks.append('Server-body rehearsal: use root/local diagnostics decisively, verify with readback/status, keep hard safety boundaries.')
if 'context' in content.lower() or 'forget' in content.lower(): playbooks.append('Anti-forgetting rehearsal: write important facts to DO_NOT_FORGET, checkpoint long turns, run boot_recall after compaction.')
if 'skill' in content.lower(): playbooks.append('Skill workflow rehearsal: search/install/verify SKILL.md, then log durable lesson.')
if not playbooks: playbooks.append('General rehearsal: orient → act locally → verify → record durable rule.')
out=out_dir/f'dream-{ts}.md'
out.write_text('# AutoClaw Dream / Offline Simulation\n\n'+'\n'.join(f'- {p}' for p in playbooks)+'\n\n## Source windows\n'+content[-12000:], encoding='utf-8')
print(out)
