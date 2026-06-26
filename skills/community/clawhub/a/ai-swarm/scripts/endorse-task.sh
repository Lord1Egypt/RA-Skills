#!/usr/bin/env bash
# endorse-task.sh — Create endorsement file for a task
# Called by the orchestrator AFTER WB approves the plan
#
# Usage: endorse-task.sh <task-id> [endorsement-note]

set -euo pipefail

SWARM_DIR="$(cd "$(dirname "$0")" && pwd)"
TASK_ID="${1:?Usage: endorse-task.sh <task-id> [endorsement-note]}"
NOTE="${2:-Endorsed}"

ENDORSE_DIR="$SWARM_DIR/endorsements"
ENDORSE_FILE="$ENDORSE_DIR/${TASK_ID}.endorsed"

mkdir -p "$ENDORSE_DIR"

cat > "$ENDORSE_FILE" << EOF
Task: $TASK_ID
Endorsed: $(date '+%Y-%m-%d %H:%M:%S')
Note: $NOTE
EOF

echo "✅ Task '$TASK_ID' endorsed → $ENDORSE_FILE"
