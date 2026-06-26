#!/bin/bash
# comments.sh - 获取视频评论

URL="${1:-}"
LIMIT="${2:-50}"

if [ -z "$URL" ]; then
    echo "用法: ./comments.sh <URL> [评论数量]"
    echo "示例: ./comments.sh 'https://www.bilibili.com/video/BV1xx411c7mD' 100"
    exit 1
fi

echo "💬 获取视频评论: $URL"
echo "   数量: $LIMIT"
echo ""

# 提取BV号并构建API请求
BV=$(echo "$URL" | grep -oP 'BV[0-9a-zA-Z]+' || echo "")

if [ -z "$BV" ]; then
    echo "❌ 无法提取BV号"
    exit 1
fi

echo "BV号: $BV"
echo ""

# 使用 Python 获取评论
python3 << EOF
import requests
import json
import re
import sys

bv = "$BV"
limit = int($LIMIT)

# BV转AV的算法
def bv2av(bvid):
    table = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
    tr = {}
    for i in range(58):
        tr[table[i]] = i
    s = [11, 10, 3, 8, 4, 6]
    xor = 177451812
    add = 8728348608
    r = 0
    for i in range(6):
        r += tr[bvid[s[i]]] * 58 ** i
    return (r - add) ^ xor

try:
    aid = bv2av(bv)
    print(f"AV号: av{aid}")
    print("")
    
    # 获取评论
    url = f"https://api.bilibili.com/x/v2/reply/main?next=0&type=1&oid={aid}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    resp = requests.get(url, headers=headers, timeout=10)
    data = resp.json()
    
    if data.get('data', {}).get('replies'):
        replies = data['data']['replies'][:limit]
        print(f"共获取 {len(replies)} 条评论:\n")
        
        for i, reply in enumerate(replies, 1):
            uname = reply['member']['uname']
            content = reply['content']['message']
            like = reply['like']
            print(f"[{i}] {uname} (👍 {like})")
            print(f"    {content[:200]}{'...' if len(content) > 200 else ''}")
            print()
    else:
        print("暂无评论或获取失败")
        
except Exception as e:
    print(f"错误: {e}")
EOF
