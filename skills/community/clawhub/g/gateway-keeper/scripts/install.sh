#!/usr/bin/env bash
# Install openclaw-gatewaykeeper as cron job (Linux/macOS)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CHECK_SCRIPT="$SCRIPT_DIR/check-gateway.sh"
WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
HEARTBEAT="$WORKSPACE/HEARTBEAT.md"
CRON_MARKER="# openclaw-openclaw-gatewaykeeper"

chmod +x "$CHECK_SCRIPT"

# Install cron job (every 15 minutes)
CRON_LINE="*/15 * * * * $CHECK_SCRIPT $CRON_MARKER"
(crontab -l 2>/dev/null | grep -v "$CRON_MARKER"; echo "$CRON_LINE") | crontab -
echo "Cron job installed (every 15 minutes)"

# Append recovery section to HEARTBEAT.md
if [ -f "$HEARTBEAT" ]; then
    if ! grep -qi "Gateway.*Crash.*Recovery" "$HEARTBEAT"; then
        cat >> "$HEARTBEAT" << 'BLOCK'

## Gateway Crash Recovery
If `logs/gateway-recovery.json` exists:
1. Read crash timestamp
2. List all active sessions/sub-agents
3. Check each for incomplete work
4. Resume or retry as needed
5. Delete the recovery file when done
BLOCK
        echo "Added recovery section to HEARTBEAT.md"
    fi
else
    echo "HEARTBEAT.md not found — add recovery section manually"
fi

echo "Installation complete. Logs: $WORKSPACE/logs/openclaw-gatewaykeeper.log"
