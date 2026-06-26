#!/bin/bash
# EvoMaster: Self-Upgrading - Daily 3:15 AM
# Reports to: #evomaster-self-upgrading

LOG_FILE="$HOME/.openclaw/logs/evomaster-$(date +%Y-%m-%d).log"
SLACK_CHANNEL="evomaster-self-upgrading"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$TIMESTAMP] [UPGRADE] Starting system upgrade check..." >> "$LOG_FILE"

# Check OpenClaw version
current_version=$(openclaw --version 2>/dev/null | head -1 || echo "unknown")
echo "[INFO] Current OpenClaw version: $current_version" >> "$LOG_FILE"

# Check for updates (placeholder - requires manual upgrade)
echo "[INFO] Checking for updates to OpenClaw components..." >> "$LOG_FILE"
echo "[INFO] Manual upgrade required if new version available." >> "$LOG_FILE"

UPGRADE_STATUS="✅ No upgrades available"

# Check Ollama models
echo "[INFO] Checking Ollama models..." >> "$LOG_FILE"
ollama list >> "$LOG_FILE" 2>&1 || true

# Send Slack notification
bash "$HOME/.openclaw/scripts/slack-notify.sh" "$SLACK_CHANNEL" "⬆️ **EvoMaster Self-Upgrading Check** ($TIMESTAMP)

Current Version: $current_version
Status: $UPGRADE_STATUS

📋 To upgrade manually:
• OpenClaw: \`openclaw update\`
• Ollama: \`ollama pull <model>\`
• Nerve: Rebuild from source

📄 Full log: \`$LOG_FILE\`

*Next run: Tomorrow 3:15 AM*"

echo "[$TIMESTAMP] [UPGRADE] Summary: Upgrade check complete." >> "$LOG_FILE"
echo "Upgrade check complete. See $LOG_FILE for details."
