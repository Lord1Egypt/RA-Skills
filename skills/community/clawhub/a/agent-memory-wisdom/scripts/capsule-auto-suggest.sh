#!/bin/bash
# capsule-auto-suggest.sh
# 任务完成后自动检查是否值得创建胶囊
# 用法: bash capsule-auto-suggest.sh "<任务结果>" "<原始任务描述>"

RESULT="${1:-}"
TASK="${2:-}"

if [ -z "$TASK" ]; then
  echo "用法: bash capsule-auto-suggest.sh \"<任务结果>\" \"<原始任务描述>\""
  exit 1
fi

echo "🔮 检查是否值得创建胶囊..."
echo ""

SHOULD_CREATE="false"
REASON=""

SUBAGENT_COUNT=$(echo "$TASK" | grep -o "subagent\|并行\|多个\|多平台" | wc -l | tr -d ' ')

COMPLEX_KEYWORDS="重构|调研|系统|架构|多步骤|跨平台|自动化"
if echo "$TASK" | grep -qE "$COMPLEX_KEYWORDS"; then
  COMPLEX="true"
else
  COMPLEX="false"
fi

TIME_KEYWORDS="30分钟|20分钟|1小时|长时间|复杂"
if echo "$TASK" | grep -qE "$TIME_KEYWORDS"; then
  TIME_CONSUME="true"
else
  TIME_CONSUME="false"
fi

if [ "$SUBAGENT_COUNT" -gt 1 ]; then
  SHOULD_CREATE="true"
  REASON="涉及多个并行子任务"
elif [ "$COMPLEX" = "true" ]; then
  SHOULD_CREATE="true"
  REASON="任务复杂，涉及多步骤"
elif [ "$TIME_CONSUME" = "true" ]; then
  SHOULD_CREATE="true"
  REASON="耗时较长，模式值得复用"
fi

if [ "$SHOULD_CREATE" = "true" ]; then
  echo "✅ 建议创建胶囊"
  echo ""
  echo "原因：$REASON"
  echo ""
  echo "创建命令："
  echo "  bash ~/.openclaw/workspace/scripts/create-capsule.sh \"<胶囊名称>\" \"<任务类型>\" \"<成功模式描述>\""
  echo ""
  echo "任务类型选项："
  echo "  research | write | refactor | automation | browser | feishu | fetch | subagent | other"
  echo ""
  echo "⚠️ 创建后记得更新 capsules.md 的成熟度列！"
else
  echo "ℹ️ 当前任务模式较简单，暂不需要创建胶囊"
  echo ""
  echo "建议创建胶囊的场景："
  echo "  - 涉及多个并行子任务"
  echo "  - 任务耗时超过30分钟"
  echo "  - 涉及多步骤/跨平台"
  echo "  - 成功完成且希望下次复用"
fi
