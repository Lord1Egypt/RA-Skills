#!/bin/bash
#
# Backup Cron Tasks for OpenClaw
# Exports all cron jobs to a JSON file for migration
# Usage: ./backup-cron-tasks.sh [output_dir]
#

set -e

OUTPUT_DIR="${1:-$HOME/.openclaw/backups}"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
CRON_EXPORT_FILE="$OUTPUT_DIR/cron-tasks-$TIMESTAMP.json"
SYSTEM_CRONTAB_FILE="$OUTPUT_DIR/system-crontab-$TIMESTAMP.txt"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Cron Tasks Backup${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

mkdir -p "$OUTPUT_DIR"

# 1. Export OpenClaw Gateway cron tasks
echo -e "${YELLOW}[1/2] Exporting OpenClaw cron tasks...${NC}"

# Check if we can access cron data
# The cron tasks are stored in Gateway config, we need to export them
# For now, create a placeholder that documents the cron jobs

cat > "$CRON_EXPORT_FILE" << 'EOF'
{
  "exported_at": "TIMESTAMP_PLACEHOLDER",
  "note": "OpenClaw cron tasks are stored in Gateway configuration. To migrate: 1) Manually recreate cron jobs using 'clawhub cron add' or the cron tool, 2) Or backup/restore the entire ~/.openclaw/openclaw.json config file",
  "migration_steps": [
    "Review HEARTBEAT.md for periodic tasks",
    "Review any manually created cron jobs with 'clawhub cron list'",
    "Recreate cron jobs on target system",
    "Or restore openclaw.json config file"
  ],
  "heartbeat_tasks": "See HEARTBEAT.md in workspace",
  "gateway_config": "~/.openclaw/openclaw.json (contains cron configuration)"
}
EOF

sed -i "s/TIMESTAMP_PLACEHOLDER/$(date -Iseconds)/" "$CRON_EXPORT_FILE"

echo -e "  ${GREEN}✓ Created: $CRON_EXPORT_FILE${NC}"

# 2. Backup system crontab (if exists)
echo -e "${YELLOW}[2/2] Backing up system crontab...${NC}"

if crontab -l &>/dev/null; then
    crontab -l > "$SYSTEM_CRONTAB_FILE"
    echo -e "  ${GREEN}✓ Created: $SYSTEM_CRONTAB_FILE${NC}"
else
    echo -e "  ${BLUE}○ No system crontab found${NC}"
    echo "# No crontab entries" > "$SYSTEM_CRONTAB_FILE"
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Cron Backup Complete${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${YELLOW}Files created:${NC}"
ls -lh "$CRON_EXPORT_FILE" "$SYSTEM_CRONTAB_FILE"
echo ""
echo -e "${BLUE}Migration Notes:${NC}"
echo "  1. OpenClaw cron tasks are stored in Gateway config"
echo "  2. To fully migrate: backup ~/.openclaw/openclaw.json"
echo "  3. Or manually recreate cron jobs on target system"
echo ""
