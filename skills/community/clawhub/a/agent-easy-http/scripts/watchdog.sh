#!/usr/bin/env bash
#
# watchdog.sh — agent-easy-http 自愈守护脚本
#
# 设计：长驻 daemon 模式，每 30s 检查一次服务，挂了就重启。
#
# 三种部署方式（按推荐顺序）：
#
#   方式 1: 直接前台跑（容器场景，推荐）
#     bash watchdog.sh run
#
#   方式 2: 后台跑（host 场景）
#     bash watchdog.sh start    # 启动守护
#     bash watchdog.sh stop     # 停止守护
#     bash watchdog.sh status   # 看状态
#
#   方式 3: OpenClaw cron（最简，但 1 分钟最小粒度）
#     openclaw cron add ... (见 README)
#
# 子命令：
#   run       前台运行守护循环（30s 间隔）
#   start     后台启动守护
#   stop      停止守护
#   status    查看守护 + 服务双状态
#   check     单次检查服务（不修复）
#   ensure    单次检查 + 必要时启动（cron 友好，幂等）
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVER_PY="$SCRIPT_DIR/server.py"
CHECK_INTERVAL="${WATCHDOG_INTERVAL:-30}"  # 秒

# 数据根（与 server.py 探测一致）
detect_data_root() {
    if [ -n "${AGENT_EASY_HTTP_DATA_ROOT:-}" ]; then
        echo "$AGENT_EASY_HTTP_DATA_ROOT"
        return
    fi
    local ws="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
    if [ -d "$ws/skills" ]; then
        echo "$ws/.agent-easy-http"
    else
        echo "$HOME/.agent-easy-http"
    fi
}

DATA_ROOT="$(detect_data_root)"
PID_FILE="$DATA_ROOT/server.pid"
WATCHDOG_PID_FILE="$DATA_ROOT/watchdog.pid"
LOG_DIR="$DATA_ROOT/logs"
LOG_FILE="$LOG_DIR/watchdog.log"

mkdir -p "$LOG_DIR"

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') [watchdog] $*" >> "$LOG_FILE"
    # 前台 run 模式也打到 stdout
    if [ "${WATCHDOG_FOREGROUND:-0}" = "1" ]; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') [watchdog] $*"
    fi
}

is_server_running() {
    [ -f "$PID_FILE" ] || return 1
    local pid
    pid="$(cat "$PID_FILE" 2>/dev/null || echo '')"
    [ -n "$pid" ] || return 1
    kill -0 "$pid" 2>/dev/null
}

is_watchdog_running() {
    [ -f "$WATCHDOG_PID_FILE" ] || return 1
    local pid
    pid="$(cat "$WATCHDOG_PID_FILE" 2>/dev/null || echo '')"
    [ -n "$pid" ] || return 1
    kill -0 "$pid" 2>/dev/null
}

ensure_hooks_and_sync_token() {
    # 检查 hooks 是否启用，若无则重新 setup；然后把 token 同步到 config.json
    local openclaw_json="$HOME/.openclaw/openclaw.json"
    if [ ! -f "$openclaw_json" ]; then
        log "⚠️  openclaw.json not found, skipping token sync"
        return 0
    fi

    local enabled token allow_session_key allowed_prefixes
    # python3 print(bool) 输出 "True"/"False"（大写），key 不存在时输出空字符串
    # 同时检查大小写两种形式以防 Python 版本差异
    enabled=$(python3 -c "import json,sys; d=json.load(open('$openclaw_json')); print(d.get('hooks',{}).get('enabled',''))" 2>/dev/null || echo "")
    token=$(python3 -c "import json,sys; d=json.load(open('$openclaw_json')); print(d.get('hooks',{}).get('token',''))" 2>/dev/null || echo "")
    # v1.0.4+ 还需要 allowRequestSessionKey + allowedSessionKeyPrefixes 才能让 /result 接口工作
    allow_session_key=$(python3 -c "import json,sys; d=json.load(open('$openclaw_json')); print(d.get('hooks',{}).get('allowRequestSessionKey',''))" 2>/dev/null || echo "")
    allowed_prefixes=$(python3 -c "import json,sys; d=json.load(open('$openclaw_json')); p=d.get('hooks',{}).get('allowedSessionKeyPrefixes',[]); print('hook:' in p)" 2>/dev/null || echo "False")

    # 任一关键配置缺失就触发 setup-hooks（init_wizard 会一并补写）
    if [ -z "$enabled" ] || [ "$enabled" = "False" ] || [ "$enabled" = "false" ] || [ -z "$token" ] \
       || [ "$allow_session_key" != "True" ] || [ "$allowed_prefixes" != "True" ]; then
        log "⚠️  hooks 配置缺失（enabled=$enabled token_set=$([ -n "$token" ] && echo Y || echo N) allowSession=$allow_session_key hookPrefix=${allowed_prefixes}），运行 setup-hooks..."
        echo "Y" | python3 "$(dirname "$SERVER_PY")/init_wizard.py" --setup-hooks-only >> "$LOG_FILE" 2>&1 || true
        # 重新读 token
        token=$(python3 -c "import json; d=json.load(open('$openclaw_json')); print(d.get('hooks',{}).get('token',''))" 2>/dev/null || echo "")
    fi

    if [ -n "$token" ]; then
        # heredoc 不带引号（<< PYEOF 而非 << 'PYEOF'），shell 在写入时展开 $DATA_ROOT/$token
        # 这是有意设计：需要把 shell 变量的值嵌入 Python 脚本；若改成带引号会导致展开失效
        python3 - << PYEOF >> "$LOG_FILE" 2>&1
import json, pathlib
cfg_path = pathlib.Path("$DATA_ROOT/config.json")
if cfg_path.exists():
    cfg = json.loads(cfg_path.read_text())
    cfg["hook_url"] = "http://127.0.0.1:18789/hooks/agent"
    cfg["hook_token"] = "$token"
    cfg_path.write_text(json.dumps(cfg, indent=2))
    print("token synced to config.json")
PYEOF
        log "✅ token synced"
    else
        log "⚠️  could not get hooks token after setup, server may fail to start"
    fi
}

start_server() {
    log "Starting agent-easy-http server..."
    # 启动前先确保 hooks token 是最新的
    ensure_hooks_and_sync_token
    nohup python3 "$SERVER_PY" start > "$LOG_DIR/server.log" 2>&1 &
    local new_pid=$!
    disown 2>/dev/null || true
    sleep 3
    if kill -0 "$new_pid" 2>/dev/null; then
        log "✅ Started (PID $new_pid)"
        return 0
    else
        log "❌ Start failed; see $LOG_DIR/server.log"
        return 1
    fi
}

is_server_healthy() {
    # 双重检查：① PID 存活 ② /health 接口返回 200 且 hook_endpoint_configured=true
    # 修复场景：外部配置中心覆盖 hooks 配置后进程活着但功能坏（返回 502）
    is_server_running || return 1

    # 读取服务端口
    local port_file="$DATA_ROOT/server.port"
    local port=7720  # 默认值（与 server.py DEFAULT_PORT 一致）
    if [ -f "$port_file" ]; then
        port=$(cat "$port_file" 2>/dev/null || echo 7720)
    fi

    # 调 /health 检查（超时 3s，避免卡住）
    local health
    health=$(curl -sf --max-time 3 "http://127.0.0.1:${port}/health" 2>/dev/null || echo "")
    if [ -z "$health" ]; then
        log "⚠️  /health 无响应（进程活但端口不通？），触发重启"
        return 1
    fi

    # 检查 hook_endpoint_configured 是否为 true
    local hook_ok
    hook_ok=$(echo "$health" | python3 -c "
import json,sys
try:
    d=json.loads(sys.stdin.read())
    print('true' if d.get('hook_endpoint_configured') else 'false')
except:
    print('unknown')
" 2>/dev/null || echo "unknown")

    if [ "$hook_ok" = "false" ]; then
        log "⚠️  hook_endpoint_configured=false（hooks 配置被覆盖），触发重启"
        return 1
    fi
    return 0
}

cmd_run() {
    # 前台守护循环
    export WATCHDOG_FOREGROUND=1
    echo "$$" > "$WATCHDOG_PID_FILE"
    log "Watchdog daemon started (interval=${CHECK_INTERVAL}s, log=$LOG_FILE)"
    trap 'log "Watchdog stopping (signal)"; rm -f "$WATCHDOG_PID_FILE"; exit 0' SIGTERM SIGINT
    while true; do
        if ! is_server_healthy; then
            log "Service down or unhealthy, recovering..."
            start_server || log "❌ Recovery failed, will retry next cycle"
        fi
        sleep "$CHECK_INTERVAL"
    done
}

cmd_start() {
    if is_watchdog_running; then
        local pid
        pid="$(cat "$WATCHDOG_PID_FILE")"
        echo "⚠️  Watchdog already running (PID $pid)"
        return 0
    fi
    nohup bash "$0" run >> "$LOG_FILE" 2>&1 &
    disown 2>/dev/null || true
    sleep 1
    if is_watchdog_running; then
        local pid
        pid="$(cat "$WATCHDOG_PID_FILE")"
        echo "✅ Watchdog started (PID $pid, log=$LOG_FILE)"
    else
        echo "❌ Watchdog start failed; see $LOG_FILE"
        return 1
    fi
}

cmd_stop() {
    if ! is_watchdog_running; then
        echo "ℹ️  Watchdog not running"
        rm -f "$WATCHDOG_PID_FILE"
        return 0
    fi
    local pid
    pid="$(cat "$WATCHDOG_PID_FILE")"
    kill -TERM "$pid" 2>/dev/null || true
    sleep 1
    if is_watchdog_running; then
        kill -9 "$pid" 2>/dev/null || true
        rm -f "$WATCHDOG_PID_FILE"
        echo "✅ Watchdog force-killed (PID $pid)"
    else
        echo "✅ Watchdog stopped (PID $pid)"
    fi
}

cmd_status() {
    echo "── Watchdog ──"
    if is_watchdog_running; then
        echo "✅ Running (PID $(cat "$WATCHDOG_PID_FILE"))"
    else
        echo "❌ Not running"
    fi
    echo
    echo "── Server ──"
    if is_server_running; then
        echo "✅ Running (PID $(cat "$PID_FILE"))"
    else
        echo "❌ Not running"
    fi
    echo
    echo "── Logs ──"
    echo "  Watchdog: $LOG_FILE"
    echo "  Server  : $LOG_DIR/server.log"
}

cmd_check() {
    if is_server_running; then
        echo "✅ Server running (PID $(cat "$PID_FILE"))"
        return 0
    else
        echo "❌ Server not running"
        return 1
    fi
}

cmd_ensure() {
    if is_server_healthy; then exit 0; fi
    log "Service down or unhealthy (cron ensure), recovering..."
    start_server || { log "❌ Recovery failed"; exit 1; }
}

case "${1:-status}" in
    run)     cmd_run ;;
    start)   cmd_start ;;
    stop)    cmd_stop ;;
    status)  cmd_status ;;
    check)   cmd_check ;;
    ensure)  cmd_ensure ;;
    -h|--help)
        sed -n '2,28p' "$0"
        ;;
    *)
        echo "Usage: $0 {run|start|stop|status|check|ensure}"
        exit 1
        ;;
esac
