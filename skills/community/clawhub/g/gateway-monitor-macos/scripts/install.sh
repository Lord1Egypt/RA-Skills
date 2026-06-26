#!/bin/zsh
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TARGET_DIR="$HOME/.openclaw/tools/gateway-monitor"
SOURCE_DIR="$SKILL_DIR/assets/gateway-monitor"
LA_DIR="$HOME/Library/LaunchAgents"
BACKUP_DIR="$HOME/.openclaw/config-backups"
LOG_DIR="$HOME/.openclaw/logs"
PORT="${PORT:-18990}"

MONITOR_LABEL="ai.openclaw.gateway-monitor"
WATCHDOG_LABEL="ai.openclaw.gateway-watchdog"
MONITOR_PLIST="$LA_DIR/${MONITOR_LABEL}.plist"
WATCHDOG_PLIST="$LA_DIR/${WATCHDOG_LABEL}.plist"

NODE_BIN="$(command -v node || true)"
if [[ -z "$NODE_BIN" && -x "/opt/homebrew/opt/node/bin/node" ]]; then
  NODE_BIN="/opt/homebrew/opt/node/bin/node"
fi
if [[ -z "$NODE_BIN" ]]; then
  echo "[ERROR] node not found"
  exit 1
fi

backup_file() {
  local file="$1"
  if [[ -f "$file" ]]; then
    local ts
    ts="$(date +%Y%m%d-%H%M%S)"
    cp "$file" "$BACKUP_DIR/$(basename "$file").bak.${ts}"
  fi
}

mkdir -p "$TARGET_DIR" "$LA_DIR" "$BACKUP_DIR" "$LOG_DIR"
rsync -a --delete "$SOURCE_DIR/" "$TARGET_DIR/"
chmod +x "$TARGET_DIR/gateway-watchdog.sh"

backup_file "$MONITOR_PLIST"
backup_file "$WATCHDOG_PLIST"

cat > "$MONITOR_PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>${MONITOR_LABEL}</string>
  <key>ProgramArguments</key>
  <array>
    <string>${NODE_BIN}</string>
    <string>${TARGET_DIR}/server.js</string>
  </array>
  <key>WorkingDirectory</key>
  <string>${TARGET_DIR}</string>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <true/>
  <key>ThrottleInterval</key>
  <integer>2</integer>
  <key>StandardOutPath</key>
  <string>${LOG_DIR}/gateway-monitor.log</string>
  <key>StandardErrorPath</key>
  <string>${LOG_DIR}/gateway-monitor.err.log</string>
  <key>EnvironmentVariables</key>
  <dict>
    <key>PORT</key>
    <string>${PORT}</string>
  </dict>
</dict>
</plist>
EOF

cat > "$WATCHDOG_PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>EnvironmentVariables</key>
  <dict>
    <key>HOME</key>
    <string>${HOME}</string>
    <key>PATH</key>
    <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
  </dict>
  <key>Label</key>
  <string>${WATCHDOG_LABEL}</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/zsh</string>
    <string>${TARGET_DIR}/gateway-watchdog.sh</string>
  </array>
  <key>RunAtLoad</key>
  <true/>
  <key>StartInterval</key>
  <integer>10</integer>
  <key>StandardOutPath</key>
  <string>${LOG_DIR}/gateway-watchdog.log</string>
  <key>StandardErrorPath</key>
  <string>${LOG_DIR}/gateway-watchdog.err.log</string>
</dict>
</plist>
EOF

UID_NUM="$(id -u)"
for label in "$MONITOR_LABEL" "$WATCHDOG_LABEL"; do
  launchctl bootout "gui/${UID_NUM}/${label}" 2>/dev/null || true
  launchctl bootstrap "gui/${UID_NUM}" "$LA_DIR/${label}.plist"
  launchctl enable "gui/${UID_NUM}/${label}" || true
  launchctl kickstart -k "gui/${UID_NUM}/${label}" || true
done

sleep 1
if command -v curl >/dev/null 2>&1; then
  curl -fsS "http://127.0.0.1:${PORT}/api/summary" >/dev/null && echo "[OK] monitor health check passed"
fi

echo "[DONE] Installed gateway monitor stack"
echo "       monitor:  http://127.0.0.1:${PORT}"
