#!/usr/bin/env bash
# 厂家检索 skill 的取数脚本。只依赖 curl，输出可直接贴给用户的候选厂家清单。
#
# 用法:
#   ./search.sh "铝合金压铸件 定制加工"
#   ./search.sh "宠物零食" --capability OEM代工 --certification SC认证
#   ./search.sh "锂电池PACK" --location 广东深圳 --page-size 20 --json
#
# 说明:
#   检索词只放主营产品/加工能力，区域走 --location 参数。
#   默认不查店内在售商品(要多花几秒)；需要看厂内在售货时加 --with-products。
#   --capability/--certification/--business-type 只并入相关性排序、不做硬过滤，
#   返回里会带说明，转述时不要说成"已按该条件筛过"。
#
# 退出码: 0 成功 / 1 参数错误 / 2 请求失败或超时 / 3 接口返回业务错误

set -uo pipefail

BASE_URL="${B2B_SKILL_BASE_URL:-https://gwgp-zmtc8kkxxzw.i.bdcloudapi.com}"
APP_SOURCE="${B2B_SKILL_SOURCE:-workbuddy}"
TIMEOUT="${B2B_SKILL_TIMEOUT:-60}"

QUERY=""
LOCATION=""
CAPABILITY=""
CERTIFICATION=""
BUSINESS_TYPE=""
PAGE_SIZE=""
FORMAT="markdown"
WITH_PRODUCTS=""
RAW_JSON=0

usage() {
    sed -n '2,14p' "$0" | sed 's/^# \{0,1\}//'
    exit 1
}

while [ $# -gt 0 ]; do
    case "$1" in
        --location)      LOCATION="${2:-}";      shift 2 ;;
        --capability)    CAPABILITY="${2:-}";    shift 2 ;;
        --certification) CERTIFICATION="${2:-}"; shift 2 ;;
        --business-type) BUSINESS_TYPE="${2:-}"; shift 2 ;;
        --page-size)     PAGE_SIZE="${2:-}";     shift 2 ;;
        --format)        FORMAT="${2:-}";        shift 2 ;;
        --with-products) WITH_PRODUCTS="1";      shift ;;
        --json)          RAW_JSON=1;             shift ;;
        -h|--help)       usage ;;
        -*)              echo "未知参数: $1" >&2; usage ;;
        *)               [ -z "$QUERY" ] && QUERY="$1" || QUERY="$QUERY $1"; shift ;;
    esac
done

[ -z "$QUERY" ] && { echo "缺少检索词" >&2; usage; }

# JSON 字符串转义: 反斜杠、双引号、制表与换行
json_escape() {
    printf '%s' "$1" | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g' -e 's/\t/ /g' | tr -d '\n'
}

BODY="{\"query\":\"$(json_escape "$QUERY")\",\"output_format\":\"$(json_escape "$FORMAT")\""
[ -n "$LOCATION" ]      && BODY="$BODY,\"location\":\"$(json_escape "$LOCATION")\""
[ -n "$CAPABILITY" ]    && BODY="$BODY,\"capability\":\"$(json_escape "$CAPABILITY")\""
[ -n "$CERTIFICATION" ] && BODY="$BODY,\"certification\":\"$(json_escape "$CERTIFICATION")\""
[ -n "$BUSINESS_TYPE" ] && BODY="$BODY,\"business_type\":\"$(json_escape "$BUSINESS_TYPE")\""
[ -n "$PAGE_SIZE" ]     && BODY="$BODY,\"page_size\":$PAGE_SIZE"
[ -n "$WITH_PRODUCTS" ] && BODY="$BODY,\"with_products\":$WITH_PRODUCTS"
BODY="$BODY}"

RESP="$(curl -sS --max-time "$TIMEOUT" -X POST "$BASE_URL/skill_api/factory_search" \
    -H "Content-Type: application/json" \
    -H "X-App-Source: $APP_SOURCE" \
    -d "$BODY" 2>&1)" || {
    echo "请求失败(网络或超时)，本次取不到厂家数据，请如实告知用户，不要臆造结果。" >&2
    echo "$RESP" >&2
    exit 2
}

[ -z "$RESP" ] && { echo "接口返回空响应，本次取不到厂家数据。" >&2; exit 2; }

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
