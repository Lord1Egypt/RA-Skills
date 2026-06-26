#!/bin/bash
# update-task-status.sh — Atomically update a task's status in active-tasks.json
# Usage: update-task-status.sh <task_id> <new_status> [commit_hash] [tokens_json] [tmux_session]
#
# tokens_json: optional JSON string e.g. '{"input":1234,"output":567,"cache_read":0,"cache_write":0}'
# This updates active-tasks.json synchronously before any follow-up handling.

set -euo pipefail

TASK_ID="${1:?Usage: update-task-status.sh <task_id> <status> [commit_hash] [tokens_json] [tmux_session]}"
NEW_STATUS="${2:?}"
COMMIT_HASH="${3:-}"
TOKENS_JSON="${4:-}"
TMUX_SESSION="${5:-}"

TASKS_FILE="$HOME/.openclaw/workspace/swarm/active-tasks.json"
LOCK_FILE="${TASKS_FILE}.lock"

# Ensure flock is available (macOS: installed via util-linux but not in default PATH)
export PATH="/opt/homebrew/opt/util-linux/bin:$PATH"

if [[ ! -f "$TASKS_FILE" ]]; then
  echo "ERROR: $TASKS_FILE not found" >&2
  exit 1
fi

# Update task status + commit + tokens + timestamp, and auto-unblock dependents.
# Uses flock to serialize concurrent writers (e.g. multiple agents finishing at
# nearly the same time).
# Special behaviour when new_status == "running":
#   - pending/failed/retrying → running claims the task (check-and-set)
#   - running → running is treated as heartbeat and only refreshes updated_at
#   - Other running transitions exit with code 2 so dispatch.sh skips duplicate dispatch
LOCK_FD_OPEN=0
cleanup_lock() {
  local ec=$?
  if [[ "${LOCK_FD_OPEN}" == "1" ]]; then
    flock -u 200 2>/dev/null || true
    exec 200>&- || true
    LOCK_FD_OPEN=0
  fi
  return "$ec"
}

exec 200>"$LOCK_FILE"
LOCK_FD_OPEN=1
trap cleanup_lock EXIT
flock -x 200

set +e
TASK_ID_ENV="$TASK_ID" \
NEW_STATUS_ENV="$NEW_STATUS" \
COMMIT_HASH_ENV="$COMMIT_HASH" \
TOKENS_JSON_ENV="$TOKENS_JSON" \
TMUX_SESSION_ENV="$TMUX_SESSION" \
TASKS_FILE_ENV="$TASKS_FILE" \
python3 - <<'PYEOF'
import json
import os
import sys
from datetime import datetime, timezone

task_id = os.environ["TASK_ID_ENV"]
new_status = os.environ["NEW_STATUS_ENV"]
commit_hash = os.environ["COMMIT_HASH_ENV"]
tokens_raw = os.environ.get("TOKENS_JSON_ENV", "")
tmux_session = os.environ.get("TMUX_SESSION_ENV", "")
tasks_file = os.environ["TASKS_FILE_ENV"]

with open(tasks_file, "r", encoding="utf-8") as f:
    data = json.load(f)

now = datetime.now(timezone.utc).isoformat()
updated = False

# Parse tokens JSON (safe fallback)
tokens = None
if tokens_raw.strip():
    try:
        tokens = json.loads(tokens_raw.strip())
    except Exception:
        pass

for task in data.get("tasks", []):
    if task["id"] == task_id:
        current_status = task.get("status", "")

        if new_status == "running":
            if current_status == "running":
                task["updated_at"] = now
                if tmux_session:
                    task["tmux"] = tmux_session
                updated = True
                break
            if current_status not in ("pending", "failed", "retrying"):
                print(
                    f"SKIP: {task_id} already {current_status} (race-condition guard)",
                    file=sys.stderr,
                )
                sys.exit(2)

        task["status"] = new_status
        task["updated_at"] = now
        if new_status == "running" and tmux_session:
            task["tmux"] = tmux_session
        if commit_hash and commit_hash != "none":
            commits = task.setdefault("commits", [])
            if commit_hash not in commits:
                commits.append(commit_hash)
        if tokens:
            prev = task.get(
                "tokens",
                {"input": 0, "output": 0, "cache_read": 0, "cache_write": 0},
            )
            task["tokens"] = {
                "input": prev.get("input", 0) + tokens.get("input", 0),
                "output": prev.get("output", 0) + tokens.get("output", 0),
                "cache_read": prev.get("cache_read", 0) + tokens.get("cache_read", 0),
                "cache_write": prev.get("cache_write", 0) + tokens.get("cache_write", 0),
            }
        updated = True
        break

if not updated:
    print(f"WARN: task {task_id} not found in {tasks_file}", file=sys.stderr)
    sys.exit(2)

if new_status == "done":
    done_ids = {task["id"] for task in data["tasks"] if task["status"] == "done"}
    unblocked = []
    for task in data["tasks"]:
        if task["status"] == "blocked":
            deps = set(task.get("depends_on", []))
            if deps and deps.issubset(done_ids):
                task["status"] = "pending"
                task["updated_at"] = now
                unblocked.append(task["id"])
    if unblocked:
        print(f"Unblocked: {unblocked}")

data["updated_at"] = now

tmp = tasks_file + ".tmp"
with open(tmp, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.flush()
    os.fsync(f.fileno())
os.replace(tmp, tasks_file)

token_str = ""
if tokens:
    token_str = (
        f" | tokens: in={tokens.get('input', 0)}"
        f" out={tokens.get('output', 0)}"
        f" cache_r={tokens.get('cache_read', 0)}"
        f" cache_w={tokens.get('cache_write', 0)}"
    )
print(f"{task_id} -> {new_status}" + (f" (commit: {commit_hash})" if commit_hash else "") + token_str)
PYEOF
UTS_EC=$?
set -e

# If task just became done, check milestone completion in background
if [[ "$NEW_STATUS" == "done" && "${UTS_EC:-0}" == "0" ]]; then
  SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
  "$SCRIPT_DIR/milestone-check.sh" "$TASK_ID" 2>/dev/null &
fi

# Propagate Python exit code (flock subshell swallows it otherwise)
exit ${UTS_EC:-0}
