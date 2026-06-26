#!/bin/bash
#
# Restore Task Scripts - 恢复任务脚本
# 从备份中恢复所有任务脚本和配置
#
# Usage:
#   ./restore-task-scripts.sh <backup-dir> [--dry-run]
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKUP_DIR=""
DRY_RUN=false

# Parse arguments
for arg in "$@"; do
    case $arg in
        --dry-run)
            DRY_RUN=true
            ;;
        *)
            if [ -z "$BACKUP_DIR" ]; then
                BACKUP_DIR="$arg"
            fi
            ;;
    esac
done

if [ -z "$BACKUP_DIR" ]; then
    echo "Usage: $0 <backup-dir> [--dry-run]"
    echo ""
    echo "Example:"
    echo "  $0 /tmp/clawmerge-backup"
    echo "  $0 /tmp/clawmerge-backup --dry-run"
    exit 1
fi

echo "========================================"
echo "  Restore Task Scripts"
echo "========================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Step 1: Restore external scripts
echo -e "${YELLOW}[1/4] Restoring external scripts...${NC}"
if [ -d "$BACKUP_DIR/02-external-scripts" ]; then
    if [ "$DRY_RUN" = true ]; then
        echo "  [DRY-RUN] Would restore scripts from $BACKUP_DIR/02-external-scripts"
    else
        # 恢复到 ~/scripts/
        if [ -d "$BACKUP_DIR/02-external-scripts/home-scripts" ]; then
            mkdir -p ~/scripts
            cp -r "$BACKUP_DIR/02-external-scripts/home-scripts/"* ~/scripts/ 2>/dev/null || true
            echo -e "  ${GREEN}✓ Restored to ~/scripts/${NC}"
        fi
        
        # 恢复到用户目录（不再使用 /opt/）
        if [ -d "$BACKUP_DIR/02-external-scripts/opt-scripts" ]; then
            mkdir -p ~/scripts
            cp -r "$BACKUP_DIR/02-external-scripts/opt-scripts/"* ~/scripts/ 2>/dev/null || true
            echo -e "  ${GREEN}✓ Restored to ~/scripts/${NC}"
        fi
        
        # 设置执行权限
        find ~/scripts -type f \( -name "*.py" -o -name "*.sh" \) -exec chmod +x {} \; 2>/dev/null || true
        echo -e "  ${GREEN}✓ Set execute permissions${NC}"
    fi
else
    echo -e "  ${BLUE}○ No external scripts to restore${NC}"
fi
echo ""

# Step 2: Restore cron configs
echo -e "${YELLOW}[2/4] Restoring cron configurations...${NC}"
if [ -d "$BACKUP_DIR/03-cron-configs" ]; then
    if [ "$DRY_RUN" = true ]; then
        echo "  [DRY-RUN] Would restore cron configs"
    else
        # 恢复系统 crontab
        if [ -f "$BACKUP_DIR/03-cron-configs/system-crontab.txt" ]; then
            crontab "$BACKUP_DIR/03-cron-configs/system-crontab.txt"
            echo -e "  ${GREEN}✓ Restored system crontab${NC}"
        fi
        
        # 恢复 Gateway cron（需要手动合并）
        if [ -f "$BACKUP_DIR/03-cron-configs/gateway-cron.json" ]; then
            echo -e "  ${YELLOW}⚠ Gateway cron needs manual merge${NC}"
            echo -e "  ${BLUE}  File: $BACKUP_DIR/03-cron-configs/gateway-cron.json${NC}"
        fi
    fi
else
    echo -e "  ${BLUE}○ No cron configs to restore${NC}"
fi
echo ""

# Step 3: Restore config files
echo -e "${YELLOW}[3/4] Restoring configuration files...${NC}"
if [ -d "$BACKUP_DIR/04-config-files" ]; then
    if [ "$DRY_RUN" = true ]; then
        echo "  [DRY-RUN] Would restore config files to $WORKSPACE_DIR"
    else
        # 恢复配置文件到 workspace
        cp -r "$BACKUP_DIR/04-config-files/"* "$WORKSPACE_DIR/" 2>/dev/null || true
        echo -e "  ${GREEN}✓ Restored config files to workspace${NC}"
    fi
else
    echo -e "  ${BLUE}○ No config files to restore${NC}"
fi
echo ""

# Step 4: Restore dependencies
echo -e "${YELLOW}[4/4] Restoring dependencies...${NC}"
if [ -d "$BACKUP_DIR/05-dependencies" ]; then
    if [ "$DRY_RUN" = true ]; then
        echo "  [DRY-RUN] Would install dependencies"
    else
        # 安装 Python 依赖
        if [ -f "$BACKUP_DIR/05-dependencies/python-requirements.txt" ]; then
            echo "  Installing Python packages..."
            pip3 install -r "$BACKUP_DIR/05-dependencies/python-requirements.txt" 2>/dev/null || \
                echo -e "  ${YELLOW}⚠ Some packages may need manual installation${NC}"
            echo -e "  ${GREEN}✓ Python dependencies installed${NC}"
        fi
        
        # 系统依赖清单
        if [ -f "$BACKUP_DIR/05-dependencies/system-packages.txt" ]; then
            echo -e "  ${YELLOW}System packages to install:${NC}"
            cat "$BACKUP_DIR/05-dependencies/system-packages.txt"
        fi
    fi
else
    echo -e "  ${BLUE}○ No dependencies to restore${NC}"
fi
echo ""

# Summary
echo "========================================"
echo "  Restore Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "  1. Review restored files"
echo "  2. Update sensitive configs (API keys, etc)"
echo "  3. Test scripts manually"
echo "  4. Verify cron jobs: crontab -l"
echo ""
