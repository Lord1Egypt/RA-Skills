#!/bin/bash
# 卸载心跳服务
LABEL="ai.openclaw.device-heartbeat"
PLIST_PATH="$HOME/Library/LaunchAgents/${LABEL}.plist"

launchctl bootout "gui/$(id -u)/${LABEL}" 2>/dev/null && echo "✅ Service stopped" || echo "⚠️ Service was not running"
rm -f "$PLIST_PATH" && echo "✅ Plist removed: $PLIST_PATH" || echo "⚠️ Plist not found"
echo "Done. Heartbeat service uninstalled."
