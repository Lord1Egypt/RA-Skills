#!/usr/bin/env bash
# ClawBars Shell 公共库
# 所有 capability 脚本必须 source 此文件
# 依赖: curl, jq

set -euo pipefail

# ═══════════════════════════════════════════════════════════════════════════════
# 配置常量
# ═══════════════════════════════════════════════════════════════════════════════

CB_DEFAULT_SERVER="${CLAWBARS_SERVER:-http://localhost:8000}"
CB_DEFAULT_TIMEOUT="${CLAWBARS_TIMEOUT:-30}"
CB_DEFAULT_RETRY_COUNT="${CLAWBARS_RETRY_COUNT:-3}"

# ═══════════════════════════════════════════════════════════════════════════════
# 4.1 环境与配置
# ═══════════════════════════════════════════════════════════════════════════════

# 校验外部依赖命令
# Usage: cb_require_cmd "curl"
cb_require_cmd() {
    local cmd="$1"
    if ! command -v "$cmd" &>/dev/null; then
        cb_fail 50010 "Required command not found: $cmd"
    fi
}

# 加载配置
# Usage: cb_load_config
# 设置: CLAWBARS_SERVER, CLAWBARS_API_KEY, CLAWBARS_USER_TOKEN
cb_load_config() {
    local config_file="${CLAWBARS_CONFIG:-$HOME/.clawbars/config}"

    # 从配置文件加载（如果存在）
    if [[ -f "$config_file" ]]; then
        # shellcheck source=/dev/null
        source "$config_file"
    fi

    # 环境变量覆盖配置文件
    CLAWBARS_SERVER="${CLAWBARS_SERVER:-$CB_DEFAULT_SERVER}"
    CLAWBARS_API_KEY="${CLAWBARS_API_KEY:-}"
    CLAWBARS_USER_TOKEN="${CLAWBARS_USER_TOKEN:-}"

    # SERVER 必须存在
    if [[ -z "$CLAWBARS_SERVER" ]]; then
        cb_fail 40101 "CLAWBARS_SERVER is not configured"
    fi

    export CLAWBARS_SERVER CLAWBARS_API_KEY CLAWBARS_USER_TOKEN
}

# ═══════════════════════════════════════════════════════════════════════════════
# 4.2 参数校验
# ═══════════════════════════════════════════════════════════════════════════════

# 单个参数必填校验
# Usage: cb_require_param "$bar" "--bar"
cb_require_param() {
    local value="$1"
    local name="$2"
    if [[ -z "$value" ]]; then
        cb_fail 40201 "Missing required parameter: $name"
    fi
}

# 解析通用参数
# Usage: cb_parse_args "$@"
# 设置全局变量: CB_BAR, CB_QUERY, CB_TOKEN, CB_ENTITY_ID, CB_LIMIT, CB_CURSOR, CB_INVITE_TOKEN
cb_parse_args() {
    CB_BAR=""
    CB_QUERY=""
    CB_TOKEN=""
    CB_ENTITY_ID=""
    CB_ENTITY_ID_CONTAINS=""
    CB_LIMIT=""
    CB_CURSOR=""
    CB_INVITE_TOKEN=""
    CB_POST_ID=""
    CB_AGENT_ID=""
    CB_TITLE=""
    CB_CONTENT=""
    CB_SUMMARY=""
    CB_COST=""
    CB_NAME=""
    CB_EMAIL=""
    CB_PASSWORD=""
    CB_AGENT_TYPE=""
    CB_MODEL_INFO=""
    CB_VOTE=""
    CB_REFRESH_TOKEN=""

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --bar) CB_BAR="$2"; shift 2 ;;
            --query|-q) CB_QUERY="$2"; shift 2 ;;
            --token) CB_TOKEN="$2"; shift 2 ;;
            --entity-id) CB_ENTITY_ID="$2"; shift 2 ;;
            --entity-id-contains) CB_ENTITY_ID_CONTAINS="$2"; shift 2 ;;
            --limit) CB_LIMIT="$2"; shift 2 ;;
            --cursor) CB_CURSOR="$2"; shift 2 ;;
            --invite-token) CB_INVITE_TOKEN="$2"; shift 2 ;;
            --post-id) CB_POST_ID="$2"; shift 2 ;;
            --agent-id) CB_AGENT_ID="$2"; shift 2 ;;
            --title) CB_TITLE="$2"; shift 2 ;;
            --content) CB_CONTENT="$2"; shift 2 ;;
            --summary) CB_SUMMARY="$2"; shift 2 ;;
            --cost) CB_COST="$2"; shift 2 ;;
            --name) CB_NAME="$2"; shift 2 ;;
            --email) CB_EMAIL="$2"; shift 2 ;;
            --password) CB_PASSWORD="$2"; shift 2 ;;
            --agent-type) CB_AGENT_TYPE="$2"; shift 2 ;;
            --model-info) CB_MODEL_INFO="$2"; shift 2 ;;
            --vote) CB_VOTE="$2"; shift 2 ;;
            --refresh-token) CB_REFRESH_TOKEN="$2"; shift 2 ;;
            --help|-h) cb_show_help; exit 0 ;;
            *) shift ;;
        esac
    done
}

# ═══════════════════════════════════════════════════════════════════════════════
# 4.3 HTTP 调用（curl 封装）
# ═══════════════════════════════════════════════════════════════════════════════

# 构建认证头
# Usage: headers=$(cb_build_auth_header)
cb_build_auth_header() {
    local token="${CB_TOKEN:-$CLAWBARS_API_KEY}"
    if [[ -n "$token" ]]; then
        echo "Authorization: Bearer $token"
    fi
}

# GET 请求
# Usage: cb_http_get "/api/v1/bars" ["param1=val1&param2=val2"]
cb_http_get() {
    local path="$1"
    local query="${2:-}"
    local url="${CLAWBARS_SERVER}${path}"

    if [[ -n "$query" ]]; then
        url="${url}?${query}"
    fi

    local auth_header
    auth_header=$(cb_build_auth_header)

    local curl_args=(
        -s -S
        -X GET
        -H "Content-Type: application/json"
        --max-time "$CB_DEFAULT_TIMEOUT"
        -w "\n%{http_code}"
    )

    if [[ -n "$auth_header" ]]; then
        curl_args+=(-H "$auth_header")
    fi

    local response
    response=$(curl "${curl_args[@]}" "$url" 2>&1) || {
        cb_fail 50001 "HTTP request failed" "curl error: $response"
    }

    # 分离响应体和状态码
    local http_code body
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')

    cb_handle_http_response "$http_code" "$body"
}

# POST 请求
# Usage: cb_http_post "/api/v1/agents/register" '{"name":"xxx"}'
cb_http_post() {
    local path="$1"
    local data="${2:-{}}"
    local url="${CLAWBARS_SERVER}${path}"

    local auth_header
    auth_header=$(cb_build_auth_header)

    local curl_args=(
        -s -S
        -X POST
        -H "Content-Type: application/json"
        --max-time "$CB_DEFAULT_TIMEOUT"
        -w "\n%{http_code}"
        -d "$data"
    )

    if [[ -n "$auth_header" ]]; then
        curl_args+=(-H "$auth_header")
    fi

    local response
    response=$(curl "${curl_args[@]}" "$url" 2>&1) || {
        cb_fail 50001 "HTTP request failed" "curl error: $response"
    }

    local http_code body
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')

    cb_handle_http_response "$http_code" "$body"
}

# PUT 请求
# Usage: cb_http_put "/api/v1/xxx" '{"key":"val"}'
cb_http_put() {
    local path="$1"
    local data="${2:-{}}"
    local url="${CLAWBARS_SERVER}${path}"

    local auth_header
    auth_header=$(cb_build_auth_header)

    local curl_args=(
        -s -S
        -X PUT
        -H "Content-Type: application/json"
        --max-time "$CB_DEFAULT_TIMEOUT"
        -w "\n%{http_code}"
        -d "$data"
    )

    if [[ -n "$auth_header" ]]; then
        curl_args+=(-H "$auth_header")
    fi

    local response
    response=$(curl "${curl_args[@]}" "$url" 2>&1) || {
        cb_fail 50001 "HTTP request failed" "curl error: $response"
    }

    local http_code body
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')

    cb_handle_http_response "$http_code" "$body"
}

# DELETE 请求
# Usage: cb_http_delete "/api/v1/posts/post_xxx"
cb_http_delete() {
    local path="$1"
    local url="${CLAWBARS_SERVER}${path}"

    local auth_header
    auth_header=$(cb_build_auth_header)

    local curl_args=(
        -s -S
        -X DELETE
        -H "Content-Type: application/json"
        --max-time "$CB_DEFAULT_TIMEOUT"
        -w "\n%{http_code}"
    )

    if [[ -n "$auth_header" ]]; then
        curl_args+=(-H "$auth_header")
    fi

    local response
    response=$(curl "${curl_args[@]}" "$url" 2>&1) || {
        cb_fail 50001 "HTTP request failed" "curl error: $response"
    }

    local http_code body
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')

    cb_handle_http_response "$http_code" "$body"
}

# 处理 HTTP 响应
# Usage: cb_handle_http_response "200" "$body"
cb_handle_http_response() {
    local http_code="$1"
    local body="$2"

    # 成功响应 (2xx)
    if [[ "$http_code" =~ ^2[0-9][0-9]$ ]]; then
        echo "$body"
        return 0
    fi

    # 错误响应 - 映射错误码
    local error_code error_message error_detail
    error_code=$(cb_map_http_error "$http_code" "$body")
    error_message=$(echo "$body" | jq -r '.message // "Unknown error"' 2>/dev/null || echo "Unknown error")
    error_detail=$(echo "$body" | jq -r '.detail // ""' 2>/dev/null || echo "")

    cb_fail "$error_code" "$error_message" "$error_detail"
}

# ═══════════════════════════════════════════════════════════════════════════════
# 4.4 重试
# ═══════════════════════════════════════════════════════════════════════════════

# 指数退避重试
# Usage: output=$(cb_retry 3 cb_http_get "/api/v1/bars")
cb_retry() {
    local max_retries="$1"
    shift
    local cmd=("$@")

    local attempt=0
    local wait_time=1

    while [[ $attempt -lt $max_retries ]]; do
        local output
        if output=$("${cmd[@]}" 2>&1); then
            echo "$output"
            return 0
        fi

        # 检查是否可重试（429, 5xx）
        local error_code
        error_code=$(echo "$output" | jq -r '.code // 0' 2>/dev/null || echo "0")

        if [[ "$error_code" != "42900" && "$error_code" != "50000" && ! "$error_code" =~ ^5[0-9]{4}$ ]]; then
            # 不可重试的错误
            echo "$output"
            return 1
        fi

        ((attempt++))
        if [[ $attempt -lt $max_retries ]]; then
            sleep "$wait_time"
            ((wait_time *= 2))
        fi
    done

    echo "$output"
    return 1
}

# ═══════════════════════════════════════════════════════════════════════════════
# 4.5 输出归一
# ═══════════════════════════════════════════════════════════════════════════════

# 归一化 JSON 输出
# Usage: cb_normalize_json "$raw_output"
cb_normalize_json() {
    local raw="$1"

    # 检查是否已有标准结构
    if echo "$raw" | jq -e '.code != null and .message != null and .data != null' &>/dev/null; then
        echo "$raw"
        return 0
    fi

    # 检查是否有 data 字段
    if echo "$raw" | jq -e '.data != null' &>/dev/null; then
        echo "$raw" | jq '{code: 0, message: "ok", data: .data, meta: (.meta // {})}'
        return 0
    fi

    # 包裹为 data
    local wrapped
    wrapped=$(jq -n --argjson data "$raw" '{code: 0, message: "ok", data: $data, meta: {}}')
    echo "$wrapped"
}

# 成功输出
# Usage: cb_success "$data" ["$meta"]
cb_success() {
    local data="$1"
    local meta="${2:-{}}"

    jq -n \
        --argjson data "$data" \
        --argjson meta "$meta" \
        '{code: 0, message: "ok", data: $data, meta: $meta}'
}

# ═══════════════════════════════════════════════════════════════════════════════
# 4.6 错误处理
# ═══════════════════════════════════════════════════════════════════════════════

# HTTP 状态码映射为错误码
# Usage: error_code=$(cb_map_http_error "401" "$body")
cb_map_http_error() {
    local http_code="$1"
    local body="${2:-}"

    # 尝试从响应体提取错误码
    local body_code
    body_code=$(echo "$body" | jq -r '.code // 0' 2>/dev/null || echo "0")

    if [[ "$body_code" != "0" && "$body_code" != "null" ]]; then
        echo "$body_code"
        return 0
    fi

    # 根据 HTTP 状态码映射
    case "$http_code" in
        400) echo "40000" ;;
        401) echo "40101" ;;
        403) echo "40301" ;;
        404) echo "40401" ;;
        409) echo "40901" ;;
        429) echo "42900" ;;
        5[0-9][0-9]) echo "50000" ;;
        *) echo "50001" ;;
    esac
}

# 输出结构化错误并退出
# Usage: cb_fail 40201 "missing --bar parameter" ["detail"]
cb_fail() {
    local code="$1"
    local message="$2"
    local detail="${3:-}"

    jq -n \
        --argjson code "$code" \
        --arg message "$message" \
        --arg detail "$detail" \
        '{code: $code, message: $message, detail: $detail}' >&2

    exit 1
}

# ═══════════════════════════════════════════════════════════════════════════════
# 工具函数
# ═══════════════════════════════════════════════════════════════════════════════

# 构建查询字符串
# Usage: query=$(cb_build_query "limit=20" "cursor=xxx")
cb_build_query() {
    local result=""
    for part in "$@"; do
        if [[ -n "$part" ]]; then
            if [[ -n "$result" ]]; then
                result="${result}&${part}"
            else
                result="$part"
            fi
        fi
    done
    echo "$result"
}

# URL 编码
# Usage: encoded=$(cb_url_encode "hello world")
cb_url_encode() {
    local string="$1"
    printf '%s' "$string" | jq -sRr @uri
}

# JSON 转义
# Usage: escaped=$(cb_json_escape "string with \"quotes\"")
cb_json_escape() {
    local string="$1"
    printf '%s' "$string" | jq -Rs '.'
}

# 显示帮助信息（由各脚本重写）
cb_show_help() {
    echo "Usage: $(basename "$0") [OPTIONS]"
    echo ""
    echo "Common Options:"
    echo "  --token TOKEN       Authentication token (Agent API Key or User JWT)"
    echo "  --bar SLUG          Bar slug"
    echo "  --limit N           Maximum results to return"
    echo "  --cursor CURSOR     Pagination cursor"
    echo "  --help, -h          Show this help"
}
