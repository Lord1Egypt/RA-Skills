#!/bin/bash
set -e

# ====================== 【脚本用法说明 - v1.0.3 全量版】 ======================
# 技能名称：梓享AI双擎搜索（付费版）
# 用途：调用梓享AI官方付费搜索接口，返回结构化JSON搜索结果
# 核心关联：
#   - API Key获取地址：https://open.zixiangai.com/dashboard/index.html（梓享AI官方控制台）
#   - 官方接口调用地址：https://search.aiserver.cloud/v1/api（梓享AI搜索服务入口）
# 调用格式（参数依次对应）：
#   用法1（仅传搜索词，使用默认参数）：./search.sh "搜索关键词"
#   用法2（传全量自定义参数）：./search.sh "搜索关键词" "引擎类型" "返回条数" "时间过滤" "指定域名" "排除域名"
# 参数说明：
#   1. 搜索关键词（必填）：字符串，如"2026 AI行业动态"
#   2. 引擎类型（可选）：china（中国区，默认）/global（全球区）
#   3. 返回条数（可选）：1-20的整数，默认10
#   4. 时间过滤（可选）：day/week/month/year，默认空
#   5. 指定域名（可选）：JSON数组字符串，如"['baidu.com','zhihu.com']"，默认[]
#   6. 排除域名（可选）：JSON数组字符串，如"['xxx.com']"，默认[]
# 完整调用示例：
#   ./search.sh "2026 AI行业动态" "global" "20" "month" "['baidu.com']" "['xxx.com']"
# 鉴权依赖：环境变量 ZIXIANGAI_API_KEY（从梓享AI官方控制台获取）

# ====================== 1. 参数定义与默认值 ======================
QUERY="${1:-}"                  # 必选：用户输入的搜索关键词
ENGINE="${2:-china}"            # 可选：引擎类型，默认china
MAX_RESULTS="${3:-10}"          # 可选：返回结果条数，默认10
TIME_FILTER="${4:-}"            # 可选：时间过滤条件，默认空
INCLUDE_DOMAINS="${5:-[]}"      # 可选：指定搜索域名，默认空数组
EXCLUDE_DOMAINS="${6:-[]}"      # 可选：排除搜索域名，默认空数组

# ====================== 2. 全量参数校验（与官方接口要求对齐） ======================
# 校验搜索词不能为空（与官方接口ERR_PARAM错误提示对齐）
if [ -z "$QUERY" ]; then
  echo '{"code":"ERR_PARAM","msg":"参数异常：搜索词不能为空"}'
  exit 1
fi

# 校验返回条数为1-20的整数
if ! [[ "$MAX_RESULTS" =~ ^[0-9]+$ ]] || [ "$MAX_RESULTS" -lt 1 ] || [ "$MAX_RESULTS" -gt 20 ]; then
  echo '{"code":400,"msg":"参数异常：max_results必须是1-20的整数"}'
  exit 1
fi

# 校验引擎类型仅支持china/global
if [ "$ENGINE" != "china" ] && [ "$ENGINE" != "global" ]; then
  echo '{"code":400,"msg":"参数异常：engine只能是china或global"}'
  exit 1
fi

# ====================== 3. 接口调用核心逻辑 ======================
API_URL="https://search.aiserver.cloud/v1/api"  # 梓享AI官方搜索接口
API_KEY="${ZIXIANGAI_API_KEY}"                  # 鉴权Key（从官方控制台获取）

# 校验域名数组格式（不依赖 jq，仅做基本格式检查：必须以 [ 开头、] 结尾）
for _arr_name in INCLUDE_DOMAINS EXCLUDE_DOMAINS; do
  _arr_val="${!_arr_name}"
  if [[ "$_arr_val" != \[* ]] || [[ "$_arr_val" != *\] ]]; then
    echo "{\"code\":400,\"msg\":\"参数异常：${_arr_name} 须为合法JSON数组（如 [] 或 [\\\"baidu.com\\\"]）\"}"
    exit 1
  fi
done

# 纯 bash 转义字符串，防止 JSON 注入：转义反斜杠、双引号、换行、回车、制表符
json_str() {
  local s="$1"
  s="${s//\\/\\\\}"     # \ → \\
  s="${s//\"/\\\"}"     # " → \"
  s="${s//$'\n'/\\n}"   # 换行
  s="${s//$'\r'/\\r}"   # 回车
  s="${s//$'\t'/\\t}"   # 制表符
  printf '%s' "$s"
}

# 构建 JSON 请求体（无需 jq）
PAYLOAD=$(printf '{"engine":"%s","query":"%s","max_results":%s,"time_filter":"%s","include_domains":%s,"exclude_domains":%s}' \
  "$(json_str "$ENGINE")" \
  "$(json_str "$QUERY")" \
  "$MAX_RESULTS" \
  "$(json_str "$TIME_FILTER")" \
  "$INCLUDE_DOMAINS" \
  "$EXCLUDE_DOMAINS")

# 发送 POST 请求（适配官方接口参数格式）
curl -s -X POST "$API_URL" \
     -H "Content-Type: application/json; charset=utf-8" \
     -H "Authorization: Bearer ${API_KEY}" \
     -d "$PAYLOAD"