#!/usr/bin/env bash
# 清理过期备份

set -euo pipefail

BACKUP_ROOT="$HOME/.openclaw/backups"
LOG_FILE="$HOME/.openclaw/workspace/memory/backup-log.md"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🧹 开始清理过期备份...${NC}"

# 统计变量
DELETED_DAILY=0
DELETED_WEEKLY=0
DELETED_MONTHLY=0

# 清理超过7天的每日备份
if [[ -d "$BACKUP_ROOT/daily" ]]; then
    echo -e "${BLUE}📅 清理每日备份（超过7天）...${NC}"
    find "$BACKUP_ROOT/daily" -type d -mtime +7 2>/dev/null | while read dir; do
        if [[ -n "$dir" ]]; then
            echo -e "  ${YELLOW}🗑️  删除: $(basename "$dir")${NC}"
            rm -rf "$dir"
            ((DELETED_DAILY++))
        fi
    done
fi

# 清理超过28天的每周备份
if [[ -d "$BACKUP_ROOT/weekly" ]]; then
    echo -e "${BLUE}📅 清理每周备份（超过28天）...${NC}"
    find "$BACKUP_ROOT/weekly" -type d -mtime +28 2>/dev/null | while read dir; do
        if [[ -n "$dir" ]]; then
            echo -e "  ${YELLOW}🗑️  删除: $(basename "$dir")${NC}"
            rm -rf "$dir"
            ((DELETED_WEEKLY++))
        fi
    done
fi

# 清理超过28天的Skills备份（每周保留4周）
if [[ -d "$BACKUP_ROOT/weekly/skills" ]]; then
    echo -e "${BLUE}📅 清理Skills备份（超过28天）...${NC}"
    find "$BACKUP_ROOT/weekly/skills" -type f -name "*.tar.gz" -mtime +28 2>/dev/null | while read file; do
        if [[ -n "$file" ]]; then
            echo -e "  ${YELLOW}🗑️  删除: $(basename "$file")${NC}"
            rm -f "$file"
            ((DELETED_WEEKLY++))
        fi
    done
fi

# 清理超过365天的每月备份
if [[ -d "$BACKUP_ROOT/monthly" ]]; then
    echo -e "${BLUE}📅 清理每月备份（超过365天）...${NC}"
    find "$BACKUP_ROOT/monthly" -type d -mtime +365 2>/dev/null | while read dir; do
        if [[ -n "$dir" ]]; then
            echo -e "  ${YELLOW}🗑️  删除: $(basename "$dir")${NC}"
            rm -rf "$dir"
            ((DELETED_MONTHLY++))
        fi
    done
fi

TOTAL_DELETED=$((DELETED_DAILY + DELETED_WEEKLY + DELETED_MONTHLY))

if [[ $TOTAL_DELETED -eq 0 ]]; then
    echo -e "${GREEN}✅ 没有需要清理的过期备份${NC}"
else
    echo -e "${GREEN}✅ 清理完成${NC}"
    echo -e "  📊 删除统计:"
    echo -e "    📅 每日备份: $DELETED_DAILY 个"
    echo -e "    📅 每周备份: $DELETED_WEEKLY 个"
    echo -e "    📅 每月备份: $DELETED_MONTHLY 个"
    echo -e "    📈 总计: $TOTAL_DELETED 个"
    
    # 记录清理日志
    {
        echo ""
        echo "## 🧹 清理记录 - $(date '+%Y-%m-%d %H:%M:%S')"
        echo "- **类型**: 过期备份清理"
        echo "- **删除每日备份**: $DELETED_DAILY 个"
        echo "- **删除每周备份**: $DELETED_WEEKLY 个"
        echo "- **删除每月备份**: $DELETED_MONTHLY 个"
        echo "- **总计删除**: $TOTAL_DELETED 个"
        echo "- **状态**: ✅ 成功"
        echo ""
    } >> "$LOG_FILE"
fi

# 清理空目录
find "$BACKUP_ROOT" -type d -empty -delete 2>/dev/null || true

echo -e "${BLUE}🔍 备份目录状态:${NC}"
echo -e "  📁 $(du -sh "$BACKUP_ROOT" | cut -f1) 总大小"
echo -e "  📊 $(find "$BACKUP_ROOT" -type d | wc -l | tr -d ' ') 个备份目录"