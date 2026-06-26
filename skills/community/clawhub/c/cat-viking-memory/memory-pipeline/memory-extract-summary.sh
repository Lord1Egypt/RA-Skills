#!/bin/bash
#
# memory-extract-summary.sh
# 使用 LLM 智能提取会话摘要、任务和待办
#

AGENT_NAME="${1:-maojingli}"
SESSION_FILE="$2"
YESTERDAY="${3:-$(date -d yesterday +%Y-%m-%d 2>/dev/null || date -v-1d +%Y-%m-%d 2>/dev/null)}"

if [ -z "$SESSION_FILE" ] || [ ! -f "$SESSION_FILE" ]; then
    echo "用法: $0 <agent_name> <session_file> [yesterday_date]"
    exit 1
fi

# 提取会话内容（限制长度）
SESSION_CONTENT=$(cat "$SESSION_FILE" | head -c 15000)

# 构建提示词
PROMPT="请分析以下会话记录，提取关键信息并以结构化格式输出：

$SESSION_CONTENT

请提取以下内容，输出格式如下：

主题: <一句话主题>

决策:
- <决策1>

待办:
- [ ] <任务1>

重要性: <high/medium/low>"

# 调用 OpenClaw Agent 使用 JSON 模式获取输出
OPENCLAW_BIN="${OPENCLAW_BIN:-/home/xlous/.npm-global/bin/openclaw}"

RESULT=$("$OPENCLAW_BIN" agent --local --agent maoxiami --message "$PROMPT" --json 2>/dev/null)

# 解析 JSON 输出获取文本内容
LLM_OUTPUT=$(echo "$RESULT" | grep '"text"' | sed 's/.*"text": *"\(.*\)".*/\1/' | head -1)

# 如果 JSON 解析失败，回退到原始输出
if [ -z "$LLM_OUTPUT" ]; then
    LLM_OUTPUT="$RESULT"
fi

# 解析结果 - 使用 LLM_OUTPUT
SUMMARY=$(echo "$LLM_OUTPUT" | grep -A 100 "主题:" | head -50)
IMPORTANCE=$(echo "$SUMMARY" | grep "重要性:" | sed 's/.*重要性: *//' | tr -d ' ')
TODO_LIST=$(echo "$SUMMARY" | grep "^- \[ \]" | head -10)

# 输出结构化结果
echo "=== 智能会话摘要 ==="
echo "Agent: $AGENT_NAME"
echo "日期: $YESTERDAY"
echo "重要性: ${IMPORTANCE:-medium}"
echo ""
echo "--- 摘要 ---"
echo "$SUMMARY"
echo ""
echo "--- 待办任务 ---"
if [ -n "$TODO_LIST" ]; then
    echo "$TODO_LIST"
else
    echo "- [ ] 检查昨日任务完成情况"
    echo "- [ ] 继续推进进行中的项目"
fi
