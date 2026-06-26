#!/usr/bin/env bash
# check-completions.sh — Cron-based backup notifier
# Runs every 5 minutes via cron. Checks pending-notifications.txt for unsent notifications.
# This is a BACKUP — primary notifications come from notify-on-complete.sh watchers.
# If watchers die (process killed, WSL restart), this catches what they missed.

# Ensure PATH includes openclaw + node (cron has minimal PATH)
export PATH="$(dirname "$(command -v openclaw 2>/dev/null || echo /usr/local/bin/openclaw)"):/usr/local/bin:/usr/bin:/bin:$PATH"

set -euo pipefail

SWARM_DIR="$(cd "$(dirname "$0")" && pwd)"
[[ -f "$SWARM_DIR/swarm.conf" ]] && source "$SWARM_DIR/swarm.conf"
NOTIFY_TARGET="${SWARM_NOTIFY_TARGET:-}"
NOTIFY_CHANNEL="${SWARM_NOTIFY_CHANNEL:-telegram}"
NOTIFY_FILE="$SWARM_DIR/pending-notifications.txt"
SENT_FILE="$SWARM_DIR/sent-notifications.txt"

# Create sent tracker if missing
touch "$SENT_FILE"

# Nothing to do if no pending notifications
[[ ! -s "$NOTIFY_FILE" ]] && exit 0

# Skip if no notification target configured
[[ -z "$NOTIFY_TARGET" ]] && exit 0

# Check each line — if not in sent file, send it
while IFS= read -r line; do
  [[ -z "$line" ]] && continue

  # Skip if already sent
  if grep -Fxq "$line" "$SENT_FILE" 2>/dev/null; then
    continue
  fi

  # Send notification
  openclaw message send --channel "$NOTIFY_CHANNEL" --target "$NOTIFY_TARGET" --message "📋 $line" 2>/dev/null && {
    echo "$line" >> "$SENT_FILE"
  }

  # Rate limit: 1 message per 2 seconds
  sleep 2
done < "$NOTIFY_FILE"

# Keep sent file from growing forever (last 200 lines)
tail -200 "$SENT_FILE" > "$SENT_FILE.tmp" && mv "$SENT_FILE.tmp" "$SENT_FILE"
