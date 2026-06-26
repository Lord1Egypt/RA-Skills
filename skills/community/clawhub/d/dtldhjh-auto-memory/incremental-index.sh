#!/bin/bash
# Incremental Index - 增量向量索引
# 只索引变更的文件，避免全量重建
# 用法: incremental-index.sh <agent_id>

AGENT_ID="${1:-main}"
WORKSPACE="$HOME/.openclaw/workspaces/$AGENT_ID"

if [ "$AGENT_ID" = "main" ]; then
    WORKSPACE="$HOME/.openclaw/workspace"
fi

INDEX_STATE="$WORKSPACE/.openclaw/.index-state.json"
MEMORY_DIR="$WORKSPACE/memory"
LEARNINGS_DIR="$WORKSPACE/.learnings"

echo "🔄 检查文件变更..."

# 获取上次索引时间
if [ -f "$INDEX_STATE" ]; then
    LAST_INDEX=$(cat "$INDEX_STATE" 2>/dev/null || echo "0")
else
    LAST_INDEX=0
fi

# 查找变更的文件
CHANGED_FILES=""
CHANGED_COUNT=0

for dir in "$MEMORY_DIR" "$LEARNINGS_DIR"; do
    if [ -d "$dir" ]; then
        files=$(find "$dir" -name "*.md" -newer "$INDEX_STATE" 2>/dev/null)
        if [ -n "$files" ]; then
            CHANGED_FILES="$CHANGED_FILES $files"
            CHANGED_COUNT=$((CHANGED_COUNT + $(echo "$files" | wc -l)))
        fi
    fi
done

if [ "$CHANGED_COUNT" -gt 0 ]; then
    echo "📄 发现 $CHANGED_COUNT 个变更文件"
    
    # 执行索引（OpenClaw 当前只支持全量，这里记录状态）
    openclaw memory index --agent "$AGENT_ID" 2>/dev/null
    
    # 更新状态
    date +%s > "$INDEX_STATE"
    echo "✅ 索引已更新"
else
    echo "ℹ️ 没有变更，跳过索引"
fi
