#!/usr/bin/env bash
# start-integration.sh — Quick integration watcher kickoff for manual spawns.
#
# Usage:
#   start-integration.sh <project-dir> "description" session1 session2 [session3 ...]
#
# Call this IMMEDIATELY after manually spawning 2+ parallel tmux agents.
# It starts the integration watcher in the background — same as spawn-batch.sh does.
#
# Example:
#   start-integration.sh "~/projects/MyApp" "Feature X (backend + frontend)" mb-backend mb-frontend

set -euo pipefail

SWARM_DIR="$(cd "$(dirname "$0")" && pwd)"
INTEGRATION_WATCHER="$SWARM_DIR/integration-watcher.sh"
LOG_DIR="$SWARM_DIR/logs"
mkdir -p "$LOG_DIR"

PROJECT_DIR="${1:?Usage: start-integration.sh <project-dir> <description> <session1> [session2] ...}"
DESCRIPTION="${2:?Missing description}"
shift 2
SESSIONS=("$@")

if [[ ${#SESSIONS[@]} -lt 2 ]]; then
  echo "⚠️  Need at least 2 sessions for integration watching (got ${#SESSIONS[@]})"
  echo "   For single agents, notify-on-complete.sh is sufficient."
  exit 1
fi

if [[ ! -x "$INTEGRATION_WATCHER" ]]; then
  echo "Error: integration-watcher.sh not found or not executable at $SWARM_DIR" >&2
  exit 1
fi

# Verify all sessions exist in tmux
ACTIVE=$(tmux ls 2>/dev/null | cut -d: -f1 || echo "")
MISSING=()
for sess in "${SESSIONS[@]}"; do
  if ! echo "$ACTIVE" | grep -qE "^${sess}$"; then
    MISSING+=("$sess")
  fi
done

if [[ ${#MISSING[@]} -gt 0 ]]; then
  echo "⚠️  Warning: these tmux sessions not found (may have already finished): ${MISSING[*]}"
  echo "   Proceeding anyway — integration watcher handles already-completed sessions."
fi

PROJECT_NAME=$(basename "$PROJECT_DIR")
INTEG_LOG="$LOG_DIR/integration-${PROJECT_NAME}-$(date +%Y%m%d-%H%M).log"

nohup "$INTEGRATION_WATCHER" "$PROJECT_DIR" "$DESCRIPTION" "${SESSIONS[@]}" >> "$INTEG_LOG" 2>&1 &
INTEG_PID=$!

echo "🔗 Integration watcher started"
echo "   PID:      $INTEG_PID"
echo "   Sessions: ${SESSIONS[*]}"
echo "   Log:      $INTEG_LOG"
echo ""
echo "   It will wait for all agents to finish, then auto-review cross-dependencies."
