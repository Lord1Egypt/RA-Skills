#!/bin/bash
# BlockBeats to ChainThink - 从律动抓取文章并保存到 ChainThink

set -e

ARTICLE_URL="$1"

if [[ -z "$ARTICLE_URL" ]]; then
  echo "用法: $0 <BlockBeats文章URL>"
  echo "示例: $0 https://www.theblockbeats.info/news/61465"
  exit 1
fi

# 提取文章ID
ARTICLE_ID=$(echo "$ARTICLE_URL" | grep -oE '[0-9]+$')

if [[ -z "$ARTICLE_ID" ]]; then
  echo "错误: 无法从URL提取文章ID"
  exit 1
fi

echo "正在抓取文章 ID: $ARTICLE_ID ..."

# 使用浏览器提取文章内容
ARTICLE_DATA=$(openclaw browser --action=act --kind=evaluate \
  --url="$ARTICLE_URL" \
  --fn='() => {
    const data = window.__NUXT__.data[0];
    return {
      title: data.info.title,
      abstract: data.info.abstract,
      content: data.info.content
    };
  }' 2>/dev/null | jq -r '.result')

TITLE=$(echo "$ARTICLE_DATA" | jq -r '.title')
ABSTRACT=$(echo "$ARTICLE_DATA" | jq -r '.abstract')
CONTENT=$(echo "$ARTICLE_DATA" | jq -r '.content')

echo "文章标题: $TITLE"
echo "正在保存到 ChainThink..."

# 从 TOOLS.md 读取 token（如果存在）
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJVVUlEIjoiY2Y3MzBlZWUtODU3YS00MWRlLTljM2EtNTMxODY5NDU0OTE5IiwiSUQiOjUxLCJVc2VybmFtZSI6ImxhYmlkIiwiTmlja05hbWUiOiJsYWJpZCIsIkF1dGhvcml0eUlkIjoxMDEsIkJ1ZmZlclRpbWUiOjg2NDAwLCJpc3MiOiJxbVBsdXMiLCJhdWQiOlsiR1ZBIl0sImV4cCI6MTc3MzI5NzIwNiwibmJmIjoxNzcyNjkyNDA2fQ.mt1dR1Qom9HJ6WIfWeGgKm0dKa_Ekoe6HWiO0uGwfgo"

# 构建 JSON payload
PAYLOAD=$(jq -n \
  --arg title "$TITLE" \
  --arg text "$CONTENT" \
  --arg abstract "$ABSTRACT" \
  '{
    "id": "0",
    "info": {},
    "is_translate": true,
    "translation": {
      "zh-CN": {
        "title": $title,
        "text": $text,
        "abstract": $abstract
      }
    },
    "type": 5,
    "admin_detail": {},
    "strong_content_tags": {},
    "chain_is_calendar": false,
    "chain_calendar_time": 0,
    "chain_calendar_tendency": 0,
    "is_push_bian": 2,
    "content_pin_top": 0,
    "is_public": false,
    "user_id": "3",
    "chain_fixed_publish_time": 0,
    "as_user_id": "3",
    "is_chain": true,
    "chain_airdrop_time": 0,
    "chain_airdrop_time_end": 0
  }')

# 调用 ChainThink API
RESPONSE=$(curl -s 'https://api-v2.chainthink.cn/ccs/v1/admin/content/publish' \
  -H 'Content-Type: application/json' \
  -H 'X-App-Id: 101' \
  -H "x-token: $TOKEN" \
  -H 'x-user-id: 51' \
  --data-raw "$PAYLOAD")

# 检查结果
CODE=$(echo "$RESPONSE" | jq -r '.code')
if [[ "$CODE" == "0" ]]; then
  ARTICLE_ID=$(echo "$RESPONSE" | jq -r '.data.id')
  echo "✅ 保存成功！"
  echo "文章 ID: $ARTICLE_ID"
  echo "可在 ChainThink 后台查看草稿"
else
  echo "❌ 保存失败"
  echo "$RESPONSE" | jq .
  exit 1
fi
