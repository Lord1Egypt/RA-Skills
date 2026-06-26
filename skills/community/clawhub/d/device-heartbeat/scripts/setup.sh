#!/bin/bash
# 设置 macOS LaunchAgent 实现开机自启心跳
# 用法: setup.sh <PING_URL> [INTERVAL_SECONDS]

set -e

PING_URL="${1:?Usage: setup.sh <PING_URL> [INTERVAL_SECONDS]}"
INTERVAL="${2:-180}"
LABEL="ai.openclaw.device-heartbeat"
PLIST_PATH="$HOME/Library/LaunchAgents/${LABEL}.plist"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
HEARTBEAT_SCRIPT="${SCRIPT_DIR}/heartbeat.sh"
LOG_DIR="$HOME/.openclaw/logs"

chmod +x "$HEARTBEAT_SCRIPT"
mkdir -p "$LOG_DIR"

# 停止已有的服务
launchctl bootout "gui/$(id -u)/${LABEL}" 2>/dev/null || true

cat > "$PLIST_PATH" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>${LABEL}</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>${HEARTBEAT_SCRIPT}</string>
        <string>${PING_URL}</string>
        <string>${INTERVAL}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>${LOG_DIR}/heartbeat.log</string>
    <key>StandardErrorPath</key>
    <string>${LOG_DIR}/heartbeat-error.log</string>
    <key>ProcessType</key>
    <string>Background</string>
    <key>LowPriorityBackgroundIO</key>
    <true/>
    <key>Nice</key>
    <integer>10</integer>
</dict>
</plist>
EOF

launchctl bootstrap "gui/$(id -u)" "$PLIST_PATH"

echo "✅ Heartbeat service installed and started"
echo "   Plist: $PLIST_PATH"
echo "   Log:   $LOG_DIR/heartbeat.log"
echo "   URL:   ${PING_URL:0:40}..."
echo "   Interval: ${INTERVAL}s"
