#!/bin/bash
# ========================================
# 🔍 即时状态查询守护进程
# 用户发"状态"→ 渠道插件写触发文件 → 本进程秒回
# 由 systemd 管理，开机自启+崩溃重启
# ========================================

export PATH="/root/.nvm/versions/node/v22.22.0/bin:/root/.local/share/pnpm:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
export HOME="/root"

TRIGGER_FILE="/tmp/status-query-trigger"
LOG_FILE="/tmp/status-query-daemon.log"
CONFIG_FILE="/tmp/agent-guardian-config.json"

echo $$ > /tmp/status-query-daemon.pid

log() {
    echo "[$(date '+%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
    tail -100 "$LOG_FILE" > "${LOG_FILE}.tmp" 2>/dev/null && mv "${LOG_FILE}.tmp" "$LOG_FILE"
}

send_status() {
    local TARGET="$1"
    local TIME_STR=$(date '+%H:%M:%S')

    # 读取配置中的渠道
    local CHANNEL=""
    if [ -f "$CONFIG_FILE" ]; then
      CHANNEL=$(python3 -c "import json; d=json.load(open('$CONFIG_FILE')); print(d.get('channel',''))" 2>/dev/null)
    fi
    [ -z "$CHANNEL" ] && CHANNEL="qqbot"

    SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
    local QUEUE_REPORT=$(python3 "$SCRIPT_DIR/msg-queue.py" report 2>/dev/null)
    local MEM=$(free -h 2>/dev/null | awk '/Mem:/{print $3"/"$2}')
    local LOAD=$(uptime 2>/dev/null | awk -F'load average:' '{print $2}' | cut -d',' -f1 | xargs)

    local MSG="📊 即时状态 $TIME_STR
${QUEUE_REPORT}
🔧 内存 $MEM | 负载 $LOAD"

    openclaw message send --channel "$CHANNEL" --target "$TARGET" --message "$MSG" 2>/dev/null
    log "Status sent to $TARGET via $CHANNEL"
}

log "Daemon started (PID $$)"
touch "$TRIGGER_FILE"

# 检查 inotifywait 是否可用
if ! command -v inotifywait &>/dev/null; then
    log "ERROR: inotifywait not found. Install inotify-tools."
    echo "ERROR: inotifywait not found. Run: apt install inotify-tools"
    exit 1
fi

while true; do
    inotifywait -q -e modify "$TRIGGER_FILE" 2>/dev/null
    if [ -f "$TRIGGER_FILE" ]; then
        TARGET=$(python3 -c "
import json
with open('$TRIGGER_FILE') as f:
    d = json.load(f)
print(d.get('from', ''))
" 2>/dev/null)
        if [ -n "$TARGET" ]; then
            log "Trigger from $TARGET"
            send_status "$TARGET"
        fi
    fi
done
