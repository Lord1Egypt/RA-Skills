#!/bin/bash
# danmaku.sh - 下载视频弹幕

URL="${1:-}"
OUTPUT="${2:-danmaku.xml}"

if [ -z "$URL" ]; then
    echo "用法: ./danmaku.sh <URL> [输出文件]"
    echo "示例: ./danmaku.sh 'https://www.bilibili.com/video/BV1xx411c7mD' danmaku.xml"
    exit 1
fi

echo "📝 正在下载弹幕: $URL"
echo "   保存到: $OUTPUT"
echo ""

# 使用 yt-dlp 下载弹幕
yt-dlp "$URL" \
    --write-subs \
    --write-auto-subs \
    --sub-format "xml" \
    --output "${OUTPUT%.xml}" \
    --skip-download \
    --quiet

# yt-dlp 默认保存为 .xml.txt，需要重命名
if [ -f "${OUTPUT}.xml.txt" ]; then
    mv "${OUTPUT}.xml.txt" "$OUTPUT"
    echo "✅ 弹幕已保存到: $OUTPUT"
elif [ -f "${OUTPUT%.xml}.xml" ]; then
    echo "✅ 弹幕已保存到: ${OUTPUT%.xml}.xml"
else
    echo "⚠️ 未找到弹幕文件"
    echo "   尝试其他方法..."
    
    # 提取CID并手动下载
    CID=$(yt-dlp "$URL" --print "id" --skip-download --quiet 2>/dev/null || echo "")
    if [ -n "$CID" ]; then
        echo "   CID: $CID"
        # B站弹幕API (简化版)
        echo "   提示: 可访问 https://comment.bilibili.com/${CID}.xml 获取弹幕"
    fi
fi
