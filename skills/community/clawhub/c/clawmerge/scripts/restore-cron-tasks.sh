#!/bin/bash
#
# Restore Cron Tasks for OpenClaw
# Imports cron jobs from a backup file
# Usage: ./restore-cron-tasks.sh <cron_export_file>
#

set -e

CRON_EXPORT_FILE="$1"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

show_usage() {
    echo -e "${YELLOW}Usage:${NC} $0 <cron_export_file>"
    echo ""
    echo -e "${YELLOW}Description:${NC}"
    echo "  Restores cron tasks from a backup file created by backup-cron-tasks.sh"
    echo ""
    echo -e "${YELLOW}Important:${NC}"
    echo "  OpenClaw cron tasks are stored in Gateway configuration."
    echo "  This script provides migration guidance, but cron jobs must be"
    echo "  manually recreated or restored via config file."
    echo ""
    echo -e "${YELLOW}Alternative (Full Config Restore):${NC}"
    echo "  cp /path/to/backup/openclaw.json ~/.openclaw/openclaw.json"
    echo "  openclaw gateway restart"
}

if [ -z "$CRON_EXPORT_FILE" ] || [ "$CRON_EXPORT_FILE" = "--help" ]; then
    show_usage
    exit 1
fi

if [ ! -f "$CRON_EXPORT_FILE" ]; then
    echo -e "${RED}Error: File not found: $CRON_EXPORT_FILE${NC}"
    exit 1
fi

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Cron Tasks Restore${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

echo -e "${YELLOW}Export file:${NC} $CRON_EXPORT_FILE"
echo ""

# Check if it's a system crontab backup
if [[ "$CRON_EXPORT_FILE" == *"system-crontab"* ]]; then
    echo -e "${YELLOW}Detected: System crontab backup${NC}"
    echo ""
    
    if grep -q "^#" "$CRON_EXPORT_FILE" && ! grep -v "^#" "$CRON_EXPORT_FILE" | grep -q "."; then
        echo -e "${BLUE}No cron entries to restore (file contains only comments)${NC}"
    else
        echo -e "${YELLOW}To restore system crontab, run:${NC}"
        echo "  crontab $CRON_EXPORT_FILE"
        echo ""
        read -p "Restore now? [y/N] " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            crontab "$CRON_EXPORT_FILE"
            echo -e "${GREEN}✓ System crontab restored${NC}"
        fi
    fi
else
    # OpenClaw cron export
    echo -e "${YELLOW}OpenClaw Cron Migration Guide:${NC}"
    echo ""
    echo "OpenClaw cron tasks are stored in the Gateway configuration file."
    echo ""
    echo -e "${BLUE}Option 1: Restore Full Config (Recommended)${NC}"
    echo "  If you backed up openclaw.json, restore it:"
    echo "  cp /path/to/backup/openclaw.json ~/.openclaw/openclaw.json"
    echo "  openclaw gateway restart"
    echo ""
    echo -e "${BLUE}Option 2: Manually Recreate Cron Jobs${NC}"
    echo "  1. List current cron jobs: clawhub cron list"
    echo "  2. Add jobs manually: clawhub cron add --job '<job_config>'"
    echo "  3. Or use the OpenClaw cron tool in your session"
    echo ""
    echo -e "${BLUE}Option 3: Check HEARTBEAT.md${NC}"
    echo "  Periodic tasks may be defined in HEARTBEAT.md"
    echo "  Review and update as needed"
    echo ""
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Restore Guidance Complete${NC}"
echo -e "${GREEN}========================================${NC}"
