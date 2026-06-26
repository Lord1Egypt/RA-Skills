#!/bin/bash
# stem-check.sh - 干细胞自我更新检测
# 检查系统自我更新状态

STATE_FILE="/root/.openclaw/workspace/.stem/state.json"
mkdir -p "$(dirname "$STATE_FILE")"

# 检查OpenClaw版本
check_openclaw_version() {
    openclaw --version 2>/dev/null | grep -oE "[0-9]+\.[0-9]+\.[0-9]+" || echo "未知"
}

# 检查最后skill更新时间
check_skill_updates() {
    local skill_dir="/root/.openclaw/workspace/skills"
    local latest=0
    
    for skill in "$skill_dir"/apollo-*/SKILL.md; do
        if [ -f "$skill" ]; then
            local mtime=$(stat -c %Y "$skill" 2>/dev/null)
            [ $mtime -gt $latest ] && latest=$mtime
        fi
    done
    
    if [ $latest -gt 0 ]; then
        local now=$(date +%s)
        local days=$(( (now - latest) / 86400 ))
        echo $days
    else
        echo -1
    fi
}

# 检查自我优化记录
check_self_improvement() {
    local improvement_file="/root/.openclaw/workspace/.learnings/LEARNINGS.md"
    if [ -f "$improvement_file" ]; then
        grep -c "## " "$improvement_file" 2>/dev/null || echo 0
    else
        echo 0
    fi
}

# 检查脚本实现程度
check_script_implementation() {
    local skill_dir="/root/.openclaw/workspace/skills"
    local implemented=0
    local total=0
    
    for skill in "$skill_dir"/apollo-*; do
        if [ -d "$skill" ]; then
            ((total++))
            if [ -d "$skill/scripts" ] && [ $(find "$skill/scripts" -name "*.sh" 2>/dev/null | wc -l) -gt 0 ]; then
                ((implemented++))
            fi
        fi
    done
    
    echo "$implemented|$total"
}

# 检查workflow状态
check_workflow_status() {
    local wf_dir="/root/.openclaw/workspace/.workflow"
    if [ -f "$wf_dir/state.json" ]; then
        grep -o '"phase":"[^"]*"' "$wf_dir/state.json" 2>/dev/null | cut -d'"' -f4 || echo "unknown"
    else
        echo "未初始化"
    fi
}

# 评估更新潜力
eval_renewal_potential() {
    local skill_days=$1
    local improvements=$2
    local impl_info=$3
    
    local implemented=$(echo "$impl_info" | cut -d'|' -f1)
    local total=$(echo "$impl_info" | cut -d'|' -f2)
    
    local score=0
    [ $skill_days -lt 7 ] && ((score++))
    [ $improvements -gt 0 ] && ((score++))
    [ $total -gt 0 ] && [ $implemented -gt 0 ] && ((score++))
    [ $implemented -eq $total ] && ((score++))  # 全部实现
    
    echo $score
}

# 主函数
main() {
    local version=$(check_openclaw_version)
    local skill_days=$(check_skill_updates)
    local improvements=$(check_self_improvement)
    local impl_info=$(check_script_implementation)
    local wf_status=$(check_workflow_status)
    local score=$(eval_renewal_potential $skill_days $improvements "$impl_info")
    
    local implemented=$(echo "$impl_info" | cut -d'|' -f1)
    local total=$(echo "$impl_info" | cut -d'|' -f2)
    
    echo "🌱 [apollo-stem] 干细胞更新报告"
    echo ""
    echo "系统状态："
    echo "  - OpenClaw版本：$version"
    echo "  - 最近Skill更新：$([ $skill_days -eq 0 ] && echo '今天' || echo \"${skill_days}天前\")"
    echo "  - 自我优化记录：${improvements}条"
    echo "  - 脚本实现：${implemented}/${total}个Skills"
    echo "  - 当前Workflow：$wf_status"
    echo ""
    
    if [ $score -ge 3 ]; then
        echo "🟢 自我更新活跃"
    elif [ $score -ge 1 ]; then
        echo "🟡 更新能力一般"
    else
        echo "🔴 需要触发自我更新"
    fi
    
    echo ""
    echo "更新建议：$([ $score -lt 3 ] && echo '运行skill更新|检查自我优化' || echo '保持当前状态')"
    
    # 保存状态
    cat > "$STATE_FILE" << EOF
{
    "openclaw_version": "$version",
    "skill_updated_days_ago": $skill_days,
    "self_improvement_count": $improvements,
    "script_implementation": "$implemented/$total",
    "workflow_status": "$wf_status",
    "renewal_score": $score,
    "checked_at": "$(date -Iseconds)"
}
EOF
}

main
