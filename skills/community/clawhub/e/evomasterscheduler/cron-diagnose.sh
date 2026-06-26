#!/bin/bash
# EvoMaster: Self-Diagnosing - Daily 3:00 AM
# Reports to: #evomaster-self-diagnosing

LOG_FILE="$HOME/.openclaw/logs/evomaster-$(date +%Y-%m-%d).log"
SLACK_CHANNEL="evomaster-self-diagnosing"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$TIMESTAMP] [DIAGNOSE] Starting system diagnosis..." >> "$LOG_FILE"

# Example Check: Disk Space
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -gt 90 ]; then
    echo "[ERROR] Disk usage is critically high: ${DISK_USAGE}%" >> "$LOG_FILE"
    DISK_STATUS="⚠️ HIGH (${DISK_USAGE}%)"
else
    echo "[INFO] Disk usage is healthy: ${DISK_USAGE}%" >> "$LOG_FILE"
    DISK_STATUS="✅ OK (${DISK_USAGE}%)"
fi

# Example Check: Process status
if pgrep -x "openclaw" > /dev/null; then
    echo "[INFO] OpenClaw gateway is running." >> "$LOG_FILE"
    GATEWAY_STATUS="✅ Running"
else
    echo "[ERROR] OpenClaw gateway is NOT running." >> "$LOG_FILE"
    GATEWAY_STATUS="❌ DOWN"
fi

# Send Slack notification
openclaw slack send --channel "$SLACK_CHANNEL" --text "🩺 **EvoMaster Self-Diagnosing Complete** ($TIMESTAMP)

📊 System Status:
• Disk Usage: $DISK_STATUS
• OpenClaw Gateway: $GATEWAY_STATUS

📄 Full log: \`$LOG_FILE\`

*Next run: Tomorrow 3:00 AM*" 2>/dev/null || echo "Slack notification failed"

echo "[$TIMESTAMP] [DIAGNOSE] Summary: Diagnosis complete." >> "$LOG_FILE"
echo "Diagnosis complete. See $LOG_FILE for details."
