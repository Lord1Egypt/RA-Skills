#!/usr/bin/env bash
# followup.sh - Set a single follow-up timer for the agent
# Usage: followup.sh <delay> "task description"
# Delay: e.g. 30s, 5m, 1h
# Reads channel config dynamically from openclaw — no hardcoded IDs.

set -euo pipefail

DELAY="${1:-5m}"
TASK="${2:-check pending task}"

# Parse delay to seconds
parse_seconds() {
  local d="$1"
  if [[ "$d" =~ ^([0-9]+)s$ ]]; then echo "${BASH_REMATCH[1]}"
  elif [[ "$d" =~ ^([0-9]+)m$ ]]; then echo $(( BASH_REMATCH[1] * 60 ))
  elif [[ "$d" =~ ^([0-9]+)h$ ]]; then echo $(( BASH_REMATCH[1] * 3600 ))
  else echo "$d"
  fi
}
SECS=$(parse_seconds "$DELAY")
AT=$(date -u -d "@$(( $(date +%s) + SECS ))" +"%Y-%m-%dT%H:%M:%SZ")
MSG="⏰ FOLLOW-UP (${DELAY}): $TASK"
NAME="followup-$(date +%s)"
SCHEDULED=0

# Telegram
TG_ENABLED=$(openclaw config get channels.telegram.enabled 2>/dev/null | tr -d '"' || echo "false")
TG_TO=$(openclaw config get channels.telegram.defaultTo 2>/dev/null | tr -d '"' || echo "")
if [[ "$TG_ENABLED" == "true" && -n "$TG_TO" ]]; then
  openclaw cron add --at "$AT" --agent main --message "$MSG" \
    --announce --channel telegram --to "$TG_TO" \
    --delete-after-run --name "${NAME}-telegram" > /dev/null 2>&1
  echo "  ✓ telegram @ +${DELAY}"
  SCHEDULED=1
fi

# WhatsApp
WA_ENABLED=$(openclaw config get channels.whatsapp.enabled 2>/dev/null | tr -d '"' || echo "false")
WA_TO=$(openclaw config get channels.whatsapp.allowFrom 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin)[0])" 2>/dev/null || echo "")
if [[ "$WA_ENABLED" == "true" && -n "$WA_TO" ]]; then
  openclaw cron add --at "$AT" --agent main --message "$MSG" \
    --announce --channel whatsapp --to "$WA_TO" \
    --delete-after-run --name "${NAME}-whatsapp" > /dev/null 2>&1
  echo "  ✓ whatsapp @ +${DELAY}"
  SCHEDULED=1
fi

if [[ "$SCHEDULED" == "0" ]]; then
  echo "⚠ no channels configured"
  exit 1
fi

echo "Follow-up set in ${DELAY}: $TASK"
