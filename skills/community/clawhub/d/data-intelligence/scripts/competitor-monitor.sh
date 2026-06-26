#!/bin/bash
# 竞品监测脚本
# Usage: ./competitor-monitor.sh <competitor-list-file>

COMPETITOR_FILE=${1:-"competitors.txt"}
DATE=$(date +%Y%m%d)
DATA_DIR="competitor-data"

mkdir -p "$DATA_DIR"

if [ ! -f "$COMPETITOR_FILE" ]; then
  echo "❌ 错误: 未找到 $COMPETITOR_FILE"
  echo "请创建文件，每行一个竞品 Instagram 用户名"
  exit 1
fi

# 检查 APIFY_TOKEN
if [ -z "$APIFY_TOKEN" ]; then
  if [ -f .env ]; then
    export $(grep APIFY_TOKEN .env | xargs)
  else
    echo "❌ 错误: 未设置 APIFY_TOKEN"
    exit 1
  fi
fi

echo "🔍 开始监测竞品..."
echo "日期: $DATE"
echo ""

while IFS= read -r competitor; do
  [ -z "$competitor" ] && continue

  echo "分析: @$competitor"

  # 采集数据
  mcpc --json mcp.apify.com \
    --header "Authorization: Bearer $APIFY_TOKEN" \
    tools-call run-actor \
    actor:="apify/instagram-profile-scraper" \
    input:="{\"usernames\": [\"$competitor\"]}" \
    > "$DATA_DIR/${competitor}-${DATE}.json" 2>/dev/null

  if [ $? -eq 0 ]; then
    # 提取关键指标
    followers=$(cat "$DATA_DIR/${competitor}-${DATE}.json" | jq -r '.[0].followersCount // "N/A"')
    posts=$(cat "$DATA_DIR/${competitor}-${DATE}.json" | jq -r '.[0].postsCount // "N/A"')
    echo "  ✅ 粉丝: $followers, 帖子: $posts"
  else
    echo "  ❌ 采集失败"
  fi

  sleep 2  # 避免请求过快
done < "$COMPETITOR_FILE"

echo ""
echo "📊 监测完成，数据保存在 $DATA_DIR/"
