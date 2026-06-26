#!/bin/zsh
set -euo pipefail

HOME_DIR="${HOME}"
TARGET_BASE="$HOME_DIR/.openclaw/tools/gateway-monitor"
LAUNCH_DIR="$HOME_DIR/Library/LaunchAgents"

MONITOR_LABEL="ai.openclaw.gateway-monitor"
WATCHDOG_LABEL="ai.openclaw.gateway-watchdog"

unload_agent() {
  local label="$1"
  local target="gui/$(id -u)/$label"
  launchctl bootout "$target" 2>/dev/null || true
  launchctl disable "$target" 2>/dev/null || true
}

echo "[uninstall] stopping launchagents"
unload_agent "$MONITOR_LABEL"
unload_agent "$WATCHDOG_LABEL"

echo "[uninstall] removing plist files"
rm -f "$LAUNCH_DIR/${MONITOR_LABEL}.plist"
rm -f "$LAUNCH_DIR/${WATCHDOG_LABEL}.plist"

echo "[uninstall] removing binaries"
rm -rf "$TARGET_BASE"

echo "[uninstall] done"
