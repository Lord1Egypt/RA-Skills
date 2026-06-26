#!/bin/bash
#
# One-Click Backup for OpenClaw Workspace v3.0.8
# Usage: ./one-click-backup.sh [output_dir] [--dry-run] [--list] [--with-sessions]
#
# Improvements in v3.0.8:
# - FIXED: tar --exclude flag applies to all paths including explicit adds, fixed by conditional EXCLUDE_ITEMS
#
# Improvements in v3.0.7:
# - Attempted fix for --with-sessions bug (but the fix was wrong)
#
# Improvements in v2.2.2:
# - FIXED: --with-sessions now correctly includes session records
# - FIXED: Removed .backup-sessions from EXCLUDE_ITEMS
#
# Improvements in v2.2.1:
# - FIXED: Cron export files correctly included in archive
# - FIXED: Changed from wildcard to explicit file addition
#
# Improvements in v2.2:
# - Session records backup (optional)
# - Cron tasks integrated into main archive
# - Better security exclusions
#

set -e

WORKSPACE_DIR="$HOME/.openclaw/workspace"
OPENCLAW_DIR="$HOME/.openclaw"
DEFAULT_OUTPUT_DIR="$HOME/.openclaw/backups"
OUTPUT_DIR=""
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Parse arguments
DRY_RUN=false
LIST_MODE=false
WITH_SESSIONS=false
OUTPUT_DIR_SET=false

for arg in "$@"; do
    case $arg in
        --dry-run)
            DRY_RUN=true
            ;;
        --list)
            LIST_MODE=true
            ;;
        --with-sessions)
            WITH_SESSIONS=true
            ;;
        *)
            if [ "$OUTPUT_DIR_SET" = false ]; then
                OUTPUT_DIR="$arg"
                OUTPUT_DIR_SET=true
            fi
            ;;
    esac
done

if [ "$OUTPUT_DIR_SET" = false ]; then
    OUTPUT_DIR="$DEFAULT_OUTPUT_DIR"
fi

BACKUP_FILE="$OUTPUT_DIR/clawmerge-$TIMESTAMP.tar.gz"

# List mode
if [ "$LIST_MODE" = true ]; then
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}  Available Backups${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    
    if [ -d "$OUTPUT_DIR" ]; then
        BACKUP_COUNT=$(ls -1 "$OUTPUT_DIR"/clawmerge-*.tar.gz 2>/dev/null | wc -l)
        if [ "$BACKUP_COUNT" -gt 0 ]; then
            echo -e "${YELLOW}Backup directory:${NC} $OUTPUT_DIR"
            echo -e "${YELLOW}Total backups:${NC} $BACKUP_COUNT"
            echo ""
            ls -lht "$OUTPUT_DIR"/clawmerge-*.tar.gz | awk '{print "  " $9 " (" $5 ") " $6 " " $7 " " $8}'
            echo ""
        else
            echo -e "${YELLOW}No backups found in $OUTPUT_DIR${NC}"
        fi
    else
        echo -e "${RED}Backup directory not found: $OUTPUT_DIR${NC}"
    fi
    exit 0
fi

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  OpenClaw Workspace Backup v3.0.8${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

if [ ! -d "$WORKSPACE_DIR" ]; then
    echo -e "${RED}Error: Workspace not found at $WORKSPACE_DIR${NC}"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

# ============================================
# Step 0: Export public configuration (auto)
# ============================================
echo -e "${YELLOW}[0/6] Exporting public configuration...${NC}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_SCRIPTS_DIR="$WORKSPACE_DIR/scripts"
CONFIGS_DIR="$WORKSPACE_DIR/configs"

# Check if export script exists
if [ -f "$WORKSPACE_SCRIPTS_DIR/export-public-config.py" ]; then
    # Ensure configs directory exists
    mkdir -p "$CONFIGS_DIR" 2>/dev/null || true
    
    # Run export
    if python3 "$WORKSPACE_SCRIPTS_DIR/export-public-config.py" >/dev/null 2>&1; then
        echo -e "  ${GREEN}✓ Public configuration exported${NC}"
    else
        echo -e "  ${YELLOW}⚠ Export script ran but may have warnings${NC}"
    fi
else
    echo -e "  ${BLUE}ℹ Export script not found (v2.3.0+ feature)${NC}"
fi
echo ""

# ============================================
# Step 0.5: Generate Python dependencies list (v2.5.0+)
# ============================================
echo -e "${YELLOW}[0.5/7] Generating Python dependencies list...${NC}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "$SCRIPT_DIR/gen-requirements.py" ]; then
    if python3 "$SCRIPT_DIR/gen-requirements.py" --output "$WORKSPACE_DIR/requirements.txt" >/dev/null 2>&1; then
        DEP_COUNT=$(wc -l < "$WORKSPACE_DIR/requirements.txt" 2>/dev/null || echo "0")
        echo -e "  ${GREEN}✓ Python dependencies exported ($DEP_COUNT packages)${NC}"
    else
        echo -e "  ${YELLOW}⚠ Python deps generation had warnings${NC}"
    fi
else
    echo -e "  ${BLUE}ℹ gen-requirements.py not found (v2.5.0+ feature)${NC}"
fi
echo ""

# ============================================
# Step 1: Discover and collect task scripts
# ============================================
echo -e "${YELLOW}[1/7] Discovering task scripts...${NC}"
if [ -f "$WORKSPACE_SCRIPTS_DIR/discover-scripts.py" ]; then
    mkdir -p "$CONFIGS_DIR" 2>/dev/null || true
    
    if python3 "$WORKSPACE_SCRIPTS_DIR/discover-scripts.py" >/dev/null 2>&1; then
        echo -e "  ${GREEN}✓ Task scripts discovered${NC}"
        echo -e "  ${BLUE}  List: $CONFIGS_DIR/scripts-list.json${NC}"
    else
        echo -e "  ${YELLOW}⚠ Script discovery completed with warnings${NC}"
    fi
else
    echo -e "  ${BLUE}ℹ Discover script not found (v2.4.0+ feature)${NC}"
fi
echo ""

# ============================================
# Step 2: Export cron tasks to temp file
# ============================================
CRON_EXPORT_DIR=$(mktemp -d)
trap "rm -rf $CRON_EXPORT_DIR" EXIT

echo -e "${YELLOW}[2/6] Exporting cron tasks...${NC}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "$SCRIPT_DIR/backup-cron-tasks.sh" ]; then
    bash "$SCRIPT_DIR/backup-cron-tasks.sh" "$CRON_EXPORT_DIR" >/dev/null 2>&1 || true
fi

# Copy cron files to workspace for inclusion in archive
cp "$CRON_EXPORT_DIR"/cron-tasks-*.json "$WORKSPACE_DIR/" 2>/dev/null && echo -e "  ${GREEN}✓ Cron tasks exported${NC}" || echo -e "  ${BLUE}○ No cron tasks${NC}"
cp "$CRON_EXPORT_DIR"/system-crontab-*.txt "$WORKSPACE_DIR/" 2>/dev/null && echo -e "  ${GREEN}✓ System crontab exported${NC}" || true
echo ""

# ============================================
# Step 3: Export session records (optional)
# ============================================
SESSIONS_EXPORT_DIR=""
if [ "$WITH_SESSIONS" = true ]; then
    SESSIONS_EXPORT_DIR=$(mktemp -d)
    trap "rm -rf $SESSIONS_EXPORT_DIR" EXIT
    
    echo -e "${YELLOW}[3/6] Exporting session records...${NC}"
    SESSIONS_DIR="$OPENCLAW_DIR/agents/main/sessions"
    
    if [ -d "$SESSIONS_DIR" ]; then
        # Copy session files
        cp -r "$SESSIONS_DIR" "$SESSIONS_EXPORT_DIR/" 2>/dev/null || true
        
        # Copy to workspace for inclusion
        if [ -d "$SESSIONS_EXPORT_DIR/sessions" ]; then
            cp -r "$SESSIONS_EXPORT_DIR/sessions" "$WORKSPACE_DIR/.backup-sessions" 2>/dev/null || true
            echo -e "  ${GREEN}✓ Session records exported${NC}"
            echo -e "  ${CYAN}  Note: Sessions include conversation history${NC}"
        fi
    else
        echo -e "  ${BLUE}○ No session records found${NC}"
    fi
    echo ""
fi

# ============================================
# Step 4: Create backup archive
# ============================================
echo -e "${YELLOW}[4/6] Creating backup archive...${NC}"

cd "$WORKSPACE_DIR"

# v3.0.8: Build EXCLUDE_ITEMS conditionally based on WITH_SESSIONS
# When WITH_SESSIONS=true, .backup-sessions must NOT be in the exclude list
EXCLUDE_ITEMS=(
    "*.tar.gz"          # Old backups
    ".git"              # Git history
    ".clawhub"          # ClawHub metadata
    ".openclaw"         # Internal configs
    "config.yaml"       # User config (sensitive)
    "*.log"             # Log files
    ".DS_Store"         # macOS metadata
    "__pycache__"       # Python cache
    "node_modules"      # NPM dependencies
    "cron-tasks-*.json" # Temp cron export (handled separately)
    "system-crontab-*.txt" # Temp cron export (handled separately)
)

# Only exclude .backup-sessions when NOT including sessions
if [ "$WITH_SESSIONS" != true ]; then
    EXCLUDE_ITEMS+=(".backup-sessions")
fi

# Build tar exclude options
TAR_EXCLUDES=""
for exc in "${EXCLUDE_ITEMS[@]}"; do
    TAR_EXCLUDES="$TAR_EXCLUDES --exclude=$exc"
done

if [ "$DRY_RUN" = true ]; then
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}  DRY RUN - Simulating backup${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    
    echo -e "${YELLOW}Files that would be backed up (excluding ${#EXCLUDE_ITEMS[@]} patterns):${NC}"
    # Use find to show what would be backed up
    find . -maxdepth 3 \
        ! -path "*/\.*" \
        ! -name "*.tar.gz" \
        ! -name "*.log" \
        ! -name "config.yaml" \
        ! -path "*/node_modules/*" \
        ! -path "*/__pycache__/*" \
        ! -path "*/.git/*" \
        ! -path "*/.clawhub/*" \
        ! -path "*/.openclaw/*" \
        ! -name ".DS_Store" \
        ! -path "*/.backup-sessions/*" \
        ! -name "cron-tasks-*.json" \
        ! -name "system-crontab-*.txt" \
        -type f 2>/dev/null | head -30
    echo "  ... (and more)"
    
    echo ""
    echo -e "${BLUE}Output would be:${NC} $BACKUP_FILE"
    echo ""
    echo -e "${GREEN}Done! (no files modified)${NC}"
    
    # Cleanup temp files
    rm -f "$WORKSPACE_DIR"/cron-tasks-*.json "$WORKSPACE_DIR"/system-crontab-*.txt 2>/dev/null || true
    rm -rf "$WORKSPACE_DIR/.backup-sessions" 2>/dev/null || true
    exit 0
fi

# Create archive - backup ALL files except excluded items
echo -e "${CYAN}  Backing up all files (except ${#EXCLUDE_ITEMS[@]} exclude patterns)...${NC}"
tar -czvf "$BACKUP_FILE" $TAR_EXCLUDES -C "$WORKSPACE_DIR" . 2>&1 | tail -10
if [ "$WITH_SESSIONS" = true ]; then
    echo -e "  ${GREEN}✓ Session records included${NC}"
fi

# Verify backup
if tar -tzf "$BACKUP_FILE" | grep -q "MEMORY.md"; then
    echo -e "  ${GREEN}✓ Core files verified in archive${NC}"
else
    echo -e "  ${YELLOW}⚠ Core files may not be in archive${NC}"
fi

echo ""

# Cleanup temp files from workspace AFTER backup is complete
rm -f "$WORKSPACE_DIR"/cron-tasks-*.json "$WORKSPACE_DIR"/system-crontab-*.txt 2>/dev/null || true
rm -rf "$WORKSPACE_DIR/.backup-sessions" 2>/dev/null || true

# ============================================
# Step 5: Verify and summary
# ============================================
echo -e "${YELLOW}[5/6] Verifying backup...${NC}"
if [ -f "$BACKUP_FILE" ]; then
    SIZE=$(ls -lh "$BACKUP_FILE" | awk '{print $5}')
    CHECKSUM=$(md5sum "$BACKUP_FILE" | awk '{print $1}')
    
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}  Backup Complete!${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo -e "File: ${YELLOW}$BACKUP_FILE${NC}"
    echo -e "Size: ${YELLOW}$SIZE${NC}"
    echo -e "MD5:  ${YELLOW}$CHECKSUM${NC}"
    echo ""
    
    # Show what was included
    echo -e "${CYAN}Backup contents:${NC}"
    tar -tzf "$BACKUP_FILE" | head -20
    if [ $(tar -tzf "$BACKUP_FILE" | wc -l) -gt 20 ]; then
        echo "  ... (and more)"
    fi
    echo ""
    
    # Rotation
    cd "$OUTPUT_DIR"
    BACKUP_COUNT=$(ls -1 clawmerge-*.tar.gz 2>/dev/null | wc -l)
    if [ "$BACKUP_COUNT" -gt 10 ]; then
        echo -e "${YELLOW}Cleaning up old backups (keeping last 10)...${NC}"
        ls -1t clawmerge-*.tar.gz | tail -n +11 | xargs -r rm -f
    fi
    
    echo -e "${BLUE}Tip:${NC} Run with --list to see all backups"
    echo -e "${BLUE}Tip:${NC} Add --with-sessions to include session records"
else
    echo -e "${RED}Error: Backup failed!${NC}"
    exit 1
fi

echo -e "${GREEN}Done!${NC}"
