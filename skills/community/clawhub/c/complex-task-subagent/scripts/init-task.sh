#!/bin/bash
# init-task.sh - 初始化任务
# 用途：创建任务进度文件和检查点目录

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 使用说明
usage() {
    echo "用法: $0 <task-id> <task-name> <phase-count>"
    echo ""
    echo "参数:"
    echo "  task-id      任务唯一标识"
    echo "  task-name    任务名称"
    echo "  phase-count  阶段数量"
    echo ""
    echo "示例:"
    echo "  $0 my-task-20260312 '我的任务' 4"
    exit 1
}

# 检查参数
if [ $# -ne 3 ]; then
    usage
fi

TASK_ID="$1"
TASK_NAME="$2"
PHASE_COUNT="$3"

WORKSPACE="/root/.openclaw/workspace"
TASK_PROGRESS_FILE="$WORKSPACE/task-progress.json"
CHECKPOINTS_DIR="$WORKSPACE/complex-task-subagent-experience/checkpoints"

# 创建检查点目录
echo -e "${YELLOW}创建检查点目录...${NC}"
mkdir -p "$CHECKPOINTS_DIR"

# 创建任务进度文件
echo -e "${YELLOW}创建任务进度文件...${NC}"

cat > "$TASK_PROGRESS_FILE" << EOF
{
  "taskId": "$TASK_ID",
  "taskName": "$TASK_NAME",
  "status": "in_progress",
  "currentPhase": 1,
  "completedPhases": 0,
  "totalPhases": $PHASE_COUNT,
  "lastUpdated": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "checkpointsDir": "$CHECKPOINTS_DIR",
  "phases": {
EOF

# 添加各个阶段
for i in $(seq 1 $PHASE_COUNT); do
    PHASE_NUM=$((i - 1))

    if [ $i -lt $PHASE_COUNT ]; then
        COMMA=","
    else
        COMMA=""
    fi

    cat >> "$TASK_PROGRESS_FILE" << EOF
    "phase$i": {
      "name": "阶段 $i",
      "status": "pending",
      "timeout": 1800000,
      "maxRetries": 3,
      "retries": 0,
      "checkpoint": "phase$i.json"
    }$COMMA
EOF
done

# 结束 JSON
cat >> "$TASK_PROGRESS_FILE" << EOF
  }
}
EOF

# 验证文件
echo -e "${YELLOW}验证 JSON 格式...${NC}"
if python3 -m json.tool "$TASK_PROGRESS_FILE" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ JSON 格式正确${NC}"
else
    echo -e "${RED}❌ JSON 格式错误${NC}"
    rm "$TASK_PROGRESS_FILE"
    exit 1
fi

echo ""
echo -e "${GREEN}✅ 任务初始化完成！${NC}"
echo ""
echo "文件位置:"
echo "  - 任务进度: $TASK_PROGRESS_FILE"
echo "  - 检查点目录: $CHECKPOINTS_DIR"
echo ""
echo "下一步:"
echo "  1. 编辑 task-progress.json，配置各个阶段"
echo "  2. 配置 HEARTBEAT.md（如需要）"
echo "  3. 启动第一个阶段："
echo "     sessions_spawn --task '...' --label 'subagent-phase1' ..."
echo ""
