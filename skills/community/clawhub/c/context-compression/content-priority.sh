#!/bin/bash
# Content Priority Scoring - v1.0
# 为内容打分，高优先级内容优先保留
# 配合 truncate-sessions-safe.sh 使用
#
# Safety note: This script performs LOCAL text analysis only.
# No network requests, no external connections.

WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"
LOG_FILE="${LOG_FILE:-$HOME/.openclaw/logs/truncation.log}"

mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# 内容优先级评分
# 返回: 0-100 分数
score_content() {
    local text=$1
    local score=50  # 基础分
    
    # === 高优先级关键词 (+30 ~ +50) ===
    
    # 用户偏好相关
    [[ "$text" =~ (用户偏好|喜欢|讨厌|偏好|习惯|风格) ]] && score=$((score + 40))
    
    # 重要标记
    [[ "$text" =~ (重要|关键|记住|别忘|必须|一定要) ]] && score=$((score + 45))
    
    # 决策相关
    [[ "$text" =~ (决定|确定|选择|方案|定下|决策) ]] && score=$((score + 35))
    
    # === 中优先级关键词 (+15 ~ +30) ===
    
    # 任务状态
    
    # 任务状态
    [[ "$text" =~ (任务|TODO|待办|进度|完成|进行中) ]] && score=$((score + 25))
    
    # 时间敏感
    [[ "$text" =~ (明天|下周|周[一二三四五六日]|[0-9]+月[0-9]+日|截止|deadline) ]] && score=$((score + 20))
    
    # 联系人
    [[ "$text" =~ (同事|老板|客户|朋友|家人) ]] && score=$((score + 15))
    
    # === 低优先级关键词 (-10 ~ -30) ===
    
    # 闲聊
    [[ "$text" =~ (哈哈|呵呵|嗯嗯|好的|收到|OK|ok) ]] && score=$((score - 10))
    
    # 系统消息
    [[ "$text" =~ (HEARTBEAT|heartbeat|system|系统消息) ]] && score=$((score - 20))
    
    # 重复/确认
    [[ "$text" =~ (明白|了解|清楚|知道了) ]] && score=$((score - 15))
    
    # === 时间衰减 ===
    # 这个需要在调用时传入时间信息，这里先留空
    
    # 限制范围
    [ $score -lt 0 ] && score=0
    [ $score -gt 100 ] && score=100
    
    echo $score
}

# 为 JSONL 文件的每一行打分
# 输出: <行号>\t<分数>\t<内容摘要>
score_session_file() {
    local file=$1
    local line_num=0
    
    while IFS= read -r line; do
        ((line_num++))
        
        # 提取文本内容
        local text=$line
        if echo "$line" | grep -q '"content"'; then
            text=$(echo "$line" | grep -oP '(?<="content":")[^"]*' | head -1)
        fi
        
        # 打分
        local score=$(score_content "$text")
        
        # 输出：行号、分数、前100字符
        local summary=$(echo "$text" | cut -c1-100 | tr '\n' ' ')
        echo -e "${line_num}\t${score}\t${summary}"
        
    done < "$file"
}

# 找出高优先级行
# 输出: 高分行号列表（空格分隔）
find_high_priority_lines() {
    local file=$1
    local threshold=${2:-70}  # 默认阈值 70 分
    
    score_session_file "$file" | \
        awk -F'\t' -v threshold="$threshold" '$2 >= threshold {print $1}' | \
        tr '\n' ' '
}

# 智能截断：保留高优先级 + 最近内容
# 返回：应该保留的行号列表
smart_truncate_plan() {
    local file=$1
    local max_lines=$2
    local total_lines=$(wc -l < "$file")
    
    # 如果文件不大，不需要截断
    if [ "$total_lines" -le "$max_lines" ]; then
        seq 1 $total_lines
        return
    fi
    
    # 1. 找出高优先级行
    local high_priority=$(find_high_priority_lines "$file" 70)
    
    # 2. 获取最近 N 行
    local recent_start=$((total_lines - max_lines / 2))  # 后半部分全保留
    local recent_lines=$(seq $recent_start $total_lines)
    
    # 3. 合并：高优先级 + 最近内容（去重）
    {
        echo "$high_priority" | tr ' ' '\n'
        echo "$recent_lines"
    } | sort -n | uniq
    
    # 注意：实际保留的行数可能超过 max_lines
    # 这是故意的：高优先级内容不应该被丢弃
}

# 统计文件中各优先级的行数
stats_priority_distribution() {
    local file=$1
    
    local high=0    # >= 70
    local medium=0  # 40-69
    local low=0     # < 40
    
    while IFS= read -r line; do
        local score=$(score_content "$line")
        
        if [ "$score" -ge 70 ]; then
            ((high++))
        elif [ "$score" -ge 40 ]; then
            ((medium++))
        else
            ((low++))
        fi
    done < <(score_session_file "$file" | cut -f2)
    
    echo "Priority distribution:"
    echo "  High (>=70):   $high"
    echo "  Medium (40-69): $medium"
    echo "  Low (<40):      $low"
}

# 如果作为独立脚本运行
if [ "${BASH_SOURCE[0]}" = "$0" ]; then
    if [ -z "$1" ]; then
        echo "Usage: $0 <session-file> [command]"
        echo "Commands:"
        echo "  score     - Score each line"
        echo "  stats     - Show priority distribution"
        echo "  high      - Find high priority lines"
        exit 1
    fi
    
    file=$1
    cmd=${2:-stats}
    
    case "$cmd" in
        score)
            score_session_file "$file"
            ;;
        stats)
            stats_priority_distribution "$file"
            ;;
        high)
            find_high_priority_lines "$file"
            ;;
        *)
            echo "Unknown command: $cmd"
            exit 1
            ;;
    esac
fi
