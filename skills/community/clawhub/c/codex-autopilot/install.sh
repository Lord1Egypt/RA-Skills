#!/bin/bash
# AIWorkFlow Autopilot — 一键部署脚本
# 用法: bash install.sh
#
# 功能:
#   1. 检查依赖 (tmux, jq, codex)
#   2. 创建运行时目录
#   3. 交互式配置 (Telegram, 项目)
#   4. 创建 tmux session + 项目窗口
#   5. 安装 launchd watchdog 服务
#   6. 验证部署

set -euo pipefail

AUTOPILOT_DIR="${HOME}/.autopilot"
SCRIPTS_DIR="${AUTOPILOT_DIR}/scripts"
STATE_DIR="${AUTOPILOT_DIR}/state"
LOGS_DIR="${AUTOPILOT_DIR}/logs"
LOCKS_DIR="${AUTOPILOT_DIR}/locks"
QUEUE_DIR="${AUTOPILOT_DIR}/task-queue"
CONF_FILE="${AUTOPILOT_DIR}/watchdog-projects.conf"
CONFIG_YAML="${AUTOPILOT_DIR}/config.yaml"
PLIST_NAME="com.autopilot.watchdog"
PLIST_PATH="${HOME}/Library/LaunchAgents/${PLIST_NAME}.plist"
TMUX="/opt/homebrew/bin/tmux"
SESSION="autopilot"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

info()  { echo -e "${BLUE}[INFO]${NC} $*"; }
ok()    { echo -e "${GREEN}[OK]${NC} $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC} $*"; }
err()   { echo -e "${RED}[ERROR]${NC} $*"; }

# ---- Step 0: 检查运行环境 ----
check_deps() {
    info "检查依赖..."
    local missing=()

    # tmux
    if command -v tmux &>/dev/null; then
        TMUX=$(command -v tmux)
        ok "tmux: $($TMUX -V)"
    elif [ -x /opt/homebrew/bin/tmux ]; then
        ok "tmux: $(/opt/homebrew/bin/tmux -V)"
    else
        missing+=("tmux")
    fi

    # jq
    if command -v jq &>/dev/null; then
        ok "jq: $(jq --version)"
    else
        missing+=("jq")
    fi

    # codex
    if command -v codex &>/dev/null; then
        ok "codex: $(command -v codex)"
    elif [ -x /opt/homebrew/bin/codex ]; then
        ok "codex: /opt/homebrew/bin/codex"
    else
        missing+=("codex")
    fi

    # python3
    if command -v python3 &>/dev/null; then
        ok "python3: $(python3 --version 2>&1)"
    else
        missing+=("python3")
    fi

    # bash 版本 (需要 4+)
    local bash_ver
    bash_ver=$(bash --version | head -1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
    ok "bash: ${bash_ver}"

    if [ ${#missing[@]} -gt 0 ]; then
        err "缺少依赖: ${missing[*]}"
        echo "  安装: brew install ${missing[*]}"
        exit 1
    fi
    echo ""
}

# ---- Step 1: 创建目录结构 ----
create_dirs() {
    info "创建运行时目录..."
    mkdir -p "$STATE_DIR" "$LOGS_DIR" "$LOCKS_DIR" "$QUEUE_DIR"
    ok "目录就绪: state/ logs/ locks/ task-queue/"
    echo ""
}

# ---- Step 2: 配置 ----
configure() {
    # Telegram 配置
    if [ -f "$CONFIG_YAML" ] && grep -q 'bot_token' "$CONFIG_YAML" 2>/dev/null; then
        ok "Telegram 配置已存在 (config.yaml)"
    else
        info "配置 Telegram 通知 (可选, 直接回车跳过)"
        read -rp "  Bot Token: " tg_token
        read -rp "  Chat ID: " tg_chat
        if [ -n "$tg_token" ] && [ -n "$tg_chat" ]; then
            cat > "$CONFIG_YAML" << EOF
telegram:
  bot_token: "${tg_token}"
  chat_id: "${tg_chat}"
EOF
            ok "Telegram 配置已保存"
        else
            warn "跳过 Telegram 配置"
        fi
    fi

    # 项目配置
    if [ -f "$CONF_FILE" ] && grep -v '^#' "$CONF_FILE" | grep -q ':'; then
        ok "项目配置已存在:"
        grep -v '^#' "$CONF_FILE" | grep -v '^$' | while IFS=: read -r w d _; do
            echo "    ${w} → ${d}"
        done
    else
        info "配置监控项目"
        echo "  格式: 窗口名:项目路径:默认nudge消息"
        echo "  示例: MyApp:/Users/you/myapp:继续下一个任务"
        echo "  输入空行结束"
        echo ""
        cat > "$CONF_FILE" << 'HEADER'
# watchdog 项目配置
# 格式: tmux_window:project_dir:nudge_message
# 添加/删除项目只需编辑此文件，watchdog 下次运行自动生效

HEADER
        while true; do
            read -rp "  项目配置 (空行结束): " line
            [ -z "$line" ] && break
            echo "$line" >> "$CONF_FILE"
        done
        ok "项目配置已保存"
    fi
    echo ""
}

# ---- Step 3: 验证脚本 ----
validate_scripts() {
    info "验证脚本语法..."
    local failed=0
    for script in watchdog.sh codex-status.sh tmux-send.sh monitor-all.sh task-queue.sh auto-nudge.sh; do
        if [ -f "${SCRIPTS_DIR}/${script}" ]; then
            if bash -n "${SCRIPTS_DIR}/${script}" 2>/dev/null; then
                ok "  ${script}"
            else
                err "  ${script} — 语法错误!"
                failed=1
            fi
        else
            warn "  ${script} — 不存在"
        fi
    done
    if [ "$failed" -eq 1 ]; then
        err "存在语法错误，请修复后重试"
        exit 1
    fi
    echo ""
}

# ---- Step 4: 创建 tmux session ----
setup_tmux() {
    info "配置 tmux session..."

    if $TMUX has-session -t "$SESSION" 2>/dev/null; then
        ok "tmux session '${SESSION}' 已存在"
        # 检查窗口是否齐全
        local existing_windows
        existing_windows=$($TMUX list-windows -t "$SESSION" -F '#{window_name}' 2>/dev/null)
        grep -v '^#' "$CONF_FILE" | grep -v '^$' | while IFS=: read -r w d _; do
            if echo "$existing_windows" | grep -q "^${w}$"; then
                ok "  窗口 '${w}' 已存在"
            else
                $TMUX new-window -t "$SESSION" -n "$w"
                $TMUX send-keys -t "${SESSION}:${w}" "cd $d" Enter
                ok "  创建窗口 '${w}'"
            fi
        done
    else
        info "创建 tmux session '${SESSION}'..."
        local first=true
        grep -v '^#' "$CONF_FILE" | grep -v '^$' | while IFS=: read -r w d _; do
            if $first; then
                $TMUX new-session -d -s "$SESSION" -n "$w"
                $TMUX send-keys -t "${SESSION}:${w}" "cd $d" Enter
                first=false
            else
                $TMUX new-window -t "$SESSION" -n "$w"
                $TMUX send-keys -t "${SESSION}:${w}" "cd $d" Enter
            fi
            ok "  创建窗口 '${w}' → ${d}"
        done
    fi
    echo ""
}

# ---- Step 5: 安装 launchd 服务 ----
install_launchd() {
    info "安装 launchd watchdog 服务..."

    # 先停旧的
    launchctl unload "$PLIST_PATH" 2>/dev/null || true

    cat > "$PLIST_PATH" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>${PLIST_NAME}</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>${SCRIPTS_DIR}/watchdog.sh</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>${LOGS_DIR}/watchdog-stdout.log</string>
    <key>StandardErrorPath</key>
    <string>${LOGS_DIR}/watchdog-stderr.log</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
    </dict>
</dict>
</plist>
EOF

    launchctl load "$PLIST_PATH"
    sleep 2

    if launchctl list | grep -q "$PLIST_NAME"; then
        ok "watchdog 服务已启动"
    else
        err "watchdog 服务启动失败，检查: ${LOGS_DIR}/watchdog-stderr.log"
        exit 1
    fi
    echo ""
}

# ---- Step 6: 清理旧版服务 ----
cleanup_legacy() {
    info "清理旧版服务..."
    local legacy_plists=(
        "com.wes.codex-autopilot"
        "com.wes.codex-watchdog"
        "com.autopilot.permission-guard"
    )
    for name in "${legacy_plists[@]}"; do
        local p="${HOME}/Library/LaunchAgents/${name}.plist"
        if [ -f "$p" ]; then
            launchctl unload "$p" 2>/dev/null || true
            rm -f "$p"
            ok "  已移除 ${name}"
        fi
    done
    echo ""
}

# ---- Step 7: 验证部署 ----
verify() {
    info "验证部署..."
    local all_ok=true

    # watchdog 进程
    if pgrep -f 'watchdog.sh' >/dev/null; then
        ok "watchdog 进程运行中 (PID $(pgrep -f 'watchdog.sh' | head -1))"
    else
        err "watchdog 未运行"
        all_ok=false
    fi

    # tmux session
    if $TMUX has-session -t "$SESSION" 2>/dev/null; then
        local win_count
        win_count=$($TMUX list-windows -t "$SESSION" | wc -l | tr -d ' ')
        ok "tmux session '${SESSION}': ${win_count} 个窗口"
    else
        err "tmux session 不存在"
        all_ok=false
    fi

    # codex-status 测试
    local first_window
    first_window=$(grep -v '^#' "$CONF_FILE" | grep -v '^$' | head -1 | cut -d: -f1)
    if [ -n "$first_window" ]; then
        local status
        status=$(bash "${SCRIPTS_DIR}/codex-status.sh" "$first_window" 2>/dev/null | jq -r '.status' 2>/dev/null || echo "error")
        ok "codex-status 测试: ${first_window} = ${status}"
    fi

    echo ""
    if $all_ok; then
        echo -e "${GREEN}═══════════════════════════════════════${NC}"
        echo -e "${GREEN}  ✅ AIWorkFlow Autopilot 部署成功!${NC}"
        echo -e "${GREEN}═══════════════════════════════════════${NC}"
        echo ""
        echo "  📺 查看 tmux:  tmux attach -t autopilot"
        echo "  📋 查看日志:  tail -f ~/.autopilot/logs/watchdog-stderr.log"
        echo "  📊 手动监控:  bash ~/.autopilot/scripts/monitor-all.sh"
        echo "  📝 添加任务:  bash ~/.autopilot/scripts/task-queue.sh add <project> <task>"
        echo "  🔧 配置项目:  vim ~/.autopilot/watchdog-projects.conf"
        echo ""
        echo "  在每个 tmux 窗口中启动 Codex:"
        echo "    codex --full-auto"
        echo ""
    else
        err "部署有问题，请检查上面的错误信息"
        exit 1
    fi
}

# ---- 主流程 ----
main() {
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════${NC}"
    echo -e "${BLUE}  AIWorkFlow Autopilot — 一键部署${NC}"
    echo -e "${BLUE}═══════════════════════════════════════${NC}"
    echo ""

    check_deps
    create_dirs
    configure
    validate_scripts
    setup_tmux
    cleanup_legacy
    install_launchd
    verify
}

main "$@"
