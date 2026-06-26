#!/usr/bin/env bash
# update-task-status.sh — Update task status in active-tasks.json
#
# Usage: update-task-status.sh <task-id> <new-status> [reason]
#        update-task-status.sh --session <tmux-session> <new-status> [reason]
#   status: pending | running | review | done | failed
#   reason: optional text (used for failed tasks)
#
# Timestamps added automatically:
#   running  → startedAt (set by spawn-agent, not here)
#   review   → reviewStartedAt
#   done     → completedAt
#   failed   → failedAt + failReason (if reason provided)
#
# Uses flock to prevent race conditions from parallel agents.
# Non-fatal: exits 0 even if task not found or file missing.

set -euo pipefail

SWARM_DIR="$(cd "$(dirname "$0")" && pwd)"
TASKS_FILE="$SWARM_DIR/active-tasks.json"
LOCK_FILE="${TASKS_FILE}.lock"

# Parse args
LOOKUP_MODE="id"
LOOKUP_VALUE=""
NEW_STATUS=""
REASON=""

if [[ "${1:-}" == "--session" ]]; then
  LOOKUP_MODE="session"
  LOOKUP_VALUE="${2:?--session requires a tmux session name}"
  NEW_STATUS="${3:?Missing status argument}"
  REASON="${4:-}"
else
  LOOKUP_VALUE="${1:?Usage: update-task-status.sh <task-id> <status> [reason]}"
  NEW_STATUS="${2:?Missing status argument}"
  REASON="${3:-}"
fi

# Validate status value
case "$NEW_STATUS" in
  pending|running|review|done|failed) ;;
  *) echo "⚠️  Invalid status: $NEW_STATUS (must be: pending|running|review|done|failed)" >&2; exit 1 ;;
esac

# Non-fatal if file missing
[[ -f "$TASKS_FILE" ]] || { echo "⚠️  No active-tasks.json found at $TASKS_FILE" >&2; exit 0; }

# Use flock to prevent race conditions from parallel agents
(
  flock -x 200 || { echo "⚠️  Could not acquire lock on $TASKS_FILE" >&2; exit 0; }

  export _UTS_TASKS_FILE="$TASKS_FILE"
  export _UTS_LOOKUP_MODE="$LOOKUP_MODE"
  export _UTS_LOOKUP_VALUE="$LOOKUP_VALUE"
  export _UTS_NEW_STATUS="$NEW_STATUS"
  export _UTS_REASON="$REASON"

  python3 << 'PYEOF'
import json, sys, os
from datetime import datetime

tasks_file   = os.environ['_UTS_TASKS_FILE']
lookup_mode  = os.environ['_UTS_LOOKUP_MODE']
lookup_value = os.environ['_UTS_LOOKUP_VALUE']
new_status   = os.environ['_UTS_NEW_STATUS']
reason       = os.environ.get('_UTS_REASON', '')

with open(tasks_file) as f:
    data = json.load(f)

task = None
for t in data.get('tasks', []):
    if lookup_mode == 'id':
        if t.get('id') == lookup_value:
            task = t
            break
    else:
        if t.get('tmuxSession') == lookup_value:
            task = t
            break

if task is None:
    print(f'⚠️  Task not found: {lookup_value} (lookup by {lookup_mode})', file=sys.stderr)
    sys.exit(0)

old_status = task.get('status', 'unknown')
task['status'] = new_status

now_ts = int(datetime.now().timestamp() * 1000)
if new_status == 'review':
    task['reviewStartedAt'] = now_ts
elif new_status == 'done':
    task['completedAt'] = now_ts
elif new_status == 'failed':
    task['failedAt'] = now_ts
    if reason:
        task['failReason'] = reason

with open(tasks_file, 'w') as f:
    json.dump(data, f, indent=2)

print(f'📋 Task {task.get("id", lookup_value)}: {old_status} → {new_status}')
PYEOF

) 200>"$LOCK_FILE"
