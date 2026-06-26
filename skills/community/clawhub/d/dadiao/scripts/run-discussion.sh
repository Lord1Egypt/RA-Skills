#!/bin/bash
# 德胧思想领袖论坛 - 讨论脚本模板
# 用法: bash run-discussion.sh [讨论类型] [参与者列表]
# 示例: bash run-discussion.sh tech "musk,huang,sam,yqo,zheng"
# 示例: bash run-discussion.sh industry "liangjz,wanhao,jinjiang,xiehui"
# 示例: bash run-discussion.sh investment "oul,sequoia,carlyle,blackstone,bridgewater"

set -e

DISCUSSION_TYPE="${1:-tech}"
PARTICIPANTS="${2:-musk,huang,zhengnanyan}"

echo "=== 德胧思想领袖论坛 ==="
echo "讨论类型: $DISCUSSION_TYPE"
echo "参与者: $PARTICIPANTS"
echo ""

# 角色池映射
declare -A ROLE_FILES
ROLE_FILES=(
  ["musk]="personas/musk.md"
  ["huang"]="personas/huang-renxun.md"
  ["sam"]="personas/sam-altman.md"
  ["zhengnanyan"]="personas/zheng-nanyan.md"
  ["liangjz"]="personas/liang-jianzhang.md"
  ["wanhao"]="personas/wanhao-cto.md"
  ["jinjiang"]="personas/jinjiang-gaoguan.md"
  ["xiehui"]="personas/xiehui-secreatry.md"
)

# 加载角色
echo ">>> 加载参与者角色..."
for role in $(echo "$PARTICIPANTS" | tr ',' ' '); do
  if [[ -f "personas/${ROLE_FILES[$role]}" ]]; then
    echo "  - 已加载: $role"
  else
    echo "  - 警告: $role 无预蒸馏文件"
  fi
done

echo ""
echo ">>> 请在AI助手输入中引用以下开场背景..."
echo ""
echo "【讨论类型】: $DISCUSSION_TYPE"
echo "【参与者】: $PARTICIPANTS"
echo ""
echo "请告知AI助手："
echo "\"用德胧思想领袖论坛skill，以【$DISCUSSION_TYPE】类型，"
echo "围绕德胧AI Native战略进行讨论，参与者包括【$PARTICIPANTS】\""
