#!/bin/bash
# video-info.sh - 获取视频详情

URL="${1:-}"

if [ -z "$URL" ]; then
    echo "用法: ./video-info.sh <URL>"
    echo "示例: ./video-info.sh 'https://www.bilibili.com/video/BV1xx411c7mD'"
    exit 1
fi

echo "📋 视频信息"
echo ""

# 获取视频信息
yt-dlp "$URL" \
    --dump-json \
    --quiet 2>/dev/null | python3 -c "
import json
import sys

try:
    data = json.load(sys.stdin)
    
    print(f\"标题: {data.get('title', 'N/A')}\")
    print(f\"UP主: {data.get('uploader', 'N/A')}\")
    print(f\"上传时间: {data.get('upload_date', 'N/A')}\")
    print(f\"时长: {data.get('duration', 0) // 60}分{data.get('duration', 0) % 60}秒\")
    print(f\"播放量: {data.get('view_count', 'N/A')}\")
    print(f\"点赞: {data.get('like_count', 'N/A')}\")
    print(f\"投币: {data.get('coin_count', 'N/A')}\")
    print(f\"收藏: {data.get('favorite_count', 'N/A')}\")
    print(f\"分享: {data.get('share_count', 'N/A')}\")
    print(f\"弹幕: {data.get('danmaku_count', 'N/A')}\")
    print(f\"简介: {data.get('description', 'N/A')[:200]}...\")
    print(f\"BV号: {data.get('id', 'N/A')}\")
    print(f\"链接: {data.get('webpage_url', 'N/A')}\")
    
    # 可用清晰度
    if 'formats' in data:
        print(\"\\n可用清晰度:\")
        heights = set()
        for f in data['formats']:
            if 'height' in f and f['height']:
                heights.add(f['height'])
        for h in sorted(heights, reverse=True):
            print(f\"  - {h}P\")
            
except Exception as e:
    print(f'错误: {e}')
"
