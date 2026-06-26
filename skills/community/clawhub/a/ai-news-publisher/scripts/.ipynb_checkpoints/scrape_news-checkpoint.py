#!/usr/bin/env python3
"""
新闻抓取脚本
使用 Scrapling 抓取科技新闻

Usage:
    python scrape_news.py --source 36kr --output /tmp/news.json
    python scrape_news.py --source huxiu --count 10
"""

import argparse
import json
import sys
from datetime import datetime

try:
    from scrapling.fetchers import Fetcher, StealthyFetcher
except ImportError:
    print("❌ Scrapling 未安装，请运行: pip install 'scrapling[all]>=0.4.2'")
    sys.exit(1)

# 新闻源配置
SOURCES = {
    "36kr": {
        "url": "https://www.36kr.com/information/AI/",
        # 使用 a 标签提取，匹配 /p/ 开头的文章链接
        "link_pattern": "/p/",
    },
    "huxiu": {
        "url": "https://www.huxiu.com/channel/106.html",
        "link_pattern": "/article/",
    },
}


def scrape_36kr(count=10, use_stealth=False):
    """抓取 36氪 AI 频道"""
    config = SOURCES["36kr"]
    
    print(f"📡 正在抓取 36氪 AI 频道...")
    
    if use_stealth:
        page = StealthyFetcher.fetch(config["url"], headless=True)
    else:
        page = Fetcher.get(config["url"], stealthy_headers=True)
    
    # 提取所有 /p/ 开头的链接
    link_pattern = config["link_pattern"]
    all_links = page.css(f'a[href*="{link_pattern}"]')
    
    seen = set()
    results = []
    for link in all_links:
        href = link.attrib.get('href', '')
        title = link.css('::text').get() or ''
        
        # 过滤条件
        if not href or not title:
            continue
        if href in seen:
            continue
        if len(title.strip()) < 5:  # 过滤太短的标题
            continue
            
        seen.add(href)
        
        # 补全链接
        if href.startswith("/"):
            full_url = f"https://www.36kr.com{href}"
        else:
            full_url = href
        
        results.append({
            "title": title.strip(),
            "link": full_url,
            "summary": "",
            "source": "36kr",
            "scraped_at": datetime.now().isoformat(),
        })
        
        if len(results) >= count:
            break
    
    print(f"✅ 抓取到 {len(results)} 条新闻")
    return results


def scrape_huxiu(count=10, use_stealth=False):
    """抓取虎嗅 AI 频道"""
    config = SOURCES["huxiu"]
    
    print(f"📡 正在抓取虎嗅 AI 频道...")
    
    if use_stealth:
        page = StealthyFetcher.fetch(config["url"], headless=True)
    else:
        page = Fetcher.get(config["url"], stealthy_headers=True)
    
    # 提取所有文章链接
    link_pattern = config["link_pattern"]
    all_links = page.css(f'a[href*="{link_pattern}"]')
    
    seen = set()
    results = []
    for link in all_links:
        href = link.attrib.get('href', '')
        title = link.css('::text').get() or ''
        
        if not href or not title:
            continue
        if href in seen:
            continue
        if len(title.strip()) < 5:
            continue
            
        seen.add(href)
        
        if href.startswith("/"):
            full_url = f"https://www.huxiu.com{href}"
        else:
            full_url = href
        
        results.append({
            "title": title.strip(),
            "link": full_url,
            "summary": "",
            "source": "huxiu",
            "scraped_at": datetime.now().isoformat(),
        })
        
        if len(results) >= count:
            break
    
    print(f"✅ 抓取到 {len(results)} 条新闻")
    return results


def scrape_article_content(url, use_stealth=False):
    """抓取文章正文"""
    print(f"📄 正在抓取文章: {url}")
    
    if use_stealth:
        page = StealthyFetcher.fetch(url, headless=True)
    else:
        page = Fetcher.get(url, stealthy_headers=True)
    
    # 尝试多种选择器
    content = (
        page.css("article .content::text").getall() or
        page.css(".article-content::text").getall() or
        page.css(".content::text").getall() or
        []
    )
    
    return "\n".join(content)


def main():
    parser = argparse.ArgumentParser(description="新闻抓取脚本")
    parser.add_argument("--source", choices=["36kr", "huxiu"], default="36kr", help="新闻源")
    parser.add_argument("--output", "-o", help="输出文件路径 (JSON)")
    parser.add_argument("--count", "-c", type=int, default=10, help="抓取数量")
    parser.add_argument("--stealth", action="store_true", help="使用隐身模式")
    parser.add_argument("--content", metavar="URL", help="抓取指定文章的正文")
    
    args = parser.parse_args()
    
    if args.content:
        # 抓取单篇文章
        content = scrape_article_content(args.content, args.stealth)
        print(content)
        return
    
    # 抓取新闻列表
    if args.source == "36kr":
        articles = scrape_36kr(args.count, args.stealth)
    else:
        articles = scrape_huxiu(args.count, args.stealth)
    
    # 输出
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)
        print(f"📝 已保存到: {args.output}")
    else:
        print(json.dumps(articles, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
