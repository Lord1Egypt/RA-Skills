#!/bin/bash
# circadian-check.sh - 昼夜节律检测
# 读取真实时钟，判断相位，输出节律报告

REALTIME_FILE="/tmp/heartbeat-realtime.json"
PHASE_STATE_FILE="/root/.openclaw/workspace/.circadian/phase-state.json"
mkdir -p "$(dirname "$PHASE_STATE_FILE")"

# 读取真实时钟
get_time() {
    if [ -f "$REALTIME_FILE" ]; then
        local time_str=$(cat "$REALTIME_FILE" 2>/dev/null | grep -o '"time":"[^"]*"' | head -1 | cut -d'"' -f4)
        if [ -n "$time_str" ]; then
            echo "$time_str"
            return
        fi
    fi
    date '+%Y-%m-%d %H:%M:%S'
}

# 判断相位（基于袁文同确认的私人节律）
# 格式：emoji|name|time_range|category
get_phase() {
    local hour=$1
    
    if [ $hour -ge 6 ] && [ $hour -lt 8 ]; then
        echo "🌅|起床清醒|06-08|起床"
    elif [ $hour -ge 8 ] && [ $hour -lt 11 ]; then
        echo "☀️|第一高效期|08-11|高效"
    elif [ $hour -ge 11 ] && [ $hour -lt 13 ]; then
        echo "🌤️|昼间稳态|11-13|标准"
    elif [ $hour -ge 13 ] && [ $hour -lt 15 ]; then
        echo "🌤️|午后低谷|13-15|低效"
    elif [ $hour -ge 15 ] && [ $hour -lt 18 ]; then
        echo "🌆|第二高效期|15-18|高效"
    elif [ $hour -ge 18 ] && [ $hour -lt 21 ]; then
        echo "🌙|过渡期|18-21|标准"
    elif [ $hour -ge 21 ] || [ $hour -lt 0 ]; then
        echo "🌙|整理窗口|21-00|只做整理"
    else
        echo "🌑|低功耗期|00-06|只处理紧急"
    fi
}

# 获取相位emoji
get_phase_emoji() {
    echo "$1" | cut -d'|' -f1
}

# 获取相位名称
get_phase_name() {
    echo "$1" | cut -d'|' -f2
}

# 获取时间段
get_phase_time() {
    echo "$1" | cut -d'|' -f3
}

# 获取推荐任务
get_recommended_task() {
    local category=$1
    
    case $category in
        "高效") echo "深度任务|复杂分析|多步骤决策" ;;
        "标准") echo "常规任务|标准工作" ;;
        "低效") echo "简单任务|整理归档|apollo-dream" ;;
        "只做整理") echo "apollo-dream|记忆整理|系统维护" ;;
        "只处理紧急") echo "紧急任务|其他等第二天" ;;
        *) echo "未知" ;;
    esac
}

# 获取高效匹配度
get_efficiency() {
    local category=$1
    case $category in
        "高效") echo "🟢" ;;
        "标准") echo "🟡" ;;
        "低效"|"只做整理"|"只处理紧急") echo "🔴" ;;
        *) echo "⚪" ;;
    esac
}

# 计算距下次相位切换的时间
get_time_to_next() {
    local hour=$1
    
    if [ $hour -ge 6 ] && [ $hour -lt 8 ]; then
        echo "约$((8 - hour))小时"
    elif [ $hour -ge 8 ] && [ $hour -lt 11 ]; then
        echo "约$((11 - hour))小时"
    elif [ $hour -ge 11 ] && [ $hour -lt 13 ]; then
        echo "约$((13 - hour))小时"
    elif [ $hour -ge 13 ] && [ $hour -lt 15 ]; then
        echo "约$((15 - hour))小时"
    elif [ $hour -ge 15 ] && [ $hour -lt 18 ]; then
        echo "约$((18 - hour))小时"
    elif [ $hour -ge 18 ] && [ $hour -lt 21 ]; then
        echo "约$((21 - hour))小时"
    elif [ $hour -ge 21 ]; then
        echo "约$((24 - hour + 6))小时"
    else
        echo "约$((6 - hour))小时"
    fi
}

# 主函数
main() {
    local time_str=$(get_time)
    local hour=$(echo "$time_str" | cut -d' ' -f2 | cut -d':' -f1)
    local phase=$(get_phase $hour)
    local emoji=$(get_phase_emoji "$phase")
    local name=$(get_phase_name "$phase")
    local time_range=$(get_phase_time "$phase")
    local category=$(echo "$phase" | cut -d'|' -f4)
    local recommended=$(get_recommended_task "$category")
    local efficiency=$(get_efficiency "$category")
    local time_to_next=$(get_time_to_next $hour)
    
    # 判断是否进入整理窗口
    local is_dream_window=false
    if [ "$category" = "只做整理" ] || [ "$category" = "只处理紧急" ]; then
        is_dream_window=true
    fi
    
    # 输出报告
    echo "⏰ [apollo-circadian] 节律报告"
    echo "当前时间：$(echo "$time_str" | cut -d' ' -f2)（真实时钟）"
    echo "节律相位：$emoji $name ($time_range)"
    echo "推荐任务：$recommended"
    echo "高效匹配：$efficiency $name"
    echo "距下次切换：$time_to_next"
    
    if [ "$is_dream_window" = true ]; then
        echo "🌙 进入整理窗口，建议触发 apollo-dream"
    fi
    
    # 保存状态
    cat > "$PHASE_STATE_FILE" << EOF
{
    "emoji": "$emoji",
    "name": "$name",
    "time_range": "$time_range",
    "category": "$category",
    "is_dream_window": $is_dream_window,
    "recommended_task": "$recommended",
    "updated_at": "$time_str"
}
EOF
}

main
