#!/usr/bin/env bash
set -euo pipefail

# Append a structured log entry to a task's execution log.
#
# Usage: bash task-log.sh <task_id> <phase> <status> ["detail"]
# Example: bash task-log.sh abc-123 fetch searching "Searching for datasets"

SKILL_DIR="$HOME/.openclaw/workspace/skills/clawgrid-connector"
source "$SKILL_DIR/scripts/_clawgrid_env.sh"

if [ $# -lt 3 ]; then
  echo "Usage: bash $0 <task_id> <phase> <status> [detail]" >&2
  echo "Example: bash $0 abc-123 fetch searching \"Searching for datasets\"" >&2
  exit 1
fi

TASK_ID="$1"
PHASE="$2"
STATUS="$3"
DETAIL="${4:-}"

mkdir -p "$LOG_DIR"

python3 - "$LOG_DIR/$TASK_ID.log" "$TASK_ID" "$PHASE" "$STATUS" "$DETAIL" <<'PYEOF'
import json
import sys
from datetime import datetime, timezone

path, task_id, phase, status, detail = sys.argv[1:]
line = {
    "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "phase": phase,
    "status": status,
    "detail": detail,
}
with open(path, "a", encoding="utf-8") as f:
    f.write(json.dumps(line, ensure_ascii=False) + "\n")
PYEOF

echo "OK: logged $PHASE/$STATUS for task $TASK_ID"
