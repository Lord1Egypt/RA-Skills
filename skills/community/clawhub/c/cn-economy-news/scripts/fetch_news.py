#!/usr/bin/env python3
"""
中国经济资讯抓取脚本
通过搜索引擎 + RSS 从官方权威媒体聚合经济新闻，过滤广告和低质量内容。

用法:
    python3 fetch_news.py                    # 默认抓取全部
    python3 fetch_news.py --limit 10         # 限制返回条数
    python3 fetch_news.py --keyword 货币政策   # 按关键词过滤
    python3 fetch_news.py --output json      # JSON 格式输出
    python3 fetch_news.py --source rss       # 仅用 RSS 源
    python3 fetch_news.py --source search    # 仅用搜索聚合
"""

import argparse
import json
import re
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime
from urllib.parse import quote, urljoin
from collections import defaultdict

try:
    import requests
except ImportError:
    print("需要安装依赖: pip3 install requests", file=sys.stderr)
    sys.exit(1)

# ==================== 官方 RSS 源 ====================
RSS_FEEDS = [
    {"name": "中国政府网·政策", "url": "https://www.gov.cn/zhengce/zuixin/ezine.xml", "icon": "🏛️", "category": "政策"},
    {"name": "新华网·财经",     "url": "http://www.news.cn/fortune/feed.xml",         "icon": "📰", "category": "综合"},
]

# ==================== 搜索聚合配置 ====================
# site: 限定官方域名，确保质量
OFFICIAL_SITES = [
    "gov.cn",
    "news.cn",
    "people.com.cn",
    "stats.gov.cn",
    "cctv.com",
    "ce.cn",          # 中国经济网（经济日报）
    "xinhuanet.com",
]

SEARCH_QUERIES = [
    "中国经济",
    "经济政策",
    "宏观经济数据",
]

# ==================== 广告/低质量过滤 ====================
AD_KEYWORDS = [
    "广告", "推广", "赞助", "优惠券", "折扣", "限时", "抢购",
    "免费领", "点击领取", "扫码", "加微信", "客服电话",
    "理财产品", "收益率高达", "稳赚", "暴涨", "暴富",
    "代理", "加盟", "招商", "培训班", "报名从速",
    "揭秘", "震惊", "惊呆", "万万没想到", "99%的人不知道",
    "视频", "图集", "直播回放", "专题",
]

TITLE_MIN_LEN = 8
TITLE_MAX_LEN = 80

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
}


# ==================== RSS 抓取 ====================
def fetch_rss(feed):
    """抓取 RSS 源"""
    try:
        resp = requests.get(feed["url"], headers=HEADERS, timeout=10, verify=False)
        resp.encoding = "utf-8"
        root = ET.fromstring(resp.text)
        articles = []
        # 尝试 RSS 2.0 格式
        for item in root.iter("item"):
            title_el = item.find("title")
            link_el = item.find("link")
            pub_el = item.find("pubDate")
            if title_el is not None and link_el is not None:
                articles.append({
                    "title": (title_el.text or "").strip(),
                    "url": (link_el.text or "").strip(),
                    "date": (pub_el.text or "").strip() if pub_el is not None else "",
                    "source": feed["name"],
                    "icon": feed["icon"],
                    "category": feed["category"],
                })
        # 尝试 Atom 格式
        if not articles:
            ns = {"atom": "http://www.w3.org/2005/Atom"}
            for entry in root.findall(".//atom:entry", ns):
                title_el = entry.find("atom:title", ns)
                link_el = entry.find("atom:link", ns)
                pub_el = entry.find("atom:published", ns) or entry.find("atom:updated", ns)
                if title_el is not None and link_el is not None:
                    articles.append({
                        "title": (title_el.text or "").strip(),
                        "url": link_el.get("href", "").strip(),
                        "date": (pub_el.text or "").strip() if pub_el is not None else "",
                        "source": feed["name"],
                        "icon": feed["icon"],
                        "category": feed["category"],
                    })
        return articles
    except Exception as e:
        print(f"  ⚠️ RSS抓取失败 {feed['name']}: {e}", file=sys.stderr)
        return []


# ==================== 搜索聚合 ====================
def search_bing_cn(query, sites, limit=20):
    """通过 Bing 中国搜索聚合官方经济新闻"""
    site_filter = " OR ".join([f"site:{s}" for s in sites])
    full_query = f"{query} ({site_filter})"
    url = f"https://cn.bing.com/search?q={quote(full_query)}&count={limit}&setlang=zh-CN&cc=CN"
    
    articles = []
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.encoding = "utf-8"
        
        # 用正则简单提取搜索结果（不依赖 bs4）
        # Bing 搜索结果格式: <h2><a href="URL">TITLE</a></h2>
        pattern = r'<h2[^>]*><a[^>]+href="(https?://[^"]+)"[^>]*>(.*?)</a></h2>'
        matches = re.findall(pattern, resp.text, re.DOTALL)
        
        for href, title_html in matches:
            title = re.sub(r'<[^>]+>', '', title_html).strip()
            # 判断来源
            source_name = "官方媒体"
            icon = "📋"
            for site in sites:
                if site in href:
                    if "gov.cn" in site: source_name, icon = "中国政府网", "🏛️"
                    elif "news.cn" in site or "xinhua" in site: source_name, icon = "新华网", "📰"
                    elif "people" in site: source_name, icon = "人民网", "📢"
                    elif "stats" in site: source_name, icon = "国家统计局", "📊"
                    elif "cctv" in site: source_name, icon = "央视财经", "📺"
                    elif "ce.cn" in site: source_name, icon = "中国经济网", "📈"
                    break
            
            articles.append({
                "title": title,
                "url": href,
                "date": "",
                "source": source_name,
                "icon": icon,
                "category": "综合",
            })
    except Exception as e:
        print(f"  ⚠️ 搜索失败: {e}", file=sys.stderr)
    
    return articles


# ==================== 过滤与去重 ====================
def is_ad_or_low_quality(article):
    title = article.get("title", "")
    if len(title) < TITLE_MIN_LEN or len(title) > TITLE_MAX_LEN:
        return True
    for kw in AD_KEYWORDS:
        if kw in title:
            return True
    if re.match(r"^[\d\s\.\-/]+$", title):
        return True
    # 过滤非官方域名
    url = article.get("url", "")
    if url and not any(site in url for site in OFFICIAL_SITES):
        return True
    return False


def deduplicate(articles):
    seen = set()
    unique = []
    for a in articles:
        key = re.sub(r'\s+', '', a["title"])[:30]
        if key not in seen:
            seen.add(key)
            unique.append(a)
    return unique


def filter_by_keyword(articles, keyword):
    if not keyword:
        return articles
    return [a for a in articles if keyword in a["title"]]


# ==================== 输出 ====================
def format_markdown(articles):
    if not articles:
        return "暂无符合条件的经济资讯。"
    lines = []
    lines.append(f"📅 **中国经济资讯** | 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"共 **{len(articles)}** 条资讯\n")
    lines.append("---\n")
    grouped = defaultdict(list)
    for a in articles:
        grouped[a["source"]].append(a)
    for source, items in grouped.items():
        icon = items[0]["icon"]
        lines.append(f"### {icon} {source}\n")
        for i, a in enumerate(items, 1):
            date_str = f" ({a['date']})" if a.get("date") else ""
            lines.append(f"{i}. [{a['title']}]({a['url']}){date_str}")
        lines.append("")
    return "\n".join(lines)


def format_json(articles):
    return json.dumps({
        "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "count": len(articles),
        "articles": articles,
    }, ensure_ascii=False, indent=2)


# ==================== 主函数 ====================
def main():
    parser = argparse.ArgumentParser(description="中国经济资讯抓取工具")
    parser.add_argument("--source", choices=["all", "rss", "search"], default="all",
                        help="数据源方式 (默认: all)")
    parser.add_argument("--limit", type=int, default=30, help="最大返回条数 (默认: 30)")
    parser.add_argument("--keyword", type=str, default="", help="关键词过滤")
    parser.add_argument("--output", choices=["markdown", "json"], default="markdown",
                        help="输出格式 (默认: markdown)")
    args = parser.parse_args()

    all_articles = []

    # RSS 抓取
    if args.source in ("all", "rss"):
        for feed in RSS_FEEDS:
            print(f"🔍 RSS抓取: {feed['name']}...", file=sys.stderr)
            articles = fetch_rss(feed)
            print(f"  ✅ 获取 {len(articles)} 条", file=sys.stderr)
            all_articles.extend(articles)
            time.sleep(0.3)

    # 搜索聚合
    if args.source in ("all", "search"):
        for query in SEARCH_QUERIES:
            print(f"🔍 搜索聚合: {query}...", file=sys.stderr)
            articles = search_bing_cn(query, OFFICIAL_SITES)
            print(f"  ✅ 获取 {len(articles)} 条", file=sys.stderr)
            all_articles.extend(articles)
            time.sleep(0.5)

    # 过滤
    before = len(all_articles)
    all_articles = [a for a in all_articles if not is_ad_or_low_quality(a)]
    print(f"🧹 过滤: {before} → {len(all_articles)}", file=sys.stderr)

    all_articles = deduplicate(all_articles)

    if args.keyword:
        all_articles = filter_by_keyword(all_articles, args.keyword)
        print(f"🔑 关键词过滤后: {len(all_articles)} 条", file=sys.stderr)

    all_articles = all_articles[:args.limit]

    if args.output == "json":
        print(format_json(all_articles))
    else:
        print(format_markdown(all_articles))


if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    main()
