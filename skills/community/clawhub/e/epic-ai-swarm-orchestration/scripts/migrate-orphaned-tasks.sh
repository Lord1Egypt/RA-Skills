#!/usr/bin/env bash
# migrate-orphaned-tasks.sh — One-time fix for tasks stuck as "running"
#
# Checks each "running" task's tmux session. If the session no longer
# exists the task is marked "done" with a migratedAt timestamp.
#
# Usage: migrate-orphaned-tasks.sh
# Safe to re-run; only touches tasks with status == "running".

set -euo pipefail

SWARM_DIR="$(cd "$(dirname "$0")" && pwd)"
TASKS_FILE="$SWARM_DIR/active-tasks.json"
LOCK_FILE="${TASKS_FILE}.lock"

[[ -f "$TASKS_FILE" ]] || { echo "No active-tasks.json found — nothing to migrate."; exit 0; }

echo "Scanning for orphaned 'running' tasks in $TASKS_FILE ..."

(
  flock -x 200 || { echo "⚠️  Could not acquire lock — aborting migration" >&2; exit 1; }

  export _MIGRATE_TASKS_FILE="$TASKS_FILE"

  python3 << 'PYEOF'
import json, sys, os, subprocess
from datetime import datetime

tasks_file = os.environ['_MIGRATE_TASKS_FILE']

with open(tasks_file) as f:
    data = json.load(f)

tasks    = data.get('tasks', [])
migrated = 0
now_ts   = int(datetime.now().timestamp() * 1000)
now_iso  = datetime.now().isoformat()

for task in tasks:
    if task.get('status') != 'running':
        continue

    tmux_session = task.get('tmuxSession', '')
    if not tmux_session:
        continue

    # Check if the tmux session still exists
    result = subprocess.run(
        ['tmux', 'has-session', '-t', tmux_session],
        capture_output=True
    )
    if result.returncode != 0:
        # Session is gone — mark as done
        old_status       = task['status']
        task['status']   = 'done'
        task['completedAt'] = now_ts
        task['migratedAt']  = now_iso
        print(f'  Migrated: {task.get("id", tmux_session)}: {old_status} → done (session gone)')
        migrated += 1

with open(tasks_file, 'w') as f:
    json.dump(data, f, indent=2)

print(f'\nMigrated {migrated} orphaned task(s) from "running" to "done"')
PYEOF

) 200>"$LOCK_FILE"
