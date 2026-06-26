#!/bin/bash
# news-fetcher.sh - 获取最近24小时的新事件

STATE_DIR="$HOME/.openclaw/workspace-group/market-monitor"
mkdir -p "$STATE_DIR"
DATE=$(date +%Y-%m-%d)
HOUR=$(date +%H)
MINUTE=$(date +%M)
TIMESTAMP=$(date +%s)

# 计算24小时前的时间戳
ONE_DAY_AGO=$((TIMESTAMP - 86400))

echo "=== 📰 最近24小时财经新闻 ($(date '+%Y-%m-%d %H:%M')) ==="
echo ""
echo "⚠️ 只关注最近24小时内发生的新事件"
echo ""

# ============ 获取新闻 ============

# 1. 新浪财经 - 要闻（增加数量到30条）
echo "【新浪财经要闻】"
curl -s "https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2509&k=&num=50&r=0.123" 2>/dev/null | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    news_list = data.get('result', {}).get('data', [])
    for item in news_list[:30]:
        title = item.get('title', '')
        ctime = item.get('ctime', '')
        url = item.get('url', '')
        if title and ctime:
            print(f'• {title}')
            print(f'  时间: {ctime}')
            print(f'  链接: {url}')
            print()
except Exception as e:
    pass
" 2>/dev/null

# 2. 财联社 - 电报（增加数量到30条）
echo "【财联社电报】"
curl -s "https://www.cls.cn/api/telegraph?app=CailianpressWeb&os=web&sv=8.4.6&sign=" 2>/dev/null | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    news_list = data.get('data', {}).get('roll_data', [])
    for item in news_list[:30]:
        content = item.get('content', '')
        time_str = item.get('ctime', '')
        id = item.get('id', '')
        url = f'https://www.cls.cn/detail/{id}' if id else ''
        if content:
            print(f'• {content[:120]}...')
            print(f'  时间: {time_str}')
            print(f'  链接: {url}')
            print()
except:
    pass
" 2>/dev/null

# 3. 华尔街见闻（增加数量到20条）
echo "【华尔街见闻】"
curl -s "https://api.wallstreetcn.com/apiv1/content/articles?platform=wscn-platform&channel=global&limit=30" 2>/dev/null | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    items = data.get('data', {}).get('items', [])
    for item in items[:20]:
        title = item.get('title', '')
        time_str = item.get('display_time', '')
        uri = item.get('uri', '')
        if uri and not uri.startswith('http'):
            uri = f'https://wallstreetcn.com/articles/{uri}'
        url = item.get('url', uri)
        if title:
            print(f'• {title}')
            print(f'  时间: {time_str}')
            print(f'  链接: {url}')
            print()
except:
    pass
" 2>/dev/null

echo ""
echo "=== 数据来源: 新浪财经 / 财联社 / 华尔街见闻 ==="
echo "=== 分析重点: 只关注最近24小时的新事件 ==="
