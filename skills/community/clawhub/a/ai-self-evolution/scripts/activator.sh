#!/bin/bash
# ai-self-evolution Activator Hook
# Triggers on UserPromptSubmit to remind Claude about learning capture
# Keep output minimal (~80-120 tokens) to minimize overhead

set -e

# Check for pending items count (if .learnings/ exists)
PENDING_COUNT=0
HIGH_COUNT=0
LEARNINGS_DIR=".learnings"

if [ -d "$LEARNINGS_DIR" ]; then
    PENDING_COUNT=$(grep -rch "Status\*\*: pending" "$LEARNINGS_DIR"/*.md 2>/dev/null | awk '{s+=$1} END {print s+0}')
    HIGH_COUNT=$(grep -rch "Priority\*\*: high\|Priority\*\*: critical" "$LEARNINGS_DIR"/*.md 2>/dev/null | awk '{s+=$1} END {print s+0}')
fi

# Output reminder as system context
cat << EOF
<ai-self-evolution-reminder>
任务完成后，评估是否出现可沉淀的经验：
- 非显而易见的解法？排查后的绕过方案？
- 项目特有的可复用模式？需要调试的错误？
- 用户纠正了你？发现了知识缺口？

若是：按 ai-self-evolution 技能格式记录到 .learnings/。
若价值高（重复出现、可广泛复用）：考虑提升到项目记忆或抽取为 skill。
待处理: ${PENDING_COUNT} 条 | 高优: ${HIGH_COUNT} 条
</ai-self-evolution-reminder>
EOF
