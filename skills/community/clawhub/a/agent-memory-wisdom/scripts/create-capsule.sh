#!/bin/bash
# create-capsule.sh
# 创建经验胶囊
# 用法: bash create-capsule.sh "<胶囊名称>" "<任务类型>" "<成功模式描述>"
# 任务类型: research | write | refactor | automation | browser | feishu | fetch | subagent | other

set -e

CAPSULES_DIR="$HOME/.openclaw/workspace/skills/私人胶囊"
CAPSULES_INDEX="$HOME/.openclaw/workspace/skills/brain-power-up/capsules/capsules.md"

NAME="${1:-}"
TYPE="${2:-}"
PATTERN="${3:-}"

if [ -z "$NAME" ] || [ -z "$TYPE" ] || [ -z "$PATTERN" ]; then
  echo "用法: bash create-capsule.sh \"<胶囊名称>\" \"<任务类型>\" \"<成功模式描述>\""
  echo "任务类型: research | write | refactor | automation | browser | feishu | fetch | subagent | other"
  exit 1
fi

DATE=$(date +%Y-%m-%d)
TIMESTAMP=$(date +%H%M%S)
CAP_ID="CAP-$(date +%m%d)-${TIMESTAMP}"

mkdir -p "$CAPSULES_DIR"

CAPSULE_FILE="$CAPSULES_DIR/${CAP_ID}.md"

cat > "$CAPSULE_FILE" << EOF
---
id: $CAP_ID
name: $NAME
type: $TYPE
created: $DATE
maturity: raw
success_count: 1
trigger_keywords: []
pattern:
  - $PATTERN
result_summary: 首次创建
notes: ""
---

# $NAME

**ID:** $CAP_ID
**类型:** $TYPE
**创建时间:** $DATE
**成熟度:** raw（原始）

## 成功模式
$PATTERN

## 使用记录
| 时间 | 任务 | 结果 |
|:---|:---|:---|
| $DATE | 首次创建 | ✅ 成功 |

## 下次改进
（暂无）
EOF

echo "✅ 胶囊创建成功！"
echo "文件: $CAPSULE_FILE"
echo ""
echo "⚠️ 请手动更新 capsules.md 成熟度索引表："
echo "   $CAPSULES_INDEX"
echo ""
echo "成熟度说明："
echo "  raw（原始）    — 首次成功，手动确认后才用"
echo "  tested（已验证）— 连续成功2次后升级"
echo "  stable（稳定） — 连续成功5次后升级"
