#!/bin/bash
#
# One-Click Full Disaster Backup for OpenClaw v1.1
# 用途：备份 workspace + 系统配置，重装系统后一键恢复
#
# 包含：
#   - workspace（所有文件，排除缓存）
#   - openclaw.json（Gateway 配置，含 token）
#   - cron/jobs.json（定时任务）
#   - agents/main/agent/（认证配置）
#   - sessions/（对话记录，可选排除）
#
# 用法：
#   ./one-click-full-backup.sh [output_path] [--dry-run] [--no-sessions]
#
set -e

OPENCLAW_DIR="$HOME/.openclaw"
WORKSPACE_DIR="$HOME/.openclaw/workspace"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
DEFAULT_OUTPUT="$HOME/openclaw-full-backup-$TIMESTAMP.tar.gz"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Parse arguments
DRY_RUN=false
NO_SESSIONS=false
OUTPUT_FILE=""

for arg in "$@"; do
    case $arg in
        --dry-run)
            DRY_RUN=true
            ;;
        --no-sessions)
            NO_SESSIONS=true
            ;;
        --help)
            echo "用法: $0 [output_path] [options]"
            echo ""
            echo "选项:"
            echo "  --dry-run      预览模式，不实际备份"
            echo "  --no-sessions  排除 session 记录（减少备份大小）"
            exit 0
            ;;
        *)
            OUTPUT_FILE="$arg"
            ;;
    esac
done

[ -z "$OUTPUT_FILE" ] && OUTPUT_FILE="$DEFAULT_OUTPUT"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  OpenClaw Full Disaster Backup v1.1${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Check prerequisites
if [ ! -d "$OPENCLAW_DIR" ]; then
    echo -e "${RED}Error: OpenClaw directory not found: $OPENCLAW_DIR${NC}"
    exit 1
fi

if [ ! -d "$WORKSPACE_DIR" ]; then
    echo -e "${RED}Error: Workspace not found: $WORKSPACE_DIR${NC}"
    exit 1
fi

# Create temp directory
TEMP_DIR=$(mktemp -d)
BACKUP_DIR="$TEMP_DIR/openclaw-full-backup"
mkdir -p "$BACKUP_DIR"

echo -e "${YELLOW}[1/5] Preparing backup directory...${NC}"
mkdir -p "$BACKUP_DIR/workspace"
mkdir -p "$BACKUP_DIR/system"
mkdir -p "$BACKUP_DIR/cron"
mkdir -p "$BACKUP_DIR/agents"
echo "  ✓ Temp directory created: $TEMP_DIR"
echo ""

# ============================================
# Step 1: Backup openclaw.json
# ============================================
echo -e "${YELLOW}[2/5] Backing up system configuration...${NC}"

OPENCLAW_JSON="$OPENCLAW_DIR/openclaw.json"
if [ -f "$OPENCLAW_JSON" ]; then
    cp "$OPENCLAW_JSON" "$BACKUP_DIR/system/openclaw.json"
    echo "  ✓ openclaw.json (Gateway config + token)"
else
    echo -e "  ${RED}✗ openclaw.json not found!${NC}"
fi

# Backup .env if exists
if [ -f "$OPENCLAW_DIR/.env" ]; then
    cp "$OPENCLAW_DIR/.env" "$BACKUP_DIR/system/.env"
    echo "  ✓ .env"
fi

# Backup agents config
AGENTS_DIR="$OPENCLAW_DIR/agents/main/agent"
if [ -d "$AGENTS_DIR" ]; then
    cp -r "$AGENTS_DIR" "$BACKUP_DIR/agents/"
    echo "  ✓ agents/main/agent/ (auth config)"
fi

echo ""

# ============================================
# Step 2: Backup cron jobs
# ============================================
echo -e "${YELLOW}[3/5] Backing up cron tasks...${NC}"

CRON_JOBS="$OPENCLAW_DIR/cron/jobs.json"
if [ -f "$CRON_JOBS" ]; then
    cp "$CRON_JOBS" "$BACKUP_DIR/cron/jobs.json"
    echo "  ✓ cron/jobs.json ($(wc -c < "$CRON_JOBS") bytes)"
fi

# Also backup jobs-state.json
if [ -f "$OPENCLAW_DIR/cron/jobs-state.json" ]; then
    cp "$OPENCLAW_DIR/cron/jobs-state.json" "$BACKUP_DIR/cron/jobs-state.json"
    echo "  ✓ cron/jobs-state.json"
fi

echo ""

# ============================================
# Step 3: Backup workspace (exclude patterns)
# ============================================
echo -e "${YELLOW}[4/5] Backing up workspace...${NC}"

# Exclusion patterns
EXCLUDE_PATTERNS=(
    "*.tar.gz"
    ".git"
    ".clawhub"
    "*.log"
    "__pycache__"
    "node_modules"
    ".DS_Store"
    "cron-tasks-*.json"
    "system-crontab-*.txt"
)

TAR_EXCLUDES=""
for exc in "${EXCLUDE_PATTERNS[@]}"; do
    TAR_EXCLUDES="$TAR_EXCLUDES --exclude=$exc"
done

if [ "$DRY_RUN" = true ]; then
    echo -e "${BLUE}DRY RUN - Would backup workspace with exclusions:${NC}"
    find "$WORKSPACE_DIR" -maxdepth 2 \
        ! -path "*/\.*" \
        ! -path "*/__pycache__/*" \
        ! -path "*/node_modules/*" \
        ! -name "*.tar.gz" \
        ! -name "*.log" \
        -type f 2>/dev/null | head -20
    echo "  ... (and more)"
else
    tar -czf "$BACKUP_DIR/workspace.tar.gz" $TAR_EXCLUDES -C "$WORKSPACE_DIR" . 2>/dev/null
    WS_SIZE=$(ls -lh "$BACKUP_DIR/workspace.tar.gz" | awk '{print $5}')
    echo "  ✓ workspace.tar.gz ($WS_SIZE)"
fi

echo ""

# ============================================
# Step 4: Backup sessions (optional)
# ============================================
echo -e "${YELLOW}[5/5] Backing up session records...${NC}"

SESSIONS_DIR="$OPENCLAW_DIR/agents/main/sessions"
SESSION_SIZE_GB=$(du -sh "$SESSIONS_DIR" 2>/dev/null | awk '{print $1}' || echo "unknown")

if [ "$NO_SESSIONS" = true ]; then
    echo -e "  ${CYAN}○ Skipped (--no-sessions specified)${NC}"
elif [ -d "$SESSIONS_DIR" ] && [ "$(ls -A "$SESSIONS_DIR" 2>/dev/null)" ]; then
    SESSION_COUNT=$(ls -1 "$SESSIONS_DIR"/*.jsonl 2>/dev/null | wc -l || echo 0)
    
    if [ "$DRY_RUN" = true ]; then
        echo -e "${BLUE}DRY RUN - Would backup sessions:${NC}"
        echo "  Directory: $SESSIONS_DIR"
        echo "  Size: $SESSION_SIZE_GB"
        echo "  Files: $SESSION_COUNT session files"
    else
        # Compress sessions
        tar -czf "$BACKUP_DIR/sessions.tar.gz" -C "$SESSIONS_DIR" . 2>/dev/null || true
        if [ -f "$BACKUP_DIR/sessions.tar.gz" ]; then
            SESSION_COMPRESSED_SIZE=$(ls -lh "$BACKUP_DIR/sessions.tar.gz" | awk '{print $5}')
            echo "  ✓ sessions.tar.gz ($SESSION_COMPRESSED_SIZE, $SESSION_COUNT files)"
        else
            echo -e "  ${YELLOW}⚠ No sessions found or failed to compress${NC}"
        fi
    fi
else
    echo -e "  ${CYAN}○ No session records found${NC}"
fi

echo ""

# ============================================
# Step 5: Create final archive
# ============================================
if [ "$DRY_RUN" = true ]; then
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}  DRY RUN Complete${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo "Would create: $OUTPUT_FILE"
    rm -rf "$TEMP_DIR"
    exit 0
fi

echo -e "${YELLOW}[6/6] Creating final archive...${NC}"

# Create manifest
cat > "$BACKUP_DIR/MANIFEST.txt" << EOF
OpenClaw Full Disaster Backup
==============================
Created: $(date +%Y-%m-%d\ %H:%M:%S)
Hostname: $(hostname)
Version: 1.1

Contents:
---------
- system/openclaw.json    : Gateway config + token
- system/.env             : Environment variables (if exists)
- agents/                 : Agent auth config
- cron/jobs.json          : Cron task definitions
- cron/jobs-state.json    : Cron state (if exists)
- workspace.tar.gz        : Full workspace
- sessions.tar.gz         : Session records (if included)

Backup command:
  ./one-click-full-restore.sh $OUTPUT_FILE

EOF

# Create final archive
FINAL_PARENT=$(dirname "$OUTPUT_FILE")
mkdir -p "$FINAL_PARENT" 2>/dev/null || true
tar -czf "$OUTPUT_FILE" -C "$TEMP_DIR" . 2>/dev/null

# Cleanup
rm -rf "$TEMP_DIR"

# Verify and report
if [ -f "$OUTPUT_FILE" ]; then
    SIZE=$(ls -lh "$OUTPUT_FILE" | awk '{print $5}')
    MD5=$(md5sum "$OUTPUT_FILE" | awk '{print $1}')
    
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}  Backup Complete!${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo -e "File: ${YELLOW}$OUTPUT_FILE${NC}"
    echo -e "Size: ${YELLOW}$SIZE${NC}"
    echo -e "MD5:  ${YELLOW}$MD5${NC}"
    echo ""
    echo -e "${CYAN}To restore after system reinstall:${NC}"
    echo "  bash ~/.openclaw/workspace/skills/clawmerge/scripts/one-click-full-restore.sh $OUTPUT_FILE"
    echo ""
    echo -e "${GREEN}Done!${NC}"
else
    echo -e "${RED}Error: Failed to create backup file!${NC}"
    exit 1
fi