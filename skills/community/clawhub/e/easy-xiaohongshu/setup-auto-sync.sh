#!/bin/bash
# Setup script for auto-sync on macOS
# Run this once to configure automatic git syncing

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SYNC_SCRIPT="$SCRIPT_DIR/auto-sync.sh"

echo "🔧 Setting up auto-sync for Easy-xiaohongshu..."

# Create LaunchAgent for macOS
LAUNCH_AGENT_DIR="$HOME/Library/LaunchAgents"
LAUNCH_AGENT_PLIST="$LAUNCH_AGENT_DIR/com.easy-xhs.auto-sync.plist"

mkdir -p "$LAUNCH_AGENT_DIR"

cat > "$LAUNCH_AGENT_PLIST" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.easy-xhs.auto-sync</string>
    <key>ProgramArguments</key>
    <array>
        <string>$SYNC_SCRIPT</string>
    </array>
    <key>StartInterval</key>
    <integer>300</integer>
    <key>StandardOutPath</key>
    <string>/tmp/easy-xhs-sync.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/easy-xhs-sync.err</string>
</dict>
</plist>
EOF

# Load the LaunchAgent
launchctl unload "$LAUNCH_AGENT_PLIST" 2>/dev/null
launchctl load "$LAUNCH_AGENT_PLIST"

echo "✅ Auto-sync configured!"
echo ""
echo "📋 Details:"
echo "   - Sync interval: Every 5 minutes"
echo "   - Log file: /tmp/easy-xhs-sync.log"
echo "   - LaunchAgent: $LAUNCH_AGENT_PLIST"
echo ""
echo "🔍 Check status:"
echo "   launchctl list | grep easy-xhs"
echo "   tail -f /tmp/easy-xhs-sync.log"
echo ""
echo "🛑 To disable:"
echo "   launchctl unload $LAUNCH_AGENT_PLIST"
