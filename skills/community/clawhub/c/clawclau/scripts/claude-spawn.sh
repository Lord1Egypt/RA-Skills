#!/usr/bin/env bash
# claude-spawn.sh — 派发 Claude Code 任务（tmux + claude -p）
#
# 用法: claude-spawn.sh [OPTIONS] <task-id> "<prompt>" [workdir]
#
# 选项:
#   --steerable        交互式模式，支持 claude-steer.sh 中途纠偏
#   --timeout <sec>    超时秒数 (默认: 600)
#   --interval <sec>   进度汇报间隔，0=关闭 (默认: 180)
#   --max-retries <n>  最大重试次数 (默认: 3)
#   --model <name>     Claude 模型名称
#   --parent <id>      父任务 ID（重试时由 claude-spawn.sh 传入）
#   --retry-count <n>  当前重试次数（内部使用）
#
# 完成后自动通过 openclaw system event 通知小八

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/clawclau-lib.sh"

# ── 默认值 ─────────────────────────────────────────────────────────────────
STEERABLE=false
TIMEOUT=600
INTERVAL=180
MAX_RETRIES=3
MODEL=""
PARENT_TASK_ID=""
RETRY_COUNT=0

# ── 参数解析 ───────────────────────────────────────────────────────────────
POSITIONAL=()
while [[ $# -gt 0 ]]; do
    case "$1" in
        --steerable)    STEERABLE=true;       shift   ;;
        --timeout)      TIMEOUT="$2";         shift 2 ;;
        --interval)     INTERVAL="$2";        shift 2 ;;
        --max-retries)  MAX_RETRIES="$2";     shift 2 ;;
        --model)        MODEL="$2";           shift 2 ;;
        --parent)       PARENT_TASK_ID="$2";  shift 2 ;;
        --retry-count)  RETRY_COUNT="$2";     shift 2 ;;
        --)             shift; break ;;
        -*) echo "ERROR: 未知参数: $1" >&2; exit 1 ;;
        *)  POSITIONAL+=("$1"); shift ;;
    esac
done
set -- "${POSITIONAL[@]+"${POSITIONAL[@]}"}"

if [[ $# -lt 2 ]]; then
    echo "Usage: claude-spawn.sh [OPTIONS] <task-id> \"<prompt>\" [workdir]" >&2
    exit 1
fi

TASK_ID="$1"
PROMPT="$2"
WORKDIR="${3:-$(pwd)}"

# ── 验证 ───────────────────────────────────────────────────────────────────
cc_validate_task_id "$TASK_ID"
cc_require tmux jq claude

if ! [[ "$TIMEOUT" =~ ^[0-9]+$ ]] || [[ "$TIMEOUT" -lt 1 ]]; then
    echo "ERROR: --timeout 必须是正整数" >&2; exit 1
fi
if ! [[ "$INTERVAL" =~ ^[0-9]+$ ]]; then
    echo "ERROR: --interval 必须是非负整数" >&2; exit 1
fi
if ! [[ -d "$WORKDIR" ]]; then
    echo "ERROR: 工作目录不存在: $WORKDIR" >&2; exit 1
fi

# ── 初始化 ─────────────────────────────────────────────────────────────────
cc_init

if $STEERABLE; then
    LOG_EXT="txt"
else
    LOG_EXT="json"
fi

LOG_FILE="$CC_LOG_DIR/${TASK_ID}.${LOG_EXT}"
PROMPT_FILE="$CC_PROMPT_DIR/${TASK_ID}.txt"
WRAPPER_FILE="$CC_PROMPT_DIR/${TASK_ID}-wrapper.sh"
TMUX_SESSION=$(cc_tmux_session "$TASK_ID")

# ── 冲突检查 ───────────────────────────────────────────────────────────────
if cc_task_exists "$TASK_ID"; then
    echo "ERROR: 任务 '$TASK_ID' 已在注册表中。请换个 ID 或先 kill。" >&2
    exit 1
fi
if tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
    echo "ERROR: tmux session '$TMUX_SESSION' 已存在" >&2
    exit 1
fi

# ── 写 prompt 文件 ─────────────────────────────────────────────────────────
printf '%s' "$PROMPT" > "$PROMPT_FILE"

# ── 辅助：轮询等待 tmux pane 就绪 ─────────────────────────────────────────
# 阶段 1 等 pane 创建完成，阶段 2 等 pane 出现可见内容（进程已启动）。
# 替代硬编码 sleep，确定性更强，超时后仍继续（已尽力等待）。
# @param $1 session   tmux session 名
# @param $2 max_tries 最大轮询次数（每次 0.1s，默认 50 次 = 最多等 5s）
_wait_tmux_ready() {
    local session="$1"
    local max_tries="${2:-50}"
    local i=0
    # 阶段 1：等 pane 存在
    until tmux list-panes -t "$session" >/dev/null 2>&1; do
        [[ $i -ge $max_tries ]] && return 0
        sleep 0.1
        (( i++ )) || true
    done
    # 阶段 2：等 pane 出现可见内容（进程已就绪）
    i=0
    local content
    until content=$(tmux capture-pane -t "$session" -p 2>/dev/null) \
          && [[ -n "${content//[[:space:]]/}" ]]; do
        [[ $i -ge $max_tries ]] && return 0
        sleep 0.1
        (( i++ )) || true
    done
}

# ── 函数：构建 wrapper 脚本 ────────────────────────────────────────────────
build_wrapper() {
    if ! $STEERABLE; then
        # Print 模式：stream-json 实时写入日志，无交互
        cat > "$WRAPPER_FILE" << 'WRAPPER_EOF'
#!/usr/bin/env bash
# Args: $1=PROMPT_FILE $2=WORKDIR $3=LOG_FILE [$4=MODEL]
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
cd "$2"
MODEL_FLAG=()
[[ -n "${4:-}" ]] && MODEL_FLAG=(--model "$4")
exec claude -p --dangerously-skip-permissions \
    --verbose --output-format stream-json \
    "${MODEL_FLAG[@]}" \
    "$(cat "$1")" > "$3" 2>&1
WRAPPER_EOF
    else
        # Steerable 模式：交互式，tmux pipe-pane 捕获输出到日志
        cat > "$WRAPPER_FILE" << 'WRAPPER_EOF'
#!/usr/bin/env bash
# Args: $1=WORKDIR [$2=MODEL]
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
cd "$1"
MODEL_FLAG=()
[[ -n "${2:-}" ]] && MODEL_FLAG=(--model "$2")
exec claude --dangerously-skip-permissions "${MODEL_FLAG[@]}"
WRAPPER_EOF
    fi
    chmod +x "$WRAPPER_FILE"
}

# ── 函数：启动 tmux session 并注入 prompt ──────────────────────────────────
start_session() {
    if ! $STEERABLE; then
        # Print 模式：wrapper 直接写日志
        tmux new-session -d -s "$TMUX_SESSION" -c "$WORKDIR" \
            "bash -l $WRAPPER_FILE $PROMPT_FILE $WORKDIR $LOG_FILE ${MODEL:-}"
    else
        # Steerable 模式：先启动交互式 claude，等就绪后挂载日志采集，再注入 prompt
        tmux new-session -d -s "$TMUX_SESSION" -c "$WORKDIR" \
            "bash -l $WRAPPER_FILE $WORKDIR ${MODEL:-}"
        _wait_tmux_ready "$TMUX_SESSION"          # 替代 sleep 0.5：等 pane 及进程就绪
        # pipe-pane 将 tmux 输出追加到日志文件
        tmux pipe-pane -t "$TMUX_SESSION" "cat >> $LOG_FILE"
        _wait_tmux_ready "$TMUX_SESSION" 30       # 替代 sleep 0.3：确认 claude 已可接收输入
        # 使用 load-buffer + paste-buffer 注入 prompt（正确处理特殊字符）
        tmux load-buffer -b "prompt-$TASK_ID" "$PROMPT_FILE"
        tmux paste-buffer -t "$TMUX_SESSION" -b "prompt-$TASK_ID" -p
        tmux send-keys -t "$TMUX_SESSION" "" Enter
    fi
}

# ── 函数：启动后台完成检测器和进度汇报器 ──────────────────────────────────
launch_monitors() {
    local _LIB="$SCRIPT_DIR/clawclau-lib.sh"

    # 完成检测器 + 超时守卫
    # 双重 fork：外层子 shell 立即退出，内层被 launchd 接管，脱离 exec 进程树
    (
    (
        set +e
        source "$_LIB"
        export PATH="/opt/homebrew/bin:/usr/local/bin:$HOME/.openclaw/bin:$PATH"
        _TASK_ID="$TASK_ID"
        _SESSION="$TMUX_SESSION"
        _LOG="$LOG_FILE"
        _TIMEOUT="$TIMEOUT"
        _START_MS="$NOW_MS"

        # 每 10s 轮询一次 tmux session 状态（确定性检查，不消耗 token）
        while tmux has-session -t "$_SESSION" 2>/dev/null; do
            _NOW=$(date +%s000)
            _ELAPSED=$(( (_NOW - _START_MS) / 1000 ))
            if [[ "$_ELAPSED" -gt "$_TIMEOUT" ]]; then
                # 超时：强制终止
                tmux kill-session -t "$_SESSION" 2>/dev/null || true
                sleep 2
                cc_task_update "$_TASK_ID" \
                    "{\"status\":\"timeout\",\"completedAt\":$_NOW}"
                cc_notify "任务 $_TASK_ID 超时（${_TIMEOUT}s），已终止"
                exit 0
            fi
            sleep 10
        done

        sleep 2  # 等待日志写入完成

        _NOW=$(date +%s000)
        _STATUS="failed"
        [[ -s "$_LOG" ]] && _STATUS="done"

        cc_task_update "$_TASK_ID" \
            "{\"status\":\"$_STATUS\",\"completedAt\":$_NOW}"

        # 提取结果摘要并通知小八
        _SNIPPET=$(cc_extract_text "$_LOG" 300)
        if [[ "$_STATUS" == "done" ]]; then
            _MSG="[完成] 任务 $_TASK_ID"
            [[ -n "$_SNIPPET" ]] && _MSG+=$'\n'"摘要: ${_SNIPPET:0:200}"
        else
            _MSG="[失败] 任务 $_TASK_ID（日志为空，请检查错误）"
        fi
        cc_notify "$_MSG"
    ) &
    ) &
    disown

    # 进度汇报器（双重 fork，仅在 INTERVAL > 0 时启动）
    if [[ "$INTERVAL" -gt 0 ]]; then
    (
    (
        set +e
        source "$_LIB"
        export PATH="/opt/homebrew/bin:/usr/local/bin:$HOME/.openclaw/bin:$PATH"
        _TASK_ID="$TASK_ID"
        _SESSION="$TMUX_SESSION"
        _LOG="$LOG_FILE"
        _INTERVAL="$INTERVAL"
        _START_MS="$NOW_MS"
        _LAST_BYTES=0

        while true; do
            sleep "$_INTERVAL"
            # session 已结束则退出，不再发通知
            tmux has-session -t "$_SESSION" 2>/dev/null || break
            [[ -f "$_LOG" ]] || continue

            _CURRENT_BYTES=$(wc -c < "$_LOG" 2>/dev/null | tr -d ' ' || echo 0)
            [[ "$_CURRENT_BYTES" -le "$_LAST_BYTES" ]] && continue
            _LAST_BYTES=$_CURRENT_BYTES

            _SNIPPET=$(cc_extract_text "$_LOG" 200)
            [[ -z "$_SNIPPET" ]] && continue

            _NOW_MS=$(date +%s000)
            _ELAPSED=$(( (_NOW_MS - _START_MS) / 1000 ))
            if [[ $_ELAPSED -lt 60 ]]; then
                _TIME_STR="${_ELAPSED}秒"
            else
                _TIME_STR="$((_ELAPSED / 60))分钟"
            fi

            _MSG="[进度] 任务 $_TASK_ID（已运行 $_TIME_STR）"
            _MSG+=$'\n'"${_SNIPPET}"
            cc_notify "$_MSG"
        done
    ) &
    ) &
    disown
    fi
}

# ── 主流程 ─────────────────────────────────────────────────────────────────

# 构建 wrapper 脚本
build_wrapper

# 启动 tmux session（steerable 模式含 prompt 注入）
start_session

# 验证 session 启动
sleep 1
if ! tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
    echo "ERROR: tmux session '$TMUX_SESSION' 启动失败" >&2
    if [[ -s "$LOG_FILE" ]]; then
        echo "日志尾部:" >&2
        tail -5 "$LOG_FILE" >&2
    fi
    exit 1
fi

# 注册任务
NOW_MS=$(cc_now_ms)
TASK_JSON=$(jq -n \
    --arg id           "$TASK_ID" \
    --arg mode         "$(if $STEERABLE; then echo steerable; else echo print; fi)" \
    --arg session      "$TMUX_SESSION" \
    --arg prompt       "$PROMPT" \
    --arg workdir      "$WORKDIR" \
    --arg log          "$LOG_FILE" \
    --arg model        "$MODEL" \
    --argjson startTs  "$NOW_MS" \
    --argjson timeout  "$TIMEOUT" \
    --argjson interval "$INTERVAL" \
    --argjson maxR     "$MAX_RETRIES" \
    --argjson retryC   "$RETRY_COUNT" \
    --arg parent       "$PARENT_TASK_ID" \
    '{
        id:           $id,
        mode:         $mode,
        tmuxSession:  $session,
        prompt:       $prompt,
        workdir:      $workdir,
        log:          $log,
        model:        $model,
        startedAt:    $startTs,
        timeout:      $timeout,
        interval:     $interval,
        status:       "running",
        completedAt:  null,
        maxRetries:   $maxR,
        retryCount:   $retryC,
        parentTaskId: (if $parent != "" then $parent else null end),
        steerLog:     []
    }')

cc_task_register "$TASK_JSON"

# 启动后台完成检测器和进度汇报器
launch_monitors

# ── 输出确认 ───────────────────────────────────────────────────────────────
MODE_STR="print (stream-json)"
$STEERABLE && MODE_STR="steerable (interactive)"

echo "已派发: $TASK_ID"
echo "  模式:     $MODE_STR"
echo "  Session:  $TMUX_SESSION"
echo "  工作目录: $WORKDIR"
echo "  日志:     $LOG_FILE"
echo "  超时:     ${TIMEOUT}s  最大重试: $MAX_RETRIES"
[[ "$INTERVAL" -gt 0 ]] && echo "  进度汇报: 每 ${INTERVAL}s"
[[ -n "$PARENT_TASK_ID" ]] && echo "  父任务:   $PARENT_TASK_ID (retry #$RETRY_COUNT)"
