#!/bin/bash
# config-lib.sh — OpenClaw Gateway Config Guardian shared library
# Not executable directly. Source'd by config-watcher.sh / gateway-recovery.sh / pre-stop.sh

# Ensure openclaw CLI is available (systemd environment has limited PATH)
export PATH="$HOME/.npm-global/bin:/usr/local/bin:$PATH"

# ── Path constants ─────────────────────────────────────────────────────────────
CONFIG="$HOME/.openclaw/openclaw.json"
BACKUP_DIR="$HOME/.openclaw"
TIMESTAMP_DIR="$HOME/.openclaw/config-backups"
MEMORY_DIR="$HOME/.openclaw/workspace/memory"
LOCK_FILE="/tmp/openclaw-config.lock"
MANAGED_RESTART_FLAG="/tmp/guardian-managed-restart"
MAX_BACKUPS=10
MAX_BROKEN=5
GATEWAY_PORT=18789

# ── Load guardian.conf (fallback notification config + LOCALE) ─────────────────
_GUARDIAN_LIB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
[ -f "$_GUARDIAN_LIB_DIR/guardian.conf" ] && source "$_GUARDIAN_LIB_DIR/guardian.conf"
# guardian.conf expected fields:
#   FALLBACK_CHANNEL=feishu
#   FALLBACK_TARGET=user:ou_xxx
#   LOCALE=zh   # or: en
#   BOT_NAME=OpenClaw             # optional: display name used in staff notifications
#   STAFF_GROUP_CHAT_ID=          # optional: group/channel id for team notifications

# ── Language strings ───────────────────────────────────────────────────────────
LOCALE="${LOCALE:-zh}"

if [ "$LOCALE" = "en" ]; then
    _MSG_FORWARD_HINT="💬 If this alert was triggered by my own action, please forward this message to me directly — no explanation needed. I'll understand the context and continue automatically."
    _MSG_MANUAL_ACTION="Please log into the server to handle this manually."
    _MSG_MEMORY_HEADER="🚨 Gateway Guardian Event"
    _MSG_TIME="Time"
    _MSG_EVENT="Event"
    _MSG_REASON="Reason"
    _MSG_LOG="Recent log"
    _MSG_ROLLED_BACK_TO="Rolled back to"

    _MSG_SUCCESS_TITLE="✅ OpenClaw Gateway Guardian"
    _MSG_SUCCESS_EVENT="Config file corrupted — auto-rolled back and recovered"

    _MSG_URGENT_TITLE="🚨 OpenClaw Gateway Guardian — Manual Action Required"
    _MSG_URGENT_NO_RESTART_EVENT="Config corrupted, rolled back, but gateway failed to restart"
    _MSG_URGENT_NO_RESTART_REASON="Gateway still unresponsive after rollback (30s timeout)"
    _MSG_URGENT_NOOP_EVENT="Config corrupted — all backups are invalid"
    _MSG_URGENT_NOOP_REASON="No usable backup found; cannot auto-recover"

    _MSG_RECOVERY_SUCCESS_TITLE="✅ OpenClaw Gateway Guardian — Gateway Recovered"
    _MSG_RECOVERY_SUCCESS_EVENT="Gateway crashed and was automatically restarted"
    _MSG_STAFF_RECOVERY="${BOT_NAME:-OpenClaw} just completed a brief system maintenance (~1-2 min) and is back online ✅
If your message didn't get a reply just now, please resend it — ${BOT_NAME:-OpenClaw} is here!"
    _MSG_RECOVERY_FAIL_TITLE="🚨 OpenClaw Gateway Guardian — Gateway Recovery Failed"
    _MSG_RECOVERY_FAIL_EVENT="Gateway crashed and could not be restarted automatically"
    _MSG_RECOVERY_FAIL_REASON="Gateway still unresponsive after restart attempts"

    _MSG_RESTART_STARTING="⚙️ Gateway is restarting, please wait..."
    _MSG_RESTART_DONE="✅ Gateway recovered. You can continue your conversation."
    _MSG_HUMAN_FIXED="✅ Gateway appears to have recovered. If you need to continue, please send me a message."

    _MSG_RESULT="Result"
    _MSG_ACTION="Action"
    _MSG_GATEWAY_LOG="Gateway log"
    _MSG_RECOVERY_WITH_ROLLBACK="Gateway crashed + config corrupted — auto-rolled back and restarted"
    _MSG_RECOVERY_NO_ROLLBACK="Gateway crashed (config healthy) — auto-restarted"
    _MSG_RECOVERY_RESET_ACTION="Reset failed count + restart gateway"
    _MSG_GATEWAY_BACK="Gateway is back online"
    _MSG_MEM_CRASH_NO_BACKUP="Gateway crashed, config corrupted with no valid backup"
    _MSG_MEM_RECOVERY_FAIL="Gateway crashed, auto-recovery failed"
    _MSG_MEM_CANNOT_RECOVER="Cannot auto-recover — manual action required"
    _MSG_MEM_TIMEOUT="Unresponsive after timeout — manual action required"
    _MSG_LATEST_BACKUP="latest backup"
else
    _MSG_FORWARD_HINT="💬 如果此次告警是由我的操作引起的，请将这条消息直接转发给我，无需添加任何说明，我会自动了解情况并继续处理。"
    _MSG_MANUAL_ACTION="请登录服务器手动处理。"
    _MSG_MEMORY_HEADER="🚨 网关守护事件"
    _MSG_TIME="时间"
    _MSG_EVENT="事件"
    _MSG_REASON="原因"
    _MSG_LOG="关键日志"
    _MSG_ROLLED_BACK_TO="回滚至"

    _MSG_SUCCESS_TITLE="✅ OpenClaw 网关守护"
    _MSG_SUCCESS_EVENT="配置文件损坏，已自动回滚并恢复"

    _MSG_URGENT_TITLE="🚨 OpenClaw 网关守护 - 需要人工处理"
    _MSG_URGENT_NO_RESTART_EVENT="配置文件损坏，已回滚，但网关无法重启"
    _MSG_URGENT_NO_RESTART_REASON="回滚后网关仍无响应（30s 超时）"
    _MSG_URGENT_NOOP_EVENT="配置文件损坏，且所有备份均无效"
    _MSG_URGENT_NOOP_REASON="无可用备份，无法自动恢复"

    _MSG_RECOVERY_SUCCESS_TITLE="✅ OpenClaw 网关守护 - 网关已恢复"
    _MSG_RECOVERY_SUCCESS_EVENT="网关崩溃后已自动重启恢复"
    _MSG_STAFF_RECOVERY="${BOT_NAME:-OpenClaw}刚才进行了一次系统自动维护（约1-2分钟），现在已恢复正常 ✅
如果刚才有消息没收到回复，请重新发一遍，${BOT_NAME:-OpenClaw}在的～"
    _MSG_RECOVERY_FAIL_TITLE="🚨 OpenClaw 网关守护 - 需要人工处理"
    _MSG_RECOVERY_FAIL_EVENT="网关崩溃，自动恢复失败"
    _MSG_RECOVERY_FAIL_REASON="多次重启后网关仍无响应"

    _MSG_RESTART_STARTING="⚙️ 网关正在重启中，请稍候..."
    _MSG_RESTART_DONE="✅ 已恢复，请发消息继续对话。"
    _MSG_HUMAN_FIXED="✅ 网关似乎已恢复正常。如需继续，请发消息给我。"

    _MSG_RESULT="结果"
    _MSG_ACTION="处置"
    _MSG_GATEWAY_LOG="网关日志"
    _MSG_RECOVERY_WITH_ROLLBACK="网关崩溃，检测到配置损坏，已自动回滚并重启"
    _MSG_RECOVERY_NO_ROLLBACK="网关崩溃（配置正常），已自动重启"
    _MSG_RECOVERY_RESET_ACTION="重置失败记录 + 重启网关"
    _MSG_GATEWAY_BACK="网关已恢复正常运行"
    _MSG_MEM_CRASH_NO_BACKUP="网关崩溃，配置损坏且无合法备份"
    _MSG_MEM_RECOVERY_FAIL="网关崩溃，自动恢复失败"
    _MSG_MEM_CANNOT_RECOVER="无法自动恢复，需要人工处理"
    _MSG_MEM_TIMEOUT="超时仍无响应，需要人工处理"
    _MSG_LATEST_BACKUP="最近备份"
fi

# ── Utility ────────────────────────────────────────────────────────────────────
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG"; }

# ── Dynamic session detection ──────────────────────────────────────────────────
# Finds the most recently active direct session; falls back to guardian.conf
detect_session() {
    local session_key
    session_key=$(timeout 10 openclaw sessions --json 2>/dev/null | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    sessions = data.get('sessions', [])
    real = [s for s in sessions if not s['key'].endswith(':main')]
    direct = [s for s in real if ':direct:' in s['key']]
    target = direct if direct else real
    target.sort(key=lambda x: x.get('updatedAt', 0), reverse=True)
    if target:
        print(target[0]['key'])
except Exception:
    pass
" 2>/dev/null)

    if [ -z "$session_key" ]; then
        DETECTED_CHANNEL="$FALLBACK_CHANNEL"
        DETECTED_TARGET="$FALLBACK_TARGET"
        return
    fi

    local channel kind id
    IFS=':' read -r _ _ channel kind id <<< "$session_key"
    DETECTED_CHANNEL="$channel"
    [ "$kind" = "direct" ] && DETECTED_TARGET="user:$id" || DETECTED_TARGET="chat:$id"
}

# ── Notification functions ─────────────────────────────────────────────────────
_send_notify() {
    local msg="$1"
    [ -z "$DETECTED_CHANNEL" ] && { log "⚠️  No notification channel configured, skipping"; return; }
    timeout 30 openclaw message send \
        --channel "$DETECTED_CHANNEL" \
        --target  "$DETECTED_TARGET" \
        --message "$msg" >> "$LOG" 2>&1 || log "⚠️  Notification send failed"
}

# 员工/团队群通知 — 仅在恢复成功时发送，未配置则静默跳过
_send_staff_group_notify() {
    [ -z "$STAFF_GROUP_CHAT_ID" ] && return
    local _channel="${FALLBACK_CHANNEL:-feishu}"
    timeout 30 openclaw message send \
        --channel "$_channel" \
        --target  "chat:${STAFF_GROUP_CHAT_ID}" \
        --message "$_MSG_STAFF_RECOVERY" >> "$LOG" 2>&1 || log "⚠️  Staff group notification send failed"
}

# Success notification — includes "forward to me" hint + optional staff group notify
# 如果配置了固定群，只发固定群；没配置才动态检测最活跃 session
notify_success() {
    local title="$1"
    local body="$2"
    if [ -n "$STAFF_GROUP_CHAT_ID" ]; then
        # 有固定群配置 → 只发固定群
        _send_staff_group_notify
    else
        # 没有固定群配置 → 动态检测最活跃 session
        detect_session
        _send_notify "${title}

${body}

${_MSG_FORWARD_HINT}"
    fi
}

# Urgent notification — requires manual intervention, no forward hint
notify_urgent() {
    local title="$1"
    local body="$2"
    detect_session
    _send_notify "${title}

${body}

${_MSG_MANUAL_ACTION}"
}

# Status notification — plain message, no trailing hint
notify_status() {
    detect_session
    _send_notify "$1"
}

# ── Memory log ────────────────────────────────────────────────────────────────
write_to_memory() {
    local content="$1"
    mkdir -p "$MEMORY_DIR"
    local file="$MEMORY_DIR/$(date +%Y-%m-%d).md"
    echo "" >> "$file"
    echo "## ${_MSG_MEMORY_HEADER} ($(date '+%H:%M'))" >> "$file"
    echo "$content" >> "$file"
}

# Extract recent structured log lines (filters out plugin-load noise)
tail_log() {
    local logfile="$1" n="${2:-8}"
    grep "^\[20" "$logfile" 2>/dev/null | tail -n "$n"
}

# Extract gateway error lines from journalctl
# Priority: keyword match; fallback: last 5 systemd lines
gateway_journal_errors() {
    local lines
    lines=$(journalctl --user -u openclaw-gateway.service \
        --no-pager -n 30 --output=short 2>/dev/null)
    local filtered
    filtered=$(echo "$lines" | \
        grep -iE "error|fail|invalid|cannot|eaddrinuse|exit code|exited.*status=[^0]" | \
        tail -5)
    if [ -n "$filtered" ]; then
        echo "$filtered"
    else
        echo "$lines" | grep -E "systemd\[|Started|Stopped|Failed|Activating|Deactivating|exited|status=" | tail -5
    fi
}

# ── Validation (3-pass) ───────────────────────────────────────────────────────
validate_file() {
    local file="$1" result exit_code
    local tmp="$CONFIG.validate.tmp"

    # Pass 1+2: JSON syntax + required fields (single python3 call)
    result=$(python3 -c "
import json, sys
try:
    d = json.load(open(sys.argv[1]))
    assert 'gateway' in d and 'port' in d.get('gateway', {}), 'missing gateway.port'
except AssertionError as e:
    print(e); sys.exit(1)
except Exception as e:
    print('JSON error:', e); sys.exit(1)
" "$file" 2>&1) || { echo "$result"; return 1; }

    # Pass 3: openclaw schema validation
    if [ "$file" = "$CONFIG" ]; then
        result=$(timeout 30 openclaw config validate 2>&1)
        exit_code=$?
    else
        cp "$CONFIG" "$tmp" 2>/dev/null || { echo "cannot read config file"; return 1; }
        if ! cp "$file" "$CONFIG" 2>/dev/null; then
            cp "$tmp" "$CONFIG"; rm -f "$tmp"
            echo "cannot copy file to config"; return 1
        fi
        result=$(timeout 30 openclaw config validate 2>&1)
        exit_code=$?
        cp "$tmp" "$CONFIG" && rm -f "$tmp"
    fi

    if [ $exit_code -ne 0 ] || echo "$result" | grep -qi "error\|invalid\|failed"; then
        echo "$result"; return 1
    fi
    return 0
}

# ── Backup ────────────────────────────────────────────────────────────────────
save_backup() {
    local bak count
    mkdir -p "$TIMESTAMP_DIR"
    bak="$TIMESTAMP_DIR/openclaw.json.$(date +%Y%m%d-%H%M%S)"
    cp "$CONFIG" "$bak"
    count=$(ls "$TIMESTAMP_DIR/" | wc -l)
    if [ "$count" -gt "$MAX_BACKUPS" ]; then
        ls -t "$TIMESTAMP_DIR/" | tail -n +$((MAX_BACKUPS + 1)) | \
            while IFS= read -r f; do rm -f "$TIMESTAMP_DIR/$f"; done
    fi
    log "💾 Backup saved: $(basename "$bak")"
}

cleanup_broken() {
    ls -t "$BACKUP_DIR"/openclaw.json.broken.* 2>/dev/null | \
        tail -n +$((MAX_BROKEN + 1)) | \
        while IFS= read -r f; do rm -f "$f"; done
}

# ── Rollback ──────────────────────────────────────────────────────────────────
# On success, writes the backup name used to ROLLBACK_USED_BACKUP
ROLLBACK_USED_BACKUP=""

rollback() {
    local result bak
    ROLLBACK_USED_BACKUP=""

    # Try timestamp backups newest-first
    while IFS= read -r f; do
        bak="$TIMESTAMP_DIR/$f"
        result=$(validate_file "$bak" 2>&1)
        if [ $? -eq 0 ]; then
            cp "$CONFIG" "$CONFIG.broken.$(date +%Y%m%d-%H%M%S)"
            cp "$bak" "$CONFIG"
            ROLLBACK_USED_BACKUP="$f"
            log "✅ Rolled back to timestamp backup: $f"
            cleanup_broken; return 0
        fi
        log "⏭️  $f invalid ($result), skipping"
    done < <(ls -t "$TIMESTAMP_DIR/" 2>/dev/null)

    # Fallback: openclaw native backups
    for bak in "$BACKUP_DIR/openclaw.json.bak" \
               "$BACKUP_DIR/openclaw.json.bak.1" \
               "$BACKUP_DIR/openclaw.json.bak.2" \
               "$BACKUP_DIR/openclaw.json.bak.3" \
               "$BACKUP_DIR/openclaw.json.bak.4"; do
        [ -f "$bak" ] || continue
        result=$(validate_file "$bak" 2>&1)
        if [ $? -eq 0 ]; then
            cp "$CONFIG" "$CONFIG.broken.$(date +%Y%m%d-%H%M%S)"
            cp "$bak" "$CONFIG"
            ROLLBACK_USED_BACKUP="$(basename "$bak")"
            log "✅ Rolled back to native backup: $(basename "$bak")"
            cleanup_broken; return 0
        fi
        log "⏭️  $(basename "$bak") invalid ($result), skipping"
    done

    log "❌ All backups invalid — rollback failed"
    return 1
}

# ── Core handler ──────────────────────────────────────────────────────────────
handle_change() {
    local result
    result=$(validate_file "$CONFIG" 2>&1)
    if [ $? -eq 0 ]; then
        log "✅ Config valid, saving backup"
        save_backup
        return
    fi

    log "❌ Config invalid: $result — starting rollback..."
    if rollback; then
        log "🔄 Rollback complete, checking gateway..."

        if nc -z 127.0.0.1 $GATEWAY_PORT 2>/dev/null; then
            log "✅ Gateway is running"
        else
            log "⚠️  Gateway not responding, attempting restart..."
            echo "watcher" > "$MANAGED_RESTART_FLAG"
            systemctl --user restart openclaw-gateway.service 2>/dev/null
            local elapsed=0
            while [ $elapsed -lt 30 ]; do
                sleep 5; elapsed=$((elapsed + 5))
                nc -z 127.0.0.1 $GATEWAY_PORT 2>/dev/null && break
            done
            if ! nc -z 127.0.0.1 $GATEWAY_PORT 2>/dev/null; then
                rm -f "$MANAGED_RESTART_FLAG"
                log "❌ Gateway restart failed"
                notify_urgent "$_MSG_URGENT_TITLE" \
"⏰ $_MSG_TIME: $(date '+%Y-%m-%d %H:%M')
📋 $_MSG_EVENT: $_MSG_URGENT_NO_RESTART_EVENT
❌ $_MSG_REASON: $_MSG_URGENT_NO_RESTART_REASON
📝 $_MSG_LOG:
$(tail_log "$LOG")"
                return
            fi
        fi

        notify_success "$_MSG_SUCCESS_TITLE" \
"⏰ $_MSG_TIME: $(date '+%Y-%m-%d %H:%M')
📋 $_MSG_EVENT: $_MSG_SUCCESS_EVENT
🔧 $_MSG_ROLLED_BACK_TO: ${ROLLBACK_USED_BACKUP:-$_MSG_LATEST_BACKUP}
📝 $_MSG_LOG:
$(tail_log "$LOG" 5)"

    else
        log "🚨 Rollback failed — manual intervention required"
        notify_urgent "$_MSG_URGENT_TITLE" \
"⏰ $_MSG_TIME: $(date '+%Y-%m-%d %H:%M')
📋 $_MSG_EVENT: $_MSG_URGENT_NOOP_EVENT
❌ $_MSG_REASON: $_MSG_URGENT_NOOP_REASON
📝 $_MSG_LOG:
$(tail_log "$LOG")"
        write_to_memory "- $_MSG_EVENT: $_MSG_URGENT_NOOP_EVENT
- $_MSG_RESULT: ❌ $_MSG_URGENT_NOOP_REASON
- $_MSG_LOG: $LOG"
    fi
}
