#!/usr/bin/env bash
# install-cron.sh — Install/update the auto-update cron job
# Usage: ./install-cron.sh [--schedule "0 2 * * *"] [--uninstall]

set -euo pipefail

if ! command -v python3 >/dev/null 2>&1; then
  echo "Error: python3 required" >&2
  exit 1
fi

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
UPDATE_SCRIPT="$SKILL_DIR/scripts/update.sh"
CRON_TAG="# openclaw-auto-update"
SCHEDULE="0 2 * * *"
UNINSTALL=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --uninstall)
      UNINSTALL=true
      shift
      ;;
    --schedule=*)
      SCHEDULE="${1#--schedule=}"
      shift
      ;;
    --schedule)
      SCHEDULE="${2}"
      shift 2
      ;;
    *)
      shift
      ;;
  esac
done

# Read config for schedule override
CONFIG_FILE="${OPENCLAW_UPDATE_CONFIG:-$HOME/.openclaw/workspace/skills/openclaw-auto-update/config.json}"
if [[ -f "$CONFIG_FILE" ]]; then
  SCHEDULE_FROM_CONFIG=$(python3 -c "
import json
cfg = json.load(open('$CONFIG_FILE'))
print(cfg.get('schedule', ''))
" 2>/dev/null || true)
  [[ -n "$SCHEDULE_FROM_CONFIG" ]] && SCHEDULE="$SCHEDULE_FROM_CONFIG"
fi

if [[ "$UNINSTALL" == "true" ]]; then
  { crontab -l 2>/dev/null | grep -Fv "$CRON_TAG" || true; } | crontab -
  echo "✅ Removed openclaw-auto-update cron job"
  exit 0
fi

# Add new cron entry
NEW_CRON="$SCHEDULE bash $UPDATE_SCRIPT >> /tmp/openclaw-auto-update.log 2>&1 $CRON_TAG"
{
  crontab -l 2>/dev/null | grep -Fv "$CRON_TAG" || true
  echo "$NEW_CRON"
} | crontab -

echo "✅ Cron job installed: $SCHEDULE"
echo "   Script: $UPDATE_SCRIPT"
echo "   Log: /tmp/openclaw-auto-update.log"
echo ""
echo "To uninstall: $0 --uninstall"
echo "To change schedule: $0 --schedule '0 3 * * *'"
