#!/bin/bash
# install-patcher.sh — Install launchd WatchPaths agent for auto-patching gateway plist
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PATCHER_SCRIPT="$SCRIPT_DIR/patch-plist.sh"
PLIST_TO_WATCH="$HOME/Library/LaunchAgents/ai.openclaw.gateway.plist"
PATCHER_PLIST="$HOME/Library/LaunchAgents/ai.openclaw.plist-patcher.plist"
LOG_DIR="$HOME/.openclaw/logs"

chmod +x "$PATCHER_SCRIPT"
mkdir -p "$LOG_DIR"

cat > "$PATCHER_PLIST" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>ai.openclaw.plist-patcher</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>$PATCHER_SCRIPT</string>
    </array>
    <key>WatchPaths</key>
    <array>
        <string>$PLIST_TO_WATCH</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>StandardOutPath</key>
    <string>$LOG_DIR/plist-patcher.log</string>
    <key>StandardErrorPath</key>
    <string>$LOG_DIR/plist-patcher.err.log</string>
</dict>
</plist>
EOF

# Load the patcher
launchctl bootout "gui/$(id -u)/ai.openclaw.plist-patcher" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$PATCHER_PLIST"

echo "✅ Plist patcher installed and active"
echo "   Watches: $PLIST_TO_WATCH"
echo "   Script: $PATCHER_SCRIPT"
echo "   Log: $LOG_DIR/plist-patcher.log"
