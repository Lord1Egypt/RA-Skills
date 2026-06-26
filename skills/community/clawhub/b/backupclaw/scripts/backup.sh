#!/bin/bash

# Backup script for OpenClaw configuration
# Usage: backup.sh <backup_dir>

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
OPENCLAW_DIR="$HOME/.openclaw"
BACKUP_ROOT="$1"

# Validate backup directory
if [ -z "$BACKUP_ROOT" ]; then
    echo -e "${RED}错误: 请指定备份目录路径${NC}"
    echo "Usage: $0 <backup_dir>"
    exit 1
fi

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_ROOT"

# Get current date
CURRENT_DATE=$(date +%Y-%m-%d)
CURRENT_TIME=$(date +%H:%M:%S)
BACKUP_DIR="$BACKUP_ROOT/$CURRENT_DATE"

# Find latest backup directory
LATEST_BACKUP=$(find "$BACKUP_ROOT" -maxdepth 1 -type d -name "20[0-9][0-9]-[0-9][0-9]-[0-9][0-9]" | sort -r | head -n 1)

# Function to compare directories
compare_dirs() {
    local dir1="$1"
    local dir2="$2"

    # Use rsync to check for differences
    local changed_files=$(rsync -anci --exclude='workspace' "$dir1/" "$dir2/" 2>/dev/null || true)

    if [ -z "$changed_files" ]; then
        return 0  # No changes
    else
        return 1  # Changes detected
    fi
}

# If no previous backup, do full backup
if [ -z "$LATEST_BACKUP" ]; then
    echo -e "${YELLOW}首次备份: 将备份 ~/.openclaw/ 到 $BACKUP_DIR${NC}"
    mkdir -p "$BACKUP_DIR"

    # Copy everything except workspace
    rsync -av --exclude='workspace' --exclude='workspace/**' "$OPENCLAW_DIR/" "$BACKUP_DIR/"

    # Record in changelog
    echo "## $CURRENT_DATE $CURRENT_TIME" >> "$BACKUP_ROOT/changelog.md"
    echo "- 首次完整备份" >> "$BACKUP_ROOT/changelog.md"
    echo "" >> "$BACKUP_ROOT/changelog.md"

    echo -e "${GREEN}✓ 备份完成！${NC}"
    echo "备份位置: $BACKUP_DIR"
    exit 0
fi

# Compare with latest backup
if compare_dirs "$OPENCLAW_DIR" "$LATEST_BACKUP"; then
    echo "配置文件没有变化，不需要备份"
    exit 0
fi

# Changes detected - perform backup
echo -e "${YELLOW}检测到配置变化，创建新备份...${NC}"
mkdir -p "$BACKUP_DIR"

# Copy everything except workspace
rsync -av --exclude='workspace' --exclude='workspace/**' "$OPENCLAW_DIR/" "$BACKUP_DIR/"

# Find changed files using diff
echo "正在比较文件差异..."
changed_list=$(diff -rq --exclude='workspace' "$LATEST_BACKUP" "$OPENCLAW_DIR" 2>/dev/null || true)

# Update changelog
echo "## $CURRENT_DATE $CURRENT_TIME" >> "$BACKUP_ROOT/changelog.md"

# Parse diff output to list changed files
if [ -n "$changed_list" ]; then
    echo "$changed_list" | while read -r line; do
        if [[ $line == *" differ"* ]]; then
            # File changed
            file=$(echo "$line" | awk '{print $2}' | sed "s|$LATEST_BACKUP/||")
            echo "- $file (已修改)" >> "$BACKUP_ROOT/changelog.md"
        elif [[ $line == *"Only in"* ]]; then
            # File added or deleted
            if [[ $line == *"$LATEST_BACKUP"* ]]; then
                # File deleted from OpenClaw
                file=$(echo "$line" | awk '{print $4}' | sed "s|$LATEST_BACKUP/||")
                echo "- $file (已删除)" >> "$BACKUP_ROOT/changelog.md"
            else
                # File added to OpenClaw
                file=$(echo "$line" | awk '{print $4}' | sed "s|$OPENCLAW_DIR/||")
                echo "- $file (已添加)" >> "$BACKUP_ROOT/changelog.md"
            fi
        fi
    done
else
    echo "- 文件变化详情未知" >> "$BACKUP_ROOT/changelog.md"
fi

echo "" >> "$BACKUP_ROOT/changelog.md"

echo -e "${GREEN}✓ 备份完成！${NC}"
echo "备份位置: $BACKUP_DIR"
echo "变更日志: $BACKUP_ROOT/changelog.md"
