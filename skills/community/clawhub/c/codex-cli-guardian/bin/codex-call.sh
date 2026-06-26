#!/bin/bash
# codex-call.sh — 带 API Key 注入的 Codex exec 封装（后台模式 + PTY）
# 用法: bash codex-call.sh "<任务描述>"
# 输出: {"task_id":"...","pid":...}
#
# 支持 -o 输出文件，summary 更干净
# 注意：Codex exec 不支持 session 持久化，每次独立 session

set -e

# 注意：init-setup.sh 里有交互式 read，set -e 下 read 返回 1 会导致脚本退出
# 所以 trigger_init_setup 里用 || true 包裹 init-setup 调用

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CRED_FILE="$SKILL_DIR/credentials.env"
STATE_DIR="$SKILL_DIR/state"
TASKS_DIR="$STATE_DIR/tasks"
LOCK_FILE="$STATE_DIR/codex.lock"
WORKDIR="$(dirname "$(dirname "$SKILL_DIR")")/tmp/codex"

mkdir -p "$STATE_DIR" "$TASKS_DIR" "$WORKDIR"

# 触发 init-setup 并重新加载 Key
trigger_init_setup() {
    echo "🔄 触发设置向导..."
    echo ""
    bash "$SKILL_DIR/scripts/init-setup.sh" || true
    source "$CRED_FILE"
    OPENAI_API_KEY_0011AI="${OPENAI_API_KEY_0011AI//$'\r'}"
}

# 加载 Key
# - 文件不存在 → 触发 init-setup
# - 文件存在 → 直接使用，不检查 KEY 是否为空
load_key() {
    if [[ ! -f "$CRED_FILE" ]]; then
        trigger_init_setup
    else
        source "$CRED_FILE"
        OPENAI_API_KEY_0011AI="${OPENAI_API_KEY_0011AI//$'\r'}"
    fi
}

generate_task_id() {
    local date_prefix
    date_prefix=$(date +%Y%m%d)
    local count
    count=$(python3 -c "
import os, glob
prefix = '$date_prefix'
files = glob.glob('$TASKS_DIR/task-' + prefix + '-*.json')
print(len(files))
" 2>/dev/null) || count=0
    printf "%s-%03d" "$date_prefix" $((count + 1))
}

check_lock() {
    if [[ -f "$LOCK_FILE" ]]; then
        local pid
        pid=$(cat "$LOCK_FILE" 2>/dev/null)
        if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
            echo "⚠️ Codex 忙碌中，请稍后再试"
            exit 1
        else
            rm -f "$LOCK_FILE"
        fi
    fi
}

if [[ $# -eq 0 ]] || [[ "$1" == "--help" ]]; then
    echo "用法: bash codex-call.sh \"任务描述\""
    exit 1
fi

TASK="$1"
load_key
check_lock

cd "$WORKDIR"
git init -q 2>/dev/null || true

TASK_ID=$(generate_task_id)

(
    STARTED_AT=$(date -u +%Y-%m-%dT%H:%M:%S+08:00)
    SUMMARY_FILE="/tmp/codex-summary-${TASK_ID}.txt"

    cat > "$STATE_DIR/current-task.json" <<EOF
{
  "task_id": "$TASK_ID",
  "description": "$TASK",
  "status": "running",
  "started_at": "$STARTED_AT",
  "max_duration_minutes": 30
}
EOF

    # 用 Python shlex.quote() 安全转义，防止 $, `, \, " 等破坏 bash 命令
    TASK_SAFE=$(python3 -c "
import sys, shlex
print(shlex.quote(sys.argv[1]))
" "$TASK")
    CODEX_CMD="script -q /dev/null env OPENAI_API_KEY_0011AI=\"$OPENAI_API_KEY_0011AI\" codex --full-auto exec --cd \"$WORKDIR\" -o \"$SUMMARY_FILE\" \"$TASK_SAFE\""

    bash -c "$CODEX_CMD" >/dev/null 2>&1 || EXIT_CODE=$?

    if [[ -f "$SUMMARY_FILE" ]] && [[ -s "$SUMMARY_FILE" ]]; then
        SUMMARY=$(cat "$SUMMARY_FILE" | sed 's/"/\\"/g' | tr '\n' ' ' | cut -c1-300)
        rm -f "$SUMMARY_FILE"
    else
        SUMMARY="任务执行完毕"
    fi

    if [[ ${EXIT_CODE:-0} -eq 0 ]]; then
        STATUS="done"
    else
        STATUS="failed"
    fi

    cat > "$TASKS_DIR/task-${TASK_ID}.json" <<EOF
{
  "task_id": "$TASK_ID",
  "description": "$TASK",
  "status": "$STATUS",
  "summary": "$SUMMARY",
  "started_at": "$STARTED_AT",
  "finished_at": "$(date -u +%Y-%m-%dT%H:%M:%S+08:00)"
}
EOF

    rm -f "$STATE_DIR/current-task.json"

) &

PID=$!
echo "$PID" > "$LOCK_FILE"
echo "{\"task_id\":\"$TASK_ID\",\"pid\":$PID}"
