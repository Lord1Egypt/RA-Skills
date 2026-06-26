#!/bin/zsh
set -euo pipefail

LA_DIR="$HOME/Library/LaunchAgents"
TARGET_DIR="$HOME/.openclaw/tools/gateway-monitor"
UID_NUM="$(id -u)"

for label in ai.openclaw.gateway-monitor ai.openclaw.gateway-watchdog; do
  launchctl bootout "gui/${UID_NUM}/${label}" 2>/dev/null || true
  launchctl disable "gui/${UID_NUM}/${label}" 2>/dev/null || true
  rm -f "$LA_DIR/${label}.plist"
done

rm -rf "$TARGET_DIR"

echo "[DONE] Uninstalled gateway monitor stack"
