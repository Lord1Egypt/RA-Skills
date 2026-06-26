#!/bin/bash
# up-videos.sh - 获取UP主视频列表

UID="${1:-}"
LIMIT="${2:-30}"

if [ -z "$UID" ]; then
    echo "用法: ./up-videos.sh <UID> [数量]"
    echo "示例: ./up-videos.sh 208259 50"
    echo ""
    echo "如何获取UID:"
    echo "  1. 打开UP主主页"
    echo "  2. URL中的数字就是UID，如 space.bilibili.com/208259"
    exit 1
fi

echo "👤 获取UP主视频列表"
echo "   UID: $UID"
echo "   数量: $LIMIT"
echo ""

# 使用 Python 获取视频列表
python3 << EOF
import requests
import json

uid = "$UID"
limit = int($LIMIT)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://space.bilibili.com'
}

page = 1
count = 0

print(f"{'序号':<6} {'标题':<40} {'BV号':<15} {'播放量':<12} {'日期':<12}")
print("-" * 90)

while count < limit:
    try:
        url = f"https://api.bilibili.com/x/space/wbi/arc/search?mid={uid}&ps=30&pn={page}"
        resp = requests.get(url, headers=headers, timeout=10)
        data = resp.json()
        
        if data.get('data', {}).get('list', {}).get('vlist'):
            videos = data['data']['list']['vlist']
            
            if not videos:
                break
                
            for video in videos:
                if count >= limit:
                    break
                    
                title = video['title'][:37] + '...' if len(video['title']) > 40 else video['title']
                bvid = video['bvid']
                play = video['play']
                created = video['created']
                
                # 格式化播放量
                if play and play > 10000:
                    play_str = f"{play/10000:.1f}万"
                else:
                    play_str = str(play) if play else "0"
                
                # 格式化日期
                from datetime import datetime
                date_str = datetime.fromtimestamp(created).strftime('%Y-%m-%d')
                
                print(f"{count+1:<6} {title:<40} {bvid:<15} {play_str:<12} {date_str:<12}")
                count += 1
            
            page += 1
        else:
            break
            
    except Exception as e:
        print(f"错误: {e}")
        break

print("")
print(f"✅ 共获取 {count} 个视频")
print("")
print("下载链接列表 (可用于批量下载):")
print("")

# 重新获取并输出URL
page = 1
count = 0
while count < limit:
    try:
        url = f"https://api.bilibili.com/x/space/wbi/arc/search?mid={uid}&ps=30&pn={page}"
        resp = requests.get(url, headers=headers, timeout=10)
        data = resp.json()
        
        if data.get('data', {}).get('list', {}).get('vlist'):
            videos = data['data']['list']['vlist']
            
            if not videos:
                break
                
            for video in videos:
                if count >= limit:
                    break
                print(f"https://www.bilibili.com/video/{video['bvid']}")
                count += 1
            
            page += 1
        else:
            break
            
    except:
        break
EOF
