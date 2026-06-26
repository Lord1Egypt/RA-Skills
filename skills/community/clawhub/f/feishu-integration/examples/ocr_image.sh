#!/bin/bash
# OCR 图片识别示例

set -e

# 获取 token
TOKEN=$(bash "$(dirname "$0")/../scripts/feishu-auth.sh" get)

# 检查参数
if [ -z "$1" ]; then
  echo "用法: $0 <image_key>"
  echo "示例: $0 img_v3_xxx"
  exit 1
fi

IMAGE_KEY="$1"

# OCR 识别
python3 "$(dirname "$0")/../scripts/feishu-ocr.py" \
  "$IMAGE_KEY" \
  "$TOKEN"
