#!/bin/bash

# 飞书消息表情回复工具
# 用法: ./add_reaction.sh <message_id> <emoji_type>

set -e

MESSAGE_ID="$1"
EMOJI_TYPE="$2"

if [ -z "$MESSAGE_ID" ] || [ -z "$EMOJI_TYPE" ]; then
  echo "用法: $0 <message_id> <emoji_type>"
  echo "示例: $0 om_xxx THUMBSUP"
  exit 1
fi

# 从环境变量或配置文件读取飞书凭证
if [ -z "$FEISHU_APP_ID_INSTANCE2" ] || [ -z "$FEISHU_APP_SECRET_INSTANCE2" ]; then
  echo "错误: 未设置飞书凭证环境变量 FEISHU_APP_ID_INSTANCE2 和 FEISHU_APP_SECRET_INSTANCE2"
  exit 1
fi

# 获取 tenant_access_token
echo "正在获取 access token..."
TOKEN_RESPONSE=$(curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d "{
    \"app_id\": \"$FEISHU_APP_ID_INSTANCE2\",
    \"app_secret\": \"$FEISHU_APP_SECRET_INSTANCE2\"
  }")

TENANT_ACCESS_TOKEN=$(echo "$TOKEN_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('tenant_access_token', ''))")

if [ -z "$TENANT_ACCESS_TOKEN" ]; then
  echo "错误: 无法获取 access token"
  echo "$TOKEN_RESPONSE"
  exit 1
fi

# 添加表情回复
echo "正在添加表情回复: $EMOJI_TYPE 到消息 $MESSAGE_ID ..."
REACTION_RESPONSE=$(curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages/$MESSAGE_ID/reactions" \
  -H "Authorization: Bearer $TENANT_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"reaction_type\": {
      \"emoji_type\": \"$EMOJI_TYPE\"
    }
  }")

# 检查结果
CODE=$(echo "$REACTION_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('code', -1))")

if [ "$CODE" = "0" ]; then
  echo "✅ 成功添加表情回复: $EMOJI_TYPE"
  echo "$REACTION_RESPONSE" | python3 -m json.tool
else
  echo "❌ 添加表情回复失败"
  echo "$REACTION_RESPONSE" | python3 -m json.tool
  exit 1
fi
