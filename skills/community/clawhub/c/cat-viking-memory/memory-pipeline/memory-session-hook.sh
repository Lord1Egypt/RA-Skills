#!/bin/bash
#
# 会话钩子：会话结束时自动保存
# 需要在 OpenClaw 配置中调用
#

AGENT_NAME="${AGENT_NAME:-maojingli}"

# 获取当前会话文件路径
SESSION_ID="${SESSION_ID:-$(date +%s)}"
SESSION_FILE="$HOME/.openclaw/agents/$AGENT_NAME/sessions/${SESSION_ID}.jsonl"

# 1. 先执行提及检测 - 更新历史记忆的 access_count
echo "🔍 检测提及..."
if [ -f "$SESSION_FILE" ]; then
    # 提取会话内容
    SESSION_CONTENT=$(cat "$SESSION_FILE" | jq -r '.message.content[].text' 2>/dev/null | head -c 5000)
    # 调用提及检测
    ~/.openclaw/skills/memory-pipeline/scripts/mp_mention_detect.sh detect "$SESSION_CONTENT" "$AGENT_NAME" 2>/dev/null || true
fi

# 获取最近的消息作为摘要
SESSION_SUMMARY="${1:-会话摘要}"

# 2. 调用自动保存
~/.openclaw/skills/memory-pipeline/scripts/memory-auto-save.sh save \
    "$SESSION_SUMMARY" \
    "会话结束-$(date +%Y-%m-%d-%H:%M)"

echo "✅ 会话已保存"
