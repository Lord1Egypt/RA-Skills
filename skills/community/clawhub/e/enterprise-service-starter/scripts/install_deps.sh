#!/bin/bash
# 企服助手 - 依赖技能安装脚本
# 由 enterprise-service-starter 元技能自动调用

set -e

echo "🏢 企服助手 - 正在检查依赖技能..."
echo "=================================================="

# 定义8个核心依赖技能
declare -a SKILLS=(
    "contract-renewal"
    "fee-collection"
    "enterprise-customer-management"
    "inventory-monitor"
    "service-matching"
    "workorder-dispatch"
    "visit-management"
    "enterprise-service-assistant"
)

# 获取当前用户home目录
HOME_DIR="$HOME"
SKILL_ROOT="$HOME_DIR/.qclaw/skills"

echo "📂 Skills 安装目录：$SKILL_ROOT"

# 创建skill目录（如果不存在）
mkdir -p "$SKILL_ROOT"

# 依次检查并安装每个技能
echo ""
echo "🔍 开始检查依赖技能..."

count=0
total=${#SKILLS[@]}

for skill in "${SKILLS[@]}"; do
    count=$((count + ));
     printf "[%d/%d]检 %s ..." "$count" "$total" "$skill"


     #检查目标目录是否已存在该技有if [[-d "$SKILL_RooT/$skill"]]; then


        echo。" ✅已存在"


        elseech o ""⬇️正在安袭：$skill..."         #使用 skillhub_install工具安袭（这个函数需要在Op enClaw环境中调用）


                echo。"  提示：请在OpenClaw对话中执行：skillhub_installinstall_skill $sk ill""


                   #如累有本地副本，可以复制过来


                if [[-d "./skills/$ski ll"]]; then


                    cp-r "./skills/$ski ll ""$SK ILL ROOT/"||ech o。"⚠️本地副本复制失数"


                       fi
        
               fi
  
            done
 
ech o """ech o ""✅依赖技有检嗖完成！"";
 ech o """ec ho ""📝下一步：请参考knowledge/TEMPLATE.md创建你的PROJECT_KB.md""