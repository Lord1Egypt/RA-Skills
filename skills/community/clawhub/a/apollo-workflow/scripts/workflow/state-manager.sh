#!/bin/bash
# apollo-workflow state-manager.sh
# 状态文件读写 + Phase推进
# 用法: state-manager.sh <command> [args]

WORKFLOW_DIR="/root/.openclaw/workspace/.workflow"
STATE_FILE="$WORKFLOW_DIR/state.json"

mkdir -p "$WORKFLOW_DIR"
mkdir -p "$WORKFLOW_DIR/gate"

# 生成UUID
generate_uuid() {
    cat /proc/sys/kernel/random/uuid 2>/dev/null || echo "uuid-$(date +%s)"
}

# 初始化新workflow
cmd_init() {
    local topic="$1"
    if [ -z "$topic" ]; then
        echo "用法: state-manager.sh init <topic>"
        exit 1
    fi
    
    cat > "$STATE_FILE" <<EOF
{
  "version": "2.0.0",
  "workflow_id": "$(generate_uuid)",
  "started_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "current_phase": "phase1",
  "topic": "$topic",
  "plan_file": "",
  "design_file": "",
  "feature_branch": "",
  "task_count": 0,
  "completed_tasks": [],
  "pending_tasks": [],
  "gates_passed": [],
  "last_updated": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
    echo "✅ Workflow已初始化: $topic"
    echo "📁 状态文件: $STATE_FILE"
    echo "📁 Gate目录: $WORKFLOW_DIR/gate/"
}

# 检查状态
cmd_check() {
    if [ ! -f "$STATE_FILE" ]; then
        echo "❌ 未找到state.json，请先运行: state-manager.sh init <topic>"
        exit 1
    fi
    
    echo "=== Workflow状态 ==="
    cat "$STATE_FILE" | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'Phase: {d[\"current_phase\"]}'); print(f'Topic: {d[\"topic\"]}'); print(f'Workflow ID: {d[\"workflow_id\"]}')"
    
    echo ""
    echo "=== Gate文件状态 ==="
    for gate in p1-design-approved p2-plan-approved p3-all-tasks-done p4-bug-fixed p5-complete; do
        if [ -f "$WORKFLOW_DIR/gate/${gate}.json" ]; then
            echo "  ✅ $gate.json"
        else
            echo "  ❌ $gate.json (缺失)"
        fi
    done
}

# 推进phase
cmd_advance() {
    local target_phase="$1"
    if [ -z "$target_phase" ]; then
        echo "用法: state-manager.sh advance <phase>"
        exit 1
    fi
    
    if [ ! -f "$STATE_FILE" ]; then
        echo "❌ 未找到state.json"
        exit 1
    fi
    
    # 更新current_phase
    python3 - <<EOF
import json

with open('$STATE_FILE', 'r') as f:
    state = json.load(f)

old_phase = state['current_phase']
state['current_phase'] = '$target_phase'
state['last_updated'] = '$(date -u +%Y-%m-%dT%H:%M:%SZ)'

with open('$STATE_FILE', 'w') as f:
    json.dump(state, f, indent=2, ensure_ascii=False)

print(f'Phase推进: {old_phase} → $target_phase')
EOF
}

# 显示帮助
cmd_help() {
    echo "apollo-workflow state-manager.sh"
    echo ""
    echo "命令:"
    echo "  init <topic>      初始化新workflow"
    echo "  check             检查状态"
    echo "  advance <phase>   推进到指定phase"
    echo "  help              显示帮助"
}

# 主入口
case "${1:-help}" in
    init)
        cmd_init "${2:-}"
        ;;
    check)
        cmd_check
        ;;
    advance)
        cmd_advance "${2:-}"
        ;;
    help|*)
        cmd_help
        ;;
esac
