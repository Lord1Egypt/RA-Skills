#!/bin/bash
# loudy.ai 定时检查脚本
# 每5分钟检查一次

# 获取工作目录（优先使用环境变量，否则使用默认路径）
WORKSPACE_DIR="${OPENCLAW_WORKSPACE:-/root/.openclaw/workspace}"

# 从环境变量读取 API Key，若未设置则退出
if [ -z "$LOUDY_API_KEY" ]; then
    echo "LOUDY_API_KEY not set"
    exit 1
fi
export LOUDY_API_KEY

LOG_FILE="$WORKSPACE_DIR/loudy_tasks.json"
LAST_FILE="$WORKSPACE_DIR/loudy_last.json"

# 获取技能目录（支持工作区安装和系统安装）
SKILL_DIR="${OPENCLAW_SKILL_DIR:-$(dirname "$(dirname "$0")")}"
if [ -f "$SKILL_DIR/scripts/check_tasks.py" ]; then
    CHECK_SCRIPT="$SKILL_DIR/scripts/check_tasks.py"
elif [ -f "/usr/lib/node_modules/openclaw/skills/loudy-ai-auto-task/scripts/check_tasks.py" ]; then
    CHECK_SCRIPT="/usr/lib/node_modules/openclaw/skills/loudy-ai-auto-task/scripts/check_tasks.py"
else
    echo "Error: check_tasks.py not found"
    exit 1
fi

# 获取当前奖池
python3 "$CHECK_SCRIPT" > "$LOG_FILE"

# 比较是否有新任务
if [ -f "$LAST_FILE" ]; then
    if diff -q "$LOG_FILE" "$LAST_FILE" > /dev/null 2>&1; then
        # 没有变化
        exit 0
    fi
fi

# 有新任务或首次运行，保存并标记需要通知
cp "$LOG_FILE" "$LAST_FILE"
echo "NEW_TASKS" > "$WORKSPACE_DIR/loudy_has_new.txt"
