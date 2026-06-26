#!/bin/bash
#
# One-Click Full Disaster Restore for OpenClaw v1.1
# 用途：重装系统后，一键恢复所有配置和数据
#
# 包含：
#   - workspace（所有文件）
#   - openclaw.json（Gateway 配置）
#   - cron/jobs.json（定时任务）
#   - agents/main/agent/（认证配置）
#   - sessions/（对话记录）
#
# 用法：
#   ./one-click-full-restore.sh <backup_file> [--dry-run] [--force] [--no-sessions] [--unsafe-overwrite]
#
set -e

OPENCLAW_DIR="$HOME/.openclaw"
WORKSPACE_DIR="$HOME/.openclaw/workspace"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
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
FORCE_MODE=false
NO_SESSIONS=false
UNSAFE_OVERWRITE=false
BACKUP_FILE=""

for arg in "$@"; do
    case $arg in
        --dry-run)
            DRY_RUN=true
            ;;
        --force)
            FORCE_MODE=true
            ;;
        --no-sessions)
            NO_SESSIONS=true
            ;;
        --unsafe-overwrite)
            UNSAFE_OVERWRITE=true
            ;;
        --help)
            echo "用法: $0 <backup_file> [options]"
            echo ""
            echo "选项:"
            echo "  --dry-run      预览模式，不实际恢复"
            echo "  --force        跳过确认提示"
            echo "  --no-sessions       不恢复 session 记录"
            echo "  --unsafe-overwrite  危险：覆盖 openclaw.json/cron/workspace/sessions（默认安全合并）"
            exit 0
            ;;
        *)
            [ -z "$BACKUP_FILE" ] && BACKUP_FILE="$arg"
            ;;
    esac
done

show_usage() {
    echo -e "${YELLOW}用法:${NC} $0 <backup文件> [选项]"
    echo ""
    echo -e "${YELLOW}选项:${NC}"
    echo "  --dry-run      预览恢复内容，不实际修改"
    echo "  --force        跳过确认提示"
    echo "  --no-sessions       不恢复 session 记录"
    echo "  --unsafe-overwrite  危险：覆盖 openclaw.json/cron/workspace/sessions（默认安全合并）"
    echo ""
    echo -e "${YELLOW}示例:${NC}"
    echo "  $0 ~/backups/openclaw-full-backup-20260502.tar.gz"
    echo "  $0 ~/backups/openclaw-full-backup-*.tar.gz --force"
}

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  OpenClaw Full Disaster Restore v1.1${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Validate arguments
if [ -z "$BACKUP_FILE" ] || [ "$BACKUP_FILE" = "--help" ]; then
    show_usage
    exit 1
fi

# Expand wildcard
if [[ "$BACKUP_FILE" == *"*"* ]]; then
    MATCHED=$(ls -t $BACKUP_FILE 2>/dev/null | head -1)
    if [ -z "$MATCHED" ]; then
        echo -e "${RED}Error: No backup files match pattern${NC}"
        exit 1
    fi
    echo -e "${YELLOW}Using most recent:${NC} $MATCHED"
    BACKUP_FILE="$MATCHED"
fi

if [ ! -f "$BACKUP_FILE" ]; then
    echo -e "${RED}Error: Backup file not found: $BACKUP_FILE${NC}"
    exit 1
fi

# Verify backup integrity
echo -e "${YELLOW}Verifying backup...${NC}"
if ! tar -tzf "$BACKUP_FILE" > /dev/null 2>&1; then
    echo -e "${RED}Error: Invalid or corrupted backup file!${NC}"
    exit 1
fi

# List contents
echo -e "${CYAN}Backup contents:${NC}"
tar -tzf "$BACKUP_FILE" | head -20
echo ""
echo -e "${GREEN}✓ Backup verified${NC}"
echo ""

# Dry run mode
if [ "$DRY_RUN" = true ]; then
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  DRY RUN - No files will be modified${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    echo -e "${YELLOW}Would restore:${NC}"
    if [ "$UNSAFE_OVERWRITE" = true ]; then
        echo "  - UNSAFE: system/openclaw.json → $OPENCLAW_DIR/openclaw.json"
        echo "  - UNSAFE: cron/jobs.json → $OPENCLAW_DIR/cron/jobs.json"
        echo "  - UNSAFE: workspace.tar.gz → $WORKSPACE_DIR/ (may overwrite)"
        echo "  - UNSAFE: sessions.tar.gz → $OPENCLAW_DIR/agents/main/sessions/"
    else
        echo "  - SAFE: system/openclaw.json → $OPENCLAW_DIR/restore-candidates/$TIMESTAMP/openclaw.json"
        echo "  - SAFE: cron/jobs.json → $OPENCLAW_DIR/restore-candidates/$TIMESTAMP/cron-jobs.json"
        echo "  - SAFE: agents/ → $OPENCLAW_DIR/restore-candidates/$TIMESTAMP/agents/"
        echo "  - SAFE: workspace.tar.gz → $WORKSPACE_DIR/ (skip existing files)"
        echo "  - SAFE: sessions.tar.gz → $OPENCLAW_DIR/agents/main/sessions-restored-$TIMESTAMP/"
    fi
    echo ""
    echo "To proceed, run without --dry-run"
    exit 0
fi

# Confirm
if [ "$FORCE_MODE" != true ]; then
    echo -e "${YELLOW}========================================${NC}"
    if [ "$UNSAFE_OVERWRITE" = true ]; then
        echo -e "${YELLOW}  ⚠ WARNING: UNSAFE mode will overwrite existing files!${NC}"
    else
        echo -e "${YELLOW}  Safe mode: configs/sessions go to restore-candidates/archive; workspace skips existing files.${NC}"
    fi
    echo -e "${YELLOW}========================================${NC}"
    echo ""
    echo "Backup: $BACKUP_FILE"
    echo ""
    read -p "Proceed with full restore? [y/N] " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Restore cancelled${NC}"
        exit 0
    fi
fi

# Extract to temp
echo -e "${YELLOW}Extracting backup...${NC}"
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

tar -xzf "$BACKUP_FILE" -C "$TEMP_DIR"
BACKUP_ROOT="$TEMP_DIR/openclaw-full-backup"

if [ ! -d "$BACKUP_ROOT" ]; then
    # Handle case where files are at root of archive
    BACKUP_ROOT="$TEMP_DIR"
fi

echo -e "${GREEN}✓ Extraction complete${NC}"
echo ""

# ============================================
# Create disaster recovery backup of current state
# ============================================
echo -e "${CYAN}[DISASTER PREVENTION] Backing up current state...${NC}"

DISASTER_DIR="$OPENCLAW_DIR/.local-backup/pre-restore-$TIMESTAMP"
mkdir -p "$DISASTER_DIR"

# Backup current critical files
[ -f "$OPENCLAW_DIR/openclaw.json" ] && cp "$OPENCLAW_DIR/openclaw.json" "$DISASTER_DIR/" && echo "  ✓ Current openclaw.json backed up"
[ -f "$OPENCLAW_DIR/cron/jobs.json" ] && cp "$OPENCLAW_DIR/cron/jobs.json" "$DISASTER_DIR/" && echo "  ✓ Current cron/jobs.json backed up"

# Backup workspace critical files
CRITICAL_FILES=("MEMORY.md" "SOUL.md" "IDENTITY.md" "USER.md" "AGENTS.md" "TOOLS.md")
for f in "${CRITICAL_FILES[@]}"; do
    [ -f "$WORKSPACE_DIR/$f" ] && cp "$WORKSPACE_DIR/$f" "$DISASTER_DIR/" && echo "  ✓ Current $f backed up"
done

echo ""
echo -e "${GREEN}✓ Current state backed up to: $DISASTER_DIR${NC}"
echo ""

# ============================================
# Restore system configs
# ============================================
echo -e "${BLUE}[1/5] Restoring system configuration...${NC}"

mkdir -p "$OPENCLAW_DIR"

RESTORE_CANDIDATE_DIR="$OPENCLAW_DIR/restore-candidates/$TIMESTAMP"
mkdir -p "$RESTORE_CANDIDATE_DIR"

# Restore or stage openclaw.json
if [ -f "$BACKUP_ROOT/system/openclaw.json" ]; then
    if [ "$UNSAFE_OVERWRITE" = true ]; then
        cp "$BACKUP_ROOT/system/openclaw.json" "$OPENCLAW_DIR/openclaw.json"
        echo -e "  ${GREEN}✓ openclaw.json restored (unsafe overwrite)${NC}"
    else
        cp "$BACKUP_ROOT/system/openclaw.json" "$RESTORE_CANDIDATE_DIR/openclaw.json"
        echo -e "  ${CYAN}○ openclaw.json staged: $RESTORE_CANDIDATE_DIR/openclaw.json${NC}"
    fi
else
    echo -e "  ${YELLOW}⚠ openclaw.json not in backup${NC}"
fi

# Restore or stage .env if exists
if [ -f "$BACKUP_ROOT/system/.env" ]; then
    if [ "$UNSAFE_OVERWRITE" = true ]; then
        cp "$BACKUP_ROOT/system/.env" "$OPENCLAW_DIR/.env"
        echo -e "  ${GREEN}✓ .env restored (unsafe overwrite)${NC}"
    else
        cp "$BACKUP_ROOT/system/.env" "$RESTORE_CANDIDATE_DIR/.env"
        echo -e "  ${CYAN}○ .env staged: $RESTORE_CANDIDATE_DIR/.env${NC}"
    fi
fi

# Restore or stage agents config
if [ -d "$BACKUP_ROOT/agents/agent" ]; then
    if [ "$UNSAFE_OVERWRITE" = true ]; then
        mkdir -p "$OPENCLAW_DIR/agents/main"
        rm -rf "$OPENCLAW_DIR/agents/main/agent"
        cp -r "$BACKUP_ROOT/agents/agent" "$OPENCLAW_DIR/agents/main/agent"
        echo -e "  ${GREEN}✓ agents/main/agent/ restored (unsafe overwrite)${NC}"
    else
        mkdir -p "$RESTORE_CANDIDATE_DIR/agents"
        cp -r "$BACKUP_ROOT/agents/agent" "$RESTORE_CANDIDATE_DIR/agents/agent"
        echo -e "  ${CYAN}○ agents staged: $RESTORE_CANDIDATE_DIR/agents/agent${NC}"
    fi
fi

echo ""

# ============================================
# Restore cron jobs
# ============================================
echo -e "${BLUE}[2/5] Restoring cron tasks...${NC}"

mkdir -p "$OPENCLAW_DIR/cron"

if [ -f "$BACKUP_ROOT/cron/jobs.json" ]; then
    if [ "$UNSAFE_OVERWRITE" = true ]; then
        cp "$BACKUP_ROOT/cron/jobs.json" "$OPENCLAW_DIR/cron/jobs.json"
        CRON_SIZE=$(wc -c < "$OPENCLAW_DIR/cron/jobs.json")
        echo -e "  ${GREEN}✓ cron/jobs.json restored ($CRON_SIZE bytes, unsafe overwrite)${NC}"
    else
        cp "$BACKUP_ROOT/cron/jobs.json" "$RESTORE_CANDIDATE_DIR/cron-jobs.json"
        CRON_SIZE=$(wc -c < "$RESTORE_CANDIDATE_DIR/cron-jobs.json")
        echo -e "  ${CYAN}○ cron/jobs.json staged ($CRON_SIZE bytes): $RESTORE_CANDIDATE_DIR/cron-jobs.json${NC}"
    fi
else
    echo -e "  ${YELLOW}⚠ cron/jobs.json not in backup${NC}"
fi

if [ -f "$BACKUP_ROOT/cron/jobs-state.json" ]; then
    if [ "$UNSAFE_OVERWRITE" = true ]; then
        cp "$BACKUP_ROOT/cron/jobs-state.json" "$OPENCLAW_DIR/cron/jobs-state.json"
        echo -e "  ${GREEN}✓ cron/jobs-state.json restored (unsafe overwrite)${NC}"
    else
        cp "$BACKUP_ROOT/cron/jobs-state.json" "$RESTORE_CANDIDATE_DIR/cron-jobs-state.json"
        echo -e "  ${CYAN}○ cron/jobs-state.json staged: $RESTORE_CANDIDATE_DIR/cron-jobs-state.json${NC}"
    fi
fi

echo ""

# ============================================
# Restore workspace
# ============================================
echo -e "${BLUE}[3/5] Restoring workspace...${NC}"

mkdir -p "$WORKSPACE_DIR"

if [ -f "$BACKUP_ROOT/workspace.tar.gz" ]; then
    WS_SIZE=$(ls -lh "$BACKUP_ROOT/workspace.tar.gz" | awk '{print $5}')
    if [ "$UNSAFE_OVERWRITE" = true ]; then
        tar -xzf "$BACKUP_ROOT/workspace.tar.gz" -C "$WORKSPACE_DIR"
        echo -e "  ${GREEN}✓ workspace.tar.gz extracted ($WS_SIZE, unsafe overwrite)${NC}"
    else
        tar --skip-old-files -xzf "$BACKUP_ROOT/workspace.tar.gz" -C "$WORKSPACE_DIR" 2>/tmp/clawmerge-workspace-skip-$TIMESTAMP.log || true
        echo -e "  ${GREEN}✓ workspace.tar.gz extracted in safe mode ($WS_SIZE; existing files skipped)${NC}"
        echo -e "  ${CYAN}○ skipped-file log: /tmp/clawmerge-workspace-skip-$TIMESTAMP.log${NC}"
    fi
else
    echo -e "  ${YELLOW}⚠ workspace.tar.gz not in backup${NC}"
fi

echo ""

# ============================================
# Restore sessions
# ============================================
echo -e "${BLUE}[4/5] Restoring session records...${NC}"

if [ "$NO_SESSIONS" = true ]; then
    echo -e "  ${CYAN}○ Skipped (--no-sessions specified)${NC}"
elif [ -f "$BACKUP_ROOT/sessions.tar.gz" ]; then
    if [ "$UNSAFE_OVERWRITE" = true ]; then
        SESSIONS_DIR="$OPENCLAW_DIR/agents/main/sessions"
        # Backup current sessions first
        if [ -d "$SESSIONS_DIR" ] && [ "$(ls -A "$SESSIONS_DIR" 2>/dev/null)" ]; then
            BACKUP_SESSIONS="$OPENCLAW_DIR/.local-backup/sessions-pre-restore-$TIMESTAMP"
            mkdir -p "$BACKUP_SESSIONS"
            cp -r "$SESSIONS_DIR"/* "$BACKUP_SESSIONS/" 2>/dev/null || true
            echo -e "  ${YELLOW}✓ Current sessions backed up to: $BACKUP_SESSIONS${NC}"
        fi
        mkdir -p "$SESSIONS_DIR"
        tar -xzf "$BACKUP_ROOT/sessions.tar.gz" -C "$SESSIONS_DIR"
        SESSION_COUNT=$(ls -1 "$SESSIONS_DIR"/*.jsonl 2>/dev/null | wc -l || echo 0)
        echo -e "  ${GREEN}✓ sessions.tar.gz restored live ($SESSION_COUNT files, unsafe overwrite)${NC}"
    else
        SESSIONS_DIR="$OPENCLAW_DIR/agents/main/sessions-restored-$TIMESTAMP"
        mkdir -p "$SESSIONS_DIR"
        tar -xzf "$BACKUP_ROOT/sessions.tar.gz" -C "$SESSIONS_DIR"
        SESSION_COUNT=$(find "$SESSIONS_DIR" -type f -name '*.jsonl*' | wc -l || echo 0)
        echo -e "  ${CYAN}○ sessions archived, not merged live: $SESSIONS_DIR ($SESSION_COUNT files)${NC}"
    fi
else
    echo -e "  ${CYAN}○ No sessions.tar.gz in backup${NC}"
fi

echo ""

# ============================================
# Final verification and summary
# ============================================
echo -e "${BLUE}[5/5] Verifying restore...${NC}"

echo -e "${CYAN}Checking critical files:${NC}"
[ -f "$OPENCLAW_DIR/openclaw.json" ] && echo "  ✓ openclaw.json" || echo "  ✗ openclaw.json MISSING"
[ -f "$OPENCLAW_DIR/cron/jobs.json" ] && echo "  ✓ cron/jobs.json" || echo "  ✗ cron/jobs.json MISSING"
[ -f "$WORKSPACE_DIR/MEMORY.md" ] && echo "  ✓ workspace/MEMORY.md" || echo "  ✗ workspace/MEMORY.md MISSING"

echo ""

# ============================================
# Summary
# ============================================
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Full Restore Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "Restored to:"
echo "  - System config: $OPENCLAW_DIR/"
echo "  - Workspace:     $WORKSPACE_DIR/"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "  1. Review any warnings above"
if [ "$UNSAFE_OVERWRITE" != true ]; then
    echo "  Safe mode staged configs/sessions instead of overwriting live runtime."
    echo "  Review candidates under: $RESTORE_CANDIDATE_DIR"
    echo ""
fi

echo "  2. Restart OpenClaw gateway if you intentionally applied live config changes:"
echo ""
echo -e "     ${CYAN}openclaw gateway restart${NC}"
echo ""
if [ -d "$DISASTER_DIR" ]; then
    echo -e "${CYAN}Pre-restore backup:${NC}"
    echo "  (in case you need to rollback)"
    echo "  $DISASTER_DIR"
    echo ""
fi
echo -e "${GREEN}Done!${NC}"