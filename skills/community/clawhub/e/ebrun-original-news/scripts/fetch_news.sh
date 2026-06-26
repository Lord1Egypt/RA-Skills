#!/usr/bin/env bash
# fetch_news.sh - 获取亿邦动力网最新电商新闻
# 用法:
#   bash fetch_news.sh <channel_path_or_url>                  # 默认输出 JSON
#   bash fetch_news.sh <channel_path_or_url> --json           # 强制输出 JSON
#   bash fetch_news.sh <channel_path_or_url> --table          # 强制输出 ASCII 表格
#   bash fetch_news.sh <channel_path_or_url> --limit 10       # 仅返回前 10 条
#   bash fetch_news.sh <channel_path_or_url> --timeout 10     # 单次请求超时秒数
#   bash fetch_news.sh <channel_path_or_url> --retries 3      # 最大请求次数
#   bash fetch_news.sh --help                                 # 显示帮助

set -euo pipefail

# 配置
ALLOWED_DOMAINS=("www.ebrun.com" "api.ebrun.com")
DEFAULT_BASE_URL="https://www.ebrun.com/"
DEFAULT_LIMIT=10
DEFAULT_TIMEOUT=10
DEFAULT_RETRIES=3
RETRYABLE_STATUS_CODES=(429 500 502 503 504)
WIDTH=72

EXIT_USAGE_ERROR=2
EXIT_SECURITY_ERROR=3
EXIT_REQUEST_ERROR=4
EXIT_NOT_FOUND=5
EXIT_FORBIDDEN=6
EXIT_JSON_ERROR=7

log_error() { echo "[ERROR] $*" >&2; }
log_warn() { echo "[WARN] $*" >&2; }

contains_value() {
    local value="$1"
    shift
    local item
    for item in "$@"; do
        if [ "$item" = "$value" ]; then
            return 0
        fi
    done
    return 1
}

is_safe_url() {
    local url="$1"
    # 强制 HTTPS
    if [[ ! "$url" =~ ^https:// ]]; then return 1; fi
    
    # 提取 Host
    local host
    host=$(echo "$url" | sed -E 's|^https://([^/]+).*|\1|')
    
    for domain in "${ALLOWED_DOMAINS[@]}"; do
        if [[ "$host" == "$domain" ]] || [[ "$host" == *".$domain" ]]; then
            return 0
        fi
    done
    return 1
}

validate_limit() {
    local limit="$1"
    if ! [[ "$limit" =~ ^[0-9]+$ ]]; then
        log_error "参数错误: --limit 必须大于等于 0"
        exit "$EXIT_USAGE_ERROR"
    fi
}

validate_positive_int() {
    local value="$1"
    local arg_name="$2"
    if ! [[ "$value" =~ ^[0-9]+$ ]] || [ "$value" -le 0 ]; then
        log_error "参数错误: $arg_name 必须大于 0"
        exit "$EXIT_USAGE_ERROR"
    fi
}

validate_base_url() {
    local base_url="$1"
    if [ -z "$base_url" ]; then
        log_error "参数错误: --base-url 不能为空"
        exit "$EXIT_USAGE_ERROR"
    fi
    if ! is_safe_url "${base_url%/}/"; then
        log_error "安全性风险: 非授权基础地址 -> $base_url"
        exit "$EXIT_SECURITY_ERROR"
    fi
}

resolve_api_url() {
    local value="$1"
    local base_url="${2:-$DEFAULT_BASE_URL}"

    if [ -z "$value" ]; then
        log_error "参数错误: channel_path_or_url 不能为空"
        exit "$EXIT_USAGE_ERROR"
    fi

    if [[ "$value" =~ ^https?:// ]]; then
        echo "$value"
        return 0
    fi

    value="${value#/}"
    if [[ "$value" != *.json ]]; then
        value="$value.json"
    fi
    echo "${base_url%/}/$value"
}

check_deps() {
    if ! command -v curl &> /dev/null; then
        log_error "需要 curl 命令，请先安装 curl"
        exit "$EXIT_USAGE_ERROR"
    fi
}

validate_articles() {
    local json="$1"

    if command -v python3 &>/dev/null; then
        if ! python3 -c 'import sys, json; data=json.loads(sys.stdin.read()); assert isinstance(data, list); assert all(isinstance(i, dict) for i in data)' <<< "$json" >/dev/null 2>&1; then
            log_error "接口返回格式异常: 顶层数据必须是对象数组"
            exit "$EXIT_JSON_ERROR"
        fi
        return 0
    fi

    if [[ ! "$json" =~ ^[[:space:]]*\[ ]]; then
        log_error "接口返回格式异常: 顶层数据不是数组"
        exit "$EXIT_JSON_ERROR"
    fi
}

sanitize_articles() {
    local json="$1"

    if command -v python3 &>/dev/null; then
        python3 -c '
import json
import re
import sys
from urllib.parse import urlparse

allowed_domains = {"www.ebrun.com", "api.ebrun.com"}
control_char_re = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")

def normalize_text(value):
    if value is None:
        return ""
    text = str(value).replace("\r", " ").replace("\n", " ").replace("\t", " ")
    text = control_char_re.sub("", text)
    return " ".join(text.split())

def is_safe_url(url):
    try:
        parsed = urlparse(url)
        if parsed.scheme != "https" or not parsed.hostname:
            return False
        return any(parsed.hostname == domain or parsed.hostname.endswith("." + domain) for domain in allowed_domains)
    except Exception:
        return False

def normalize_url(value):
    normalized = normalize_text(value)
    return normalized if normalized and is_safe_url(normalized) else ""

data = json.loads(sys.stdin.read())
sanitized = []
for item in data:
    row = dict(item)
    for field in ("title", "author", "summary", "description", "publish_time", "publishTime"):
        if field in row:
            row[field] = normalize_text(row.get(field))
    for field in ("url", "link"):
        if field in row:
            row[field] = normalize_url(row.get(field))
    sanitized.append(row)

print(json.dumps(sanitized, ensure_ascii=False))
' <<< "$json"
        return 0
    fi

    echo "$json"
}

limit_articles() {
    local json="$1"
    local limit="$2"

    if [ "$limit" -eq 0 ]; then
        echo "$json"
        return 0
    fi

    if command -v python3 &>/dev/null; then
        python3 -c "import sys, json; data=json.loads(sys.stdin.read()); print(json.dumps(data[:int(sys.argv[1])], ensure_ascii=False))" "$limit" <<< "$json"
    else
        echo "$json"
    fi
}

map_http_exit_code() {
    local status_code="$1"
    case "$status_code" in
        403) return "$EXIT_FORBIDDEN" ;;
        404) return "$EXIT_NOT_FOUND" ;;
        *) return "$EXIT_REQUEST_ERROR" ;;
    esac
}

http_error_message() {
    local status_code="$1"
    case "$status_code" in
        403) echo "请求被拒绝: HTTP 403，请检查请求来源或访问限制" ;;
        404) echo "资源不存在: HTTP 404，请检查频道路径或该频道当前是否有数据" ;;
        503) echo "服务暂时不可用: HTTP 503，可稍后重试" ;;
        *) echo "请求失败: HTTP $status_code" ;;
    esac
}

is_retryable_http() {
    local status_code="$1"
    contains_value "$status_code" "${RETRYABLE_STATUS_CODES[@]}"
}

network_error_message() {
    local curl_code="$1"
    case "$curl_code" in
        28) echo "网络请求超时，请稍后重试" ;;
        *) echo "网络请求失败: curl exit code $curl_code" ;;
    esac
}

extract_field() {
    local json="$1"
    local field="$2"
    
    # 使用管道传参而非 argv，避免大型 JSON 触及系统参数长度限制 (ARG_MAX)
    if command -v python3 &>/dev/null; then
        python3 -c "import sys, json; data=json.loads(sys.stdin.read()); v=data.get(sys.argv[1], ''); print(v if v is not None else '')" "$field" <<< "$json" 2>/dev/null
    else
        # 降级方案：简单的正则提取
        echo "$json" | grep -o "\"$field\"[^\"]*\"[^\"]*\"" | sed -E 's/'"\"$field\":[[:space:]]*\"//; s/\"$//" | head -1
    fi
}

fetch_news() {
    local api_url="$1"
    local limit="$2"
    local retries="$3"
    local timeout="$4"
    
    if ! is_safe_url "$api_url"; then
        log_error "安全性风险: 禁止请求非授权域名或不安全协议 -> $api_url"
        return "$EXIT_SECURITY_ERROR"
    fi

    local attempt=1
    local last_exit_code="$EXIT_REQUEST_ERROR"
    while [ "$attempt" -le "$retries" ]; do
        local tmp_body tmp_stderr curl_code http_code json message
        tmp_body=$(mktemp)
        tmp_stderr=$(mktemp)

        set +e
        http_code=$(curl -sS -o "$tmp_body" -w "%{http_code}" --max-time "$timeout" \
            -H "User-Agent: Mozilla/5.0 (EbrunSkill/1.0)" \
            -H "Accept: application/json, text/plain, */*" \
            -H "Referer: https://www.ebrun.com/" \
            "$api_url" 2>"$tmp_stderr")
        curl_code=$?
        set -e

        if [ "$curl_code" -eq 0 ] && [ "$http_code" = "200" ]; then
            json=$(cat "$tmp_body")
            rm -f "$tmp_body" "$tmp_stderr"
            validate_articles "$json"
            json=$(sanitize_articles "$json")
            limit_articles "$json" "$limit"
            return 0
        fi

        if [ "$curl_code" -ne 0 ]; then
            message=$(network_error_message "$curl_code")
            last_exit_code="$EXIT_REQUEST_ERROR"
        else
            message=$(http_error_message "$http_code")
            map_http_exit_code "$http_code"
            last_exit_code=$?
        fi

        rm -f "$tmp_body" "$tmp_stderr"

        if { [ "$curl_code" -eq 28 ] || { [ "$curl_code" -eq 0 ] && is_retryable_http "$http_code"; }; } && [ "$attempt" -lt "$retries" ]; then
            log_warn "$message. 第 $attempt 次请求失败，准备重试..."
            sleep "$(( attempt < 2 ? attempt : 2 ))"
            attempt=$((attempt + 1))
            continue
        fi

        log_error "$message"
        return "$last_exit_code"
    done

    log_error "获取数据失败: 未知错误"
    return "$EXIT_REQUEST_ERROR"
}

print_ascii_table() {
    local json="$1"

    if [ "$json" = "[]" ] || [ -z "$json" ]; then
        echo "暂无文章数据"
        return
    fi

    # 格式化 JSON 为每行一个对象
    local items
    if command -v python3 &>/dev/null; then
        items=$(python3 -c "import sys, json; data=json.loads(sys.stdin.read()); [print(json.dumps(i)) for i in data]" <<< "$json")
    else
        items=$(echo "$json" | sed 's/^\[//; s/]$//; s/},{/}\n{/g')
    fi

    echo
    printf "┌%*s┐\n" $((WIDTH - 2)) "" | sed 's/ /─/g'
    printf "│  亿邦动力网 - 最新电商新闻%*s│\n" $((WIDTH - 2 - 24)) ""
    printf "├%*s┤\n" $((WIDTH - 2)) "" | sed 's/ /─/g'

    local i=0
    while IFS= read -r article; do
        [ -z "$article" ] && continue
        i=$((i + 1))

        local title=$(extract_field "$article" "title")
        local author=$(extract_field "$article" "author")
        local pub_time=$(extract_field "$article" "publish_time")
        [ -z "$pub_time" ] && pub_time=$(extract_field "$article" "publishTime")
        local summary=$(extract_field "$article" "summary")
        [ -z "$summary" ] && summary=$(extract_field "$article" "description")
        local url=$(extract_field "$article" "url")
        [ -z "$url" ] && url=$(extract_field "$article" "link")

        printf "│  %2d. %-58s │\n" "$i" "${title:0:58}"
        printf "│       👤 %-12s  🕐 %-16s │\n" "${author:0:12}" "${pub_time:0:16}"
        printf "│       %-*s │\n" $((WIDTH - 8)) "${summary:0:64}"
        [ -n "$url" ] && printf "│       %-*s │\n" $((WIDTH - 8)) "${url:0:64}"
        
        # 简单分割线
        printf "├%*s┤\n" $((WIDTH - 2)) "" | sed 's/ /─/g'
    done <<<"$items"

    echo "共 $i 篇文章"
}

main() {
    local input_value=""
    local force_json=false
    local force_table=false
    local base_url="$DEFAULT_BASE_URL"
    local limit="$DEFAULT_LIMIT"
    local timeout="$DEFAULT_TIMEOUT"
    local retries="$DEFAULT_RETRIES"

    while [ $# -gt 0 ]; do
        case "$1" in
            --json) force_json=true; shift ;;
            --table) force_table=true; shift ;;
            --base-url)
                [ $# -lt 2 ] && { log_error "参数错误: --base-url 缺少值"; exit "$EXIT_USAGE_ERROR"; }
                base_url="$2"; shift 2 ;;
            --limit)
                [ $# -lt 2 ] && { log_error "参数错误: --limit 缺少值"; exit "$EXIT_USAGE_ERROR"; }
                limit="$2"; shift 2 ;;
            --timeout)
                [ $# -lt 2 ] && { log_error "参数错误: --timeout 缺少值"; exit "$EXIT_USAGE_ERROR"; }
                timeout="$2"; shift 2 ;;
            --retries)
                [ $# -lt 2 ] && { log_error "参数错误: --retries 缺少值"; exit "$EXIT_USAGE_ERROR"; }
                retries="$2"; shift 2 ;;
            --help|-h) grep -E '^# ' "$0" | sed 's/^# //'; exit 0 ;;
            --*) log_error "参数错误: 不支持的选项 $1"; exit "$EXIT_USAGE_ERROR" ;;
            *)
                if [ -n "$input_value" ]; then
                    log_error "参数错误: 仅支持一个 channel_path_or_url"
                    exit "$EXIT_USAGE_ERROR"
                fi
                input_value="$1"; shift ;;
        esac
    done

    if [ -z "$input_value" ]; then
        log_error "缺少参数: channel_path_or_url"
        exit "$EXIT_USAGE_ERROR"
    fi

    if $force_json && $force_table; then
        log_error "参数错误: --json 和 --table 不能同时使用"
        exit "$EXIT_USAGE_ERROR"
    fi

    check_deps
    validate_limit "$limit"
    validate_positive_int "$timeout" "--timeout"
    validate_positive_int "$retries" "--retries"
    validate_base_url "$base_url"

    local api_url
    api_url=$(resolve_api_url "$input_value" "$base_url")
    local json
    json=$(fetch_news "$api_url" "$limit" "$retries" "$timeout")

    if $force_json || ! $force_table; then
        if command -v python3 &>/dev/null; then
            echo "$json" | python3 -m json.tool
        else
            echo "$json"
        fi
    else
        print_ascii_table "$json"
    fi
}

main "$@"
