#!/bin/bash
# swarm-new-batch.sh - Archive the current swarm batch and start a new one.
# Usage:
#   swarm-new-batch.sh --project <name> [--repo <github-url>] [--dir <swarm-dir>]

set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  swarm-new-batch.sh --project <name> [--repo <github-url>] [--dir <swarm-dir>] [--force]

Options:
  --project   Required. Project name written to batch_id and active-tasks.json
  --repo      Optional. Repository URL stored in active-tasks.json
  --dir       Optional. Swarm directory (default: ~/.openclaw/workspace/swarm)
  --force     Proceed even if running tasks still exist in active-tasks.json
  --help      Show this help
EOF
}

PROJECT=""
REPO=""
SWARM_DIR="${HOME}/.openclaw/workspace/swarm"
FORCE="false"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project)
      [[ $# -ge 2 ]] || {
        echo "ERROR: --project requires a value" >&2
        usage >&2
        exit 1
      }
      PROJECT="$2"
      shift 2
      ;;
    --repo)
      [[ $# -ge 2 ]] || {
        echo "ERROR: --repo requires a value" >&2
        usage >&2
        exit 1
      }
      REPO="$2"
      shift 2
      ;;
    --dir)
      [[ $# -ge 2 ]] || {
        echo "ERROR: --dir requires a value" >&2
        usage >&2
        exit 1
      }
      SWARM_DIR="$2"
      shift 2
      ;;
    --force)
      FORCE="true"
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "ERROR: Unknown argument: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if [[ -z "$PROJECT" ]]; then
  usage >&2
  exit 1
fi

ACTIVE_TASKS_FILE="$SWARM_DIR/active-tasks.json"
HISTORY_DIR="$SWARM_DIR/history"
LOCAL_DATE="$(date +%Y-%m-%d)"
PROJECT_SLUG="${PROJECT// /-}"

mkdir -p "$SWARM_DIR" "$HISTORY_DIR"

resolve_archive_target() {
  local base_name="$LOCAL_DATE-$PROJECT_SLUG"
  local candidate="$HISTORY_DIR/$base_name.json"
  local seq=2

  while [[ -e "$candidate" ]]; do
    candidate="$HISTORY_DIR/$base_name-$seq.json"
    seq=$((seq + 1))
  done

  printf '%s\n' "$candidate"
}

should_archive() {
  local tasks_file="$1"

  [[ -f "$tasks_file" ]] || return 2

  python3 - "$tasks_file" <<'PY'
import json
import sys

tasks_file = sys.argv[1]

try:
    with open(tasks_file, "r", encoding="utf-8") as f:
        data = json.load(f)
except Exception as exc:
    print(f"ERROR: failed to read {tasks_file}: {exc}", file=sys.stderr)
    sys.exit(1)

tasks = data.get("tasks")
if isinstance(tasks, list) and len(tasks) > 0:
    sys.exit(0)
sys.exit(2)
PY
}

ARCHIVE_PATH="$(resolve_archive_target)"
BATCH_ID="$(basename "$ARCHIVE_PATH" .json)"

RUNNING_COUNT="$(
  python3 - "$ACTIVE_TASKS_FILE" <<'PY'
import json
import sys

tasks_file = sys.argv[1]

try:
    with open(tasks_file, "r", encoding="utf-8") as f:
        data = json.load(f)
except Exception:
    print(0)
    sys.exit(0)

running = [
    task for task in data.get("tasks", [])
    if task.get("status") == "running"
]
print(len(running))
PY
)"

if [[ "$RUNNING_COUNT" -gt 0 ]]; then
  echo "❌ Cannot start new batch: $RUNNING_COUNT task(s) still running." >&2
  echo "   Wait for them to complete, or manually mark them failed first." >&2
  echo "   Use --force to override (data loss risk)." >&2
  if [[ "$FORCE" != "true" ]]; then
    exit 1
  fi
  echo "⚠️  --force specified, proceeding anyway" >&2
fi

if should_archive "$ACTIVE_TASKS_FILE"; then
  cp "$ACTIVE_TASKS_FILE" "$ARCHIVE_PATH"
  echo "✅ Archived → history/$(basename "$ARCHIVE_PATH")"
else
  SHOULD_ARCHIVE_EC=$?
  if [[ "$SHOULD_ARCHIVE_EC" == "1" ]]; then
    exit 1
  fi
  echo "No active tasks to archive; starting a fresh batch."
fi

python3 - "$ACTIVE_TASKS_FILE" "$BATCH_ID" "$PROJECT" "$REPO" <<'PY'
import json
import sys
from datetime import datetime, timezone

tasks_file, batch_id, project, repo = sys.argv[1:5]
now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

payload = {
    "batch_id": batch_id,
    "project": project,
    "repo": repo,
    "created_at": now,
    "updated_at": now,
    "tasks": [],
}

with open(tasks_file, "w", encoding="utf-8") as f:
    json.dump(payload, f, indent=2, ensure_ascii=False)
    f.write("\n")
PY

echo "✅ New batch: $BATCH_ID"
