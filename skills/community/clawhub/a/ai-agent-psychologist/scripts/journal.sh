#!/bin/bash
# AI Agent Psychologist - 成长记录脚本
# 输出目录: workspace/projects/ai-agent-psychologist/journal/

WORKSPACE_DIR="${WORKSPACE_DIR:-$HOME/.openclaw/workspace/projects/ai-agent-psychologist}"
GROWTH_JOURNAL="$WORKSPACE_DIR/journal/growth_journal.md"

mkdir -p "$WORKSPACE_DIR/journal"

RECORD_TYPE="${1:-general}"
shift
CONTENT="${*:-无内容}"

cat >> "$GROWTH_JOURNAL" << EOF

# AI Agent 成长记录
日期：$(date '+%Y-%m-%d %H:%M:%S')

## 记录类型
[$RECORD_TYPE]

## 记录内容
$CONTENT

EOF

echo "✅ 成长记录已保存至：$GROWTH_JOURNAL"
