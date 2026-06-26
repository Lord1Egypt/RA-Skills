#!/bin/bash
#
# Gate CrossEx API Shell 工具集
# 使用 curl 和 openssl 进行 API 调用
#

# 配置部分
API_KEY="${GATE_API_KEY}"
API_SECRET="${GATE_API_SECRET}"
BASE_URL="https://api.gateio.ws"
API_PREFIX="/api/v4/crossex"

# 检查环境变量
if [ -z "$API_KEY" ] || [ -z "$API_SECRET" ]; then
    echo "❌ 错误: 请设置环境变量 GATE_API_KEY 和 GATE_API_SECRET"
    echo "   export GATE_API_KEY=\"your_api_key\""
    echo "   export GATE_API_SECRET=\"your_api_secret\""
    exit 1
fi

# 生成签名函数
generate_signature() {
    local method="$1"
    local url="$2"
    local query_string="$3"
    local payload="$4"

    # 生成时间戳
    local timestamp=$(date +%s)

    # 计算 payload 的 SHA512 哈希
    local payload_hash=$(printf "%s" "$payload" | openssl dgst -sha512 -hex | awk '{print $2}')

    # 构造签名字符串
    local sign_string="${method}\n${url}\n${query_string}\n${payload_hash}\n${timestamp}"

    # 生成 HMAC-SHA512 签名
    local signature=$(printf "%b" "$sign_string" | openssl dgst -sha512 -hmac "$API_SECRET" -hex | awk '{print $2}')

    # 返回请求头
    echo "-H \"KEY: ${API_KEY}\""
    echo "-H \"Timestamp: ${timestamp}\""
    echo "-H \"SIGN: ${signature}\""
    echo "-H \"Accept: application/json\""
    echo "-H \"Content-Type: application/json\""
}

# 发送 GET 请求
api_get() {
    local endpoint="$1"
    local params="$2"

    local url="${BASE_URL}${API_PREFIX}${endpoint}"
    if [ -n "$params" ]; then
        url="${url}?${params}"
    fi

    local headers=$(generate_signature "GET" "${API_PREFIX}${endpoint}" "$params" "")

    eval curl -s -X GET \"${url}\" $headers
}

# 发送 POST 请求
api_post() {
    local endpoint="$1"
    local data="$2"

    local url="${BASE_URL}${API_PREFIX}${endpoint}"
    local headers=$(generate_signature "POST" "${API_PREFIX}${endpoint}" "" "$data")

    eval curl -s -X POST \"${url}\" $headers -d \"${data}\"
}

# ========== 公共接口 ==========

# 查询币对信息
get_symbols() {
    local symbols="$1"
    local params=""
    if [ -n "$symbols" ]; then
        params="symbols=${symbols}"
    fi

    echo "📊 查询币对信息..."
    api_get "/rule/symbols" "$params" | jq '.'
}

# 查询风险限额
get_risk_limits() {
    local symbols="$1"

    echo "⚠️  查询风险限额..."
    api_get "/rule/risk_limits" "symbols=${symbols}" | jq '.'
}

# 查询支持的币种
get_support_currencies() {
    echo "💰 查询支持的划转币种..."
    api_get "/rule/support_currencies" | jq '.'
}

# ========== 账户管理 ==========

# 查询账户资产
get_account() {
    echo "💼 查询账户资产..."
    api_get "/accounts" | jq '.'
}

# 查询杠杆仓位
get_margin_position() {
    echo "📈 查询杠杆仓位..."
    api_get "/position/margin" | jq '.'
}

# 查询合约仓位
get_futures_position() {
    echo "📊 查询合约仓位..."
    api_get "/position/futures" | jq '.'
}

# ========== 资金划转 ==========

# 资金划转
transfer_funds() {
    local currency="$1"
    local amount="$2"
    local from_account="$3"
    local to_account="$4"

    local data=$(cat <<EOF
{
  "currency": "${currency}",
  "amount": "${amount}",
  "from": "${from_account}",
  "to": "${to_account}"
}
EOF
)

    echo "💸 资金划转: ${amount} ${currency} 从 ${from_account} 到 ${to_account}..."
    api_post "/wallet/transfers" "$data" | jq '.'
}

# ========== 使用帮助 ==========

show_help() {
    cat <<HELP
Gate CrossEx API Shell 工具集

使用方法:
  export GATE_API_KEY="your_api_key"
  export GATE_API_SECRET="your_api_secret"
  source gate_crossex.sh

可用命令:

公共接口:
  get_symbols [symbols]              查询币对信息
  get_risk_limits <symbols>          查询风险限额
  get_support_currencies             查询支持的币种

账户管理:
  get_account                        查询账户资产
  get_margin_position                查询杠杆仓位
  get_futures_position               查询合约仓位

资金划转:
  transfer_funds <currency> <amount> <from> <to>  资金划转

示例:
  # 查询 BTC 价格
  get_symbols "BINANCE_FUTURE_BTC_USDT"

  # 查询账户资产
  get_account

  # 划转资金
  transfer_funds "USDT" "1000" "UNIFIED" "BINANCE"

HELP
}

# 导出函数
export -f get_symbols get_risk_limits get_support_currencies
export -b get_account get_margin_position get_futures_position
export -b transfer_funds

# 如果直接执行脚本，显示帮助
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    show_help
fi
