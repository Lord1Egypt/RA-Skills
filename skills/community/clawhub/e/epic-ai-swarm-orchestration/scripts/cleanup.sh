#!/usr/bin/env bash
# cleanup.sh — Clean up stale swarm data
#
# Usage: cleanup.sh [--dry-run]
#
# Cleans:
# 1. Endorsement files older than 7 days
# 2. /tmp/worklog-*, /tmp/review-*, /tmp/blockers-*, /tmp/review-verdict-*, /tmp/integration-prompt-* older than 3 days
# 3. pulse-state.json entries for sessions not in active-tasks.json as "running"
# 4. Completed tasks older than 30 days archived from active-tasks.json to archived-tasks.json
#
# Run weekly via heartbeat or cron.

set -euo pipefail

SWARM_DIR="$(cd "$(dirname "$0")" && pwd)"
DRY_RUN=0

if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=1
  echo "[DRY RUN] No files will be modified."
fi

# Counters
COUNT_ENDORSEMENTS=0
COUNT_TMPFILES=0
COUNT_PULSE=0
COUNT_ARCHIVED=0
COUNT_ACTIVE_REMAINING=0

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

do_delete() {
  local path="$1"
  if [[ $DRY_RUN -eq 1 ]]; then
    echo "  [dry-run] would remove: $path"
  else
    if command -v trash &>/dev/null; then
      trash "$path" 2>/dev/null || rm -f "$path"
    else
      rm -f "$path"
    fi
  fi
}

# ---------------------------------------------------------------------------
# 1. Endorsement files older than 7 days
# ---------------------------------------------------------------------------

ENDORSE_DIR="$SWARM_DIR/endorsements"

if [[ -d "$ENDORSE_DIR" ]]; then
  while IFS= read -r -d '' file; do
    do_delete "$file"
    (( COUNT_ENDORSEMENTS++ )) || true
  done < <(find "$ENDORSE_DIR" -name "*.endorsed" -mtime +7 -type f -print0 2>/dev/null)
fi

# ---------------------------------------------------------------------------
# 2. Temp files older than 3 days
# ---------------------------------------------------------------------------

while IFS= read -r -d '' file; do
  do_delete "$file"
  (( COUNT_TMPFILES++ )) || true
done < <(find /tmp -maxdepth 1 \( \
    -name "worklog-*" \
    -o -name "review-*" \
    -o -name "blockers-*" \
    -o -name "review-verdict-*" \
    -o -name "integration-prompt-*" \
  \) -mtime +3 -type f -print0 2>/dev/null)

# ---------------------------------------------------------------------------
# 3. Pulse state cleanup — remove entries for sessions not running
# ---------------------------------------------------------------------------

PULSE_STATE="$SWARM_DIR/pulse-state.json"
TASKS_FILE="$SWARM_DIR/active-tasks.json"

if [[ -f "$PULSE_STATE" ]]; then
  export _CU_PULSE_FILE="$PULSE_STATE"
  export _CU_TASKS_FILE="$TASKS_FILE"
  export _CU_DRY_RUN="$DRY_RUN"
  RESULT=$(python3 << 'PYEOF'
import json, os, sys

pulse_file = os.environ['_CU_PULSE_FILE']
tasks_file = os.environ['_CU_TASKS_FILE']
dry_run    = os.environ['_CU_DRY_RUN'] == '1'

with open(pulse_file) as f:
    pulse = json.load(f)

running_sessions = set()
if os.path.isfile(tasks_file):
    with open(tasks_file) as f:
        data = json.load(f)
    for t in data.get('tasks', []):
        if t.get('status') == 'running' and t.get('tmuxSession'):
            running_sessions.add(t['tmuxSession'])

stale_keys = [k for k in pulse if k not in running_sessions]

if dry_run:
    for k in stale_keys:
        print(f"  [dry-run] would prune pulse entry: {k}")
else:
    for k in stale_keys:
        del pulse[k]
    with open(pulse_file, 'w') as f:
        json.dump(pulse, f, indent=2)

print(len(stale_keys))
PYEOF
)
  # Last line is the count; preceding lines are dry-run messages
  while IFS= read -r line; do
    if [[ "$line" =~ ^[0-9]+$ ]]; then
      COUNT_PULSE=$line
    else
      echo "$line"
    fi
  done <<< "$RESULT"
fi

# ---------------------------------------------------------------------------
# 4. Archive completed tasks older than 30 days
# ---------------------------------------------------------------------------

ARCHIVED_FILE="$SWARM_DIR/archived-tasks.json"

if [[ -f "$TASKS_FILE" ]]; then
  export _CU_TASKS_FILE="$TASKS_FILE"
  export _CU_ARCHIVED_FILE="$ARCHIVED_FILE"
  export _CU_DRY_RUN="$DRY_RUN"

  RESULT=$(python3 << 'PYEOF'
import json, os, sys
from datetime import datetime, timezone

tasks_file   = os.environ['_CU_TASKS_FILE']
archive_file = os.environ['_CU_ARCHIVED_FILE']
dry_run      = os.environ['_CU_DRY_RUN'] == '1'

now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
threshold_ms = 30 * 24 * 60 * 60 * 1000  # 30 days in ms

with open(tasks_file) as f:
    data = json.load(f)

keep = []
to_archive = []

for t in data.get('tasks', []):
    status = t.get('status', '')
    if status == 'done':
        completed_at = t.get('completedAt', 0)
        age_ms = now_ms - completed_at
        if age_ms >= threshold_ms:
            to_archive.append(t)
            if dry_run:
                task_id = t.get('id', '?')
                age_days = int(age_ms / (24 * 60 * 60 * 1000))
                print(f"  [dry-run] would archive task: {task_id} (done {age_days} days ago)")
            continue
    keep.append(t)

archived_count = len(to_archive)

if not dry_run and to_archive:
    # Load or init archived-tasks.json
    if os.path.isfile(archive_file):
        with open(archive_file) as f:
            archive_data = json.load(f)
    else:
        archive_data = {'tasks': []}

    archive_data['tasks'].extend(to_archive)

    with open(archive_file, 'w') as f:
        json.dump(archive_data, f, indent=2)

    data['tasks'] = keep
    with open(tasks_file, 'w') as f:
        json.dump(data, f, indent=2)

active_remaining = len(keep)
# Output: "archived_count active_remaining"
print(f"{archived_count} {active_remaining}")
PYEOF
)

  while IFS= read -r line; do
    if [[ "$line" =~ ^[0-9]+\ [0-9]+$ ]]; then
      COUNT_ARCHIVED="${line%% *}"
      COUNT_ACTIVE_REMAINING="${line##* }"
    else
      echo "$line"
    fi
  done <<< "$RESULT"
else
  # No tasks file — count active remaining as 0
  COUNT_ACTIVE_REMAINING=0
fi

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

echo ""
echo "Swarm Cleanup Summary"
echo "─────────────────────────"
echo "Endorsements removed:      $COUNT_ENDORSEMENTS"
echo "Temp files removed:        $COUNT_TMPFILES"
echo "Pulse state entries pruned: $COUNT_PULSE"
echo "Tasks archived:            $COUNT_ARCHIVED (30+ days old)"
echo "Active tasks remaining:    $COUNT_ACTIVE_REMAINING"
