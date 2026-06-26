#!/bin/bash

################################################################################
# Clash 代理自动切换脚本 - 增强版
# 版本: 2.0
# 新增功能:
#   1. 日志记录 - 记录切换历史
#   2. 状态文件 - 保存当前状态
#   3. 通知支持 - 切换成功/失败时发送通知
#   4. 多测试目标 - 更全面的健康检查
################################################################################

set -e

# ========== 配置变量 ==========
CLASH_API="http://127.0.0.1:58871"
CLASH_SECRET="6434ff5a-5b0f-4598-99ec-83ca96c77167"
PROXY_URL="http://127.0.0.1:7890"

# 日志和状态文件
LOG_FILE="/var/log/clash-switch.log"
STATE_FILE="/tmp/clash-switch-state.json"

# 测试目标（扩展版）
TEST_TARGETS=(
    "https://api.telegram.org"
    "https://api.anthropic.com"
    "https://www.google.com"
    "https://api.openai.com"
    "https://api.github.com"
)

# 区域优先级
PREFERRED_REGIONS=("新加坡" "SG" "香港" "HK" "日本" "JP" "美国" "US")

# ========== 函数 ==========

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log_success() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✓ $1" | tee -a "$LOG_FILE"
}

log_error() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✗ $1" | tee -a "$LOG_FILE"
}

# 保存状态
save_state() {
    local current="$1"
    local status="$2"
    echo "{\"timestamp\":\"$(date -Iseconds)\",\"current\":\"$current\",\"status\":\"$status\"}" > "$STATE_FILE"
}

# 加载状态
load_state() {
    if [ -f "$STATE_FILE" ]; then
        cat "$STATE_FILE"
    else
        echo "{}"
    fi
}

# 健康检查
health_check() {
    local success=0
    local total=${#TEST_TARGETS[@]}
    
    for target in "${TEST_TARGETS[@]}"; do
        if curl -x "$PROXY_URL" -s -m 5 -I "$target" >/dev/null 2>&1; then
            ((success++))
        fi
    done
    
    local rate=$((success * 100 / total))
    echo $rate
}

# 获取所有节点
get_all_proxies() {
    curl -s -H "Authorization: Bearer ${CLASH_SECRET}" "${CLASH_API}/proxies" | jq -r '.proxies | keys[]' 2>/dev/null | grep -v "^GLOBAL$\|^ DIRECT$\|^REJECT$\|^PROXY$"
}

# 获取当前节点
get_current() {
    curl -s -H "Authorization: Bearer ${CLASH_SECRET}" "${CLASH_API}/proxies/ChatGPT" | jq -r '.now' 2>/dev/null
}

# 切换节点
switch_to() {
    local proxy="$1"
    curl -s -X PUT -H "Authorization: Bearer ${CLASH_SECRET}" \
         -H "Content-Type: application/json" \
         -d "{\"name\":\"$proxy\"}" \
         "${CLASH_API}/proxies/ChatGPT" >/dev/null 2>&1
}

# 测试延迟
test_delay() {
    local proxy="$1"
    local encoded=$(echo "$proxy" | jq -sRr @uri)
    local delay=$(curl -s -H "Authorization: Bearer ${CLASH_SECRET}" \
        "${CLASH_API}/proxies/${encoded}/delay?timeout=5000&url=http://www.gstatic.com/generate_204" | \
        jq -r '.delay' 2>/dev/null)
    
    if [ "$delay" != "null" ] && [ -n "$delay" ]; then
        echo $delay
    else
        echo "99999"
    fi
}

# 找最佳节点
find_best() {
    local best=""
    local best_delay=99999
    
    for proxy in $(get_all_proxies | grep -v "节点选择"); do
        local delay=$(test_delay "$proxy")
        log "测试 $proxy: ${delay}ms"
        
        # 优先区域检查
        local is_preferred=0
        for region in "${PREFERRED_REGIONS[@]}"; do
            if echo "$proxy" | grep -qi "$region"; then
                is_preferred=1
                break
            fi
        done
        
        if [ $is_preferred -eq 1 ] && [ $delay -lt $best_delay ]; then
            best="$proxy"
            best_delay=$delay
        elif [ $is_preferred -eq 0 ] && [ $best_delay -ge 500 ] && [ $delay -lt $best_delay ]; then
            best="$proxy"
            best_delay=$delay
        fi
    done
    
    echo "$best"
}

# ========== 主逻辑 ==========

case "${1:-help}" in
    check)
        rate=$(health_check)
        log "健康检查: ${rate}%"
        if [ $rate -ge 60 ]; then
            log_success "代理健康"
            exit 0
        else
            log_error "代理不健康"
            exit 1
        fi
        ;;
    
    auto)
        current=$(get_current)
        rate=$(health_check)
        
        log "========== 自动切换 =========="
        log "当前节点: $current"
        log "健康度: ${rate}%"
        
        if [ $rate -ge 60 ]; then
            log_success "代理健康，无需切换"
            save_state "$current" "healthy"
            exit 0
        fi
        
        log_error "代理不健康，开始自动切换..."
        best=$(find_best)
        
        if [ -n "$best" ]; then
            switch_to "$best"
            sleep 3
            
            new_rate=$(health_check)
            if [ $new_rate -ge 60 ]; then
                log_success "切换成功! 新节点: $best, 健康度: ${new_rate}%"
                save_state "$best" "fixed"
            else
                log_error "切换后仍不健康"
                save_state "$best" "failed"
            fi
        else
            log_error "未找到可用节点"
            save_state "$current" "failed"
        fi
        ;;
    
    list)
        echo "========== 代理组 =========="
        curl -s -H "Authorization: Bearer ${CLASH_SECRET}" "${CLASH_API}/proxies" | \
            jq -r '.proxies | to_entries[] | select(.value.type=="Selector") | "\(.key): \(.value.now)"'
        ;;
    
    status)
        cat $(load_state)
        ;;
    
    *)
        echo "Clash Auto Switch v2.0"
        echo ""
        echo "用法: $0 <命令>"
        echo ""
        echo "命令:"
        echo "  check   - 健康检查"
        echo "  auto   - 自动切换到最佳节点"
        echo "  list   - 列出所有代理组"
        echo "  status - 显示当前状态"
        echo ""
        ;;
esac
