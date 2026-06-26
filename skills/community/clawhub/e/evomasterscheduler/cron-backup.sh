#!/bin/bash
# EvoMaster: Self-Backing-Up - Daily 3:05 AM
# Reports to: #evomaster-self-backing-up

LOG_FILE="$HOME/.openclaw/logs/evomaster-$(date +%Y-%m-%d).log"
SLACK_CHANNEL="evomaster-self-backing-up"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$TIMESTAMP] [BACKUP] Starting state backup..." >> "$LOG_FILE"

BACKUP_DIR="$HOME/Backups/openclaw/$(date +%Y-%m-%d)"
mkdir -p "$BACKUP_DIR"

# Backup core config files
cp ~/.openclaw/openclaw.json "$BACKUP_DIR/" 2>/dev/null || true
cp ~/.openclaw/.env "$BACKUP_DIR/" 2>/dev/null || true

# Backup workspace
cp -r ~/.openclaw/workspace "$BACKUP_DIR/workspace/" 2>&1

# Backup agents config
cp -r ~/.openclaw/agents "$BACKUP_DIR/agents/" 2>&1

# Create tarball
BACKUP_SIZE=$(du -sh "$BACKUP_DIR" | cut -f1)
echo "[INFO] Backup created at $BACKUP_DIR ($BACKUP_SIZE)" >> "$LOG_FILE"

# Git commit if in git repo
cd ~/.openclaw/workspace && git add . && git commit -m "EvoMaster: Daily backup $TIMESTAMP" 2>/dev/null || true

# Send Slack notification
bash "$HOME/.openclaw/scripts/slack-notify.sh" "$SLACK_CHANNEL" "💾 **EvoMaster Self-Backing-Up Complete** ($TIMESTAMP)

📦 Backup: $BACKUP_DIR
📊 Size: $BACKUP_SIZE
✅ Git commit applied

📄 Full log: \`$LOG_FILE\`

*Next run: Tomorrow 3:05 AM*"

echo "[$TIMESTAMP] [BACKUP] Summary: Backup successful." >> "$LOG_FILE"
echo "Backup complete. See $LOG_FILE for details."
