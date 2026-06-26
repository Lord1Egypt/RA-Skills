#!/bin/bash
# epi-check.sh - 表观遗传知识传承检测
# 检查知识传承状态，确保经验能传递给后续任务

STATE_FILE="/root/.openclaw/workspace/.epi/state.json"
mkdir -p "$(dirname "$STATE_FILE")"

# 检查MEMORY.md最后更新时间
check_memory_update() {
    local memory_file="/root/.openclaw/workspace/MEMORY.md"
    if [ -f "$memory_file" ]; then
        local mtime=$(stat -c %Y "$memory_file" 2>/dev/null)
        local now=$(date +%s)
        local days=$(( (now - mtime) / 86400 ))
        echo $days
    else
        echo -1
    fi
}

# 检查今日memory文件
check_today_memory() {
    local today_file="/root/.openclaw/workspace/memory/$(date +%Y-%m-%d).md"
    if [ -f "$today_file" ]; then
        echo 1
    else
        echo 0
    fi
}

# 检查经验总结数量
count_experiences() {
    local memory_file="/root/.openclaw/workspace/MEMORY.md"
    if [ -f "$memory_file" ]; then
        grep -c "## " "$memory_file" 2>/dev/null || echo 0
    else
        echo 0
    fi
}

# 检查learnings目录
check_learnings() {
    local learnings_dir="/root/.openclaw/workspace/.learnings"
    if [ -d "$learnings_dir" ]; then
        find "$learnings_dir" -name "*.md" 2>/dev/null | wc -l
    else
        echo 0
    fi
}

# 检查Skills文档化程度
check_skill_docs() {
    local skill_dir="/root/.openclaw/workspace/skills"
    local documented=0
    local total=0
    
    for skill in "$skill_dir"/apollo-*; do
        if [ -d "$skill" ]; then
            ((total++))
            if [ -f "$skill/SKILL.md" ]; then
                ((documented++))
            fi
        fi
    done
    
    echo "$documented|$total"
}

# 判断传承状态
eval_inheritance() {
    local mem_days=$1
    local today=$2
    local experiences=$3
    local learnings=$4
    local docs_info=$5
    
    local documented=$(echo "$docs_info" | cut -d'|' -f1)
    local total=$(echo "$docs_info" | cut -d'|' -f2)
    
    local score=0
    [ $today -eq 1 ] && ((score++))
    [ $experiences -gt 5 ] && ((score++))
    [ $learnings -gt 0 ] && ((score++))
    [ $mem_days -lt 7 ] && ((score++))
    [ $total -gt 0 ] && [ $documented -eq $total ] && ((score++))
    
    echo $score
}

# 获取传承建议
get_inheritance_advice() {
    local score=$1
    local mem_days=$2
    local today=$3
    local experiences=$4
    
    if [ $score -ge 4 ]; then
        echo "传承状态良好|经验积累充分"
    elif [ $score -ge 2 ]; then
        echo "需要补充传承|建议记录今日经验"
    else
        if [ $today -eq 0 ]; then
            echo "创建今日memory|开启传承记录"
        elif [ $experiences -lt 3 ]; then
            echo "积累更多经验|及时记录重要决策"
        else
            echo "完善MEMORY.md|确保经验可查询"
        fi
    fi
}

# 主函数
main() {
    local mem_days=$(check_memory_update)
    local today=$(check_today_memory)
    local experiences=$(count_experiences)
    local learnings=$(check_learnings)
    local docs_info=$(check_skill_docs)
    local score=$(eval_inheritance $mem_days $today $experiences $learnings "$docs_info")
    local advice=$(get_inheritance_advice $score $mem_days $today $experiences)
    
    local mem_status="未知"
    if [ $mem_days -ge 0 ]; then
        if [ $mem_days -eq 0 ]; then
            mem_status="今天"
        else
            mem_status="${mem_days}天前"
        fi
    fi
    
    local documented=$(echo "$docs_info" | cut -d'|' -f1)
    local total=$(echo "$docs_info" | cut -d'|' -f2)
    
    echo "🧬 [apollo-epi] 表观遗传传承报告"
    echo ""
    echo "传承状态："
    echo "  - MEMORY.md：$mem_status更新"
    echo "  - 今日memory：$([ $today -eq 1 ] && echo '存在' || echo '未创建')"
    echo "  - 经验章节：${experiences}个"
    echo "  - Learnings：${learnings}个"
    echo "  - Skills文档化：${documented}/${total}个"
    echo ""
    
    if [ $score -ge 4 ]; then
        echo "🟢 传承状态良好"
    elif [ $score -ge 2 ]; then
        echo "🟡 传承需要加强"
    else
        echo "🔴 传承状态堪忧"
    fi
    echo ""
    echo "传承建议：$advice"
    
    # 保存状态
    cat > "$STATE_FILE" << EOF
{
    "memory_updated_days_ago": $mem_days,
    "today_memory_exists": $([ $today -eq 1 ] && echo "true" || echo "false"),
    "experience_count": $experiences,
    "learnings_count": $learnings,
    "skill_docs": "$documented/$total",
    "inheritance_score": $score,
    "advice": "$advice",
    "checked_at": "$(date -Iseconds)"
}
EOF
}

main
