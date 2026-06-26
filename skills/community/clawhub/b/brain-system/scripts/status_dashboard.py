#!/usr/bin/env python3
"""Brain/body status dashboard."""
from pathlib import Path
import json, glob, subprocess, shutil
ws = Path('/root/.openclaw/workspace')
def load(rel):
    p=ws/rel
    if not p.exists(): return None
    try: return json.loads(p.read_text())
    except Exception: return p.read_text(errors='replace')
print('🧠 OpenClaw Brain/Body Dashboard')
print('workspace=', ws)
print('\n== root ==')
subprocess.run(['id'])
print('\n== exec policy ==')
subprocess.run(['openclaw','exec-policy','show'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
brain=load('skills/brain-system/state/brain-state.json') or {}
auth=load('skills/server-body-ops/state/authority.json') or {}
tq=load('skills/brain-system/state/task-queue.json') or {}
print('\n== brain ==')
print('mode=', brain.get('activeMode'), 'rhythm=', brain.get('activeRhythm'))
print('fast nerves=', len(brain.get('fastNerves', [])))
print('\n== authority ==')
print('mode=', auth.get('mode'), 'rootVerified=', auth.get('rootVerified'))
print('\n== queue ==')
print('tasks=', len(tq.get('tasks', [])))
print('\n== checkpoints ==')
ckpts=sorted(glob.glob(str(ws/'context-checkpoints'/'checkpoint-*.md')))
print('count=', len(ckpts), 'latest=', ckpts[-1] if ckpts else None)
print('\n== disk ==')
subprocess.run(['df','-h','/root/.openclaw'])
