#!/bin/bash
###############################################################################
# 工具脚本: 清理旧数据
# 用法: ./cleanup.sh [保留天数，默认30天]
###############################################################################

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PIPELINE_DIR="$(dirname "$SCRIPT_DIR")"
KEEP_DAYS="${1:-30}"

echo ""
echo "🧹 清理AI内容流水线旧数据"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "保留最近 $KEEP_DAYS 天的数据"
echo ""

# 计算删除阈值日期
CUTOFF_DATE=$(date -v-${KEEP_DAYS}d +%Y-%m-%d 2>/dev/null || date -d "$KEEP_DAYS days ago" +%Y-%m-%d)
echo "删除 $CUTOFF_DATE 之前的数据"
echo ""

# 清理 collected 目录
if [[ -d "$PIPELINE_DIR/collected" ]]; then
    echo "📁 清理 collected 目录..."
    
    for dir in "$PIPELINE_DIR/collected"/[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]; do
        if [[ -d "$dir" ]]; then
            DIR_NAME=$(basename "$dir")
            if [[ "$DIR_NAME" < "$CUTOFF_DATE" ]]; then
                echo "  删除: $DIR_NAME"
                rm -rf "$dir"
            fi
        fi
    done
fi

# 清理 filtered 目录
if [[ -d "$PIPELINE_DIR/filtered" ]]; then
    echo "📁 清理 filtered 目录..."
    
    for dir in "$PIPELINE_DIR/filtered"/[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]; do
        if [[ -d "$dir" ]]; then
            DIR_NAME=$(basename "$dir")
            if [[ "$DIR_NAME" < "$CUTOFF_DATE" ]]; then
                echo "  删除: $DIR_NAME"
                rm -rf "$dir"
            fi
        fi
    done
fi

echo ""
echo "✅ 清理完成"
echo ""
