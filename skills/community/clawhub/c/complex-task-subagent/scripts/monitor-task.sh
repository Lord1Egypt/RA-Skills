#!/bin/bash
# monitor-task.sh - 监控任务进度
# 用途：显示任务进度、检查点状态和子代理信息

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 默认参数
TASK_PROGRESS_FILE="/root/.openclaw/workspace/task-progress.json"
CHECKPOINTS_DIR="/root/.openclaw/workspace/complex-task-subagent-experience/checkpoints"
LOG_FILE="/root/.openclaw/workspace/task-monitor.log"
CONTINUOUS=false
INTERVAL=10

# 使用说明
usage() {
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  -f, --file <path>    任务进度文件（默认: $TASK_PROGRESS_FILE）"
    echo "  -c, --continuous     持续监控模式"
    echo "  -i, --interval <s>   刷新间隔，秒（默认: 10）"
    echo "  -h, --help           显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  $0                           # 显示一次进度"
    echo "  $0 --continuous              # 持续监控（每 10 秒）"
    echo "  $0 -c -i 30                 # 持续监控（每 30 秒）"
    exit 1
}

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -f|--file)
            TASK_PROGRESS_FILE="$2"
            shift 2
            ;;
        -c|--continuous)
            CONTINUOUS=true
            shift
            ;;
        -i|--interval)
            INTERVAL="$2"
            shift 2
            ;;
        -h|--help)
            usage
            ;;
        *)
            echo -e "${RED}未知选项: $1${NC}"
            usage
            ;;
    esac
done

# 检查文件是否存在
if [ ! -f "$TASK_PROGRESS_FILE" ]; then
    echo -e "${RED}错误: 任务进度文件不存在: $TASK_PROGRESS_FILE${NC}"
    exit 1
fi

# 读取任务信息
TASK_ID=$(python3 -c "import json; print(json.load(open('$TASK_PROGRESS_FILE')).get('taskId', 'N/A'))")
TASK_NAME=$(python3 -c "import json; print(json.load(open('$TASK_PROGRESS_FILE')).get('taskName', 'N/A'))")
STATUS=$(python3 -c "import json; print(json.load(open('$TASK_PROGRESS_FILE')).get('status', 'N/A'))")
CURRENT_PHASE=$(python3 -c "import json; print(json.load(open('$TASK_PROGRESS_FILE')).get('currentPhase', 0))")
COMPLETED_PHASES=$(python3 -c "import json; print(json.load(open('$TASK_PROGRESS_FILE')).get('completedPhases', 0))")
TOTAL_PHASES=$(python3 -c "import json; print(json.load(open('$TASK_PROGRESS_FILE')).get('totalPhases', 0))")
LAST_UPDATED=$(python3 -c "import json; print(json.load(open('$TASK_PROGRESS_FILE')).get('lastUpdated', 'N/A'))")

# 计算进度百分比
if [ "$TOTAL_PHASES" -gt 0 ]; then
    PROGRESS=$((COMPLETED_PHASES * 100 / TOTAL_PHASES))
else
    PROGRESS=0
fi

# 显示任务信息
show_header() {
    clear
    echo -e "${CYAN}========================================${NC}"
    echo -e "${CYAN}       任务监控 Dashboard${NC}"
    echo -e "${CYAN}========================================${NC}"
    echo ""
    echo -e "${BLUE}任务 ID:${NC}   $TASK_ID"
    echo -e "${BLUE}任务名称:${NC} $TASK_NAME"
    echo -e "${BLUE}状态:${NC}     $(get_status_color $STATUS)$STATUS${NC}"
    echo -e "${BLUE}进度:${NC}     ${GREEN}$PROGRESS%${NC} ($COMPLETED_PHASES/$TOTAL_PHASES)"
    echo -e "${BLUE}最后更新:${NC} $LAST_UPDATED"
    echo -e "${CYAN}========================================${NC}"
    echo ""
}

# 状态颜色
get_status_color() {
    local status=$1
    case $status in
        "completed")
            echo -n "${GREEN}"
            ;;
        "in_progress")
            echo -n "${YELLOW}"
            ;;
        "failed")
            echo -n "${RED}"
            ;;
        *)
            echo -n "${NC}"
            ;;
    esac
}

# 显示阶段列表
show_phases() {
    echo -e "${YELLOW}阶段详情:${NC}"
    echo ""

    python3 << PYTHON_SCRIPT
import json
from pathlib import Path

# 读取任务进度
with open('$TASK_PROGRESS_FILE', 'r') as f:
    task = json.load(f)

# 遍历阶段
for phase_id, phase in sorted(task['phases'].items()):
    status = phase.get('status', 'unknown')
    name = phase.get('name', phase_id)
    retries = phase.get('retries', 0)
    started_at = phase.get('startedAt', '-')
    completed_at = phase.get('completedAt', '-')

    # 状态图标
    icons = {
        'pending': '⏳',
        'starting': '🔄',
        'running': '🔄',
        'completed': '✅',
        'failed': '❌'
    }
    icon = icons.get(status, '❓')

    # 颜色代码
    colors = {
        'pending': '\033[0m',
        'starting': '\033[1;33m',
        'running': '\033[0;34m',
        'completed': '\033[0;32m',
        'failed': '\033[0;31m'
    }
    color = colors.get(status, '\033[0m')
    reset = '\033[0m'

    # 检查点状态
    checkpoint_file = Path('$CHECKPOINTS_DIR') / phase.get('checkpoint', '')
    checkpoint_exists = '✓' if checkpoint_file.exists() else '✗'

    # 输出
    print(f"{color}{icon} {phase_id}: {name}{reset}")
    print(f"    状态: {status}")

    if status == 'running':
        print(f"    开始时间: {started_at}")
    elif status == 'completed':
        print(f"    完成时间: {completed_at}")

    if retries > 0:
        print(f"    重试次数: {retries}")

    print(f"    检查点: {checkpoint_exists}")
    print("")
PYTHON_SCRIPT
}

# 显示子代理状态
show_subagents() {
    echo -e "${YELLOW}子代理状态:${NC}"
    echo ""

    # 获取子代理列表
    if command -v openclaw &> /dev/null; then
        openclaw subagents list 2>/dev/null | head -20 || echo "  无法获取子代理信息"
    else
        echo "  openclaw 命令不可用"
    fi
    echo ""
}

# 显示最近日志
show_logs() {
    echo -e "${YELLOW}最近日志（最后 10 行）:${NC}"
    echo ""

    if [ -f "$LOG_FILE" ]; then
        tail -10 "$LOG_FILE"
    else
        echo "  日志文件不存在: $LOG_FILE"
    fi
    echo ""
}

# 主监控循环
if [ "$CONTINUOUS" = true ]; then
    while true; do
        show_header
        show_phases
        show_subagents
        show_logs

        echo -e "${CYAN}下次刷新: ${INTERVAL} 秒后（按 Ctrl+C 退出）${NC}"
        sleep $INTERVAL
    done
else
    show_header
    show_phases
    show_subagents
    show_logs
fi
