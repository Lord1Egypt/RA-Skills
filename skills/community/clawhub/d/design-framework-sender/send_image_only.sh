#!/usr/bin/env bash
set -e

IMAGE_FILE="${1:-}"
TARGET="${2:-}"

if [ -z "$IMAGE_FILE" ] || [ -z "$TARGET" ]; then
  echo "Usage: ./send_image_only.sh \"<图片文件路径>\" \"<telegram_user_id>\"" >&2
  exit 1
fi

# 检查图片文件是否存在且非空
if [ ! -f "$IMAGE_FILE" ]; then
  echo "[send_image_only] 错误：图片文件不存在: $IMAGE_FILE" >&2
  exit 1
fi

if [ ! -s "$IMAGE_FILE" ]; then
  echo "[send_image_only] 错误：图片文件为空: $IMAGE_FILE" >&2
  exit 1
fi

BOT_TOKEN=$(python3 -c "import json; print(json.load(open('$HOME/.openclaw/openclaw.json'))['channels']['telegram']['botToken'])")

RESPONSE=$(curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendPhoto" \
  -F "chat_id=${TARGET}" \
  -F "photo=@${IMAGE_FILE}" \
  -F "caption=🎨 设计框架图")

# 检查响应是否成功
OK=$(echo "$RESPONSE" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('ok', False))" 2>/dev/null || echo "False")
if [ "$OK" != "True" ]; then
  echo "[send_image_only] 发送失败，Telegram 响应: $RESPONSE" >&2
  exit 1
fi

echo "✅ 图片已私发给 ${TARGET}"

