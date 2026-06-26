#!/bin/bash
# Health Check — 第二层守护
# 用途：每 5 分钟检查 Gateway 健康状态，崩溃则自动回滚
# 原理：用最轻量的 Haiku 模型检测，~500 token/次，连续 3 次健康则自治关闭

WORK_DIR="$HOME/.openclaw/workspace/.lib/config-safety"
LOG_FILE="$WORK_DIR/health-check.log"
GATEWAY_URL="${GATEWAY_URL:-http://localhost:18789}"
MAX_RETRIES=3

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

check_health() {
    curl -s --max-time 5 "$GATEWAY_URL/health" > /dev/null 2>&1
    return $?
}

restart_and_recover() {
    log "Gateway 不健康，尝试恢复..."
    
    # 执行回滚
    python3 "$WORK_DIR/guard.py" rollback
    
    # 等待 Gateway 重启
    sleep 10
    
    # 验证恢复
    if check_health; then
        log "Gateway 恢复健康 ✅"
        exit 0
    else
        log "恢复失败，需要人工介入 ❌"
        exit 1
    fi
}

# 主逻辑
if check_health; then
    log "Gateway 健康 ✅"
    exit 0
else
    log "Gateway 不健康，5 秒后重试..."
    sleep 5
    
    if check_health; then
        log "Gateway 恢复 ✅"
        exit 0
    else
        log "Gateway 仍然不健康，触发回滚..."
        restart_and_recover
    fi
fi
