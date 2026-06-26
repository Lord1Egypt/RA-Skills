#!/bin/bash
# Workspace Backup/Restore/Merge Helper Script

set -e

WORKSPACE_DIR="$HOME/.openclaw/workspace"
BACKUP_DIR="$HOME/openclaw-backups"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

show_usage() {
    echo "Usage: $0 <command> [options]"
    echo ""
    echo "Commands:"
    echo "  backup              Create a backup of workspace"
    echo "  list                List available backups"
    echo "  restore <file>     Restore from a backup file"
    echo "  merge <dir>         Merge another workspace directory"
    echo ""
}

cmd_backup() {
    mkdir -p "$BACKUP_DIR"
    cd "$WORKSPACE_DIR"
    
    BACKUP_FILE="$BACKUP_DIR/workspace-$(date +%Y%m%d-%H%M%S).tar.gz"
    
    tar -czf "$BACKUP_FILE" \
        MEMORY.md memory/ USER.md IDENTITY.md SOUL.md AGENTS.md TOOLS.md HEARTBEAT.md 2>/dev/null
        
    echo -e "${GREEN}Backup created: $BACKUP_FILE${NC}"
    ls -lh "$BACKUP_FILE"
}

cmd_list() {
    echo "Available backups:"
    ls -lh "$BACKUP_DIR"/workspace-*.tar.gz 2>/dev/null || echo "No backups found"
}

cmd_restore() {
    if [ -z "$2" ]; then
        echo "Usage: $0 restore <backup-file>"
        exit 1
    fi
    
    BACKUP_FILE="$2"
    if [ ! -f "$BACKUP_FILE" ]; then
        BACKUP_FILE="$BACKUP_DIR/$2"
    fi
    
    if [ ! -f "$BACKUP_FILE" ]; then
        echo -e "${RED}Backup file not found: $BACKUP_FILE${NC}"
        exit 1
    fi
    
    echo -e "${YELLOW}Restoring from: $BACKUP_FILE${NC}"
    tar -xzf "$BACKUP_FILE" -C "$WORKSPACE_DIR"
    echo -e "${GREEN}Restore complete!${NC}"
}

cmd_merge() {
    if [ -z "$2" ]; then
        echo "Usage: $0 merge <source-workspace-dir>"
        exit 1
    fi
    
    SOURCE_DIR="$2"
    if [ ! -d "$SOURCE_DIR" ]; then
        echo -e "${RED}Source directory not found: $SOURCE_DIR${NC}"
        exit 1
    fi
    
    echo -e "${YELLOW}Merging from: $SOURCE_DIR${NC}"
    
    # Merge memory files
    if [ -d "$SOURCE_DIR/memory" ]; then
        echo "Merging memory files..."
        mkdir -p "$WORKSPACE_DIR/memory"
        cp -rn "$SOURCE_DIR/memory/"* "$WORKSPACE_DIR/memory/" 2>/dev/null || true
    fi
    
    # Merge TOOLS.md
    if [ -f "$SOURCE_DIR/TOOLS.md" ]; then
        echo "Merging TOOLS.md..."
        cat "$SOURCE_DIR/TOOLS.md" >> "$WORKSPACE_DIR/TOOLS.md"
    fi
    
    # 提示用户手动合并
    echo ""
    echo -e "${YELLOW}Manual merge needed for:${NC}"
    echo "  - MEMORY.md (use vimdiff)"
    echo "  - IDENTITY.md (choose one)"
    echo "  - SOUL.md (choose one or merge)"
    echo ""
    echo "Run: vimdiff $WORKSPACE_DIR/MEMORY.md $SOURCE_DIR/MEMORY.md"
}

case "$1" in
    backup)
        cmd_backup "$@"
        ;;
    list)
        cmd_list
        ;;
    restore)
        cmd_restore "$@"
        ;;
    merge)
        cmd_merge "$@"
        ;;
    *)
        show_usage
        ;;
esac
