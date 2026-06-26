#!/usr/bin/env python3
from pathlib import Path
import json, glob, subprocess, os
ws=Path('/root/.openclaw/workspace')
checks=[]
def exists(label, rel): checks.append((label, (ws/rel).exists()))
exists('brain skill', 'skills/brain-system/SKILL.md')
exists('brain state', 'skills/brain-system/state/brain-state.json')
exists('server authority', 'skills/server-body-ops/state/authority.json')
exists('pinned memory', 'memory/DO_NOT_FORGET.md')
exists('boot recall', 'skills/brain-system/scripts/boot_recall.py')
exists('context checkpoint', 'skills/brain-system/scripts/context_checkpoint.py')
exists('sleep consolidation', 'skills/brain-system/scripts/sleep_consolidate.py')
exists('dream system', 'skills/brain-system/scripts/autoclaw_dream.py')
exists('hot reload watcher', 'skills/brain-system/scripts/hot_reload_watch.py')
exists('backup script', 'skills/brain-system/scripts/brain_backup.sh')
exists('task queue', 'skills/brain-system/state/task-queue.json')
exists('maintenance loop', 'skills/brain-system/scripts/brain_maintenance.sh')
checks.append(('checkpoints exist', bool(glob.glob(str(ws/'context-checkpoints/checkpoint-*.md')))))
checks.append(('dreams exist', bool(glob.glob(str(ws/'memory/dreams/dream-*.md')))))
checks.append(('backups exist', bool(glob.glob(str(ws/'skills/brain-system/backups/openclaw-brain-backup-*.tar.gz')))))
pidfile=ws/'skills/brain-system/state/hot-reload.pid'
hot=False
if pidfile.exists():
    pid=pidfile.read_text().strip()
    hot=subprocess.run(['bash','-lc',f'kill -0 {pid}'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode==0
checks.append(('hot reload running', hot))
cron=subprocess.run(['bash','-lc','crontab -l 2>/dev/null | grep -q OPENCLAW_BRAIN_SYSTEM'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode==0
checks.append(('cron installed', cron))
score=sum(v for _,v in checks); total=len(checks)
print(f'brain_fullness={score}/{total} ({score/total*10:.1f}/10)')
for k,v in checks: print(('✅' if v else '❌'), k)
