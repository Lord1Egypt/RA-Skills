#!/bin/bash

# Restore script for OpenClaw configuration
# Usage: restore.sh <backup_dir> <date>

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
OPENCLAW_DIR="$HOME/.openclaw"
BACKUP_ROOT="$1"
RESTORE_DATE="$2"

# Validate backup directory
if [ -z "$BACKUP_ROOT" ]; then
    echo -e "${RED}错误: 请指定备份目录路径${NC}"
    echo "Usage: $0 <backup_dir> <date>"
    exit 1
fi

# Validate date format
if [ -z "$RESTORE_DATE" ]; then
    echo -e "${RED}错误: 请指定恢复日期 (YYYY-MM-DD)${NC}"
    echo "Usage: $0 <backup_dir> <date>"
    echo ""
    echo -e "${BLUE}可用的备份日期:${NC}"
    find "$BACKUP_ROOT" -maxdepth 1 -type d -name "20[0-9][0-9]-[0-9][0-9]-[0-9][0-9]" | sort -r | xargs -I {} basename "{}"
    exit 1
fi

# Check if backup directory exists
RESTORE_DIR="$BACKUP_ROOT/$RESTORE_DATE"
if [ ! -d "$RESTORE_DIR" ]; then
    echo -e "${RED}错误: 找不到日期为 $RESTORE_DATE 的备份${NC}"
    echo ""
    echo -e "${BLUE}可用的备份日期:${NC}"
    find "$BACKUP_ROOT" -maxdepth 1 -type d -name "20[0-9][0-9]-[0-9][0-9]-[0-9][0-9]" | sort -r | xargs -I {} basename "{}"
    exit 1
fi

# Show what will be restored
echo -e "${BLUE}准备从 $RESTORE_DATE 恢复备份...${NC}"
echo ""
echo "备份内容:"
rsync -av --dry-run --exclude='workspace' --exclude='workspace/**' "$RESTORE_DIR/" "$OPENCLAW_DIR/" | grep -E '^sent|^total|^receiving|^skipping|^creating|^$' || true
echo ""

# Warning and confirmation
echo -e "${YELLOW}⚠️  警告: 此操作将覆盖当前 ~/.openclaw/ 配置文件！${NC}"
echo -e "${YELLOW}Workspace 目录不会被覆盖。${NC}"
echo ""
read -p "确认恢复？(yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo -e "${YELLOW}操作已取消${NC}"
    exit 0
fi

# Perform restore
echo -e "${BLUE}正在恢复备份...${NC}"
rsync -av --exclude='workspace' --exclude='workspace/**' "$RESTORE_DIR/" "$OPENCLAW_DIR/"

# Restart OpenClaw gateway if needed
if pgrep -f "openclaw gateway" > /dev/null; then
    echo ""
    echo -e "${YELLOW}检测到 OpenClaw Gateway 正在运行，建议重启以使配置生效${NC}"
    echo "运行: openclaw gateway restart"
fi

echo ""
echo -e "${GREEN}✓ 恢复完成！${NC}"
echo "已从 $RESTORE_DATE 恢复到 $OPENCLAW_DIR"
