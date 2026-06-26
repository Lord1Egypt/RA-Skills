#!/bin/bash
# download-batch.sh - 批量下载视频

URL_FILE="${1:-}"
QUALITY="${2:-best}"
OUTPUT_DIR="${3:-./downloads}"

if [ -z "$URL_FILE" ] || [ ! -f "$URL_FILE" ]; then
    echo "用法: ./download-batch.sh <URL文件> [清晰度] [输出目录]"
    echo ""
    echo "URL文件格式 (每行一个URL):"
    echo "  https://www.bilibili.com/video/BV1xx411c7mD"
    echo "  https://www.bilibili.com/video/BV1yy411c7nE"
    echo ""
    echo "示例: ./download-batch.sh urls.txt 1080 ./downloads"
    exit 1
fi

# 统计URL数量
TOTAL=$(wc -l < "$URL_FILE" | tr -d ' ')
CURRENT=0

echo "📥 批量下载开始"
echo "   文件: $URL_FILE"
echo "   共 $TOTAL 个视频"
echo "   清晰度: $QUALITY"
echo "   保存到: $OUTPUT_DIR"
echo ""

# 逐行读取并下载
while IFS= read -r URL; do
    # 跳过空行和注释
    [[ -z "$URL" || "$URL" =~ ^# ]] && continue
    
    CURRENT=$((CURRENT + 1))
    echo "[$CURRENT/$TOTAL] 正在下载: $URL"
    
    ./download.sh "$URL" "$QUALITY" "$OUTPUT_DIR"
    
    echo ""
done < "$URL_FILE"

echo "✅ 批量下载完成！共 $CURRENT 个视频"
