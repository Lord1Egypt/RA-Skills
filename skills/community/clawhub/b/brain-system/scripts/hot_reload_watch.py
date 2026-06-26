#!/usr/bin/env python3
"""Brain-system hot reload watcher.
Watches key brain/body files and runs lightweight refresh actions when they change.
No external dependencies, no network calls, no OpenClaw core patching.
"""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import subprocess
import time
import sys

WS = Path('/root/.openclaw/workspace')
STATE = WS / 'skills/brain-system/state/hot-reload-state.json'
LOG = WS / 'skills/brain-system/state/hot-reload.log'
WATCH_PATHS = [
    WS / 'skills/brain-system/SKILL.md',
    WS / 'skills/brain-system/state/brain-state.json',
    WS / 'skills/server-body-ops/SKILL.md',
    WS / 'skills/server-body-ops/state/authority.json',
    WS / 'memory/DO_NOT_FORGET.md',
    WS / 'TOOLS.md',
    WS / 'HEARTBEAT.md',
]
WATCH_DIRS = [
    WS / 'skills/brain-system/scripts',
]

def digest(path: Path):
    if not path.exists() or not path.is_file():
        return None
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()

def snapshot():
    files = list(WATCH_PATHS)
    for d in WATCH_DIRS:
        if d.exists():
            files.extend(sorted(p for p in d.rglob('*') if p.is_file()))
    return {str(p): digest(p) for p in files}

def load_state():
    if STATE.exists():
        try:
            return json.loads(STATE.read_text())
        except Exception:
            pass
    return {'version': 1, 'files': {}, 'events': []}

def save_state(state):
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n')

def log(msg):
    line = f"{datetime.now().isoformat(timespec='seconds')} {msg}\n"
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open('a', encoding='utf-8') as f:
        f.write(line)
    print(line, end='')

def refresh(changed):
    # Lightweight hot reload: create checkpoint and consolidation; avoid loops by not watching outputs.
    cmds = [
        ['python3', str(WS / 'skills/brain-system/scripts/context_checkpoint.py')],
        ['python3', str(WS / 'skills/brain-system/scripts/sleep_consolidate.py')],
    ]
    for cmd in cmds:
        try:
            subprocess.run(cmd, cwd=str(WS), check=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=30)
        except Exception as e:
            log(f'refresh command failed {cmd}: {e}')
    log('hot-reloaded changed=' + ','.join(Path(p).name for p in changed))

def once():
    state = load_state()
    old = state.get('files', {})
    new = snapshot()
    changed = [p for p, h in new.items() if old.get(p) != h]
    state['files'] = new
    state['updatedAt'] = datetime.now().isoformat(timespec='seconds')
    if changed:
        event = {'at': state['updatedAt'], 'changed': changed[:50]}
        state.setdefault('events', []).append(event)
        state['events'] = state['events'][-50:]
        refresh(changed)
    save_state(state)
    return changed

def main():
    if '--once' in sys.argv:
        changed = once()
        print('changed:', len(changed))
        return
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    interval = float(args[0]) if args else 5.0
    log(f'hot reload watcher started interval={interval}s')
    while True:
        once()
        time.sleep(interval)

if __name__ == '__main__':
    main()
