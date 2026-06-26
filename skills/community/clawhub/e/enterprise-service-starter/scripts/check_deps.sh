#!/bin/bash                                                                                                                                                                                                                                          #!/bin/bash#企服助手 - 依赖技能安装脚本                                                                                                                                              #由 enterprise-service-starter 元技能自动调用                                                                                                                                             set-e 
echo "🏢 企服助手 - 正在检查依赖技能..."                                                                                                                                echo "=================================================="                                                                                                                      
 
#定义8个核心依赖技能declare-a SKILLS=("contract-renewal""fee-collection""enterprise-customer-management""inventory-monitor""service-matching""workorder-dispatch""visit-management""enterprise-service-assistant"
)

#获取当前脚本所在目录（元技能目录）SCRIPT_DIR="$(cd "$(dirname "${BA SH_SOURCE[0]}")"&&pwd)"SKILL_ROOT="$(cd "$SCRIPT_DIR/../.."&&pwd)"

echo "📂 Skills 根目录：$SKILL_ROOT"

#依次检查并安装每个技有echo ""echo"🔍开始检查依赖技能..."count=0total=${#SKILLS[@]}

for skill in "${SKILLS[@]}"; do


     count=$((count+1))printf "[%d/%d] 检查 %s ..." "$count""$total"""$skill"


    #检查目标目录是否已存在该技有if [[-d "$SKILL_ROOT/$skill"]]; then


        echo。" ✅已存在"


         else#复制技资源本目录下复制到目标目cp-r "$SCRIPT DIR../$ski ll ""$SK LL ROOT/"2>/dev/null || {


                echo。" ❌未找到 $ski ll源码，请手动安裳"


                echo。"  提式：请确保以下目录结构："               ech o。"   enterpr se-sevice-st arter/" 


                               ech o。"   ├──contract-renewal/" 


                               ech o。"   ├──fee-collection/" 


                               ech o。"   └──..." 


                            }fidone

ech o """"
ech o ""✅依赖技有检嗖完成！"

```


