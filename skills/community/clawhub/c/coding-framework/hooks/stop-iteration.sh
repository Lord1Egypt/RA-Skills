#!/bin/bash
# stop-iteration.sh — 迭代循环 Stop Hook
# 借鉴 Claude Code Ralph Wiggum 的 Stop Hook 自引用循环模式
#
# 在会话结束前检查是否有未完成的迭代承诺。
# 如果存在 <promise> 标签且未完成，阻止停止并返回提示。
#
# v10.2 改进:
#   - 与 loop-controller 集成：自动调用 cleanup 或 rollback
#   - 支持 auto-rollback：如果配置了 auto-commit，回滚到最近的安全点
#
# 从 stdin 读取 JSON Stop 事件数据：
# {
#   "session": "session-id",
#   "reason": "user_request|timeout|complete",
#   "summary": "会话摘要"
# }

set -euo pipefail

EVENT_DATA=$(cat)

# 提取字段
if command -v jq &>/dev/null; then
    SESSION=$(echo "$EVENT_DATA" | jq -r '.session // "unknown"')
    REASON=$(echo "$EVENT_DATA" | jq -r '.reason // "unknown"')
    SUMMARY=$(echo "$EVENT_DATA" | jq -r '.summary // ""')
else
    SESSION=$(echo "$EVENT_DATA" | grep -o '"session"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*: *"//;s/"$//')
    REASON=$(echo "$EVENT_DATA" | grep -o '"reason"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*: *"//;s/"$//')
    SUMMARY=""
fi

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date +"%Y-%m-%dT%H:%M:%SZ")

# ─── 检查迭代循环状态 ────────────────────────────────────────────────────
WORKSPACE="${OPENCLAW_WORKSPACE:-.}"
STATE_FILE="$WORKSPACE/loop-state.json"
PROMISE_FILE="$WORKSPACE/.pending-promises"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../scripts" && pwd)"

SHOULD_STOP=true
MESSAGE="会话可以安全停止"
PENDING_TASKS=()
ACTIONS_TAKEN=()

# 检查是否有活跃的迭代循环
if [[ -f "$STATE_FILE" ]]; then
    if command -v jq &>/dev/null; then
        LOOP_STATUS=$(jq -r '.status // "unknown"' "$STATE_FILE" 2>/dev/null || echo "unknown")
        LOOP_ITER=$(jq -r '.current_iteration // 0' "$STATE_FILE" 2>/dev/null || echo "0")
        LOOP_MAX=$(jq -r '.max_iterations // 0' "$STATE_FILE" 2>/dev/null || echo "0")
        LOOP_NAME=$(jq -r '.name // "unknown"' "$STATE_FILE" 2>/dev/null || echo "unknown")
        LOOP_AUTO_COMMIT=$(jq -r '.auto_commit // false' "$STATE_FILE" 2>/dev/null || echo "false")
    else
        LOOP_STATUS=$(grep -o '"status"[[:space:]]*:[[:space:]]*"[^"]*"' "$STATE_FILE" | head -1 | sed 's/.*: *"//;s/"$//')
        LOOP_ITER=0
        LOOP_MAX=0
        LOOP_NAME="unknown"
        LOOP_AUTO_COMMIT="false"
    fi

    if [[ "$LOOP_STATUS" == "running" ]]; then
        # v10.2: 根据停止原因采取不同行动
        case "$REASON" in
            "complete")
                # 正常完成，清理状态
                if [[ -f "$SCRIPT_DIR/loop-controller.py" ]]; then
                    python "$SCRIPT_DIR/loop-controller.py" cleanup --state "$STATE_FILE" --force 2>/dev/null || true
                    ACTIONS_TAKEN+=("cleanup:loop-complete")
                fi
                ;;
            "timeout")
                # 超时停止
                if [[ "$LOOP_AUTO_COMMIT" == "true" ]]; then
                    # 有 auto-commit，回滚到上一次迭代
                    if [[ -f "$SCRIPT_DIR/loop-controller.py" ]]; then
                        python "$SCRIPT_DIR/loop-controller.py" rollback --name "$LOOP_NAME" --prev --state "$STATE_FILE" 2>/dev/null || true
                        ACTIONS_TAKEN+=("rollback:timeout-recovery")
                    fi
                else
                    # 没有 auto-commit，仅标记状态
                    SHOULD_STOP=false
                    MESSAGE="迭代循环 '$LOOP_NAME' 因超时停止 (迭代 $LOOP_ITER/$LOOP_MAX)，建议手动检查"
                    PENDING_TASKS+=("loop:$LOOP_NAME:timeout")
                fi
                ;;
            *)
                # 用户主动停止或其他原因
                SHOULD_STOP=false
                MESSAGE="迭代循环 '$LOOP_NAME' 仍在运行 (迭代 $LOOP_ITER/$LOOP_MAX)，请先完成或取消循环"
                PENDING_TASKS+=("loop:$LOOP_NAME")
                ;;
        esac
    fi
fi

# 检查是否有待完成的承诺
if [[ -f "$PROMISE_FILE" ]]; then
    while IFS= read -r promise; do
        if [[ -n "$promise" ]]; then
            SHOULD_STOP=false
            MESSAGE="存在未完成的承诺: $promise"
            PENDING_TASKS+=("promise:$promise")
        fi
    done < "$PROMISE_FILE"
fi

# ─── 记录停止事件 ────────────────────────────────────────────────────────
LOG_DIR="$WORKSPACE/memory"
mkdir -p "$LOG_DIR" 2>/dev/null || true
echo "[$TIMESTAMP] [Stop] session=$SESSION reason=$REASON should_stop=$SHOULD_STOP tasks=${#PENDING_TASKS[@]} actions=${#ACTIONS_TAKEN[@]}" >> "$LOG_DIR/hook-audit.log" 2>/dev/null || true

# ─── 构建输出 ────────────────────────────────────────────────────────────
TASKS_JSON="["
for i in "${!PENDING_TASKS[@]}"; do
    if [[ $i -gt 0 ]]; then TASKS_JSON+=","; fi
    TASKS_JSON+="\"${PENDING_TASKS[$i]}\""
done
TASKS_JSON+="]"

ACTIONS_JSON="["
for i in "${!ACTIONS_TAKEN[@]}"; do
    if [[ $i -gt 0 ]]; then ACTIONS_JSON+=","; fi
    ACTIONS_JSON+="\"${ACTIONS_TAKEN[$i]}\""
done
ACTIONS_JSON+="]"

if $SHOULD_STOP; then
    DECISION="allow"
else
    DECISION="block"
fi

cat <<EOF
{
  "decision": "$DECISION",
  "message": "$MESSAGE",
  "should_stop": $SHOULD_STOP,
  "pending_tasks": $TASKS_JSON,
  "actions_taken": $ACTIONS_JSON,
  "matched_rules": [],
  "timestamp": "$TIMESTAMP"
}
EOF
