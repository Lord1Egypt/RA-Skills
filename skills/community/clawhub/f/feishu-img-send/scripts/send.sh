#!/bin/bash
# 飞书发送图片脚本

APP_ID="cli_a92d303bf7f9dcc8"
APP_SECRET="uvP39NArvXPjzPG2bvdZZs2SfZ231YFk"
IMAGE_PATH="$1"
TARGET_USER="$2"

if [ -z "$IMAGE_PATH" ] || [ -z "$TARGET_USER" ]; then
    echo "用法: $0 <图片路径> <用户ID>"
    echo "示例: $0 /tmp/test.png ou_fdc89990aa96e4bf2dc299cdcae70a6c"
    exit 1
fi

# 获取token
TOKEN=$(curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d "{\"app_id\":\"$APP_ID\",\"app_secret\":\"$APP_SECRET\"}" | python3 -c "import json,sys; print(json.load(sys.stdin).get('tenant_access_token',''))")

if [ -z "$TOKEN" ]; then
    echo "获取token失败"
    exit 1
fi

# 上传图片
IMAGE_KEY=$(curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/images" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: multipart/form-data" \
  -F "image_type=message" \
  -F "image=@$IMAGE_PATH" | python3 -c "import json,sys; print(json.load(sys.stdin).get('data',{}).get('image_key',''))")

if [ -z "$IMAGE_KEY" ]; then
    echo "图片上传失败"
    exit 1
fi

# 发送图片消息
RESULT=$(curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"receive_id\": \"$TARGET_USER\",
    \"msg_type\": \"image\",
    \"content\": \"{\\\"image_key\\\":\\\"$IMAGE_KEY\\\"}\"
  }")

echo "$RESULT"
