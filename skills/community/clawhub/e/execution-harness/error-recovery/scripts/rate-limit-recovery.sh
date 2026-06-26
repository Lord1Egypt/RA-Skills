#!/usr/bin/env bash
# rate-limit-recovery.sh — Standalone script: scan tmux panes for rate-limit stalls
# Run via cron or manually. NOT a hook — runs independently.

set -euo pipefail

COOLDOWN_DIR="${HOME}/.openclaw/shared-context/rate-limit-cooldown"
COOLDOWN_SECONDS=60

mkdir -p "$COOLDOWN_DIR"

# Check tmux is available
if ! command -v tmux &>/dev/null; then
  echo "tmux not found" >&2
  exit 0
fi

# Check tmux server is running
if ! tmux list-sessions &>/dev/null 2>&1; then
  echo "No tmux server running" >&2
  exit 0
fi

# Scan all panes
tmux list-panes -a -F "#{pane_id}" 2>/dev/null | while read -r PANE_ID; do
  # Capture last 20 lines
  CONTENT=$(tmux capture-pane -p -t "$PANE_ID" -S -20 2>/dev/null || echo "")
  [ -z "$CONTENT" ] && continue

  # Check for rate limit patterns
  if echo "$CONTENT" | grep -qiE '(rate.?limit|429|Too Many Requests|try again in|Retry-After|overloaded_error)'; then
    # Check cooldown
    COOLDOWN_FILE="${COOLDOWN_DIR}/${PANE_ID//\//_}"
    if [ -f "$COOLDOWN_FILE" ]; then
      LAST=$(cat "$COOLDOWN_FILE" 2>/dev/null || echo "0")
      NOW=$(date +%s)
      ELAPSED=$((NOW - LAST))
      if [ "$ELAPSED" -lt "$COOLDOWN_SECONDS" ]; then
        continue
      fi
    fi

    # Safety: skip if pane shows a confirmation prompt (could accidentally confirm destructive action)
    if echo "$CONTENT" | grep -qiE '(are you sure|confirm|delete|destroy|y/n|yes/no)'; then
      echo "Skipped pane $PANE_ID (confirmation prompt detected alongside rate limit)" >&2
      continue
    fi

    # Send Enter to resume
    tmux send-keys -t "$PANE_ID" Enter 2>/dev/null || true
    date +%s > "$COOLDOWN_FILE"
    echo "Recovered pane $PANE_ID (rate limit detected)" >&2
  fi
done
