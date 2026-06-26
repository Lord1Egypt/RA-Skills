#!/usr/bin/env bash
# ralph-init.sh — Initialize ralph persistent execution state for a session
# Usage: ralph-init.sh <session-id> [max-iterations]
#
# Creates session-scoped state directory and ralph state file.
# If a prior session state exists (crash recovery), resumes from last iteration.
# Call before starting a Claude Code session that needs persistent execution.

set -euo pipefail

SESSION_ID="${1:?Usage: ralph-init.sh <session-id> [max-iterations]}"
MAX_ITERATIONS="${2:-50}"

SESSION_DIR="${HOME}/.openclaw/shared-context/sessions/${SESSION_ID}"
mkdir -p "$SESSION_DIR/handoffs"

STATE_FILE="${SESSION_DIR}/ralph.json"
NOW=$(date -u +%FT%TZ)

# --- Crash recovery: resume from existing state ---
if [ -f "$STATE_FILE" ]; then
  PREV_ACTIVE=$(jq -r '.active // false' "$STATE_FILE")
  PREV_ITER=$(jq -r '.iteration // 0' "$STATE_FILE")
  PREV_REASON=$(jq -r '.deactivation_reason // ""' "$STATE_FILE")

  if [ "$PREV_ACTIVE" = "true" ] || [ "$PREV_REASON" = "stale" ]; then
    # Previous session was active or stale-timed-out → resume
    echo "Resuming ralph from iteration ${PREV_ITER} (previous state: active=${PREV_ACTIVE}, reason=${PREV_REASON})"
    TMP="${STATE_FILE}.${$}.$(date +%s).tmp"
    jq --argjson max "$MAX_ITERATIONS" --arg ts "$NOW" \
      '.active = true | .max_iterations = $max | .last_checked_at = $ts | .deactivation_reason = null | .resumed_at = $ts' \
      "$STATE_FILE" > "$TMP"
    mv "$TMP" "$STATE_FILE"
    echo "Ralph resumed: ${STATE_FILE} (iteration ${PREV_ITER}/${MAX_ITERATIONS})"
    exit 0
  fi
fi

# --- Fresh init ---
TMP="${STATE_FILE}.${$}.$(date +%s).tmp"
jq -n --arg sid "$SESSION_ID" --argjson max "$MAX_ITERATIONS" --arg ts "$NOW" \
  '{session_id: $sid, active: true, iteration: 0, max_iterations: $max, created_at: $ts, last_checked_at: $ts}' \
  > "$TMP"
mv "$TMP" "$STATE_FILE"
echo "Ralph initialized: ${STATE_FILE} (max ${MAX_ITERATIONS} iterations)"
