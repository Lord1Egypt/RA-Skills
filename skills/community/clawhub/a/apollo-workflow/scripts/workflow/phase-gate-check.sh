#!/bin/bash
# apollo-workflow phase-gate-check.sh
# HARD GATE门禁检查
# 用法: phase-gate-check.sh <target_phase>

WORKFLOW_DIR="/root/.openclaw/workspace/.workflow"
STATE_FILE="$WORKFLOW_DIR/state.json"

# 检查state.json是否存在
check_state() {
    if [ ! -f "$STATE_FILE" ]; then
        echo "⛔ 未找到workflow state.json"
        echo "请先运行: state-manager.sh init <topic>"
        return 1
    fi
    return 0
}

# HG-1: phase2需要p1 gate
check_hg1() {
    local gate_file="$WORKFLOW_DIR/gate/p1-design-approved.json"
    if [ ! -f "$gate_file" ]; then
        echo "⛔ HARD GATE HG-1 未通过"
        echo ""
        echo "缺少:"
        echo "  ❌ $gate_file"
        echo ""
        echo "当前处于 Phase 1 (Brainstorming)。"
        echo "请先完成设计文档并获得用户批准。"
        return 1
    fi
    echo "Gate passed: p1"
    return 0
}

# HG-2: phase3需要p2 gate
check_hg2() {
    local gate_file="$WORKFLOW_DIR/gate/p2-plan-approved.json"
    if [ ! -f "$gate_file" ]; then
        echo "⛔ HARD GATE HG-2 未通过"
        echo ""
        echo "缺少:"
        echo "  ❌ $gate_file"
        echo ""
        echo "当前处于 Phase 2 (Writing Plans)。"
        echo "请先完成实现计划。"
        return 1
    fi
    echo "Gate passed: p2"
    return 0
}

# HG-3: phase5需要p3 gate
check_hg3() {
    local gate_file="$WORKFLOW_DIR/gate/p3-all-tasks-done.json"
    if [ ! -f "$gate_file" ]; then
        echo "⛔ HARD GATE HG-3 未通过"
        echo ""
        echo "缺少:"
        echo "  ❌ $gate_file"
        echo ""
        echo "当前处于 Phase 3 (Subagent Development)。"
        echo "请先完成所有任务。"
        return 1
    fi
    echo "Gate passed: p3"
    return 0
}

# HG-4: debug完成需要p4 gate
check_hg4() {
    local gate_file="$WORKFLOW_DIR/gate/p4-bug-fixed.json"
    if [ ! -f "$gate_file" ]; then
        echo "⛔ HARD GATE HG-4 未通过"
        echo ""
        echo "缺少:"
        echo "  ❌ $gate_file"
        echo ""
        echo "Bug已修复但尚未验证。"
        echo "请确保: 1) 根因已写入commit 2) 有捕获此Bug的测试 3) 全套测试通过"
        return 1
    fi
    echo "Gate passed: p4-bug-fixed"
    return 0
}

# HG-5: finish需要p5 gate
check_hg5() {
    local gate_file="$WORKFLOW_DIR/gate/p5-complete.json"
    if [ ! -f "$gate_file" ]; then
        echo "⛔ HARD GATE HG-5 未通过"
        echo ""
        echo "缺少:"
        echo "  ❌ $gate_file"
        echo ""
        echo "请先完成Phase 1-4并确认交付方式。"
        return 1
    fi
    echo "Gate passed: p5-complete"
    return 0
}

# 主入口
TARGET="$1"

if [ -z "$TARGET" ]; then
    echo "用法: phase-gate-check.sh <phase1|phase2|phase3|phase4|phase5|debug-complete|finish>"
    exit 1
fi

case "$TARGET" in
    phase1)
        # Phase 1可随时进入，只需state.json存在
        check_state
        echo "Gate passed: phase1-init"
        ;;
    phase2)
        check_state && check_hg1
        ;;
    phase3)
        check_state && check_hg2
        ;;
    phase4)
        # Phase 4可随时进入（debug模式）
        check_state
        echo "Gate passed: phase4-entry (Phase 4可随时进入)"
        ;;
    phase5)
        check_state && check_hg3
        ;;
    debug-complete)
        # HG-4: debug完成需要p4 gate
        check_state && check_hg4
        ;;
    finish)
        # HG-5: finish需要p5 gate
        check_state && check_hg5
        ;;
    *)
        echo "未知phase: $TARGET"
        echo "用法: phase-gate-check.sh <phase1|phase2|phase3|phase4|phase5|debug-complete|finish>"
        exit 1
        ;;
esac
