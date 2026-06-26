#!/bin/bash
# check_state.sh - 检查自我状态

WORKSPACE="/home/node/.openclaw/workspace"
SELF_STATE="$WORKSPACE/SELF_STATE.md"

echo "=== 元认知状态检查 ==="
echo ""

if [ -f "$SELF_STATE" ]; then
    echo "📄 SELF_STATE.md 存在"
    echo ""
    echo "最后更新:"
    grep "最后更新" "$SELF_STATE" | head -1
    echo ""
    echo "当前模型:"
    grep "模型" "$SELF_STATE" | head -1
    echo ""
    echo "待办承诺:"
    grep -A 5 "## 待办承诺" "$SELF_STATE" | head -6
else
    echo "❌ SELF_STATE.md 不存在"
    echo "请从模板创建: cp skills/metacognition-skill/templates/SELF_STATE.md ."
fi

echo ""
echo "=== 检查完成 ==="
