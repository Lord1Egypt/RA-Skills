#!/bin/bash
# ClawHub 下载脚本
# 用法：./download.sh <技能名>

set -e

SLUG="$1"

if [ -z "$SLUG" ]; then
  echo "❌ 用法：$0 <技能名>"
  echo "示例：$0 agile-toolkit"
  exit 1
fi

echo "📥 正在下载：${SLUG}..."

# 使用 ClawHub 官方下载 API
DOWNLOAD_URL="https://clawhub.com/api/v1/download?slug=${SLUG}"

echo "  → 下载链接：${DOWNLOAD_URL}"

# 下载 ZIP
ZIP_FILE="/tmp/${SLUG}.zip"
curl -sL "$DOWNLOAD_URL" -o "$ZIP_FILE" \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

# 验证是否为有效 ZIP
if file "$ZIP_FILE" | grep -q "Zip archive"; then
  SIZE=$(ls -lh "$ZIP_FILE" | awk '{print $5}')
  echo ""
  echo "✅ 下载成功！"
  echo "  文件：$ZIP_FILE"
  echo "  大小：$SIZE"
  ls -la "$ZIP_FILE"
else
  echo ""
  echo "❌ 下载失败 - 文件不是有效的 ZIP"
  echo "  实际内容："
  head -5 "$ZIP_FILE"
  rm -f "$ZIP_FILE"
  exit 1
fi
