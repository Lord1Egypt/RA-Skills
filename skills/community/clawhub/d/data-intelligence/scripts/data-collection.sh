#!/bin/bash
# 数据采集工作流模板
# Usage: ./data-collection.sh <actor-id> <search-term> <location>

ACTOR_ID=${1:-"compass/crawler-google-places"}
SEARCH_TERM=${2:-"coffee shop"}
LOCATION=${3:-"New York"}
OUTPUT_FILE="data-$(date +%Y%m%d-%H%M).csv"

echo "🚀 开始数据采集"
echo "Actor: $ACTOR_ID"
echo "搜索: $SEARCH_TERM"
echo "地点: $LOCATION"
echo ""

# 检查 APIFY_TOKEN
if [ -z "$APIFY_TOKEN" ]; then
  if [ -f .env ]; then
    export $(grep APIFY_TOKEN .env | xargs)
  else
    echo "❌ 错误: 未设置 APIFY_TOKEN"
    echo "请设置环境变量: export APIFY_TOKEN=your_token"
    exit 1
  fi
fi

# 运行采集
echo "📡 正在采集数据..."
mcpc --json mcp.apify.com \
  --header "Authorization: Bearer $APIFY_TOKEN" \
  tools-call run-actor \
  actor:="$ACTOR_ID" \
  input:="{\"searchStrings\": [\"$SEARCH_TERM\"], \"location\": \"$LOCATION\", \"maxCrawledPlaces\": 50}"

if [ $? -eq 0 ]; then
  echo ""
  echo "✅ 采集完成"
  echo "📁 数据已保存"
else
  echo ""
  echo "❌ 采集失败"
  exit 1
fi
