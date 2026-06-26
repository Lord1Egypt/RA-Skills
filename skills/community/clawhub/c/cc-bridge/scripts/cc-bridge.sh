#!/usr/bin/env bash
# cc-bridge.sh — OpenClaw ↔ Claude Code CLI 桥接脚本
#
# Usage:
#   cc-bridge.sh <session_id> start                    # 启动新 CC 会话
#   cc-bridge.sh <session_id> send "<message>"         # 发送消息并等待回复
#   cc-bridge.sh <session_id> send "<message>" --long   # 长任务模式 (5分钟超时)
#   cc-bridge.sh <session_id> approve [1|2|3|y|n]      # 回应 CC 的审批提示
#   cc-bridge.sh <session_id> stop                     # 关闭会话
#   cc-bridge.sh <session_id> restart                  # 重启会话
#   cc-bridge.sh <session_id> status                   # 查看状态
#   cc-bridge.sh <session_id> peek                     # 查看当前屏幕内容
#   cc-bridge.sh <session_id> history [N]              # 查看最近 N 行滚动缓冲区
#   cc-bridge.sh <session_id> interrupt                # 发送 Ctrl+C 中断当前操作
#   cc-bridge.sh <session_id> key "<key>"              # 发送特殊按键 (Escape/Up/Down/Tab)

set -euo pipefail

SESSION_ID="${1:?[cc-bridge] 缺少 session_id 参数}"
ACTION="${2:?[cc-bridge] 缺少 action 参数 (start|send|approve|stop|restart|status|peek|history)}"
MESSAGE="${3:-}"
FLAG="${4:-}"

# ── 常量 ─────────────────────────────────────────────────────────────────────
CLAUDE_BIN="${CLAUDE_BIN:-$HOME/.local/bin/claude}"
STATE_DIR="$HOME/.openclaw/cc-bridge"
SCROLLBACK_LINES=50000           # tmux 滚动缓冲区大小
STABLE_INTERVAL=0.8              # 轮询间隔(秒)
STABLE_NEEDED=3                  # 连续稳定次数
DEFAULT_TIMEOUT=90               # 默认最长等待(秒)
LONG_TIMEOUT=300                 # 长任务最长等待(秒)
mkdir -p "$STATE_DIR"

# 清理可能残留的 stale tmux socket（macOS 常见问题）
_tmux_socket="/private/tmp/tmux-$(id -u)/default"
if [[ -S "$_tmux_socket" ]] && ! tmux list-sessions &>/dev/null; then
    rm -f "$_tmux_socket"
fi

# 把任意 session_id 变成合法 tmux 名（字母数字下划线，<=20字符）
SAFE_ID="$(echo "$SESSION_ID" | tr -cd '[:alnum:]_' | cut -c1-20)"
TMUX_NAME="ccb_${SAFE_ID}"
LOG_FILE="$STATE_DIR/${TMUX_NAME}.log"
OFFSET_FILE="$STATE_DIR/${TMUX_NAME}.offset"

# ── 工具函数 ──────────────────────────────────────────────────────────────────

is_running() {
    tmux has-session -t "$TMUX_NAME" 2>/dev/null
}

current_log_size() {
    wc -c < "$LOG_FILE" 2>/dev/null | tr -d ' ' || echo 0
}

capture_full() {
    # 抓取完整滚动缓冲区（不只是可见区域），-S - 表示从头开始
    tmux capture-pane -t "$TMUX_NAME" -p -S - 2>/dev/null || true
}

capture_clean() {
    # 抓取并清理：去掉装饰性行，保留实际内容
    capture_full \
        | grep -v '^[─━═─▪]\{3,\}' \
        | grep -v '^\s*[?]\s*for\s*shortcuts' \
        | grep -v '^\s*esc\s*to\s*\(interrupt\|cancel\)' \
        | grep -v '^\s*Tab\s*to\s*amend' \
        | grep -v '^\s*ctrl+e\s*to\s*explain' \
        | grep -v '^[[:space:]]*$' \
        || true
}

read_new_output() {
    # 使用行号偏移（而非 sort+comm）保持输出顺序
    local offset=0
    [[ -f "$OFFSET_FILE" ]] && offset=$(cat "$OFFSET_FILE")

    local full
    full=$(capture_clean)
    local total_lines
    total_lines=$(echo "$full" | wc -l | tr -d ' ')

    if (( total_lines > offset )); then
        # 输出从 offset+1 行开始的新内容
        echo "$full" | tail -n "+$((offset + 1))" | head -500
        echo "$total_lines" > "$OFFSET_FILE"
    fi
}

save_current_offset() {
    local total
    total=$(capture_clean | wc -l | tr -d ' ')
    echo "$total" > "$OFFSET_FILE"
}

wait_for_stable_output() {
    # 轮询直到日志大小连续 N 次不再增长（CC 回复完毕）
    local max_wait="${1:-$DEFAULT_TIMEOUT}"

    local prev_size
    prev_size=$(current_log_size)
    local stable_count=0
    local iterations
    iterations=$(awk "BEGIN{printf \"%d\", $max_wait / $STABLE_INTERVAL}")

    local i
    for (( i=0; i<iterations; i++ )); do
        sleep "$STABLE_INTERVAL"
        local curr_size
        curr_size=$(current_log_size)

        if (( curr_size == prev_size )); then
            stable_count=$((stable_count + 1))
            if (( stable_count >= STABLE_NEEDED )); then
                break
            fi
        else
            stable_count=0
            prev_size="$curr_size"
        fi
    done
}

# ── 动作实现 ──────────────────────────────────────────────────────────────────

do_start() {
    if is_running; then
        echo "[cc-bridge] ⚠️  已有活跃会话 ($TMUX_NAME)，如需重开请先 stop 或 restart"
        return 0
    fi

    # 清理旧日志
    > "$LOG_FILE"
    echo "0" > "$OFFSET_FILE"

    echo "[cc-bridge] 🚀 正在启动 Claude Code..."

    # 构建启动命令：
    #   - unset CLAUDECODE/CLAUDE_CODE  防止 "nested session" 错误
    #   - export TERM                    保证 CC 可以正常渲染
    local launch_cmd
    launch_cmd="unset CLAUDECODE CLAUDE_CODE; export TERM=xterm-256color; exec '$CLAUDE_BIN'"

    # 在 tmux 中启动 claude
    #   - set history-limit 为大滚动缓冲区，确保长会话不丢内容
    tmux new-session -d -s "$TMUX_NAME" -x 220 -y 50 "bash --login -c '$launch_cmd'"
    tmux set-option -t "$TMUX_NAME" history-limit "$SCROLLBACK_LINES" 2>/dev/null || true
    sleep 0.5

    # 通过 pipe-pane 把所有输出追加到日志（用于 wait_for_stable_output 的 size 检测）
    tmux pipe-pane -t "$TMUX_NAME" -o "cat >> '$LOG_FILE'"

    # 等待 CC 初始化完成
    wait_for_stable_output 15

    # 记录初始偏移
    save_current_offset

    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "✅ Claude Code 会话已启动！"
    echo "📌 会话 ID: $SESSION_ID"
    echo "💬 现在发消息就会直接转发给 Claude Code"
    echo "🔧 CC 斜杠命令也可直接发送：/plan /model /compact 等"
    echo "🛑 发送「关闭cc」退出会话"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

do_send() {
    if ! is_running; then
        echo "[cc-bridge] ❌ 没有活跃的 CC 会话，请先发送「启动cc」"
        return 1
    fi

    if [[ -z "$MESSAGE" ]]; then
        echo "[cc-bridge] ⚠️  消息为空"
        return 1
    fi

    # 记录发送前的行偏移
    save_current_offset

    # 将消息注入 tmux pane（逐字发送避免特殊字符被 tmux 拦截）
    tmux send-keys -t "$TMUX_NAME" -l "$MESSAGE"
    tmux send-keys -t "$TMUX_NAME" Enter

    # 选择超时：--long 标志 → 5分钟，否则 90秒
    local timeout="$DEFAULT_TIMEOUT"
    if [[ "$FLAG" == "--long" ]]; then
        timeout="$LONG_TIMEOUT"
    fi

    # 等待 CC 响应完毕
    wait_for_stable_output "$timeout"

    # 返回新增的输出
    read_new_output
}

do_approve() {
    # 处理 CC 的 TUI 审批菜单（上下选择 + Enter 确认）
    if ! is_running; then
        echo "[cc-bridge] ❌ 没有活跃的 CC 会话"
        return 1
    fi

    save_current_offset

    local choice="${MESSAGE:-y}"

    case "$choice" in
        1|y|yes|是)
            # 选项 1 (Yes)：直接按 Enter（默认已选中第一项）
            tmux send-keys -t "$TMUX_NAME" Enter
            ;;
        2)
            # 选项 2：下移一行 → Enter
            tmux send-keys -t "$TMUX_NAME" Down
            sleep 0.2
            tmux send-keys -t "$TMUX_NAME" Enter
            ;;
        3|n|no|否)
            # 选项 3 (No)：下移两行 → Enter
            tmux send-keys -t "$TMUX_NAME" Down
            sleep 0.2
            tmux send-keys -t "$TMUX_NAME" Down
            sleep 0.2
            tmux send-keys -t "$TMUX_NAME" Enter
            ;;
        esc|cancel|取消)
            # 按 Escape 取消
            tmux send-keys -t "$TMUX_NAME" Escape
            ;;
        *)
            echo "[cc-bridge] ⚠️  未知审批选项: $choice"
            echo "可用: 1/y/yes/是, 2, 3/n/no/否, esc/cancel/取消"
            return 1
            ;;
    esac

    # 等待 CC 处理审批后的响应
    wait_for_stable_output "$DEFAULT_TIMEOUT"
    read_new_output
}

do_stop() {
    if is_running; then
        # 先尝试优雅退出
        tmux send-keys -t "$TMUX_NAME" "/exit" Enter 2>/dev/null || true
        sleep 2
        # 如果还在就强杀
        tmux kill-session -t "$TMUX_NAME" 2>/dev/null || true
    fi
    rm -f "$LOG_FILE" "$OFFSET_FILE"
    echo "✅ Claude Code 会话已关闭"
}

do_restart() {
    echo "[cc-bridge] 🔄 正在重启..."
    do_stop
    sleep 1
    do_start
}

do_status() {
    if is_running; then
        local log_size
        log_size=$(current_log_size)
        local scroll_lines
        scroll_lines=$(capture_full | wc -l | tr -d ' ')
        echo "✅ Claude Code 会话运行中"
        echo "   tmux 会话: $TMUX_NAME"
        echo "   滚动缓冲: ${scroll_lines} 行"
        echo "   日志大小: ${log_size} bytes"

        # 检测 CC 是否在等待审批
        local screen
        screen=$(capture_full | tail -20)
        if echo "$screen" | grep -q "Do you want to proceed"; then
            echo "   ⚠️  CC 正在等待审批！发送 approve 来回应"
        fi
    else
        echo "⭕ 没有活跃的 Claude Code 会话"
        echo "   发送「启动cc」开始使用"
    fi
}

do_peek() {
    if ! is_running; then
        echo "[cc-bridge] 没有活跃会话"
        return 1
    fi
    capture_full | tail -50
}

do_history() {
    if ! is_running; then
        echo "[cc-bridge] 没有活跃会话"
        return 1
    fi
    local lines="${MESSAGE:-100}"
    capture_clean | tail -n "$lines"
}

do_interrupt() {
    if ! is_running; then
        echo "[cc-bridge] 没有活跃会话"
        return 1
    fi
    save_current_offset
    tmux send-keys -t "$TMUX_NAME" C-c
    sleep 1
    read_new_output
    echo "[cc-bridge] ⚡ 已发送中断信号 (Ctrl+C)"
}

do_key() {
    # 发送特殊按键：Escape, Up, Down, Tab, Enter, Space 等
    if ! is_running; then
        echo "[cc-bridge] 没有活跃会话"
        return 1
    fi

    local key="${MESSAGE:-Enter}"
    save_current_offset

    case "$key" in
        esc|escape|Escape)      tmux send-keys -t "$TMUX_NAME" Escape ;;
        up|Up)                  tmux send-keys -t "$TMUX_NAME" Up ;;
        down|Down)              tmux send-keys -t "$TMUX_NAME" Down ;;
        left|Left)              tmux send-keys -t "$TMUX_NAME" Left ;;
        right|Right)            tmux send-keys -t "$TMUX_NAME" Right ;;
        tab|Tab)                tmux send-keys -t "$TMUX_NAME" Tab ;;
        shift+tab|Shift+Tab)    tmux send-keys -t "$TMUX_NAME" BTab ;;
        enter|Enter)            tmux send-keys -t "$TMUX_NAME" Enter ;;
        space|Space)            tmux send-keys -t "$TMUX_NAME" Space ;;
        ctrl+c|Ctrl+C)          tmux send-keys -t "$TMUX_NAME" C-c ;;
        ctrl+d|Ctrl+D)          tmux send-keys -t "$TMUX_NAME" C-d ;;
        ctrl+b|Ctrl+B)          tmux send-keys -t "$TMUX_NAME" C-b C-b ;;
        ctrl+f|Ctrl+F)          tmux send-keys -t "$TMUX_NAME" C-f ;;
        ctrl+g|Ctrl+G)          tmux send-keys -t "$TMUX_NAME" C-g ;;
        ctrl+l|Ctrl+L)          tmux send-keys -t "$TMUX_NAME" C-l ;;
        ctrl+o|Ctrl+O)          tmux send-keys -t "$TMUX_NAME" C-o ;;
        ctrl+r|Ctrl+R)          tmux send-keys -t "$TMUX_NAME" C-r ;;
        ctrl+s|Ctrl+S)          tmux send-keys -t "$TMUX_NAME" C-s ;;
        ctrl+t|Ctrl+T)          tmux send-keys -t "$TMUX_NAME" C-t ;;
        ctrl+e|Ctrl+E)          tmux send-keys -t "$TMUX_NAME" C-e ;;
        alt+p|Alt+P)            tmux send-keys -t "$TMUX_NAME" M-p ;;
        alt+t|Alt+T)            tmux send-keys -t "$TMUX_NAME" M-t ;;
        alt+m|Alt+M)            tmux send-keys -t "$TMUX_NAME" M-m ;;
        esc+esc|Esc+Esc)        tmux send-keys -t "$TMUX_NAME" Escape; sleep 0.2; tmux send-keys -t "$TMUX_NAME" Escape ;;
        *)
            echo "[cc-bridge] ⚠️  未知按键: $key"
            echo "可用: esc, up, down, left, right, tab, shift+tab, enter, space"
            echo "      ctrl+c/d/b/f/g/l/o/r/s/t/e, alt+p/t/m, esc+esc"
            return 1
            ;;
    esac

    wait_for_stable_output 10
    read_new_output
}

# ── 入口 ──────────────────────────────────────────────────────────────────────

case "$ACTION" in
    start)      do_start     ;;
    send)       do_send      ;;
    approve)    do_approve   ;;
    stop)       do_stop      ;;
    restart)    do_restart   ;;
    status)     do_status    ;;
    peek)       do_peek      ;;
    history)    do_history   ;;
    interrupt)  do_interrupt ;;
    key)        do_key       ;;
    *)
        echo "[cc-bridge] ❌ 未知 action: $ACTION"
        echo "可用: start | send | approve | stop | restart | status | peek | history | interrupt | key"
        exit 1
        ;;
esac
