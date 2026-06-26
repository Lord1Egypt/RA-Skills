#!/bin/bash
# EvoMap Auto Maintainer Skill v1.0.0
# 自动维护 EvoMap 节点在线状态

set -e

# 配置
NODE_ID="${EVOMAP_NODE_ID:-}"
NODE_SECRET="${EVOMAP_SECRET:-}"
HUB_URL="https://evomap.ai"
LOG_FILE="${EVOMAP_LOG:-/tmp/evomap-maintainer.log}"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 检查节点状态
check_status() {
    log "检查节点状态..."
    
    if [ -z "$NODE_ID" ]; then
        log "❌ 错误: 未设置 EVOMAP_NODE_ID"
        log "请先设置: export EVOMAP_NODE_ID=node_your_node_id"
        return 1
    fi
    
    log "节点ID: $NODE_ID"
    local response
    response=$(curl -s "${HUB_URL}/api/health?node_id=${NODE_ID}" 2>/dev/null || echo '{"status":"error"}')
    
    if echo "$response" | grep -q '"status":"ok"'; then
        log "✅ 节点在线"
        return 0
    else
        log "⚠️  节点离线或异常"
        return 1
    fi
}

# 发送心跳
send_heartbeat() {
    log "发送心跳..."
    
    if [ -z "$NODE_ID" ] || [ -z "$NODE_SECRET" ]; then
        log "❌ 缺少 NODE_ID 或 NODE_SECRET"
        return 1
    fi
    
    local payload
    payload="{\"protocol\":\"gep-a2a\",\"protocol_version\":\"1.0.0\",\"message_type\":\"heartbeat\",\"message_id\":\"msg_$(date +%s)_$$\",\"sender_id\":\"$NODE_ID\",\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"payload\":{\"status\":\"alive\",\"credit_balance\":0,\"active_sessions\":1}}"
    
    local response
    response=$(curl -s -X POST "${HUB_URL}/a2a/heartbeat" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $NODE_SECRET" \
        -d "$payload" 2>/dev/null || echo '{"status":"error"}')
    
    if echo "$response" | grep -q '"status":"ok"'; then
        log "✅ 心跳成功"
        return 0
    else
        log "❌ 心跳失败: $response"
        return 1
    fi
}

# 设置自动维护
setup_auto() {
    log "设置自动维护..."
    
    local script_path
    script_path="$(cd "$(dirname "$0")" && pwd)/$(basename "$0")"
    
    # 检查是否已有 cron 任务
    if crontab -l 2>/dev/null | grep -q "evomap-maintainer"; then
        log "⚠️  自动任务已存在"
    else
        # 添加 cron 任务
        (crontab -l 2>/dev/null; echo "*/15 * * * * $script_path heartbeat >> /tmp/evomap-cron.log 2>&1") | crontab -
        log "✅ 已设置每15分钟自动心跳"
    fi
    
    log ""
    log "配置完成！当前设置:"
    log "  节点ID: $NODE_ID"
    log "  日志文件: $LOG_FILE"
    log "  查看日志: tail -f $LOG_FILE"
}

# 显示帮助
show_help() {
    cat << 'EOF'
EvoMap Auto Maintainer v1.0.0
自动维护 EvoMap 节点在线状态

用法: maintainer.sh [命令]

命令:
  status     检查节点当前状态
  heartbeat  立即发送一次心跳
  setup      设置自动维护（添加cron任务）
  help       显示此帮助

环境变量:
  EVOMAP_NODE_ID    你的 EvoMap 节点ID
  EVOMAP_SECRET     你的节点密钥
  EVOMAP_LOG        日志文件路径（默认/tmp/evomap-maintainer.log）

示例:
  export EVOMAP_NODE_ID="node_xxx"
  export EVOMAP_SECRET="your_secret"
  
  # 检查状态
  ./maintainer.sh status
  
  # 设置自动维护
  ./maintainer.sh setup
  
  # 手动发送心跳
  ./maintainer.sh heartbeat

购买此技能: clawhub install evomap-auto-maintainer
支持: zl18616313005@gmail.com
EOF
}

# 主函数
main() {
    case "${1:-help}" in
        status)
            check_status
            ;;
        heartbeat)
            send_heartbeat
            ;;
        setup)
            setup_auto
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            echo "未知命令: $1"
            show_help
            exit 1
            ;;
    esac
}

main "$@"
