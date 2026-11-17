#!/usr/bin/env bash
# 商品检索 skill 的取数脚本。只依赖 curl，输出可直接贴给用户的商品清单。
#
# 用法:
#   ./search.sh "工业冷水机 注塑冷却"
#   ./search.sh "工业冷水机 注塑冷却" --price-max 10000 --location 河北
#   ./search.sh "包子机" --page-size 20 --json      # 要结构化字段时加 --json
#
# 说明:
#   query 只放商品词/用途/规格，预算与地域走 --price-max / --location 参数，
#   不要把"1万以内""上海的"这类词拼进 query，否则站内商品会一条都召回不到。
#
# 退出码: 0 成功 / 1 参数错误 / 2 请求失败或超时 / 3 接口返回业务错误

set -uo pipefail

BASE_URL="${B2B_SKILL_BASE_URL:-https://gwgp-zmtc8kkxxzw.i.bdcloudapi.com}"
APP_SOURCE="${B2B_SKILL_SOURCE:-workbuddy}"
TIMEOUT="${B2B_SKILL_TIMEOUT:-60}"

QUERY=""
PRICE_MIN=""
PRICE_MAX=""
LOCATION=""
CATEGORY=""
PAGE_SIZE=""
FORMAT="markdown"
RAW_JSON=0

usage() {
    sed -n '2,14p' "$0" | sed 's/^# \{0,1\}//'
    exit 1
}

while [ $# -gt 0 ]; do
    case "$1" in
        --price-min)  PRICE_MIN="${2:-}"; shift 2 ;;
        --price-max)  PRICE_MAX="${2:-}"; shift 2 ;;
        --location)   LOCATION="${2:-}";  shift 2 ;;
        --category)   CATEGORY="${2:-}";  shift 2 ;;
        --page-size)  PAGE_SIZE="${2:-}"; shift 2 ;;
        --format)     FORMAT="${2:-}";    shift 2 ;;
        --json)       RAW_JSON=1;         shift ;;
        -h|--help)    usage ;;
        -*)           echo "未知参数: $1" >&2; usage ;;
        *)            [ -z "$QUERY" ] && QUERY="$1" || QUERY="$QUERY $1"; shift ;;
    esac
done

[ -z "$QUERY" ] && { echo "缺少检索词" >&2; usage; }

# JSON 字符串转义: 反斜杠、双引号、制表与换行
json_escape() {
    printf '%s' "$1" | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g' -e 's/\t/ /g' | tr -d '\n'
}

BODY="{\"query\":\"$(json_escape "$QUERY")\",\"output_format\":\"$(json_escape "$FORMAT")\""
[ -n "$PRICE_MIN" ] && BODY="$BODY,\"price_min\":$PRICE_MIN"
[ -n "$PRICE_MAX" ] && BODY="$BODY,\"price_max\":$PRICE_MAX"
[ -n "$LOCATION" ]  && BODY="$BODY,\"location\":\"$(json_escape "$LOCATION")\""
[ -n "$CATEGORY" ]  && BODY="$BODY,\"category_id\":\"$(json_escape "$CATEGORY")\""
[ -n "$PAGE_SIZE" ] && BODY="$BODY,\"page_size\":$PAGE_SIZE"
BODY="$BODY}"

RESP="$(curl -sS --max-time "$TIMEOUT" -X POST "$BASE_URL/skill_api/product_search" \
    -H "Content-Type: application/json" \
    -H "X-App-Source: $APP_SOURCE" \
    -d "$BODY" 2>&1)" || {
    echo "请求失败(网络或超时)，本次取不到商品数据，请如实告知用户，不要臆造结果。" >&2
    echo "$RESP" >&2
    exit 2
}

[ -z "$RESP" ] && { echo "接口返回空响应，本次取不到商品数据。" >&2; exit 2; }

# 取 JSON 字段: 优先 python3, 其次 jq, 都没有就原样输出
extract() {  # $1=python 表达式 $2=jq 表达式
    if command -v python3 >/dev/null 2>&1; then
        printf '%s' "$RESP" | python3 -c "import sys,json; d=json.load(sys.stdin); print($1)" 2>/dev/null
    elif command -v jq >/dev/null 2>&1; then
        printf '%s' "$RESP" | jq -r "$2" 2>/dev/null
    else
        return 1
    fi
}

if [ "$RAW_JSON" = "1" ]; then
    extract 'json.dumps(d, ensure_ascii=False, indent=2)' '.' || printf '%s\n' "$RESP"
    exit 0
fi

CODE="$(extract 'd.get("code")' '.code')" || { printf '%s\n' "$RESP"; exit 0; }
if [ "$CODE" != "0" ]; then
    echo "接口返回错误 code=$CODE: $(extract 'd.get("message","")' '.message')" >&2
    exit 3
fi

extract 'd["data"]["content"]' '.data.content'
