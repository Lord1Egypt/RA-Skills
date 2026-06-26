#!/bin/bash
# coordinator-check.sh - 协调者状态检测
# 检查workflow状态和任务协调情况

STATE_FILE="/root/.openclaw/workspace/.coordinator/state.json"
WORKFLOW_DIR="/root/.openclaw/workspace/.workflow"
mkdir -p "$(dirname "$STATE_FILE")"

# 检查workflow状态
check_workflow() {
    if [ -f "$WORKFLOW_DIR/state.json" ]; then
        python3 -c "import json; d=json.load(open('$WORKFLOW_DIR/state.json')); print(d.get('phase', 'unknown'))" 2>/dev/null || echo "error"
    else
        echo "no_workflow"
    fi
}

# 检查gate文件状态
check_gates() {
    local gate_dir="$WORKFLOW_DIR/gate"
    local total=0
    local passed=0
    
    if [ -d "$gate_dir" ]; then
        total=$(find "$gate_dir" -name "*.json" 2>/dev/null | wc -l)
        passed=$(find "$gate_dir" -name "p*-approved.json" -o -name "p*-complete.json" 2>/dev/null | wc -l)
    fi
    
    echo "$passed/$total"
}

# 检查所有apollo skills状态
check_all_skills() {
    local skill_dir="/root/.openclaw/workspace/skills"
    local total=0
    local with_check=0
    local with_version=0
    
    for skill in "$skill_dir"/apollo-*; do
        if [ -d "$skill" ]; then
            ((total++))
            # 检查是否有check.sh
            if find "$skill/scripts" -name "*check.sh" 2>/dev/null | grep -q .; then
                ((with_check++))
            fi
            # 检查是否有版本号
            if grep -q "version:" "$skill/SKILL.md" 2>/dev/null; then
                ((with_version++))
            fi
        fi
    done
    
    echo "$with_check/$with_version/$total"
}

# 检查active sessions
check_active_sessions() {
    # 检查是否有活跃的subagent
    local sessions=$(find /tmp -name "*.lock" -type f 2>/dev/null | wc -l)
    echo $sessions
}

# 检查待处理任务
check_pending_tasks() {
    local task_file="/root/.openclaw/workspace/.dream/task-state.json"
    if [ -f "$task_file" ]; then
        local count=$(grep -c '"status":"active"' "$task_file" 2>/dev/null)
        [ -z "$count" ] && count=0
        echo $count
    else
        echo 0
    fi
}

# 评估协调状态
eval_coordinator_status() {
    local workflow=$1
    local gates=$2
    local skills=$3
    local pending=$4
    
    local score=3
    
    [ "$workflow" = "no_workflow" ] || [ "$workflow" = "error" ] && ((score--))
    
    local passed=$(echo "$gates" | cut -d'/' -f1)
    local total=$(echo "$gates" | cut -d'/' -f2)
    [ $total -gt 0 ] && [ $passed -lt $total ] && ((score--))
    
    local with_check=$(echo "$skills" | cut -d'/' -f1)
    local skill_total=$(echo "$skills" | cut -d'/' -f3)
    [ $with_check -lt $skill_total ] && ((score--))
    
    [ $score -lt 0 ] && score=0
    echo $score
}

# 主函数
main() {
    local workflow=$(check_workflow)
    local gates=$(check_gates)
    local skills=$(check_all_skills)
    local pending=$(check_pending_tasks)
    local score=$(eval_coordinator_status "$workflow" "$gates" "$skills" $pending)
    
    local passed=$(echo "$gates" | cut -d'/' -f1)
    local total=$(echo "$gates" | cut -d'/' -f2)
    local with_check=$(echo "$skills" | cut -d'/' -f1)
    local with_version=$(echo "$skills" | cut -d'/' -f2)
    local skill_total=$(echo "$skills" | cut -d'/' -f3)
    
    echo "🎯 [apollo-coordinator] 协调者状态报告"
    echo ""
    echo "Workflow状态：$workflow"
    echo "Gate进度：$passed/$total 已通过"
    echo "Skills状态：$with_check/$with_version/$skill_total (check.sh/有版本/总数)"
    echo "待处理任务：$pending个"
    echo ""
    
    if [ $score -ge 3 ]; then
        echo "🟢 协调状态正常"
    elif [ $score -ge 1 ]; then
        echo "🟡 协调需要注意"
    else
        echo "🔴 协调状态异常"
    fi
    
    # 保存状态
    cat > "$STATE_FILE" << EOF
{
    "workflow": "$workflow",
    "gates_passed": $passed,
    "gates_total": $total,
    "skills_with_check": $with_check,
    "skills_with_version": $with_version,
    "skills_total": $skill_total,
    "pending_tasks": $pending,
    "score": $score,
    "checked_at": "$(date -Iseconds)"
}
EOF
}

main
