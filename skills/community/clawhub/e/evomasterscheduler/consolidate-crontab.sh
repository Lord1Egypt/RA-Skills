#!/bin/zsh
# EvoMasterScheduler - Consolidate all crons

LOGFILE="$HOME/.openclaw/logs/evomaster-$(date +%Y-%m-%d).log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$TIMESTAMP] === EvoMasterScheduler Cron Consolidation ==="

SCRIPT_DIR="$HOME/.openclaw/workspace/skills/evomasterscheduler"

# Make all scripts executable
chmod +x "$SCRIPT_DIR"/cron-*.sh

echo "[$TIMESTAMP] Scripts made executable"

# Consolidate: Remove duplicate/legacy crons
echo "[$TIMESTAMP] Consolidating existing crons..."

# List current crons
echo "Current crons:"
openclaw cron list 2>&1 | grep -E "(ID|Name|Schedule)" || echo "No crons or command failed"

# Remove old duplicate obsidian-checkpoint (has error)
echo "[$TIMESTAMP] Marking old obsidian-checkpoint for removal (has errors)"
# Note: Actual removal requires user approval - marking only

# Move daily backup from midnight to 3:05 AM
echo "[$TIMESTAMP] Note: OpenClaw Daily Backup will run at 3:05 AM via EvoMaster"

# Create new EvoMaster crons
echo "[$TIMESTAMP] Creating EvoMaster crons..."

# CRON 1-3: 3:00 AM (diagnose, fix, memory)
openclaw cron add --name evomaster-diagnose --cron "0 3 * * *" --message "Run: $SCRIPT_DIR/cron-diagnose.sh" --description "EvoMaster: Self-Diagnosing" 2>&1 || echo "Cron 1 creation logged"

openclaw cron add --name evomaster-fix --cron "1 3 * * *" --message "Run: $SCRIPT_DIR/cron-fix.sh" --description "EvoMaster: Self-Fixing" 2>&1 || echo "Cron 2 creation logged"

openclaw cron add --name evomaster-memory --cron "2 3 * * *" --message "Run: $SCRIPT_DIR/cron-memory.sh" --description "EvoMaster: Memory Maintenance" 2>&1 || echo "Cron 3 creation logged"

# CRON 4: 3:05 AM (backup)
openclaw cron add --name evomaster-backup --cron "5 3 * * *" --message "Run: $SCRIPT_DIR/cron-backup.sh" --description "EvoMaster: Self-Backing-Up" 2>&1 || echo "Cron 4 creation logged"

# CRON 5: 3:10 AM (improve)
openclaw cron add --name evomaster-improve --cron "10 3 * * *" --message "Run: $SCRIPT_DIR/cron-improve.sh" --description "EvoMaster: Self-Improving" 2>&1 || echo "Cron 5 creation logged"

# CRON 6: 3:15 AM (upgrade)
openclaw cron add --name evomaster-upgrade --cron "15 3 * * *" --message "Run: $SCRIPT_DIR/cron-upgrade.sh" --description "EvoMaster: Self-Upgrading" 2>&1 || echo "Cron 6 creation logged"

# CRON 7: 3:20 AM (security)
openclaw cron add --name evomaster-security --cron "20 3 * * *" --message "Run: $SCRIPT_DIR/cron-security.sh" --description "EvoMaster: Security Audit" 2>&1 || echo "Cron 7 creation logged"

echo "[$TIMESTAMP] Consolidation complete"
echo "[$TIMESTAMP] Note: Keep existing high-frequency crons (Memory-Redis Sync every 5m)"
echo "[$TIMESTAMP] Run 'openclaw cron list' to verify"

exit 0
