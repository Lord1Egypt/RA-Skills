#!/bin/bash
# OpenClaw 健康检测与自动恢复
#
# 功能：
# 1. 检测 Gateway 进程和端口
# 2. 连续失败 3 次触发自动恢复
# 3. 恢复到黄金备份
# 4. 发送系统通知 + Telegram 通知（可选）
#
# 用法：由 LaunchAgent 每 2 分钟调用

# 注意：不使用 set -e，因为我们需要处理失败情况

# ============ 配置 ============
GOLDEN_CONFIG="$HOME/.openclaw/backups/golden-config/openclaw.json"
CURRENT_CONFIG="$HOME/.openclaw/openclaw.json"
LOG_FILE="$HOME/.openclaw/logs/health-recovery.log"
RECOVERY_HISTORY="$HOME/.openclaw/logs/recovery-history.log"
STATE_FILE="$HOME/.openclaw/state/recovery-count"
BACKUP_LOG="$HOME/.openclaw/backups/README.md"
CONFIG_FILE="$HOME/.openclaw/config/keepalive.conf"
MAX_FAILURES=3
GATEWAY_PORT=18789
LOG_MAX_SIZE_MB=5
LOG_KEEP_DAYS=30

# Telegram 通知配置（从配置文件读取）
if [ -f "$CONFIG_FILE" ]; then
    source "$CONFIG_FILE"
fi

# ============ 初始化 ============
mkdir -p "$(dirname "$LOG_FILE")"
mkdir -p "$(dirname "$STATE_FILE")"
mkdir -p "$(dirname "$CONFIG_FILE")"

if [ ! -f "$STATE_FILE" ]; then
    echo "0" > "$STATE_FILE"
fi

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

log_recovery() {
    # 恢复记录同时写入主日志和历史文件（永久保留）
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $1"
    echo "$msg" >> "$LOG_FILE"
    echo "$msg" >> "$RECOVERY_HISTORY"
}

rotate_log() {
    # 检查日志大小
    local size_mb=$(du -m "$LOG_FILE" 2>/dev/null | cut -f1)
    if [ "$size_mb" -ge "$LOG_MAX_SIZE_MB" ]; then
        local backup="$LOG_FILE.$(date +%Y%m%d-%H%M%S).gz"
        gzip -c "$LOG_FILE" > "$backup"
        > "$LOG_FILE"  # 清空当前日志
        log "📦 日志已轮转: $backup"

        # 删除 30 天前的旧日志
        find "$(dirname "$LOG_FILE")" -name "health-recovery.log.*.gz" -mtime +$LOG_KEEP_DAYS -delete 2>/dev/null
    fi
}

notify_system() {
    osascript -e "display notification \"$1\" with title \"OpenClaw 健康检测\" sound name \"Submarine\"" 2>/dev/null || true
}

notify_telegram() {
    # 只有配置了 Telegram 才发送
    if [ -n "$TELEGRAM_BOT_TOKEN" ] && [ -n "$TELEGRAM_CHAT_ID" ]; then
        curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
            -d chat_id="$TELEGRAM_CHAT_ID" \
            -d text="🛡️ OpenClaw 自动恢复\n\n$1" \
            -d parse_mode="Markdown" \
            > /dev/null 2>&1 || true
    fi
}

update_backup_log() {
    local operation="$1"
    local reason="$2"
    local result="$3"

    # 追加到 README.md
    echo "| $(date '+%Y-%m-%d %H:%M') | $operation | $reason | $result |" >> "$BACKUP_LOG"
}

increment_failure() {
    local count=$(cat "$STATE_FILE")
    count=$((count + 1))
    echo "$count" > "$STATE_FILE"
    log "❌ 健康检测失败 (第 $count 次)"
    echo "$count"  # 输出 count，而不是 return
}

reset_failure() {
    echo "0" > "$STATE_FILE"
}

# ============ 健康检测 ============
check_health() {
    local failed=0
    local reason=""

    # 检测 1: Gateway 进程（使用 ps + grep，兼容 macOS）
    if ! ps aux | grep -v grep | grep -q "openclaw-gateway"; then
        reason="Gateway 进程不存在"
        failed=1
    fi

    # 检测 2: 端口响应
    if [ $failed -eq 0 ]; then
        if ! nc -z localhost "$GATEWAY_PORT" 2>/dev/null; then
            reason="端口 $GATEWAY_PORT 无响应"
            failed=1
        fi
    fi

    # 检测 3: Gateway RPC（如果进程和端口都正常）
    if [ $failed -eq 0 ]; then
        if ! openclaw gateway status 2>/dev/null | grep -q "RPC probe: ok"; then
            reason="Gateway RPC 无响应"
            failed=1
        fi
    fi

    # 返回结果
    if [ $failed -eq 1 ]; then
        echo "$reason"
        return 1
    else
        return 0
    fi
}

# ============ 配置差异记录 ============
record_config_diff() {
    local old_config="$1"
    local new_config="$2"
    local reason="$3"

    if [ ! -f "$old_config" ] || [ ! -f "$new_config" ]; then
        return
    fi

    # 记录关键差异（简化版，只记录 agent 列表变化）
    local old_agents=$(grep -o '"id": "[^"]*"' "$old_config" | sort)
    local new_agents=$(grep -o '"id": "[^"]*"' "$new_config" | sort)

    if [ "$old_agents" != "$new_agents" ]; then
        log "📋 配置差异检测:"
        log "  恢复原因: $reason"
        log "  Agent 列表已变化"
    fi
}

# ============ 自动恢复 ============
trigger_recovery() {
    local reason="$1"

    log_recovery "🚨 触发自动恢复 - 原因: $reason"

    # 检查黄金备份是否存在
    if [ ! -f "$GOLDEN_CONFIG" ]; then
        log_recovery "❌ 黄金备份不存在，无法恢复"
        notify_system "❌ 自动恢复失败：黄金备份不存在"
        notify_telegram "❌ 自动恢复失败\n\n原因: 黄金备份不存在\n位置: $GOLDEN_CONFIG"
        return 1
    fi

    # 备份当前配置（即使它有问题）
    local backup_before="$HOME/.openclaw/backups/openclaw.json.before-auto-recovery-$(date +%Y%m%d-%H%M%S)"
    cp "$CURRENT_CONFIG" "$backup_before" 2>/dev/null || true
    log "📦 当前配置已备份: $backup_before"

    # 记录配置差异（恢复前）
    record_config_diff "$backup_before" "$GOLDEN_CONFIG" "$reason"

    # 恢复黄金备份
    cp "$GOLDEN_CONFIG" "$CURRENT_CONFIG"
    log "✅ 黄金备份已恢复"

    # 停止 Gateway（直接操作 launchctl）
    launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.gateway.plist 2>/dev/null || true
    sleep 2

    # 启动 Gateway（直接操作 launchctl）
    launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.gateway.plist 2>&1 || true
    sleep 15  # 给 LaunchAgent 足够时间启动

    # 验证恢复
    if check_health > /dev/null 2>&1; then
        log_recovery "✅ 自动恢复成功"
        notify_system "✅ OpenClaw 已自动恢复"
        notify_telegram "✅ 自动恢复成功\n\n原因: $reason\n操作: 恢复到黄金备份\n时间: $(date '+%Y-%m-%d %H:%M:%S')"
        update_backup_log "自动恢复" "$reason" "✅ 成功"
        reset_failure
        return 0
    else
        log_recovery "❌ 自动恢复失败 - Gateway 仍未正常"
        notify_system "❌ 自动恢复失败，请手动处理"
        notify_telegram "❌ 自动恢复失败\n\n原因: $reason\n状态: Gateway 仍未正常\n请手动检查:\nopenclaw gateway status"
        update_backup_log "自动恢复" "$reason" "❌ 失败"
        return 1
    fi
}

# ============ 更新黄金备份 ============
update_golden_backup() {
    if check_health > /dev/null 2>&1; then
        cp "$CURRENT_CONFIG" "$GOLDEN_CONFIG"
        log "✅ 黄金备份已更新（健康检测通过）"
    fi
}

# ============ 主流程 ============
main() {
    rotate_log  # 先检查是否需要轮转
    log "🔍 开始健康检测"

    if check_health; then
        log "✅ 健康检测通过"
        reset_failure
        update_golden_backup
    else
        reason=$(check_health)
        increment_failure
        count=$(cat "$STATE_FILE")

        if [ $count -ge $MAX_FAILURES ]; then
            log_recovery "⚠️ 连续失败 $count 次，触发自动恢复"
            trigger_recovery "$reason"
        else
            log "⚠️ 失败计数: $count/$MAX_FAILURES"
            if [ $count -ge 3 ]; then
                notify_system "⚠️ OpenClaw 健康检测异常 ($count/$MAX_FAILURES)"
            fi
        fi
    fi
}

main "$@"
