#!/bin/bash
# OpenClaw Configuration Restore Script
# Usage: ./restore_openclaw.sh <backup-archive>

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check arguments
if [ -z "$1" ]; then
    echo -e "${RED}Error: Backup archive path required${NC}"
    echo "Usage: $0 <backup-archive.tar.gz>"
    exit 1
fi

BACKUP_ARCHIVE="$1"

# Check if archive exists
if [ ! -f "$BACKUP_ARCHIVE" ]; then
    echo -e "${RED}Error: Backup archive not found: $BACKUP_ARCHIVE${NC}"
    exit 1
fi

# Check for info file
INFO_FILE="${BACKUP_ARCHIVE%.tar.gz}.info"
if [ -f "$INFO_FILE" ]; then
    echo -e "${BLUE}=== Backup Information ===${NC}"
    cat "$INFO_FILE"
    echo ""
fi

# Warning prompt
echo -e "${YELLOW}⚠ WARNING: This will overwrite your current OpenClaw configuration!${NC}"
echo -e "${YELLOW}Files to be restored:${NC}"
tar -tzf "$BACKUP_ARCHIVE" | sed 's|^|  - |'

echo ""
read -p "$(echo -e ${BLUE}Continue? (yes/no): ${NC})" confirm

if [ "$confirm" != "yes" ]; then
    echo -e "${YELLOW}Restore cancelled.${NC}"
    exit 0
fi

# Create temporary directory for extraction
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

echo ""
echo -e "${GREEN}Extracting backup...${NC}"
tar -xzf "$BACKUP_ARCHIVE" -C "$TEMP_DIR"

# Restore function
restore_item() {
    local source="$1"
    local target="$2"
    local name="$3"
    
    if [ -e "$TEMP_DIR/$source" ]; then
        echo -e "${GREEN}[✓]${NC} Restoring $name..."
        
        # Backup existing if it exists
        if [ -e "$target" ]; then
            echo -e "${YELLOW}  → Backing up existing $name to ${target}.bak${NC}"
            mv "$target" "${target}.bak"
        fi
        
        # Move restored item to target
        mv "$TEMP_DIR/$source" "$target"
        return 0
    else
        echo -e "${YELLOW}[−]${NC} $name not in backup, skipping..."
        return 0
    fi
}

# Restore OpenClaw configuration directories
restore_item ".openclaw" "$HOME/.openclaw" ".openclaw (main config)"
restore_item ".config/openclaw" "$HOME/.config/openclaw" ".config/openclaw (system config)"
restore_item ".local/share/openclaw" "$HOME/.local/share/openclaw" ".local/share/openclaw (local data)"

echo ""
echo -e "${GREEN}=== Restore Complete ===${NC}"
echo -e "${YELLOW}Original configurations backed up with .bak extension${NC}"
echo -e "${YELLOW}Restart OpenClaw Gateway to apply changes:${NC}"
echo -e "  systemctl --user restart openclaw-gateway"
echo ""
