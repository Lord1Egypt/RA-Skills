#!/bin/bash
# 设计日报 - 36氪抓取脚本
# 从 https://36kr.com 抓取科技资讯

set -e

CACHE_FILE="/Applications/QClaw.app/Contents/Resources/openclaw/config/skills/design-daily-news/.cache/36kr_news.json"
CACHE_TTL=1800  # 缓存30分钟

# 检查缓存
if [ -f "$CACHE_FILE" ]; then
    CACHE_AGE=$(($(date +%s) - $(stat -f%m "$CACHE_FILE" 2>/dev/null || stat -c%Y "$CACHE_FILE" 2>/dev/null || echo 0)))
    if [ $CACHE_AGE -lt $CACHE_TTL ]; then
        cat "$CACHE_FILE"
        exit 0
    fi
fi

# 36氪有严格的反爬虫，使用 RSS 订阅源
# 尝试获取 36氪的 RSS
RSS_DATA=$(curl -s -L "https://36kr.com/feed" \
    -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
    --connect-timeout 10 \
    --max-time 30 2>/dev/null || echo "")

# 解析 RSS 为 JSON
JSON_DATA=$(echo "$RSS_DATA" | python3 -c "
import sys
import re
import json
from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    try:
        s.feed(html)
        return s.get_data()
    except:
        return html

rss = sys.stdin.read()
articles = []

# 提取 item 节点
items = re.findall(r'<item[^>]*>(.*?)</item>', rss, re.DOTALL)
for item in items[:10]:
    title_match = re.search(r'<title[^>]*>(.*?)</title>', item, re.DOTALL)
    link_match = re.search(r'<link[^>]*>(.*?)</link>', item, re.DOTALL)
    desc_match = re.search(r'<description[^>]*>(.*?)</description>', item, re.DOTALL)
    
    if title_match:
        title = strip_tags(title_match.group(1)).strip()
        link = strip_tags(link_match.group(1)).strip() if link_match else ''
        desc = strip_tags(desc_match.group(1)).strip() if desc_match else ''
        
        # 清理 CDATA
        title = re.sub(r'<!\[CDATA\[(.*?)\]\]>', r'\1', title)
        link = re.sub(r'<!\[CDATA\[(.*?)\]\]>', r'\1', link)
        desc = re.sub(r'<!\[CDATA\[(.*?)\]\]>', r'\1', desc)
        
        articles.append({
            'title': title,
            'url': link,
            'summary': desc[:200] if desc else ''
        })

print(json.dumps({'articles': articles}, ensure_ascii=False))
" 2>/dev/null || echo '{"articles":[]}')

# 保存缓存
mkdir -p "$(dirname "$CACHE_FILE")"
echo "$JSON_DATA" > "$CACHE_FILE"

# 输出 JSON
echo "$JSON_DATA"
