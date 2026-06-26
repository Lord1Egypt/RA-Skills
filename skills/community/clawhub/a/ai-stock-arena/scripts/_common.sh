#!/bin/bash
# AI 股场通用函数

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG_FILE="$SKILL_DIR/config.json"

# 检查配置
check_config() {
    if [ ! -f "$CONFIG_FILE" ]; then
        echo "❌ 配置文件不存在"
        echo "请创建 $CONFIG_FILE 并配置 apiKey"
        echo ""
        echo "示例:"
        echo '{"apiKey": "ask_xxx", "baseUrl": "https://arena.wade.xylife.net/api"}'
        exit 1
    fi
}

# 读取配置
get_config() {
    local key="$1"
    local default="$2"
    jq -r ".$key // \"$default\"" "$CONFIG_FILE"
}

# API 请求
api_request() {
    local method="$1"
    local endpoint="$2"
    local data="$3"
    
    local api_key=$(get_config "apiKey" "")
    local base_url=$(get_config "baseUrl" "https://arena.wade.xylife.net/api")
    
    if [ -z "$api_key" ] || [ "$api_key" = "null" ]; then
        echo '{"success":false,"error":{"message":"API Key 未配置"}}'
        return 1
    fi
    
    curl -s -X "$method" \
        -H "Authorization: Bearer $api_key" \
        -H "Content-Type: application/json" \
        ${data:+-d "$data"} \
        "${base_url}${endpoint}"
}

# 格式化金额
format_money() {
    local amount="$1"
    local currency="${2:-CNY}"
    
    case "$currency" in
        CNY) printf "¥%.2f" "$amount" ;;
        HKD) printf "HK$%.2f" "$amount" ;;
        USD) printf "$%.2f" "$amount" ;;
        *) printf "%.2f" "$amount" ;;
    esac
}

# 格式化百分比
format_percent() {
    local pct="$1"
    local value=$(echo "$pct * 100" | bc 2>/dev/null || echo "0")
    printf "%+.2f%%" "$value"
}

# 颜色输出
red() { echo -e "\033[31m$1\033[0m"; }
green() { echo -e "\033[32m$1\033[0m"; }
yellow() { echo -e "\033[33m$1\033[0m"; }
