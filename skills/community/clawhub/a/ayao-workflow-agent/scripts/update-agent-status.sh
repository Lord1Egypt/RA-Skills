#!/bin/bash
# update-agent-status.sh — Update a single agent's status in agent-pool.json
# Usage: update-agent-status.sh <session_id> <status> [task_id]
#   status: idle | busy | dead
#   task_id: current task (empty string to clear)

set -euo pipefail

SESSION_ID="${1:?Usage: update-agent-status.sh <session_id> <status> [task_id]}"
NEW_STATUS="${2:?}"
CURRENT_TASK="${3:-}"

POOL_FILE="$HOME/.openclaw/workspace/swarm/agent-pool.json"
POOL_LOCK="${POOL_FILE}.lock"
export PATH="/opt/homebrew/opt/util-linux/bin:$PATH"
[[ ! -f "$POOL_FILE" ]] && exit 0

(
  flock -x 9
  SESSION_ID="$SESSION_ID" \
  NEW_STATUS="$NEW_STATUS" \
  CURRENT_TASK="$CURRENT_TASK" \
  POOL_FILE="$POOL_FILE" \
  python3 - <<'PYEOF'
import json
import os
from datetime import datetime, timezone

pool_file = os.environ['POOL_FILE']
session_id = os.environ['SESSION_ID']
new_status = os.environ['NEW_STATUS']
current_task = os.environ.get('CURRENT_TASK', '')
now = datetime.now(timezone.utc).isoformat()

with open(pool_file, 'r') as f:
    pool = json.load(f)

found = False
for a in pool.get('agents', []):
    if a.get('id') == session_id or a.get('tmux') == session_id:
        a['status'] = new_status
        a['last_seen'] = now
        a['current_task'] = current_task if current_task else None
        found = True
        break

if not found:
    # Agent not in pool yet (e.g. pre-existing fixed session).
    pass

pool['updated_at'] = now

tmp = pool_file + '.tmp'
with open(tmp, 'w') as f:
    json.dump(pool, f, indent=2, ensure_ascii=False)
    f.flush()
    os.fsync(f.fileno())
os.replace(tmp, pool_file)
PYEOF
) 9>"$POOL_LOCK" 2>/dev/null || true

exit 0
