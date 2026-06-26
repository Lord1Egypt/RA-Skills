#!/bin/bash
# EvoMaster: Self-Fixing - Daily 3:01 AM
# Reports to: #evomaster-self-fixing

LOG_FILE="$HOME/.openclaw/logs/evomaster-$(date +%Y-%m-%d).log"
SLACK_CHANNEL="evomaster-self-fixing"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$TIMESTAMP] [FIX] Starting automated remediation..." >> "$LOG_FILE"

FIXES_APPLIED=0

# Fix: Restart OpenClaw if down
if ! pgrep -x "openclaw" > /dev/null; then
    echo "[WARN] OpenClaw is down. Attempting restart..." >> "$LOG_FILE"
    openclaw gateway start >> "$LOG_FILE" 2>&1
    echo "[INFO] Restart command issued." >> "$LOG_FILE"
    FIXES_APPLIED=$((FIXES_APPLIED + 1))
else
    echo "[INFO] OpenClaw is healthy. No fix needed." >> "$LOG_FILE"
fi

# Send Slack notification
bash "$HOME/.openclaw/scripts/slack-notify.sh" "$SLACK_CHANNEL" "🔧 **EvoMaster Self-Fixing Complete** ($TIMESTAMP)

🔧 Fixes applied: $FIXES_APPLIED

📄 Full log: \`$LOG_FILE\`

*Next run: Tomorrow 3:01 AM*"

echo "[$TIMESTAMP] [FIX] Summary: Remediation complete." >> "$LOG_FILE"
echo "Remediation complete. See $LOG_FILE for details."
