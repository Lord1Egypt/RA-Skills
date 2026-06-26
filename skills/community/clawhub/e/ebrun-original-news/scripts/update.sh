#!/usr/bin/env bash
# update.sh - 检查 ebrun-original-news Skill 是否有新版本
# 用法:
#   bash update.sh                                      # 默认输出 JSON 结果
#   bash update.sh --json                               # 输出 JSON 结果
#   bash update.sh --table                              # 输出文本结果
#   bash update.sh --timeout 10 --retries 3            # 调整超时与重试
#   bash update.sh --version-url <url>                 # 自定义版本接口地址

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VERSION_FILE="$SCRIPT_DIR/../references/version.json"
CACHE_FILE="${TMPDIR:-/tmp}/ebrun-original-news-version-cache.json"
SKILL_NAME="ebrun-original-news"
VERSION_API_URL="https://www.ebrun.com/_index/ClaudeCode/SkillJson/skill_version.json"
DEFAULT_TIMEOUT=10
DEFAULT_RETRIES=3
DEFAULT_CHECK_INTERVAL_HOURS=24
ALLOWED_DOMAINS=("www.ebrun.com" "api.ebrun.com" "github.com" "raw.githubusercontent.com" "gitee.com")
RETRYABLE_STATUS_CODES=(429 500 502 503 504)

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
    if [[ ! "$url" =~ ^https:// ]]; then return 1; fi
    local host
    host=$(echo "$url" | sed -E 's|^https://([^/]+).*|\1|')
    local domain
    for domain in "${ALLOWED_DOMAINS[@]}"; do
        if [[ "$host" == "$domain" ]] || [[ "$host" == *".$domain" ]]; then
            return 0
        fi
    done
    return 1
}

validate_positive_int() {
    local value="$1"
    local arg_name="$2"
    if ! [[ "$value" =~ ^[0-9]+$ ]] || [ "$value" -le 0 ]; then
        log_error "参数错误: $arg_name 必须大于 0"
        exit "$EXIT_USAGE_ERROR"
    fi
}

validate_url() {
    local url="$1"
    local label="$2"
    if [ -z "$url" ]; then
        log_error "参数错误: $label 不能为空"
        exit "$EXIT_USAGE_ERROR"
    fi
    if ! is_safe_url "$url"; then
        log_error "安全性风险: 非授权地址 -> $url"
        exit "$EXIT_SECURITY_ERROR"
    fi
}

json_get_field() {
    local json="$1"
    local field="$2"

    if command -v python3 >/dev/null 2>&1; then
        python3 -c "import sys, json; data=json.loads(sys.stdin.read()); value=data.get(sys.argv[1], ''); print(value if value is not None else '')" "$field" <<< "$json" 2>/dev/null
        return 0
    fi

    if command -v jq >/dev/null 2>&1; then
        jq -r --arg key "$field" '.[$key] // ""' <<< "$json" 2>/dev/null
        return 0
    fi

    sed -n -E "s/.*\"$field\"[[:space:]]*:[[:space:]]*\"([^\"]*)\".*/\1/p" <<< "$json" | head -1
}

json_get_raw_field() {
    local json="$1"
    local field="$2"

    if command -v python3 >/dev/null 2>&1; then
        python3 -c "import sys, json; data=json.loads(sys.stdin.read()); value=data.get(sys.argv[1], ''); print(value if value is not None else '')" "$field" <<< "$json" 2>/dev/null
        return 0
    fi

    if command -v jq >/dev/null 2>&1; then
        jq -r --arg key "$field" '.[$key] // ""' <<< "$json" 2>/dev/null
        return 0
    fi

    sed -n -E "s/.*\"$field\"[[:space:]]*:[[:space:]]*([^,}\"]+|\"[^\"]*\").*/\1/p" <<< "$json" | head -1 | sed 's/^"//; s/"$//'
}

validate_json_object() {
    local json="$1"
    if command -v python3 >/dev/null 2>&1; then
        if ! python3 -c 'import sys, json; data=json.loads(sys.stdin.read()); assert isinstance(data, dict)' <<< "$json" >/dev/null 2>&1; then
            log_error "接口返回格式异常: 顶层必须是对象"
            exit "$EXIT_JSON_ERROR"
        fi
        return 0
    fi

    if [[ ! "$json" =~ ^[[:space:]]*\{ ]]; then
        log_error "接口返回格式异常: 顶层必须是对象"
        exit "$EXIT_JSON_ERROR"
    fi
}

read_local_version_file() {
    if [ ! -f "$VERSION_FILE" ]; then
        log_error "未找到本地版本文件: $VERSION_FILE"
        exit "$EXIT_NOT_FOUND"
    fi
    local json
    json=$(cat "$VERSION_FILE")
    validate_json_object "$json"
    echo "$json"
}

read_cache_file() {
    if [ ! -f "$CACHE_FILE" ]; then
        echo '{}'
        return 0
    fi

    local json
    json=$(cat "$CACHE_FILE")

    if command -v python3 >/dev/null 2>&1; then
        if ! python3 -c 'import sys, json; data=json.loads(sys.stdin.read()); assert isinstance(data, dict)' <<< "$json" >/dev/null 2>&1; then
            log_warn "忽略损坏的版本缓存文件: $CACHE_FILE"
            echo '{}'
            return 0
        fi
    elif command -v jq >/dev/null 2>&1; then
        if ! jq -e 'type == "object"' >/dev/null 2>&1 <<< "$json"; then
            log_warn "忽略损坏的版本缓存文件: $CACHE_FILE"
            echo '{}'
            return 0
        fi
    elif [[ ! "$json" =~ ^[[:space:]]*\{ ]]; then
        log_warn "忽略损坏的版本缓存文件: $CACHE_FILE"
        echo '{}'
        return 0
    fi

    echo "$json"
}

persist_check_cache() {
    local version_api_url="$1"
    local last_check_time="$2"
    local last_known_version="$3"
    local last_check_source="$4"
    local last_update_available="$5"
    local last_version_file_url="$6"

    if [ -z "$last_known_version" ] || [ "$last_known_version" = "unknown" ]; then
        return 0
    fi

    if command -v python3 >/dev/null 2>&1; then
        python3 - "$CACHE_FILE" "$version_api_url" "$last_check_time" "$last_known_version" "$last_check_source" "$last_update_available" "$last_version_file_url" <<'PY'
import json
import sys

file_path = sys.argv[1]
version_api_url = sys.argv[2]
last_check_time = int(sys.argv[3])
last_known_version = sys.argv[4]
last_check_source = sys.argv[5]
last_update_available = sys.argv[6].lower() == 'true'
last_version_file_url = sys.argv[7]

data = {
    'version_api_url': version_api_url,
    'last_check_time': last_check_time,
    'last_known_version': last_known_version,
    'last_check_source': last_check_source,
    'last_update_available': last_update_available,
    'last_version_file_url': last_version_file_url,
}

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write('\n')
PY
        return 0
    fi

    if command -v jq >/dev/null 2>&1; then
        local tmp_file
        tmp_file=$(mktemp)
        jq \
            -n \
            --arg version_api_url "$version_api_url" \
            --argjson last_check_time "$last_check_time" \
            --arg last_known_version "$last_known_version" \
            --arg last_check_source "$last_check_source" \
            --argjson last_update_available "$last_update_available" \
            --arg last_version_file_url "$last_version_file_url" \
            '{version_api_url: $version_api_url,
              last_check_time: $last_check_time,
              last_known_version: $last_known_version,
              last_check_source: $last_check_source,
              last_update_available: $last_update_available,
              last_version_file_url: $last_version_file_url}' \
            > "$tmp_file"
        mv "$tmp_file" "$CACHE_FILE"
        return 0
    fi

    cat > "$CACHE_FILE" <<EOF
{
  "version_api_url": "$(json_escape "$version_api_url")",
  "last_check_time": $last_check_time,
  "last_known_version": "$(json_escape "$last_known_version")",
  "last_check_source": "$(json_escape "$last_check_source")",
  "last_update_available": $(json_bool "$last_update_available"),
  "last_version_file_url": "$(json_escape "$last_version_file_url")"
}
EOF
    return 0
}

http_error_message() {
    local status_code="$1"
    case "$status_code" in
        403) echo "版本接口请求被拒绝: HTTP 403" ;;
        404) echo "版本接口不存在: HTTP 404" ;;
        503) echo "版本接口暂时不可用: HTTP 503，可稍后重试" ;;
        *) echo "版本接口请求失败: HTTP $status_code" ;;
    esac
}

http_error_exit_code() {
    local status_code="$1"
    case "$status_code" in
        403) return "$EXIT_FORBIDDEN" ;;
        404) return "$EXIT_NOT_FOUND" ;;
        *) return "$EXIT_REQUEST_ERROR" ;;
    esac
}

network_error_message() {
    local curl_code="$1"
    case "$curl_code" in
        28) echo "版本接口请求超时，请稍后重试" ;;
        *) echo "版本接口请求失败: curl exit code $curl_code" ;;
    esac
}

is_retryable_http() {
    local status_code="$1"
    contains_value "$status_code" "${RETRYABLE_STATUS_CODES[@]}"
}

fetch_remote_version_json() {
    local version_url="$1"
    local timeout="$2"
    local retries="$3"

    validate_url "$version_url" "--version-url"

    local attempt=1
    while [ "$attempt" -le "$retries" ]; do
        local tmp_body tmp_stderr curl_code http_code message
        tmp_body=$(mktemp)
        tmp_stderr=$(mktemp)

        set +e
        http_code=$(curl -sS -o "$tmp_body" -w "%{http_code}" --max-time "$timeout" \
            -H "User-Agent: Mozilla/5.0 (EbrunSkillUpdate/1.0)" \
            -H "Accept: application/json, text/plain, */*" \
            -H "Referer: https://www.ebrun.com/" \
            "$version_url" 2>"$tmp_stderr")
        curl_code=$?
        set -e

        if [ "$curl_code" -eq 0 ] && [ "$http_code" = "200" ]; then
            cat "$tmp_body"
            rm -f "$tmp_body" "$tmp_stderr"
            return 0
        fi

        if [ "$curl_code" -ne 0 ]; then
            message=$(network_error_message "$curl_code")
            rm -f "$tmp_body" "$tmp_stderr"
            if [ "$curl_code" -eq 28 ] && [ "$attempt" -lt "$retries" ]; then
                log_warn "$message. 第 $attempt 次请求失败，准备重试..."
                sleep "$(( attempt < 2 ? attempt : 2 ))"
                attempt=$((attempt + 1))
                continue
            fi
            log_error "$message"
            return "$EXIT_REQUEST_ERROR"
        fi

        message=$(http_error_message "$http_code")
        rm -f "$tmp_body" "$tmp_stderr"
        if is_retryable_http "$http_code" && [ "$attempt" -lt "$retries" ]; then
            log_warn "$message. 第 $attempt 次请求失败，准备重试..."
            sleep "$(( attempt < 2 ? attempt : 2 ))"
            attempt=$((attempt + 1))
            continue
        fi

        log_error "$message"
        http_error_exit_code "$http_code"
        return $?
    done

    log_error "版本接口请求失败: 未知错误"
    return "$EXIT_REQUEST_ERROR"
}

check_url_reachable() {
    local url="$1"
    local timeout="$2"
    if [ -z "$url" ]; then
        return 1
    fi
    if ! is_safe_url "$url"; then
        return 1
    fi

    if curl -I -L -sS --max-time "$timeout" "$url" >/dev/null 2>&1; then
        return 0
    fi
    if curl -L -sS --max-time "$timeout" "$url" >/dev/null 2>&1; then
        return 0
    fi
    return 1
}

build_repo_version_file_urls() {
    local repo_url="$1"
    local candidates=""

    if [[ "$repo_url" =~ ^https://github\.com/([^/]+)/([^/]+) ]]; then
        local owner="${BASH_REMATCH[1]}"
        local repo="${BASH_REMATCH[2]}"
        printf '%s\n' "https://raw.githubusercontent.com/$owner/$repo/main/references/version.json"
        printf '%s\n' "https://raw.githubusercontent.com/$owner/$repo/master/references/version.json"
        return 0
    fi

    if [[ "$repo_url" =~ ^https://gitee\.com/([^/]+)/([^/]+) ]]; then
        local owner="${BASH_REMATCH[1]}"
        local repo="${BASH_REMATCH[2]}"
        printf '%s\n' "https://gitee.com/$owner/$repo/raw/main/references/version.json"
        printf '%s\n' "https://gitee.com/$owner/$repo/raw/master/references/version.json"
        return 0
    fi

    return 1
}

fetch_repo_version_json() {
    local repo_url="$1"
    local timeout="$2"
    local retries="$3"
    local candidate_url
    local fetch_output

    while IFS= read -r candidate_url; do
        [ -z "$candidate_url" ] && continue
        if fetch_output=$(fetch_remote_version_json "$candidate_url" "$timeout" "$retries" 2>/dev/null); then
            printf '%s\t%s\n' "$candidate_url" "$fetch_output"
            return 0
        fi
    done < <(build_repo_version_file_urls "$repo_url")

    return 1
}

json_bool() {
    case "$(printf '%s' "$1" | tr '[:upper:]' '[:lower:]')" in
        true|1|yes)
        printf 'true'
            ;;
        *)
        printf 'false'
            ;;
    esac
}

json_escape() {
    printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g'
}

print_json_result() {
    local skill_name="$1"
    local current_version="$2"
    local latest_version="$3"
    local update_available="$4"
    local check_source="$5"
    local status="$6"
    local message="$7"
    local github_url="$8"
    local gitee_url="$9"
    local github_reachable="${10}"
    local gitee_reachable="${11}"
    local remote_error="${12}"
    local version_api_url="${13}"
    local version_file_url="${14:-}"
    local repo_version_check_error="${15:-}"
    local remote_error_line=""
    local repo_version_check_error_line=""

    if [ -n "$remote_error" ]; then
        remote_error_line=$(printf ',\n  "remote_check_error": "%s"' "$(json_escape "$remote_error")")
    fi
    if [ -n "$repo_version_check_error" ]; then
        repo_version_check_error_line=$(printf ',\n  "repo_version_check_error": "%s"' "$(json_escape "$repo_version_check_error")")
    fi

    cat <<EOF
{
    "skill_name": "$(json_escape "$skill_name")",
    "current_version": "$(json_escape "$current_version")",
    "latest_version": "$(json_escape "$latest_version")",
  "update_available": $(json_bool "$update_available"),
    "check_source": "$(json_escape "$check_source")",
    "status": "$(json_escape "$status")",
    "version_api_url": "$(json_escape "$version_api_url")",
    "update_url_github": "$(json_escape "$github_url")",
    "update_url_gitee": "$(json_escape "$gitee_url")",
    "version_file_url": "$(json_escape "$version_file_url")",
  "update_url_github_reachable": $(json_bool "$github_reachable"),
    "update_url_gitee_reachable": $(json_bool "$gitee_reachable")$remote_error_line$repo_version_check_error_line,
    "message": "$(json_escape "$message")"
}
EOF
}

print_table_result() {
    local skill_name="$1"
    local current_version="$2"
    local latest_version="$3"
    local update_available="$4"
    local check_source="$5"
    local status="$6"
    local message="$7"
    local github_url="$8"
    local gitee_url="$9"
    local remote_error="${10}"
    local version_file_url="${11:-}"
    local repo_version_check_error="${12:-}"

    printf 'Skill 版本检查结果\n'
    printf -- '- skill_name: %s\n' "$skill_name"
    printf -- '- current_version: %s\n' "$current_version"
    printf -- '- latest_version: %s\n' "$latest_version"
    printf -- '- update_available: %s\n' "$update_available"
    printf -- '- check_source: %s\n' "$check_source"
    printf -- '- status: %s\n' "$status"
    printf -- '- message: %s\n' "$message"
    [ -n "$github_url" ] && printf -- '- update_url_github: %s\n' "$github_url"
    [ -n "$gitee_url" ] && printf -- '- update_url_gitee: %s\n' "$gitee_url"
    [ -n "$remote_error" ] && printf -- '- remote_check_error: %s\n' "$remote_error"
    [ -n "$version_file_url" ] && printf -- '- version_file_url: %s\n' "$version_file_url"
    [ -n "$repo_version_check_error" ] && printf -- '- repo_version_check_error: %s\n' "$repo_version_check_error"
    return 0
}

main() {
    local force_json=false
    local force_table=false
    local force_check=false
    local timeout="$DEFAULT_TIMEOUT"
    local retries="$DEFAULT_RETRIES"
    local version_url="$VERSION_API_URL"

    while [ $# -gt 0 ]; do
        case "$1" in
            --json) force_json=true; shift ;;
            --table) force_table=true; shift ;;
            --force) force_check=true; shift ;;
            --timeout)
                [ $# -lt 2 ] && { log_error "参数错误: --timeout 缺少值"; exit "$EXIT_USAGE_ERROR"; }
                timeout="$2"; shift 2 ;;
            --retries)
                [ $# -lt 2 ] && { log_error "参数错误: --retries 缺少值"; exit "$EXIT_USAGE_ERROR"; }
                retries="$2"; shift 2 ;;
            --version-url)
                [ $# -lt 2 ] && { log_error "参数错误: --version-url 缺少值"; exit "$EXIT_USAGE_ERROR"; }
                version_url="$2"; shift 2 ;;
            --help|-h) grep -E '^# ' "$0" | sed 's/^# //'; exit 0 ;;
            --*) log_error "参数错误: 不支持的选项 $1"; exit "$EXIT_USAGE_ERROR" ;;
            *) log_error "参数错误: update.sh 不接受位置参数"; exit "$EXIT_USAGE_ERROR" ;;
        esac
    done

    if $force_json && $force_table; then
        log_error "参数错误: --json 和 --table 不能同时使用"
        exit "$EXIT_USAGE_ERROR"
    fi

    validate_positive_int "$timeout" "--timeout"
    validate_positive_int "$retries" "--retries"

    local local_json cache_json current_version github_url gitee_url check_interval_hours last_check_time last_known_version last_check_source last_update_available last_version_file_url cached_version_api_url
    local_json=$(read_local_version_file)
    cache_json=$(read_cache_file)
    current_version=$(json_get_field "$local_json" "current_version")
    github_url=$(json_get_field "$local_json" "update_url_github")
    gitee_url=$(json_get_field "$local_json" "update_url_gitee")
    check_interval_hours=$(json_get_raw_field "$local_json" "check_interval_hours")
    last_check_time=$(json_get_raw_field "$cache_json" "last_check_time")
    last_known_version=$(json_get_field "$cache_json" "last_known_version")
    last_check_source=$(json_get_field "$cache_json" "last_check_source")
    last_update_available=$(json_get_raw_field "$cache_json" "last_update_available")
    last_version_file_url=$(json_get_field "$cache_json" "last_version_file_url")
    cached_version_api_url=$(json_get_field "$cache_json" "version_api_url")

    if [ -z "$current_version" ]; then
        log_error "本地 version.json 缺少 current_version"
        exit "$EXIT_JSON_ERROR"
    fi
    [ -z "$check_interval_hours" ] && check_interval_hours="$DEFAULT_CHECK_INTERVAL_HOURS"
    validate_positive_int "$check_interval_hours" "check_interval_hours"
    [ -z "$last_check_time" ] && last_check_time=0
    [ -z "$last_update_available" ] && last_update_available=false

    local now_ts interval_seconds
    now_ts=$(date +%s)
    interval_seconds=$(( check_interval_hours * 3600 ))

    local result_latest result_update_available result_source result_status result_message result_version_file_url="" repo_version_check_error=""
    local github_reachable=false gitee_reachable=false remote_error=""

    if ! $force_check && [ "$last_check_time" -gt 0 ] && [ -n "$last_known_version" ] && [ -n "$last_check_source" ] && [ -n "$cached_version_api_url" ] && [ "$cached_version_api_url" = "$version_url" ] && [ $(( now_ts - last_check_time )) -lt "$interval_seconds" ]; then
        result_latest="$last_known_version"
        result_update_available="$last_update_available"
        result_source="$last_check_source"
        result_status="cached"
        result_message="未到检查间隔，返回上次缓存结果"
        result_version_file_url="$last_version_file_url"

        if $force_table; then
            print_table_result "$SKILL_NAME" "$current_version" "$result_latest" "$result_update_available" "$result_source" "$result_status" "$result_message" "$github_url" "$gitee_url" "$remote_error" "$result_version_file_url" "$repo_version_check_error"
        else
            print_json_result "$SKILL_NAME" "$current_version" "$result_latest" "$result_update_available" "$result_source" "$result_status" "$result_message" "$github_url" "$gitee_url" "$github_reachable" "$gitee_reachable" "$remote_error" "$version_url" "$result_version_file_url" "$repo_version_check_error"
        fi
        return 0
    fi

    local remote_json remote_version remote_fetch_ok=true remote_stderr
    remote_stderr=$(mktemp)
    set +e
    remote_json=$(fetch_remote_version_json "$version_url" "$timeout" "$retries" 2>"$remote_stderr")
    local remote_exit=$?
    set -e
    if [ "$remote_exit" -ne 0 ]; then
        remote_fetch_ok=false
        remote_error=$(tr '\n' ' ' < "$remote_stderr" | sed 's/[[:space:]]*$//')
        remote_error=$(printf '%s' "$remote_error" | sed 's/^\[ERROR\][[:space:]]*//; s/^\[WARN\][[:space:]]*//')
        if [ -z "$remote_error" ]; then
            case "$remote_exit" in
                3) remote_error="安全性风险: 非授权版本接口地址" ;;
                5) remote_error="版本接口不存在: HTTP 404" ;;
                6) remote_error="版本接口请求被拒绝: HTTP 403" ;;
                7) remote_error="版本接口 JSON 解析失败" ;;
                *) remote_error="版本接口请求失败" ;;
            esac
        fi
    else
        validate_json_object "$remote_json"
        remote_version=$(json_get_field "$remote_json" "$SKILL_NAME")
        if [ -z "$remote_version" ]; then
            remote_fetch_ok=false
            remote_error="版本接口未返回 $SKILL_NAME 字段"
        fi
    fi
    rm -f "$remote_stderr"

    if $remote_fetch_ok; then
        result_latest="$remote_version"
        if [ "$result_latest" != "$current_version" ]; then
            result_update_available=true
            result_message="检测到新版本: $result_latest"
        else
            result_update_available=false
            result_message="检测完成"
        fi
        result_source="remote_api"
        result_status="ok"
    else
        local repo_fetch_payload="" repo_fetch_ok=false repo_source_name="" repo_version_json="" repo_current_version=""

        if [ -n "$gitee_url" ] && repo_fetch_payload=$(fetch_repo_version_json "$gitee_url" "$timeout" "$retries" 2>/dev/null); then
            repo_fetch_ok=true
            result_source="gitee_version_json"
        elif [ -n "$github_url" ] && repo_fetch_payload=$(fetch_repo_version_json "$github_url" "$timeout" "$retries" 2>/dev/null); then
            repo_fetch_ok=true
            result_source="github_version_json"
        fi

        if $repo_fetch_ok; then
            result_version_file_url="${repo_fetch_payload%%$'\t'*}"
            repo_version_json="${repo_fetch_payload#*$'\t'}"
            validate_json_object "$repo_version_json"
            repo_current_version=$(json_get_field "$repo_version_json" "current_version")
            if [ -z "$repo_current_version" ]; then
                repo_version_check_error="远端仓库 version.json 缺少 current_version"
                result_latest="unknown"
                result_update_available=false
                result_source="unavailable"
                result_status="degraded"
                result_message="版本接口不可用，且远端仓库 version.json 缺少 current_version，当前无法判断是否有新版本"
            else
                result_latest="$repo_current_version"
                if [ "$result_latest" != "$current_version" ]; then
                    result_update_available=true
                    result_message="版本接口不可用，已降级到远端仓库 version.json；检测到版本不一致: $current_version -> $result_latest"
                else
                    result_update_available=false
                    result_message="版本接口不可用，已降级到远端仓库 version.json；当前未发现版本变化"
                fi
                result_status="degraded"
            fi
        else
            result_latest="unknown"
            result_update_available=false
            result_source="unavailable"
            result_status="degraded"
            result_message="版本接口不可用，且无法从远端仓库读取 references/version.json，当前无法判断是否有新版本"
            repo_version_check_error="无法从 GitHub/Gitee 远端仓库读取 references/version.json"
        fi

        check_url_reachable "$github_url" "$timeout" && github_reachable=true
        check_url_reachable "$gitee_url" "$timeout" && gitee_reachable=true
    fi

    persist_check_cache \
        "$version_url" \
        "$now_ts" \
        "$result_latest" \
        "$result_source" \
        "$result_update_available" \
        "$result_version_file_url"

    if $force_table; then
        print_table_result "$SKILL_NAME" "$current_version" "$result_latest" "$result_update_available" "$result_source" "$result_status" "$result_message" "$github_url" "$gitee_url" "$remote_error" "$result_version_file_url" "$repo_version_check_error"
    else
        print_json_result "$SKILL_NAME" "$current_version" "$result_latest" "$result_update_available" "$result_source" "$result_status" "$result_message" "$github_url" "$gitee_url" "$github_reachable" "$gitee_reachable" "$remote_error" "$version_url" "$result_version_file_url" "$repo_version_check_error"
    fi
}

main "$@"
