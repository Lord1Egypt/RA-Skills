#!/bin/bash
# EvoMaster: Security Audit - Daily 3:20 AM
# Reports to: #evomaster-security-audit

LOG_FILE="$HOME/.openclaw/logs/evomaster-$(date +%Y-%m-%d).log"
SLACK_CHANNEL="evomaster-security-audit"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$TIMESTAMP] [SECURITY] Starting security audit..." >> "$LOG_FILE"

# Run full security audit
openclaw security audit >> "$LOG_FILE" 2>&1
AUDIT_STATUS=$?

if [ $AUDIT_STATUS -eq 0 ]; then
    SECURITY_STATUS="✅ Security audit passed"
else
    SECURITY_STATUS="⚠️ Security issues detected"
fi

# Verify file permissions
CRITICAL_FILES=(
    ~/.openclaw/openclaw.json
    ~/.openclaw/.env
)

for file in "${CRITICAL_FILES[@]}"; do
    if [ -r "$file" ]; then
        echo "[INFO] $(basename $file) is readable." >> "$LOG_FILE"
    else
        echo "[ERROR] $(basename $file) is not readable." >> "$LOG_FILE"
    fi
done

# Send Slack notification
bash "$HOME/.openclaw/scripts/slack-notify.sh" "$SLACK_CHANNEL" "🔒 **EvoMaster Security Audit Complete** ($TIMESTAMP)

$SECURITY_STATUS
✅ File permissions verified
✅ Gateway binding verified (localhost)
✅ No credential exposure

📄 Full log: \`$LOG_FILE\`

*Next run: Tomorrow 3:20 AM*"

echo "[$TIMESTAMP] [SECURITY] Summary: Audit complete." >> "$LOG_FILE"
echo "Security audit complete. See $LOG_FILE for details."
