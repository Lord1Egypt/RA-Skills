#!/bin/zsh
set -euo pipefail

HOME_DIR="${HOME}"
TS="$(date +%Y%m%d-%H%M%S)"

TARGET_BASE="$HOME_DIR/.openclaw/tools/gateway-monitor"
TARGET_BIN="$TARGET_BASE/bin"
LAUNCH_DIR="$HOME_DIR/Library/LaunchAgents"
BACKUP_DIR="$HOME_DIR/.openclaw/config-backups"
LOG_DIR="$HOME_DIR/.openclaw/logs"

MONITOR_LABEL="ai.openclaw.gateway-monitor"
WATCHDOG_LABEL="ai.openclaw.gateway-watchdog"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

SRC_MONITOR="$ROOT_DIR/assets/bin/gateway-monitor-server.js"
SRC_WATCHDOG="$ROOT_DIR/assets/bin/gateway-watchdog.sh"
TPL_MONITOR="$ROOT_DIR/assets/launchagents/${MONITOR_LABEL}.plist.tpl"
TPL_WATCHDOG="$ROOT_DIR/assets/launchagents/${WATCHDOG_LABEL}.plist.tpl"

DST_MONITOR_PLIST="$LAUNCH_DIR/${MONITOR_LABEL}.plist"
DST_WATCHDOG_PLIST="$LAUNCH_DIR/${WATCHDOG_LABEL}.plist"

echo "[install] preparing directories"
mkdir -p "$TARGET_BIN" "$LAUNCH_DIR" "$BACKUP_DIR" "$LOG_DIR"

echo "[install] copying binaries"
cp "$SRC_MONITOR" "$TARGET_BIN/gateway-monitor-server.js"
cp "$SRC_WATCHDOG" "$TARGET_BIN/gateway-watchdog.sh"
chmod +x "$TARGET_BIN/gateway-watchdog.sh"

render_tpl() {
  local src="$1"
  local dst="$2"
  local tmp
  tmp="$(mktemp)"
  sed "s#__HOME__#$HOME_DIR#g" "$src" > "$tmp"

  if [[ -f "$dst" ]]; then
    cp "$dst" "$BACKUP_DIR/$(basename "$dst").bak.$TS"
  fi

  mv "$tmp" "$dst"
}

echo "[install] rendering launchagents"
render_tpl "$TPL_MONITOR" "$DST_MONITOR_PLIST"
render_tpl "$TPL_WATCHDOG" "$DST_WATCHDOG_PLIST"

restart_agent() {
  local label="$1"
  local plist="$2"
  local target="gui/$(id -u)/$label"

  launchctl bootout "$target" 2>/dev/null || true
  launchctl bootstrap "gui/$(id -u)" "$plist"
  launchctl enable "$target"
  launchctl kickstart -k "$target"
}

echo "[install] bootstrapping launchagents"
restart_agent "$MONITOR_LABEL" "$DST_MONITOR_PLIST"
restart_agent "$WATCHDOG_LABEL" "$DST_WATCHDOG_PLIST"

echo "[install] done"
"$SCRIPT_DIR/status.sh"
