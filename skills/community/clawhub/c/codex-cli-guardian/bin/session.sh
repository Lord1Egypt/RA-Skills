#!/bin/bash
# session.sh — Codex Guardian 状态管理
# 用法: bash bin/session.sh [status|list|kill]

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STATE_DIR="$SKILL_DIR/state"
TASKS_DIR="$STATE_DIR/tasks"

show_status() {
    local current_task="$STATE_DIR/current-task.json"
    local lock_file="$STATE_DIR/codex.lock"

    # 检查是否在运行
    RUNNING_PID=""
    if [[ -f "$lock_file" ]]; then
        local pid
        pid=$(cat "$lock_file" 2>/dev/null)
        if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
            RUNNING_PID="$pid"
        fi
    fi

    if [[ -n "$RUNNING_PID" ]] && [[ -f "$current_task" ]]; then
        # 任务运行中 — 用 Python 统一解析 JSON + 计算时长
        STATUS_INFO=$(python3 -c "
import json, datetime, sys, os

task_file = '$current_task'
with open(task_file) as f:
    d = json.load(f)

task_id = d.get('task_id', '')
desc = d.get('description', '')[:40]
started_at = d.get('started_at', '')
max_duration = d.get('max_duration_minutes', 30)

elapsed_minutes = 0
if started_at:
    try:
        t = datetime.datetime.fromisoformat(started_at.replace('+08:00', '+08:00'))
        now = datetime.datetime.now()
        elapsed_minutes = int((now - t).total_seconds() // 60)
    except:
        elapsed_minutes = 0

task_count = len([f for f in os.listdir('$TASKS_DIR') if f.startswith('task-') and f.endswith('.json')])

print(f'{task_id}|{desc}|{elapsed_minutes}|{max_duration}|{task_count}')
" 2>/dev/null) || STATUS_INFO="||||"

        IFS='|' read -r task_id desc elapsed_minutes max_duration task_count <<< "$STATUS_INFO"

        local elapsed_display="${elapsed_minutes} 分钟"
        local timeout_warning=""
        if (( elapsed_minutes >= max_duration )); then
            timeout_warning=" ⚠️ 已超时 ${max_duration} 分钟，请决定是否终止"
        elif (( elapsed_minutes >= max_duration - 5 )); then
            timeout_warning=" ⚠️ 即将超时（${elapsed_minutes}/${max_duration} 分钟）"
        fi

        echo "=== Codex Guardian 状态 ==="
        echo "任务状态   : running"
        echo "当前任务   : [$task_id] $desc"
        echo "运行时长   : ${elapsed_display} / ${max_duration} 分钟${timeout_warning}"
        echo "PID        : $RUNNING_PID"
        echo "累计任务   : ${task_count:-0}"
        echo ""
        echo "如需终止任务，请说：「终止任务」"
    else
        # idle 状态 — 用 Python 计算最后使用时间
        LAST_DISPLAY=$(python3 -c "
import json, datetime, os

tasks_dir = '$TASKS_DIR'
files = sorted([f for f in os.listdir(tasks_dir) if f.startswith('task-') and f.endswith('.json')], reverse=True)
if not files:
    print('无任务记录')
else:
    last_file = os.path.join(tasks_dir, files[0])
    with open(last_file) as f:
        d = json.load(f)
    t_str = d.get('finished_at', '')
    if not t_str:
        print('无任务记录')
    else:
        try:
            t = datetime.datetime.fromisoformat(t_str.replace('+08:00', '+08:00'))
            now = datetime.datetime.now()
            diff = (now - t).total_seconds()
            if diff < 60:
                print(f'{int(diff)} 秒前')
            elif diff < 3600:
                print(f'{int(diff // 60)} 分钟前')
            else:
                print(f'{int(diff // 3600)} 小时前')
        except:
            print('未知')
" 2>/dev/null) || LAST_DISPLAY="无任务记录"

        TASK_COUNT=$(python3 -c "
import os
print(len([f for f in os.listdir('$TASKS_DIR') if f.startswith('task-') and f.endswith('.json')]))
" 2>/dev/null) || TASK_COUNT=0

        echo "=== Codex Guardian 状态 ==="
        echo "任务状态   : idle"
        echo "累计任务   : ${TASK_COUNT}"
        echo "最后使用   : $LAST_DISPLAY"
        echo "当前任务   : 无"
    fi
}

case "${1:-}" in
    status)
        show_status
        ;;

    list)
        if [[ ! -d "$TASKS_DIR" ]] || [[ -z "$(ls "$TASKS_DIR"/task-*.json 2>/dev/null)" ]]; then
            echo "📋 暂无任务记录"
        else
            echo "📋 最近任务："
            ls -t "$TASKS_DIR"/task-*.json 2>/dev/null | head -10 | while IFS= read -r f; do
                python3 -c "
import json, sys, os
f = sys.argv[1]
try:
    with open(f) as fp:
        d = json.load(fp)
    tid = d.get('task_id', '')
    desc = d.get('description', '')[:30]
    status = d.get('status', '')
    print(f'  [{tid}] {desc}... — {status}')
except:
    print(f'  {os.path.basename(f)}')
" "$f"
            done
        fi
        ;;

    kill)
        local lock_file="$STATE_DIR/codex.lock"
        if [[ -f "$lock_file" ]]; then
            local pid
            pid=$(cat "$lock_file" 2>/dev/null)
            if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
                kill "$pid" 2>/dev/null && echo "✅ 已发送 SIGTERM 终止任务 (PID: $pid)" || echo "❌ 终止失败"
            else
                echo "ℹ️  没有运行中的任务"
            fi
        else
            echo "ℹ️  没有运行中的任务"
        fi
        rm -f "$lock_file" "$STATE_DIR/current-task.json"
        ;;

    reset)
        rm -f "$STATE_DIR/current-task.json" "$STATE_DIR/codex.lock"
        echo "✅ 状态已重置"
        ;;

    help|--help|-h)
        echo "用法: bash bin/session.sh [status|list|kill|reset]"
        echo ""
        echo "  status  — 健康检查（默认）"
        echo "  list    — 列出最近任务"
        echo "  kill    — 终止当前运行中的任务"
        echo "  reset   — 重置当前状态（不清历史）"
        ;;

    *)
        show_status
        ;;
esac
