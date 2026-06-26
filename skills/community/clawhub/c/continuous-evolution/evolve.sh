#!/bin/bash
# Continuous Evolution - 持续进化模块
# 功能：在每次任务执行中自动学习、总结、进化

set -eo pipefail

TASKS_DIR="/root/.openclaw/workspace/tasks"
MEMORY_DIR="/root/.openclaw/workspace/memory"
SKILLS_DIR="/root/.openclaw/workspace/skills"
EVOLUTION_DIR="${MEMORY_DIR}/evolution"
LOG_PREFIX="[evolution]"

log() {
    echo "$LOG_PREFIX $1"
}

ensure_dirs() {
    mkdir -p "$EVOLUTION_DIR"
}

# 记录本次任务的经验
record_experience() {
    local task_id="$1"
    local task="$2"
    local result="$3"
    local audit_score="$4"
    local exp_file="${EVOLUTION_DIR}/experience-$(date +%Y-%m-%d).md"
    
    log "📚 记录经验：$task_id"
    
    cat >> "$exp_file" << EOF

---

## $(date "+%H:%M:%S") - $task_id

**任务**: $task
**结果**: $result
**审计评分**: $audit_score/100

EOF

    # 低分任务记录改进点
    if [[ $audit_score -lt 80 ]]; then
        cat >> "$exp_file" << EOF
**待改进**:
- 需要分析原因
- 记录教训

EOF
    fi
}

# 分析能力缺口
analyze_gaps() {
    local task="$1"
    local gaps_file="${EVOLUTION_DIR}/gaps-$(date +%Y-%m-%d).md"
    
    log "🔍 分析能力缺口"
    
    # 检查任务类型
    if echo "$task" | grep -qi "code\|program"; then
        echo "- [ ] 代码能力需要增强" >> "$gaps_file"
    fi
    
    if echo "$task" | grep -qi "data\|analyze"; then
        echo "- [ ] 数据分析能力需要增强" >> "$gaps_file"
    fi
    
    if echo "$task" | grep -qi "search\|research"; then
        echo "- [ ] 搜索能力需要增强" >> "$gaps_file"
    fi
}

# 生成进化任务
generate_evolution_task() {
    local gap="$1"
    local task_file="${TASKS_DIR}/queue/P1_evol-$(date +%Y%m%d-%H%M%S)-$$.json"
    
    local task_desc="增强能力：$gap"
    
    cat > "$task_file" << EOF
{
    "id": "evol-$(date +%Y%m%d-%H%M%S)-$$",
    "priority": "P1",
    "task": "$task_desc",
    "type": "evolution",
    "created_at": "$(date -Iseconds)",
    "status": "pending"
}
EOF
    
    log "✅ 生成进化任务：$task_file"
    echo "$task_file"
}

# 更新能力评估
update_capability_assessment() {
    local audit_score="$1"
    local assess_file="${EVOLUTION_DIR}/capability-assessment.json"
    
    # 读取当前评估
    local total_tasks=0
    local avg_score=0
    
    if [[ -f "$assess_file" ]]; then
        total_tasks=$(jq -r '.total_tasks // 0' "$assess_file" 2>/dev/null || echo "0")
        avg_score=$(jq -r '.average_score // 0' "$assess_file" 2>/dev/null || echo "0")
    fi
    
    # 确保是数字
    [[ ! "$avg_score" =~ ^[0-9.]+$ ]] && avg_score=0
    
    # 计算新平均值
    total_tasks=$((total_tasks + 1))
    avg_score=$(awk "BEGIN {printf \"%.2f\", ($avg_score * ($total_tasks - 1) + $audit_score) / $total_tasks}")
    
    # 确定能力等级
    local level="basic"
    if (( $(echo "$avg_score >= 80" | bc -l) )); then
        level="advanced"
    elif (( $(echo "$avg_score >= 60" | bc -l) )); then
        level="intermediate"
    fi
    
    # 更新评估
    cat > "$assess_file" << EOF
{
    "total_tasks": $total_tasks,
    "average_score": $avg_score,
    "last_updated": "$(date -Iseconds)",
    "capability_level": "$level"
}
EOF
    
    log "📊 能力评估更新：平均分 $avg_score/100 ($level)"
}

# 主流程
if [[ $# -lt 4 ]]; then
    echo "用法：$0 <任务 ID> <任务描述> <执行结果> <审计评分>"
    exit 1
fi

TASK_ID="$1"
TASK="$2"
RESULT="$3"
AUDIT_SCORE="${4:-70}"  # 默认值

# 确保是数字
if ! [[ "$AUDIT_SCORE" =~ ^[0-9]+$ ]]; then
    AUDIT_SCORE=70
fi

ensure_dirs

log "🔄 持续进化流程启动..."

# 1. 记录经验
record_experience "$TASK_ID" "$TASK" "$RESULT" "$AUDIT_SCORE"

# 2. 分析能力缺口
analyze_gaps "$TASK"

# 3. 更新能力评估
update_capability_assessment "$AUDIT_SCORE"

# 4. 如果分数低，自动生成进化任务
if [[ $AUDIT_SCORE -lt 70 ]]; then
    log "⚠️ 评分较低，生成进化任务..."
    generate_evolution_task "任务执行质量 (当前评分：$AUDIT_SCORE/100)"
fi

log "✅ 进化流程完成"
echo "evolution_completed"
