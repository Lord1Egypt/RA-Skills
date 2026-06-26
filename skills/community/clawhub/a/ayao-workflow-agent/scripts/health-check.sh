#!/bin/bash
# health-check.sh — Inspect all active agent sessions and detect stuck/dead agents
# Usage: health-check.sh
#
# Called by: HEARTBEAT.md / cron (every ~15 min during active swarm)
# Checks:
#   1. For each "running" task: is its tmux session alive? Any recent output?
#   2. Sessions idle > STUCK_MINUTES with a running task → mark stuck, notify
#   3. Sessions where tmux pane shows shell prompt ($) but task still "running" → agent exited silently
#   4. Update agent-pool.json status accordingly

set -euo pipefail

STUCK_MINUTES=15
TASKS_FILE="$HOME/.openclaw/workspace/swarm/active-tasks.json"
POOL_FILE="$HOME/.openclaw/workspace/swarm/agent-pool.json"
POOL_LOCK="${POOL_FILE}.lock"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
NOTIFY_TARGET=$(cat "$HOME/.openclaw/workspace/swarm/notify-target" 2>/dev/null || echo "")
NOW_TS=$(date +%s)
export PATH="/opt/homebrew/opt/util-linux/bin:$PATH"

mark_pool_session_dead() {
  local target_session="$1"
  (
    flock -x 9
    POOL_FILE="$POOL_FILE" TARGET_SESSION="$target_session" python3 - <<'PYEOF'
import json
import os
from datetime import datetime, timezone

pool_file = os.environ['POOL_FILE']
target_session = os.environ['TARGET_SESSION']

with open(pool_file, 'r') as f:
    pool = json.load(f)

now = datetime.now(timezone.utc).isoformat()
for agent in pool.get('agents', []):
    if agent.get('tmux') == target_session:
        agent['status'] = 'dead'
        agent['last_seen'] = now

pool['updated_at'] = now
tmp = pool_file + '.tmp'
with open(tmp, 'w') as f:
    json.dump(pool, f, indent=2, ensure_ascii=False)
    f.flush()
    os.fsync(f.fileno())
os.replace(tmp, pool_file)
PYEOF
  ) 9>"$POOL_LOCK" 2>/dev/null || true
}

sync_pool_live_statuses() {
  (
    flock -x 9
    POOL_FILE="$POOL_FILE" python3 - <<'PYEOF'
import json
import os
import subprocess
from datetime import datetime, timezone

pool_file = os.environ['POOL_FILE']
if not os.path.exists(pool_file):
    raise SystemExit(0)

with open(pool_file, 'r') as f:
    pool = json.load(f)

now = datetime.now(timezone.utc).isoformat()
for agent in pool.get('agents', []):
    tmux_session = agent.get('tmux')
    if not tmux_session:
        continue
    result = subprocess.run(['tmux', 'has-session', '-t', tmux_session], capture_output=True)
    if result.returncode == 0:
        agent['last_seen'] = now
        if agent.get('status') == 'dead':
            agent['status'] = 'idle'
    elif agent.get('status') != 'dead':
        agent['status'] = 'dead'

pool['updated_at'] = now
tmp = pool_file + '.tmp'
with open(tmp, 'w') as f:
    json.dump(pool, f, indent=2, ensure_ascii=False)
    f.flush()
    os.fsync(f.fileno())
os.replace(tmp, pool_file)
print('Pool updated.')
PYEOF
  ) 9>"$POOL_LOCK" 2>/dev/null || true
}

mark_running_tasks_failed_for_session() {
  local dead_session="$1"
  local reason="$2"
  local stuck_tasks=""

  stuck_tasks=$(DEAD_SESSION="$dead_session" TASKS_FILE="$TASKS_FILE" python3 - <<'PYEOF'
import json
import os

tasks_file = os.environ['TASKS_FILE']
dead_session = os.environ['DEAD_SESSION']

try:
    with open(tasks_file, 'r') as f:
        data = json.load(f)
except Exception:
    raise SystemExit(0)

for task in data.get('tasks', []):
    if task.get('status') == 'running' and task.get('tmux') == dead_session:
        print(task.get('id', ''))
PYEOF
)

  for task_id in $stuck_tasks; do
    [[ -z "$task_id" ]] && continue
    echo "⚠️  Marking stuck task $task_id as failed (${reason}: $dead_session)" >&2
    "$SCRIPT_DIR/update-task-status.sh" "$task_id" "failed" "" "" "$dead_session" || true
  done
}

run_prompt_validation() {
  if [[ -x "$SCRIPT_DIR/validate-prompts.sh" ]]; then
    "$SCRIPT_DIR/validate-prompts.sh" || true
  else
    echo "⚠️  validate-prompts.sh not found or not executable. Skipping prompt validation."
  fi
}

trap run_prompt_validation EXIT

if [[ ! -f "$TASKS_FILE" ]]; then
  echo "No active swarm. Exiting."
  exit 0
fi

# Check if swarm is active (any running/pending tasks)
HAS_ACTIVE=$(python3 -c "
import json
tasks = json.load(open('$TASKS_FILE'))['tasks']
print('yes' if any(t['status'] in ('running','pending','reviewing') for t in tasks) else 'no')
")

if [[ "$HAS_ACTIVE" == "no" ]]; then
  echo "No active tasks. Skipping health check."
  exit 0
fi

echo "🔍 Running health check..."

ISSUES_FOUND=false

# Get all running tasks with their tmux sessions
python3 -c "
import json
tasks = json.load(open('$TASKS_FILE'))['tasks']
for t in tasks:
    if t['status'] == 'running' and t.get('tmux'):
        print(f\"{t['id']}|{t['tmux']}|{t.get('updated_at','')}\")
" | while IFS="|" read -r TASK_ID TMUX_SESSION UPDATED_AT; do

  # Check if tmux session exists
  if ! tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
    echo "💀 $TASK_ID: tmux session '$TMUX_SESSION' is DEAD (task still marked running)"
    ISSUES_FOUND=true
    mark_pool_session_dead "$TMUX_SESSION"
    mark_running_tasks_failed_for_session "$TMUX_SESSION" "tmux session dead"

    if [[ -n "$NOTIFY_TARGET" ]]; then
      openclaw message send --channel telegram --target "$NOTIFY_TARGET" \
        -m "💀 $TASK_ID ($TMUX_SESSION): tmux session 已死亡但任务仍标 running，请检查" --silent 2>/dev/null &
    fi
    continue
  fi

  # Capture last 5 lines of pane output
  PANE_OUTPUT=$(tmux capture-pane -t "$TMUX_SESSION" -p 2>/dev/null | tail -5 | tr '\n' ' ')

  # Check if agent finished silently (pane shows shell prompt with no active process)
  # Look for patterns like "$ " or "❯ " at end of output (shell waiting for input)
  if echo "$PANE_OUTPUT" | grep -qE '(\$\s*$|❯\s*$|%\s*$)'; then
    echo "⚠️ $TASK_ID ($TMUX_SESSION): agent may have exited (shell prompt visible)"
    echo "   Last output: $PANE_OUTPUT"
    ISSUES_FOUND=true
    mark_running_tasks_failed_for_session "$TMUX_SESSION" "shell prompt visible"
    if [[ -n "$NOTIFY_TARGET" ]]; then
      openclaw message send --channel telegram --target "$NOTIFY_TARGET" \
        -m "⚠️ $TASK_ID ($TMUX_SESSION): agent 可能已退出但未触发 on-complete。请检查 tmux。" --silent 2>/dev/null &
    fi
    continue
  fi

  # Check if stuck (no status update for > STUCK_MINUTES)
  if [[ -n "$UPDATED_AT" ]]; then
    # Parse ISO8601 to epoch — pass via env var to avoid code injection
    UPDATED_TS=$(UPDATED_AT_VAL="$UPDATED_AT" python3 - <<'PY' 2>/dev/null || echo 0
import os
from datetime import datetime
try:
    val = os.environ['UPDATED_AT_VAL']
    dt = datetime.fromisoformat(val.replace('Z', '+00:00'))
    print(int(dt.timestamp()))
except Exception:
    print(0)
PY
)

    ELAPSED=$(( NOW_TS - UPDATED_TS ))
    STUCK_SECS=$(( STUCK_MINUTES * 60 ))

    if [[ $ELAPSED -gt $STUCK_SECS ]]; then
      ELAPSED_MIN=$(( ELAPSED / 60 ))
      echo "⏱️ $TASK_ID ($TMUX_SESSION): no status update for ${ELAPSED_MIN}min (threshold: ${STUCK_MINUTES}min)"
      echo "   Last output: $PANE_OUTPUT"
      ISSUES_FOUND=true
      mark_running_tasks_failed_for_session "$TMUX_SESSION" "no status update for ${ELAPSED_MIN}min"
      if [[ -n "$NOTIFY_TARGET" ]]; then
        openclaw message send --channel telegram --target "$NOTIFY_TARGET" \
          -m "⏱️ $TASK_ID ($TMUX_SESSION): 已 ${ELAPSED_MIN} 分钟无进展，可能卡住了。最近输出：$PANE_OUTPUT" --silent 2>/dev/null &
      fi
    else
      echo "✅ $TASK_ID ($TMUX_SESSION): active (last update ${ELAPSED}s ago)"
    fi
  fi

done

# Update last_seen for all live sessions in pool
sync_pool_live_statuses

echo "🔍 Health check complete."
exit 0
