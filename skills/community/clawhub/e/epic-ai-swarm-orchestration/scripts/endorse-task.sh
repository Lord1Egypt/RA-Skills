#!/usr/bin/env bash
# endorse-task.sh — Create endorsement file for a task
# Called by the orchestrator AFTER the human/operator approves the plan
#
# Usage: endorse-task.sh <task-id> [endorsement-note]
#        endorse-task.sh --batch <task-id> [endorsement-note]
#
# The --batch flag is used by spawn-batch.sh to indicate this endorsement
# is part of an already-approved batch (human endorsed the whole batch verbally).
# Without --batch, a 30-second cooldown is enforced before spawn-agent.sh will
# accept the endorsement — this prevents the orchestrator from endorsing and
# spawning in the same turn without presenting the plan to the human first.

set -euo pipefail

SWARM_DIR="$(cd "$(dirname "$0")" && pwd)"

BATCH_MODE="false"
if [[ "${1:-}" == "--batch" ]]; then
  BATCH_MODE="true"
  shift
fi

TASK_ID="${1:?Usage: endorse-task.sh [--batch] <task-id> [endorsement-note]}"
NOTE="${2:-Endorsed}"

ENDORSE_DIR="$SWARM_DIR/endorsements"
ENDORSE_FILE="$ENDORSE_DIR/${TASK_ID}.endorsed"

mkdir -p "$ENDORSE_DIR"

cat > "$ENDORSE_FILE" << EOF
Task: $TASK_ID
Endorsed: $(date '+%Y-%m-%d %H:%M:%S')
Endorsed_Epoch: $(date +%s)
Batch: $BATCH_MODE
Note: $NOTE
EOF

echo "✅ Task '$TASK_ID' endorsed → $ENDORSE_FILE"
