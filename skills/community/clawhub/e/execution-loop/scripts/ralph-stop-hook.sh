#!/usr/bin/env bash
# ralph-stop-hook.sh — Stop hook for persistent execution loops
# Blocks Claude Code stop events when ralph mode is active.
# Reads JSON from stdin (Claude Code hook protocol).
# Outputs JSON via jq (no string interpolation — injection-safe).
#
# 4 Safety invariants (NEVER block):
#   1. authentication errors (401/403 detected in last_assistant_message)
#   2. cancel signal (with TTL)
#   3. stale state (>2 hours idle)
#   4. max iterations reached
#
# NOTE: Context usage >= 95% safety valve is NOT implemented because
# Claude Code transcripts do not contain context_window_size. That data
# is only available via the statusLine stdin pipe (HUD plugins), not
# accessible to hook scripts. Claude Code's own reactive compaction
# handles context overflow independently.

set -euo pipefail

SESSIONS_DIR="${HOME}/.openclaw/shared-context/sessions"
STALE_THRESHOLD_S=7200  # 2 hours
allow() { echo '{"continue":true}'; exit 0; }

block_with_reason() {
  jq -n --arg reason "$1" '{"decision":"block","reason":$reason}'
  exit 0
}

write_atomic() {
  local target="$1" content="$2"
  local tmp="${target}.${$}.$(date +%s).tmp"
  echo "$content" > "$tmp"
  mv "$tmp" "$target"
}

parse_utc_epoch() {
  local ts="$1"
  local clean=$(echo "$ts" | sed 's/T/ /;s/Z//')
  TZ=UTC date -j -f "%Y-%m-%d %H:%M:%S" "$clean" +%s 2>/dev/null || \
  date -u -d "$ts" +%s 2>/dev/null || \
  python3 -c "import datetime; print(int(datetime.datetime.fromisoformat('$ts'.replace('Z','+00:00')).timestamp()))" 2>/dev/null || \
  echo 0
}

# Read hook input
INPUT=$(head -c 20000)

# Determine session ID: prefer stdin JSON, fallback to env var
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // ""' 2>/dev/null)
[ -z "$SESSION_ID" ] && SESSION_ID="${NC_SESSION:-}"
[ -z "$SESSION_ID" ] && allow

# Session directory
SESSION_DIR="${SESSIONS_DIR}/${SESSION_ID}"

# Check ralph state file exists
STATE_FILE="${SESSION_DIR}/ralph.json"
[ -f "$STATE_FILE" ] || allow

# Parse state
STATE=$(cat "$STATE_FILE")
ACTIVE=$(echo "$STATE" | jq -r '.active // false')
[ "$ACTIVE" = "true" ] || allow

ITERATION=$(echo "$STATE" | jq -r '.iteration // 0')
MAX=$(echo "$STATE" | jq -r '.max_iterations // 50')
LAST_CHECKED=$(echo "$STATE" | jq -r '.last_checked_at // ""')

# === Safety valve 1: authentication errors ===
# Note: Stop hook does not receive a stop_reason field. Check last_assistant_message
# for API error indicators that suggest auth failure.
LAST_MSG=$(echo "$INPUT" | jq -r '.last_assistant_message // ""' 2>/dev/null)
if echo "$LAST_MSG" | grep -qiE '401|403|unauthorized|forbidden|authentication.*failed|token.*expired|APIAuthenticationError'; then
  write_atomic "$STATE_FILE" "$(echo "$STATE" | jq '.active = false | .deactivation_reason = "auth_error"')"
  allow
fi

# === Safety valve 2: stale (>2 hours since last activity) ===
if [ -n "$LAST_CHECKED" ]; then
  LAST_EPOCH=$(parse_utc_epoch "$LAST_CHECKED")
  NOW_EPOCH=$(date +%s)
  IDLE_S=$(( NOW_EPOCH - LAST_EPOCH ))
  if [ "$IDLE_S" -gt "$STALE_THRESHOLD_S" ]; then
    write_atomic "$STATE_FILE" "$(echo "$STATE" | jq '.active = false | .deactivation_reason = "stale"')"
    allow
  fi
fi

# === Safety valve 3: cancel signal ===
CANCEL_FILE="${SESSION_DIR}/cancel.json"
if [ -f "$CANCEL_FILE" ]; then
  EXPIRES=$(jq -r '.expires_at // ""' "$CANCEL_FILE")
  if [ -n "$EXPIRES" ]; then
    EXPIRES_EPOCH=$(parse_utc_epoch "$EXPIRES")
    NOW_EPOCH=$(date +%s)
    if [ "$NOW_EPOCH" -lt "$EXPIRES_EPOCH" ]; then
      write_atomic "$STATE_FILE" "$(echo "$STATE" | jq '.active = false | .deactivation_reason = "cancelled"')"
      rm -f "$CANCEL_FILE"
      allow
    else
      rm -f "$CANCEL_FILE"  # expired, clean up
    fi
  fi
fi

# === Safety valve 4: max iterations ===
if [ "$ITERATION" -ge "$MAX" ]; then
  write_atomic "$STATE_FILE" "$(echo "$STATE" | jq '.active = false | .deactivation_reason = "max_iterations"')"
  allow
fi

# Block stop and increment iteration
NEW_ITERATION=$(( ITERATION + 1 ))
NOW=$(date -u +%FT%TZ)
UPDATED=$(echo "$STATE" | jq \
  --argjson iter "$NEW_ITERATION" \
  --arg ts "$NOW" \
  '.iteration = $iter | .last_checked_at = $ts')
write_atomic "$STATE_FILE" "$UPDATED"

# Block message uses prompt-hardening P5 (anti-reasoning) to counter
# the agent's tendency to rationalize premature completion
block_with_reason "[RALPH LOOP ${NEW_ITERATION}/${MAX}] Task is NOT done. Do NOT rationalize that the remaining work can be done in a follow-up. Do NOT claim completion with caveats like 'mostly done' or 'should work'. Check your original task and verify EVERY requirement is met before attempting to stop again."
