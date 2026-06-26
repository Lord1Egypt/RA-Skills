#!/bin/bash

################################################################################
# Clash 代理自动切换脚本
# 版本: 1.0
# 功能:
#   1. 健康检查：测试当前代理连通性
#   2. 自动切换：检测到故障时自动切换节点
#   3. 区域优先：优先选择美国/新加坡节点
################################################################################

set -e

# 配置变量
CLASH_API="http://127.0.0.1:58871"
CLASH_SECRET="6434ff5a-5b0f-4598-99ec-83ca96c77167"
PROXY_URL="http://127.0.0.1:7890"

# 测试目标（用于验证代理连通性）
TEST_TARGETS=(
    "https://api.telegram.org"
    "https://api.anthropic.com"
    "https://www.google.com"
)

# 区域优先级（新加坡 > 香港 > 日本 > 其他）- 美国延迟高
PREFERRED_REGIONS=("新加坡" "🇸🇬" "SG" "Singapore" "香港" "🇭🇰" "HK" "Hong Kong" "日本" "🇯🇵" "JP" "Japan")

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 日志函数
log_info() { echo -e "${GREEN}[INFO]${NC} $(date '+%Y-%m-%d %H:%M:%S') $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $(date '+%Y-%m-%d %H:%M:%S') $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $(date '+%Y-%m-%d %H:%M:%S') $1"; }
log_success() { echo -e "${GREEN}[OK]${NC} $(date '+%Y-%m-%d %H:%M:%S') $1"; }

# URL 编码函数
urlencode() {
    local string="$1"
    python3 -c "import urllib.parse; print(urllib.parse.quote('''$string'''))" 2>/dev/null || \
    echo "$string" | sed 's/ /%20/g'
}

# Clash API 调用
clash_api_get() {
    local endpoint="$1"
    curl -s -H "Authorization: Bearer ${CLASH_SECRET}" "${CLASH_API}${endpoint}"
}

clash_api_put() {
    local endpoint="$1"
    local data="$2"
    curl -s -X PUT -H "Authorization: Bearer ${CLASH_SECRET}" \
         -H "Content-Type: application/json" \
         -d "${data}" "${CLASH_API}${endpoint}"
}

# 测试代理连通性
test_proxy() {
    local target="$1"
    local timeout=10

    if curl -x "${PROXY_URL}" -s -m ${timeout} -I "${target}" >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# 全面健康检查
health_check() {
    log_info "开始健康检查..."

    local success_count=0
    local total_count=${#TEST_TARGETS[@]}

    for target in "${TEST_TARGETS[@]}"; do
        if test_proxy "$target"; then
            log_success "✓ ${target} 可达"
            ((success_count++))
        else
            log_error "✗ ${target} 不可达"
        fi
    done

    local success_rate=$((success_count * 100 / total_count))
    log_info "健康检查完成: ${success_count}/${total_count} (${success_rate}%)"

    if [ $success_rate -ge 66 ]; then
        return 0  # 健康
    else
        return 1  # 不健康
    fi
}

# 获取所有可用节点
get_all_proxies() {
    clash_api_get "/proxies" | jq -r '.proxies | keys[]' 2>/dev/null | grep -v "^GLOBAL$\|^DIRECT$\|^REJECT$\|^PROXY$\|^♻️\|^🔰\|^⚓️\|^✈️\|^🎬\|^🎮\|^🍎\|^🎨\|^❗\|^🚀"
}

# 获取当前选中的节点
get_current_proxy() {
    clash_api_get "/proxies/PROXY" | jq -r '.now' 2>/dev/null
}

# 切换到指定节点
switch_proxy() {
    local proxy_name="$1"
    local result=$(clash_api_put "/proxies/PROXY" "{\"name\":\"${proxy_name}\"}")

    if [ $? -eq 0 ]; then
        log_success "已切换到节点: ${proxy_name}"
        return 0
    else
        log_error "切换失败: ${proxy_name}"
        return 1
    fi
}

# 测试节点延迟
test_proxy_delay() {
    local proxy_name="$1"
    local encoded_name=$(urlencode "$proxy_name")
    local delay=$(clash_api_get "/proxies/${encoded_name}/delay?timeout=5000&url=http://www.gstatic.com/generate_204" | jq -r '.delay' 2>/dev/null)

    if [ "$delay" != "null" ] && [ -n "$delay" ] && [ "$delay" != "0" ]; then
        echo "$delay"
        return 0
    else
        echo "9999"  # 超时或不可用
        return 1
    fi
}

# 检查节点是否属于优先区域
is_preferred_region() {
    local proxy_name="$1"

    for region in "${PREFERRED_REGIONS[@]}"; do
        if echo "$proxy_name" | grep -qi "$region"; then
            return 0
        fi
    done

    return 1
}

# 获取最佳节点（优先区域 + 最低延迟）
get_best_proxy() {
    log_info "正在测试所有节点..."

    local best_proxy=""
    local best_delay=9999
    local preferred_proxy=""
    local preferred_delay=9999

    # 获取所有节点
    local proxies=$(get_all_proxies | grep -v "DIRECT\|REJECT\|PROXY\|GLOBAL")

    while IFS= read -r proxy; do
        [ -z "$proxy" ] && continue

        log_info "测试节点: ${proxy}"
        local delay=$(test_proxy_delay "$proxy")

        log_info "  延迟: ${delay}ms"

        # 检查是否属于优先区域
        if is_preferred_region "$proxy"; then
            log_info "  ★ 优先区域节点"
            if [ "$delay" -lt "$preferred_delay" ]; then
                preferred_proxy="$proxy"
                preferred_delay="$delay"
            fi
        fi

        # 记录全局最佳节点
        if [ "$delay" -lt "$best_delay" ]; then
            best_proxy="$proxy"
            best_delay="$delay"
        fi
    done <<< "$proxies"

    # 优先返回优先区域的最佳节点
    if [ -n "$preferred_proxy" ] && [ "$preferred_delay" -lt 3000 ]; then
        echo "$preferred_proxy"
        log_success "选择优先区域节点: ${preferred_proxy} (${preferred_delay}ms)"
        return 0
    elif [ -n "$best_proxy" ]; then
        echo "$best_proxy"
        log_success "选择最佳节点: ${best_proxy} (${best_delay}ms)"
        return 0
    else
        log_error "未找到可用节点"
        return 1
    fi
}

# 自动切换到最佳节点
auto_switch() {
    log_info "========== Clash 自动切换 =========="

    # 1. 检查当前健康状态
    local current_proxy=$(get_current_proxy)
    log_info "当前节点: ${current_proxy}"

    if health_check; then
        log_success "当前代理健康，无需切换"
        return 0
    fi

    log_warn "当前代理不健康，开始寻找最佳节点..."

    # 2. 寻找最佳节点
    local best_proxy=$(get_best_proxy)

    if [ -z "$best_proxy" ]; then
        log_error "未找到可用节点"
        return 1
    fi

    # 3. 切换到最佳节点
    if [ "$best_proxy" != "$current_proxy" ]; then
        switch_proxy "$best_proxy"

        # 4. 等待并重新检查
        log_info "等待5秒后重新检查..."
        sleep 5

        if health_check; then
            log_success "切换成功！代理已恢复正常"
            return 0
        else
            log_error "切换后仍不健康，可能需要手动干预"
            return 1
        fi
    else
        log_info "当前已是最佳节点，但连接仍有问题"
        return 1
    fi
}

# 列出所有节点
list_proxies() {
    log_info "========== 可用节点列表 =========="

    local current_proxy=$(get_current_proxy)
    local proxies=$(get_all_proxies | grep -v "DIRECT\|REJECT\|PROXY\|GLOBAL")

    while IFS= read -r proxy; do
        [ -z "$proxy" ] && continue

        local marker=" "
        [ "$proxy" = "$current_proxy" ] && marker="★"

        local region_marker=""
        if is_preferred_region "$proxy"; then
            region_marker=" ${GREEN}[优先]${NC}"
        fi

        echo -e "${marker} ${proxy}${region_marker}"
    done <<< "$proxies"
}

# 手动切换节点
manual_switch() {
    local target_proxy="$1"

    if [ -z "$target_proxy" ]; then
        log_error "请指定节点名称"
        list_proxies
        return 1
    fi

    switch_proxy "$target_proxy"

    log_info "等待5秒后检查..."
    sleep 5

    health_check
}

# 区域切换（美国/新加坡）
region_switch() {
    local region="$1"

    log_info "正在搜索 ${region} 区域节点..."

    local proxies=$(get_all_proxies | grep -v "DIRECT\|REJECT\|PROXY\|GLOBAL")
    local region_proxies=""

    case "$region" in
        "us"|"USA"|"美国")
            region_proxies=$(echo "$proxies" | grep -E "美国|🇺🇲")
            ;;
        "sg"|"SG"|"新加坡")
            region_proxies=$(echo "$proxies" | grep -E "新加坡|🇸🇬")
            ;;
        *)
            log_error "不支持的区域: ${region}"
            log_info "支持的区域: us (美国), sg (新加坡)"
            return 1
            ;;
    esac

    if [ -z "$region_proxies" ]; then
        log_error "未找到 ${region} 区域节点"
        return 1
    fi

    log_info "找到以下节点："
    echo "$region_proxies" | while read -r proxy; do
        echo "  - ${proxy}"
    done

    # 测试并选择最佳节点
    local best_proxy=""
    local best_delay=9999

    while IFS= read -r proxy; do
        [ -z "$proxy" ] && continue

        local delay=$(test_proxy_delay "$proxy")
        log_info "${proxy}: ${delay}ms"

        if [ "$delay" -lt "$best_delay" ]; then
            best_proxy="$proxy"
            best_delay="$delay"
        fi
    done <<< "$region_proxies"

    if [ -n "$best_proxy" ]; then
        switch_proxy "$best_proxy"
        sleep 5
        health_check
    else
        log_error "未找到可用节点"
        return 1
    fi
}

# 使用说明
usage() {
    cat << EOF
Clash 代理自动切换脚本 v1.0

用法: $0 [命令] [参数]

命令:
  check       健康检查当前代理
  auto        自动切换到最佳节点（推荐）
  list        列出所有可用节点
  switch      手动切换到指定节点
  us          切换到美国节点
  sg          切换到新加坡节点
  help        显示此帮助信息

示例:
  $0 check                    # 检查当前代理健康状态
  $0 auto                     # 自动切换到最佳节点
  $0 list                     # 列出所有节点
  $0 switch "美国 01"         # 切换到指定节点
  $0 us                       # 切换到最佳美国节点
  $0 sg                       # 切换到最佳新加坡节点

配置:
  Clash API: ${CLASH_API}
  代理地址:  ${PROXY_URL}
  控制密钥:  ${CLASH_SECRET}

EOF
}

# 主函数
main() {
    local command="${1:-help}"

    case "$command" in
        check)
            health_check
            ;;
        auto)
            auto_switch
            ;;
        list)
            list_proxies
            ;;
        switch)
            manual_switch "$2"
            ;;
        us|usa|美国)
            region_switch "us"
            ;;
        sg|singapore|新加坡)
            region_switch "sg"
            ;;
        help|--help|-h)
            usage
            ;;
        *)
            log_error "未知命令: $command"
            echo ""
            usage
            exit 1
            ;;
    esac
}

# 执行主函数
main "$@"
