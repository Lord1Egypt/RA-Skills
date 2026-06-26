#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$HOME/.openclaw/workspace/skills/clawgrid-connector"
source "$SKILL_DIR/scripts/_clawgrid_env.sh"
IS_MACOS=false
[ "$(uname -s)" = "Darwin" ] && IS_MACOS=true

if [ ! -f "$CONFIG" ]; then
  echo "Config not found at $CONFIG — run setup first" >&2
  exit 1
fi

# --- Pre-flight: ensure exec approval is configured for automated sessions ---
CHECK_EXEC="$SKILL_DIR/scripts/check-exec-approval.sh"
if [ -x "$CHECK_EXEC" ]; then
  _EA_STATUS=$(bash "$CHECK_EXEC" 2>/dev/null | head -1 || echo "UNKNOWN")
  if [ "$_EA_STATUS" != "OK" ]; then
    SETUP_EXEC="$SKILL_DIR/scripts/setup-exec-approval.sh"
    if [ -x "$SETUP_EXEC" ]; then
      echo "[setup-crons] Configuring exec approval for automated sessions..."
      bash "$SETUP_EXEC" --quiet || true
    fi
  fi
fi

echo "=== ClawGrid Cron Setup ==="

# Delegate heartbeat scheduler + keepalive cron to heartbeat-ctl.sh
bash "$SKILL_DIR/scripts/heartbeat-ctl.sh" start

echo ""
echo "=== All cron jobs configured ==="
if $IS_MACOS; then
  echo "Verify with: launchctl list | grep clawgrid  &&  openclaw cron list"
else
  echo "Verify with: crontab -l | grep clawgrid  &&  openclaw cron list"
fi
