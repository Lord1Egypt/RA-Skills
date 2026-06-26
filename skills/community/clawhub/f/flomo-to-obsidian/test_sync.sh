#!/bin/bash
# Flomo 自动同步测试脚本

echo "======================================"
echo "Flomo 自动同步测试"
echo "======================================"
echo ""

# 检查参数
if [ -z "$1" ] || [ -z "$2" ]; then
    echo "用法: ./test_sync.sh <email> <password>"
    echo ""
    echo "示例:"
    echo "  ./test_sync.sh your-email@example.com your-password"
    echo ""
    exit 1
fi

EMAIL="$1"
PASSWORD="$2"
OUTPUT_DIR="/Users/ryanbzhou/mynote/flomo"

echo "配置信息："
echo "  邮箱: $EMAIL"
echo "  密码: ********"
echo "  输出: $OUTPUT_DIR"
echo ""

# 进入脚本目录
cd "$(dirname "$0")"

echo "开始同步..."
echo ""

python scripts/auto_sync.py \
  --email "$EMAIL" \
  --password "$PASSWORD" \
  --output "$OUTPUT_DIR" \
  --tag-prefix "flomo/" \
  --no-headless \
  --verbose

echo ""
echo "======================================"
echo "同步完成！"
echo "======================================"
