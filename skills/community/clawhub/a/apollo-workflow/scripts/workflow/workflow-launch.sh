#!/bin/bash
# apollo-workflow workflow-launch.sh
# 启动完整workflow
# 用法: ./workflow-launch.sh "<topic>"

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
WORKFLOW_DIR="/root/.openclaw/workspace/.workflow"
STATE_MANAGER="$SCRIPT_DIR/state-manager.sh"
GATE_CHECK="$SCRIPT_DIR/phase-gate-check.sh"

TOPIC="${1:-}"

if [ -z "$TOPIC" ]; then
    echo "用法: ./workflow-launch.sh \"<你的想法或任务>\""
    echo ""
    echo "示例: ./workflow-launch.sh \"给项目加一个缓存功能\""
    exit 1
fi

echo "🚀 启动Apollo Workflow"
echo "====================="
echo "Topic: $TOPIC"
echo ""

# Step 1: 初始化
echo "📝 Step 1: 初始化workflow..."
bash "$STATE_MANAGER" init "$TOPIC"

# Step 2: 检查HG-0通过
echo ""
echo "🚪 Step 2: HG-0 启动门检查..."
if bash "$GATE_CHECK" phase1; then
    echo "✅ HG-0 通过，进入 Phase 1"
else
    echo "❌ HG-0 失败"
    exit 1
fi

# Step 3: 显示当前状态
echo ""
echo "📊 当前状态:"
bash "$STATE_MANAGER" check

echo ""
echo "====================="
echo "✅ Workflow已启动！"
echo ""
echo "下一步: 进入Phase 1 (Brainstorming)"
echo "  - 定义问题/需求"
echo "  - 提出解决方案"
echo "  - 完成后运行: bash $GATE_CHECK phase2"
