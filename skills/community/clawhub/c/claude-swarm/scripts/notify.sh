#!/usr/bin/env bash
# Claude Swarm — Send notification via webhook or telegram
# Usage: notify.sh "message text"
set -euo pipefail

SWARM_DIR="$(cd "$(dirname "$0")/.." && pwd)"
[ -f "$SWARM_DIR/config/swarm.conf" ] && source "$SWARM_DIR/config/swarm.conf"

MSG="${1:?Usage: notify.sh <message>}"
NOTIFY="${SWARM_NOTIFY:-none}"

case "$NOTIFY" in
  webhook)
    if [ -n "${SWARM_WEBHOOK_URL:-}" ]; then
      curl -s -X POST "$SWARM_WEBHOOK_URL" \
        -H "Content-Type: application/json" \
        -d "{\"text\": \"$MSG\"}" 2>/dev/null || true
    fi
    ;;
  telegram)
    if [ -n "${SWARM_TELEGRAM_BOT_TOKEN:-}" ] && [ -n "${SWARM_TELEGRAM_CHAT_ID:-}" ]; then
      curl -s "https://api.telegram.org/bot${SWARM_TELEGRAM_BOT_TOKEN}/sendMessage" \
        -d "chat_id=${SWARM_TELEGRAM_CHAT_ID}" \
        -d "text=${MSG}" \
        -d "parse_mode=Markdown" 2>/dev/null || true
    fi
    ;;
  none|"")
    # Log only
    echo "[notify] $MSG"
    ;;
esac

# Always log
mkdir -p "$SWARM_DIR/logs"
echo "[$(date -Iseconds)] $MSG" >> "$SWARM_DIR/logs/notifications.log"
