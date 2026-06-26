#!/usr/bin/env bash
# Claude Swarm — Endorse a task (safety gate before spawning)
set -euo pipefail
SWARM_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TASK_ID="${1:?Usage: endorse-task.sh <task-id>}"
mkdir -p "$SWARM_DIR/endorsements"
echo "Endorsed at $(date)" > "$SWARM_DIR/endorsements/${TASK_ID}.endorsed"
echo "✅ Task '$TASK_ID' endorsed → $SWARM_DIR/endorsements/${TASK_ID}.endorsed"
