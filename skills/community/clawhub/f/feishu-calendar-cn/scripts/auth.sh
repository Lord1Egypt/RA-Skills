#!/bin/bash

# 飞书认证脚本 - 获取 tenant_access_token
# 需要环境变量：FEISHU_APP_ID, FEISHU_APP_SECRET

APP_ID="${FEISHU_APP_ID}"
APP_SECRET="${FEISHU_APP_SECRET}"

if [ -z "$APP_ID" ] || [ -z "$APP_SECRET" ]; then
    echo '{"error": "请设置环境变量 FEISHU_APP_ID 和 FEISHU_APP_SECRET"}'
    exit 1
fi

# 获取 tenant_access_token
RESPONSE=$(curl -s -X POST \
    "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
    -H "Content-Type: application/json" \
    -d "{
        \"app_id\": \"$APP_ID\",
        \"app_secret\": \"$APP_SECRET\"
    }")

# 检查是否有错误
CODE=$(echo "$RESPONSE" | grep -o '"code":[0-9]*' | head -1 | cut -d':' -f2)
if [ "$CODE" != "0" ]; then
    echo "{\"error\": \"认证失败\", \"response\": $RESPONSE}"
    exit 1
fi

# 解析 token
TOKEN=$(echo "$RESPONSE" | grep -o '"tenant_access_token":"[^"]*"' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
    echo "{\"error\": \"获取 token 失败\", \"response\": $RESPONSE}"
    exit 1
fi

echo "$TOKEN"