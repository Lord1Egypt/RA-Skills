#!/bin/bash
# cn-data-scraper CLI tool
# Usage: ./scripts/scrape.sh <platform> <keyword> [output_file]

PLATFORM=$1
KEYWORD=$2
OUTPUT=${3:-/tmp/scrape_result.json}

if [ -z "$PLATFORM" ] || [ -z "$KEYWORD" ]; then
    echo "Usage: ./scripts/scrape.sh <platform> <keyword> [output_file]"
    echo "Platforms: baidu zhihu weibo csdn"
    echo ""
    echo "Note: taobao/douyin/1688/xiaohongshu require login cookies."
    echo "Use the Python API with cookie injection for these platforms."
    exit 1
fi

python3 -c "
from scrapling import StealthyFetcher, Fetcher
import json
import sys

platform = '$PLATFORM'
keyword = '$KEYWORD'
output = '$OUTPUT'

URLS = {
    'baidu': f'https://www.baidu.com/s?wd={keyword}',
    'zhihu': f'https://www.zhihu.com/search?type=content&q={keyword}',
    'weibo': f'https://s.weibo.com/weibo?q={keyword}',
    'csdn': f'https://so.csdn.net/so/search?q={keyword}',
}

url = URLS.get(platform)
if not url:
    print(json.dumps({
        'error': f'Platform {platform} not supported for CLI scraping.',
        'hint': 'Use Python API with cookie injection for taobao/douyin/1688/xiaohongshu'
    }, ensure_ascii=False))
    sys.exit(0)

try:
    if platform in ['baidu', 'zhihu', 'weibo']:
        page = StealthyFetcher.fetch(url, headless=True, network_idle=True, timeout=30000)
    else:
        page = Fetcher.get(url)
    
    texts = [el.text() for el in page.css('p, span, h1, h2, h3, h4, h5, h6') if el.text()]
    
    result = {
        'platform': platform,
        'keyword': keyword,
        'url': url,
        'content_count': len(texts),
        'preview': texts[:20],
    }
    
    with open(output, 'w') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(json.dumps(result, ensure_ascii=False, indent=2))
except Exception as e:
    error_result = {'error': str(e), 'platform': platform, 'keyword': keyword}
    print(json.dumps(error_result, ensure_ascii=False))
    sys.exit(1)
"
