#!/bin/bash
# 设计日报 - 虎嗅网抓取脚本
# 从 https://www.huxiu.com 抓取科技资讯

set -e

CACHE_FILE="/Applications/QClaw.app/Contents/Resources/openclaw/config/skills/design-daily-news/.cache/huxiu_news.json"
CACHE_TTL=1800  # 缓存30分钟

# 检查缓存
if [ -f "$CACHE_FILE" ]; then
    CACHE_AGE=$(($(date +%s) - $(stat -f%m "$CACHE_FILE" 2>/dev/null || stat -c%Y "$CACHE_FILE" 2>/dev/null || echo 0)))
    if [ $CACHE_AGE -lt $CACHE_TTL ]; then
        cat "$CACHE_FILE"
        exit 0
    fi
fi

# 抓取虎嗅网数据
HTML=$(curl -s -L "https://www.huxiu.com" \
    -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
    -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
    -H "Accept-Language: zh-CN,zh;q=0.9,en;q=0.8" \
    --connect-timeout 10 \
    --max-time 30)

# 提取文章数据 - 从 __NUXT_DATA__ 中提取
# 虎嗅网使用 Vue SSR，数据在 script 标签中
JSON_DATA=$(echo "$HTML" | python3 -c "
import sys
import re
import json

html = sys.stdin.read()

# 尝试提取 __NUXT_DATA__
match = re.search(r'<script type=\"application/json\" data-nuxt-data=\"nuxt-app\"[^>]*>(.*?)</script>', html, re.DOTALL)
if match:
    try:
        data = json.loads(match.group(1))
        # 提取文章列表
        articles = []
        if isinstance(data, list) and len(data) > 1:
            state = data[1]
            if 'data' in state and 'home-index' in state['data']:
                home_data = state['data']['home-index']
                # 提取焦点文章
                if 'focus' in home_data:
                    for item in home_data['focus']:
                        if isinstance(item, dict) and 'title' in item:
                            articles.append({
                                'title': item.get('title', ''),
                                'url': item.get('url', ''),
                                'summary': item.get('summary', ''),
                                'channel': item.get('channel_info', {}).get('name', '')
                            })
        print(json.dumps({'articles': articles[:10]}, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({'error': str(e), 'articles': []}, ensure_ascii=False))
else:
    print(json.dumps({'articles': []}, ensure_ascii=False))
" 2>/dev/null || echo '{"articles":[]}')

# 保存缓存
mkdir -p "$(dirname "$CACHE_FILE")"
echo "$JSON_DATA" > "$CACHE_FILE"

# 输出 JSON
echo "$JSON_DATA"
