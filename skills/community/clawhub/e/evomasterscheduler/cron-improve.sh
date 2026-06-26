#!/bin/bash
# EvoMaster: Self-Improving - Daily 3:10 AM
# Reports to: #evomaster-self-improving

LOG_FILE="$HOME/.openclaw/logs/evomaster-$(date +%Y-%m-%d).log"
SLACK_CHANNEL="evomaster-self-improving"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$TIMESTAMP] [IMPROVE] Starting self-improvement analysis..." >> "$LOG_FILE"

# Analyze errors in logs
ERROR_COUNT=$(grep -c "ERROR" "$LOG_FILE" 2>/dev/null || echo 0)
WARN_COUNT=$(grep -c "WARN" "$LOG_FILE" 2>/dev/null || echo 0)

if [ "$ERROR_COUNT" -gt 0 ]; then
    echo "[INFO] Found $ERROR_COUNT errors in today's log." >> "$LOG_FILE"
    STATUS="⚠️ Issues Found"
else
    echo "[INFO] No critical errors found. System stability high." >> "$LOG_FILE"
    STATUS="✅ System Stable"
fi

# Log learnings
LEARNING="EvoMaster analysis at $TIMESTAMP: $ERROR_COUNT errors, $WARN_COUNT warnings"
echo "$LEARNING" >> ~/.openclaw/workspace/skills/xiucheng-self-improving-agent/.learnings/daily.log

# Send Slack notification
bash "$HOME/.openclaw/scripts/slack-notify.sh" "$SLACK_CHANNEL" "📈 **EvoMaster Self-Improving Complete** ($TIMESTAMP)

$STATUS
🔴 Errors: $ERROR_COUNT
⚠️ Warnings: $WARN_COUNT

📝 Learning logged to daily.log

📄 Full log: \`$LOG_FILE\`

*Next run: Tomorrow 3:10 AM*"

echo "[$TIMESTAMP] [IMPROVE] Summary: Analysis complete." >> "$LOG_FILE"
echo "Improvement analysis complete. See $LOG_FILE for details."
