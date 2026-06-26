#!/bin/bash
# 设计日报 - 优设读报抓取脚本
# 从 https://www.uisdc.com/news 抓取每日设计资讯

set -e

CACHE_FILE="/Applications/QClaw.app/Contents/Resources/openclaw/config/skills/design-daily-news/.cache/uisdc_news.json"
CACHE_TTL=3600  # 缓存1小时

# 检查缓存
if [ -f "$CACHE_FILE" ]; then
    CACHE_AGE=$(($(date +%s) - $(stat -f%m "$CACHE_FILE" 2>/dev/null || stat -c%Y "$CACHE_FILE" 2>/dev/null || echo 0)))
    if [ $CACHE_AGE -lt $CACHE_TTL ]; then
        cat "$CACHE_FILE"
        exit 0
    fi
fi

# 抓取优设读报数据
HTML=$(curl -s -L "https://www.uisdc.com/news" \
    -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
    -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
    -H "Accept-Language: zh-CN,zh;q=0.9,en;q=0.8" \
    --connect-timeout 10 \
    --max-time 30)

# 提取 uisdc_news 变量中的 JSON 数据
# 数据格式: var uisdc_news = "[...]";
JSON_LINE=$(echo "$HTML" | grep 'var uisdc_news = ' | head -1)

if [ -z "$JSON_LINE" ]; then
    echo "Error: Failed to find uisdc_news data" >&2
    exit 1
fi

# 提取引号内的内容并解码 Unicode
python3 -c "
import json
import re
import sys

line = sys.stdin.read()

# 提取引号内的内容
match = re.search(r'var uisdc_news = \"(.*)\";', line, re.DOTALL)
if not match:
    print(json.dumps({'error': 'Failed to extract JSON'}, ensure_ascii=False))
    sys.exit(1)

json_str = match.group(1)

# 解码 Unicode 转义序列
# 先把 \\uXXXX 转为实际的 Unicode 字符
decoded = json_str.encode('utf-8').decode('unicode_escape')

# 解析 JSON 数组
try:
    news_array = json.loads(decoded)
    print(json.dumps(news_array, ensure_ascii=False))
except Exception as e:
    print(json.dumps({'error': str(e)}, ensure_ascii=False))
    sys.exit(1)
" <<< "$JSON_LINE"
