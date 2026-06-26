#!/bin/bash
# neuro-check.sh - 神经决策路由
# 判断任务类型，选择最佳处理路径

STATE_FILE="/root/.openclaw/workspace/.neuro/route-state.json"
mkdir -p "$(dirname "$STATE_FILE")"

# 任务类型判断
# 高效期路径：深度分析、多步骤、新领域
# 低效期路径：快速执行、简单任务

# 路由决策
# 输入: 任务描述
# 输出: 路径建议

# 高效期特征词
HIGH_EFFORT_KEYWORDS="分析|研究|设计|架构|复杂|深度|评估|比较|推理|规划"

# 紧急特征词
URGENT_KEYWORDS="紧急|马上|立刻|尽快|deadline|着急|重要|必须"

# 简单任务特征词
SIMPLE_KEYWORDS="简单|容易|快速|查一下|告诉|回答|整理|归档"

# 判断任务类型
classify_task() {
    local task=$1
    local is_urgent=0
    local is_high_effort=0
    local is_simple=0
    
    # 检查紧急
    echo "$task" | grep -qE "$URGENT_KEYWORDS" && is_urgent=1
    
    # 检查高难度
    echo "$task" | grep -qE "$HIGH_EFFORT_KEYWORDS" && is_high_effort=1
    
    # 检查简单
    echo "$task" | grep -qE "$SIMPLE_KEYWORDS" && is_simple=1
    
    # 组合判断
    if [ $is_urgent -eq 1 ]; then
        echo "urgent"
    elif [ $is_simple -eq 1 ] && [ $is_high_effort -eq 0 ]; then
        echo "simple"
    elif [ $is_high_effort -eq 1 ]; then
        echo "high_effort"
    else
        echo "standard"
    fi
}

# 获取路由建议
get_route_suggestion() {
    local task_type=$1
    
    case $task_type in
        "urgent") echo "🔴 直接执行|不走快速路径|紧急任务优先处理" ;;
        "simple") echo "🟢 快速路径|简单任务直接处理|跳过深度分析" ;;
        "high_effort") echo "🟡 深度路径|建议高效期处理|必要时拆解任务" ;;
        "standard") echo "🟡 标准路径|正常流程处理" ;;
    esac
}

# 获取路径emoji
get_path_emoji() {
    local task_type=$1
    case $task_type in
        "urgent") echo "🔴" ;;
        "simple") echo "🟢" ;;
        "high_effort") echo "🟡" ;;
        "standard") echo "🟡" ;;
    esac
}

# 获取Circadian相位（如果可用）
get_circadian() {
    local phase_file="/root/.openclaw/workspace/.circadian/phase-state.json"
    if [ -f "$phase_file" ]; then
        python3 -c "
import json
try:
    with open('$phase_file') as f:
        data = json.load(f)
        print(data.get('name', '未知'))
except:
    print('未知')
" 2>/dev/null || echo "未知"
    else
        echo "未知"
    fi
}

# 检查当前是否高效期
is_high_efficiency_time() {
    local circadian=$(get_circadian)
    case $circadian in
        "第一高效期"|"第二高效期") return 0 ;;
        *) return 1 ;;
    esac
}

# 综合路由决策
get_final_route() {
    local task_type=$1
    local is_efficient=$2
    
    # 紧急任务直接执行
    if [ "$task_type" = "urgent" ]; then
        echo "直接执行"
        return
    fi
    
    # 高效期+高难度 = 深度路径
    if [ "$task_type" = "high_effort" ] && [ $is_efficient -eq 0 ]; then
        echo "深度路径（当前高效期）"
        return
    fi
    
    # 高效期+高难度 = 建议等待
    if [ "$task_type" = "high_effort" ] && [ $is_efficient -eq 1 ]; then
        echo "建议等待（当前低效期）"
        return
    fi
    
    # 简单任务快速处理
    if [ "$task_type" = "simple" ]; then
        echo "快速路径"
        return
    fi
    
    # 标准任务标准流程
    echo "标准路径"
}

# 主函数
main() {
    local task="${1:-}"
    local circadian=$(get_circadian)
    local is_efficient=1
    if is_high_efficiency_time; then
        is_efficient=0
    fi
    
    echo "🧠 [apollo-neuro] 神经路由报告"
    echo ""
    echo "当前状态："
    echo "  - 当前相位：$circadian"
    echo "  - 高效期：$( [ $is_efficient -eq 0 ] && echo '是' || echo '否')"
    echo ""
    
    if [ -z "$task" ]; then
        echo "用法: neuro-check.sh <任务描述>"
        echo ""
        echo "🧠 路由状态：待机"
        echo "推荐：等待任务输入"
    else
        local task_type=$(classify_task "$task")
        local suggestion=$(get_route_suggestion "$task_type")
        local final_route=$(get_final_route "$task_type" $is_efficient)
        local emoji=$(get_path_emoji "$task_type")
        
        echo "任务分析："
        echo "  - 任务类型：$emoji $task_type"
        echo "  - 基础建议：$suggestion"
        echo ""
        echo "🧠 路由决策：$final_route"
        
        # 保存状态
        cat > "$STATE_FILE" << EOF
{
    "task": "$task",
    "task_type": "$task_type",
    "route": "$final_route",
    "circadian": "$circadian",
    "is_efficient": $is_efficient,
    "decided_at": "$(date -Iseconds)"
}
EOF
    fi
}

main "$@"
