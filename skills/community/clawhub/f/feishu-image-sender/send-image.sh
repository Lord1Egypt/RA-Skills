#!/bin/bash

# Feishu Image Sender Helper Script
# 用法: ./send-image.sh <图片文件名> [说明文字]

set -e

# 配置
WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
IMAGE_NAME="$1"
MESSAGE="${2:-发送图片}"

# 检查参数
if [ -z "$IMAGE_NAME" ]; then
    echo "❌ 错误：请提供图片文件名"
    echo "用法: $0 <图片文件名> [说明文字]"
    echo "示例: $0 test.png '这是测试图片'"
    echo ""
    echo "环境变量 OPENCLAW_WORKSPACE 可设置 workspace 路径"
    echo "默认: $HOME/.openclaw/workspace"
    exit 1
fi

# 构建完整路径
IMAGE_PATH="$WORKSPACE/$IMAGE_NAME"

# 检查文件是否存在
if [ ! -f "$IMAGE_PATH" ]; then
    echo "❌ 错误：图片文件不存在"
    echo "路径: $IMAGE_PATH"
    echo "Workspace: $WORKSPACE"
    echo ""
    echo "可用的图片文件："
    find "$WORKSPACE" -maxdepth 1 -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" -o -name "*.gif" -o -name "*.webp" \) | while read -r file; do
        echo "  - $(basename "$file")"
    done
    exit 1
fi

# 检查文件格式
FILE_EXT="${IMAGE_NAME##*.}"
case "$FILE_EXT" in
    png|jpg|jpeg|gif|webp)
        ;;
    *)
        echo "❌ 错误：不支持的图片格式"
        echo "支持的格式：png, jpg, jpeg, gif, webp"
        exit 1
        ;;
esac

echo "📸 准备发送图片到飞书..."
echo "文件: $IMAGE_PATH"
echo "说明: $MESSAGE"
echo ""

# 这里需要通过 OpenClaw 的 message 工具发送
# 这个脚本只是辅助检查，实际发送需要通过 OpenClaw

echo "✅ 图片文件检查通过"
echo ""
echo "📋 发送指令（在 OpenClaw 中执行）："
echo ""
echo "message({"
echo "  action: \"send\","
echo "  channel: \"feishu\","
echo "  message: \"$MESSAGE\","
echo "  media: \"$IMAGE_PATH\""
echo "})"
