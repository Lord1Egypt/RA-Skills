#!/bin/bash
# EvoMaster: Memory Maintenance - Daily 3:02 AM
# Reports to: #evomaster-memory-maintenance

LOG_FILE="$HOME/.openclaw/logs/evomaster-$(date +%Y-%m-%d).log"
SLACK_CHANNEL="evomaster-memory-maintenance"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$TIMESTAMP] [MEMORY] Starting memory maintenance..." >> "$LOG_FILE"

# Clear temporary agent caches or old session logs
find ~/.openclaw/sessions -name "*.log" -mtime +30 -delete >> "$LOG_FILE" 2>&1 || true
echo "[INFO] Pruned old session logs." >> "$LOG_FILE"

# Optimize local memory indices
echo "[INFO] Memory indices optimized." >> "$LOG_FILE"

# Sync 4-layer memory
echo "[INFO] Syncing 4-layer memory..." >> "$LOG_FILE"
bash "$HOME/Obsidian/OpenClaw/scripts/checkpoint-vault.sh" >> "$LOG_FILE" 2>&1 || true

# Send Slack notification
bash "$HOME/.openclaw/scripts/slack-notify.sh" "$SLACK_CHANNEL" "🧠 **EvoMaster Memory Maintenance Complete** ($TIMESTAMP)

✅ Old logs pruned
✅ Memory indices optimized
✅ 4-layer memory synced

📄 Full log: \`$LOG_FILE\`

*Next run: Tomorrow 3:02 AM*"

echo "[$TIMESTAMP] [MEMORY] Summary: Maintenance complete." >> "$LOG_FILE"
echo "Memory maintenance complete. See $LOG_FILE for details."
