#!/bin/bash
# Content Matrix Publisher - 发布脚本

set -e

CONTENT_FILE="$1"
PLATFORM="${2:-xiaohongshu}"
DRY_RUN="${3:-true}"

if [ ! -f "$CONTENT_FILE" ]; then
    echo "❌ 内容文件不存在: $CONTENT_FILE"
    exit 1
fi

echo "🚀 准备发布到: $PLATFORM"
echo "📄 内容文件: $CONTENT_FILE"

# 解析内容
TITLE=$(jq -r '.title' "$CONTENT_FILE")
BODY=$(jq -r '.body' "$CONTENT_FILE")

echo "📝 标题: $TITLE"

if [ "$DRY_RUN" = "true" ]; then
    echo ""
    echo "⚠️  DRY RUN 模式 - 不会实际发布"
    echo "---"
    echo "标题: $TITLE"
    echo "内容预览:"
    echo "$BODY" | head -c 200
    echo "..."
    echo "---"
    exit 0
fi

case "$PLATFORM" in
    xiaohongshu)
        echo "📱 发布到小红书..."
        # 调用 xiaohongshu-mcp
        xiaohongshu-mcp publish \
            --title "$TITLE" \
            --content "$BODY" \
            --images "$(jq -r '.images[]' "$CONTENT_FILE" | tr '\n' ',')"
        ;;
    wechat)
        echo "📢 发布到公众号..."
        # 调用公众号助手
        wechat-article-pro publish \
            --title "$TITLE" \
            --content "$BODY"
        ;;
    *)
        echo "❌ 不支持的平台: $PLATFORM"
        exit 1
        ;;
esac

echo "✅ 发布完成！"