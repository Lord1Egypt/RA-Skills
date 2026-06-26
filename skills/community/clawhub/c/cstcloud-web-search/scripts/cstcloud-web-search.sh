#!/bin/bash
#
# CSTCloud Web Search Tool
# Usage: ./cstcloud-web-search.sh <query> [count]
# Example: ./cstcloud-web-search.sh "大语言模型最新进展" 5

API_KEY="${CSTCLOUD_API_KEY:-}"
ENDPOINT="https://uni-api.cstcloud.cn/v1/web-search"
MODEL="web-search"

if [ -z "$API_KEY" ]; then
  echo "Error: CSTCLOUD_API_KEY environment variable is not set"
  echo "请先设置环境变量: export CSTCLOUD_API_KEY=your_key"
  exit 1
fi

QUERY="${1:-}"
COUNT="${2:-5}"

if [ -z "$QUERY" ]; then
  echo "Error: 搜索关键词不能为空"
  echo "Usage: $0 <query> [count]"
  exit 1
fi

if ! [[ "$COUNT" =~ ^[0-9]+$ ]] || [ "$COUNT" -lt 1 ] || [ "$COUNT" -gt 10 ]; then
  echo "Error: count 必须是 1-10 之间的数字"
  exit 1
fi

response=$(curl -s --connect-timeout 30 -X POST "$ENDPOINT" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d "$(jq -n --arg model "$MODEL" --arg query "$QUERY" --argjson count "$COUNT" \
    '{model: $model, query: $query, count: $count}')" 2>&1)

if ! echo "$response" | jq -e . >/dev/null 2>&1; then
  echo "Error: 请求失败或返回无效 JSON"
  echo "Response: $response"
  exit 1
fi

code=$(echo "$response" | jq -r '.code')
if [ "$code" != "200" ]; then
  msg=$(echo "$response" | jq -r '.msg // .message // empty')
  echo "Error: API 返回错误 [$code] $msg"
  exit 1
fi

results=$(echo "$response" | jq -c '.data.webPages.value // []')
total=$(echo "$results" | jq 'length')

if [ "$total" -eq 0 ] || [ "$total" == "null" ]; then
  echo "未找到相关结果。"
  exit 0
fi

echo "找到 $total 条结果（显示前 $COUNT 条）："
echo ""

echo "$results" | jq -r \
  --argjson count "$COUNT" \
  '.[0:$count] | .[] |
  "\(.name)\n   URL: \(.url)\n   来源: \(.siteName // empty)\n   摘要: \(.snippet | if length > 200 then .[0:200] + "..." else . end)\n"' 2>/dev/null

echo "=== 搜索完成 ==="
