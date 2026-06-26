#!/usr/bin/env python3
"""Tiny durable task queue."""
from pathlib import Path
from datetime import datetime
import json, sys, uuid
p=Path('/root/.openclaw/workspace/skills/brain-system/state/task-queue.json')
p.parent.mkdir(parents=True, exist_ok=True)
if p.exists(): data=json.loads(p.read_text())
else: data={'version':1,'tasks':[]}
cmd=sys.argv[1] if len(sys.argv)>1 else 'list'
if cmd=='add':
    text=' '.join(sys.argv[2:]).strip()
    if not text: raise SystemExit('task text required')
    item={'id':str(uuid.uuid4())[:8], 'createdAt':datetime.now().isoformat(timespec='seconds'), 'status':'pending', 'text':text}
    data['tasks'].append(item); data['updatedAt']=datetime.now().isoformat(timespec='seconds')
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n'); print('added', item['id'])
elif cmd=='done':
    tid=sys.argv[2]
    for t in data['tasks']:
        if t['id'].startswith(tid): t['status']='done'; t['doneAt']=datetime.now().isoformat(timespec='seconds')
    data['updatedAt']=datetime.now().isoformat(timespec='seconds')
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
else:
    for t in data.get('tasks',[]): print(f"{t['id']} [{t['status']}] {t['text']}")
