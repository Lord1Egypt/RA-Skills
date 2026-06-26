"""
每日简报生成器 - 真实数据抓取版
从多个中文新闻源抓取当日热点，生成结构化简报。

依赖: requests (必须), feedparser (可选，RSS模式更丰富)
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse, urljoin

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    import feedparser
    HAS_FEEDPARSER = True
except ImportError:
    HAS_FEEDPARSER = False


DEFAULT_SOURCES = [
    {
        "name": "Hacker News",
        "type": "api",
        "url": "https://hacker-news.firebaseio.com/v0/topstories.json",
        "detail_url": "https://hacker-news.firebaseio.com/v0/item/{}.json",
        "parser": "hn_api",
        "category": "tech"
    },
    {
        "name": "36氪",
        "type": "rss",
        "url": "https://36kr.com/feed",
        "parser": "rss",
        "category": "business"
    },
    {
        "name": "V2EX热门",
        "type": "rss",
        "url": "https://www.v2ex.com/feed/tab/hot.xml",
        "parser": "rss",
        "category": "tech"
    },
    {
        "name": "InfoQ中文",
        "type": "rss",
        "url": "https://www.infoq.cn/feed",
        "parser": "rss",
        "category": "tech"
    },
    {
        "name": "GitHub Trending",
        "type": "webpage",
        "url": "https://github.com/trending?since=daily",
        "parser": "github_trending",
        "category": "dev"
    },
]

CATEGORY_EMOJI = {
    "tech": "🔧",
    "business": "🏢",
    "finance": "💰",
    "news": "📰",
    "dev": "💻",
    "ai": "🤖",
}


def fetch_hn_top(source):
    """从 Hacker News API 获取热门文章"""
    if not HAS_REQUESTS:
        return []

    try:
        resp = requests.get(source["url"], timeout=10)
        resp.raise_for_status()
        item_ids = resp.json()[:15]

        articles = []
        for iid in item_ids[:10]:
            try:
                detail = requests.get(source["detail_url"].format(iid), timeout=5).json()
                articles.append({
                    "title": detail.get("title", ""),
                    "url": detail.get("url", ""),
                    "summary": detail.get("title", ""),
                    "source": source["name"],
                    "category": source["category"],
                    "score": detail.get("score", 0),
                    "comments": detail.get("descendants", 0)
                })
            except Exception as e:
                continue

        return articles
    except Exception as e:
        print("[WARN] HN API失败: {}".format(e))
        return []


def fetch_rss(source):
    """从 RSS feed 获取文章"""
    if not HAS_FEEDPARSER or not HAS_REQUESTS:
        return _fallback_rss(source)

    try:
        feed = feedparser.parse(source["url"])
        articles = []
        for entry in feed.entries[:12]:
            content = ""
            if hasattr(entry, "content") and entry.content:
                content = entry.content[0].get("value", "")
            elif hasattr(entry, "summary"):
                content = entry.summary

            articles.append({
                "title": entry.get("title", "无标题"),
                "url": entry.get("link", ""),
                "summary": _strip_html(content)[:200],
                "source": source["name"],
                "category": source.get("category", "news")
            })
        return articles
    except Exception as e:
        print("[WARN] RSS [{}] 失败: {}".format(source.get("name"), e))
        return []


def fetch_github_trending(source):
    """从 GitHub Trending 页面提取项目"""
    if not HAS_REQUESTS:
        return []

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(source["url"], headers=headers, timeout=15)
        resp.raise_for_status()
        html = resp.text

        articles = []
        pattern = r'<article class="Box-row">.*?<h2.*?<a[^>]*href="(/[^"]+)"[^>]*>([^<]+)</a>.*?<p[^>]*>([^<]*)</p>'

        matches = re.findall(pattern, html, re.S)
        for url_path, title, desc in matches[:10]:
            full_url = "https://github.com" + url_path
            articles.append({
                "title": title.strip(),
                "url": full_url,
                "summary": desc.strip()[:200],
                "source": source["name"],
                "category": source.get("category", "dev")
            })

        return articles
    except Exception as e:
        print("[WARN] GitHub Trending 失败: {}".format(e))
        return []


def _fallback_rss(source):
    """无feedparser时的降级：返回提示信息"""
    return [{
        "title": "[{}] 需要安装feedparser".format(source["name"]),
        "url": source.get("url", ""),
        "summary": "运行 pip install feedparser 后可获取此源内容",
        "source": source["name"],
        "category": source.get("category", "news")
    }]


def _strip_html(html):
    if not html:
        return ""
    text = re.sub(r'<[^>]+>', '', html)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def fetch_all(sources=None, keywords=None):
    """抓取所有信息源

    Args:
        sources: list of source dicts (default: DEFAULT_SOURCES)
        keywords: list of str, 关键词过滤

    Returns:
        dict: {category: [articles]}
    """
    sources = sources or DEFAULT_SOURCES
    all_articles = {}

    for source in sources:
        parser_type = source.get("parser", "rss")

        if parser_type == "hn_api":
            articles = fetch_hn_top(source)
        elif parser_type == "github_trending":
            articles = fetch_github_trending(source)
        else:
            articles = fetch_rss(source)

        cat = source.get("category", "other")
        emoji = CATEGORY_EMOJI.get(cat, "")

        if keywords:
            kw_lower = [k.lower() for k in keywords]
            articles = [
                a for a in articles
                if any(k in a.get("title","").lower() or k in a.get("summary","").lower() for k in kw_lower)
            ]

        if cat not in all_articles:
            all_articles[cat] = []
        all_articles[cat].extend(articles)

        print("[OK] {}: {} 篇文章".format(emoji + " " + source["name"], len(articles)))

    return all_articles


def generate_report(articles_by_category, title=None):
    """生成 Markdown 格式的简报"""
    now = datetime.now().strftime("%Y年%m月%d日 %H:%M")
    title = title or "📰 每日简报 — {}".format(now.split()[0])

    lines = [
        "# {}".format(title),
        "",
        "> 自动生成于 {} | 数据来源: Hacker News / 36氪 / V2EX / InfoQ / GitHub".format(now),
        "",
        "---",
        ""
    ]

    total = 0
    for category, articles in articles_by_category.items():
        if not articles:
            continue

        emoji = CATEGORY_EMOJI.get(category, "")
        cat_names = {
            "tech": "🔧 科技动态",
            "business": "🏢 商业财经",
            "finance": "💰 金融资讯",
            "news": "📰 时政要闻",
            "dev": "💻 开发者",
            "ai": "🤖 AI前沿",
        }

        lines.append("## {} {}".format(emoji, cat_names.get(category, category.upper())))
        lines.append("")

        for i, article in enumerate(articles[:8], 1):
            score_info = ""
            if article.get("score"):
                score_info = " | 👍{} 💬{}".format(article["score"], article.get("comments", 0))

            lines.append("**{}.** [{}]({}){}".format(
                i,
                article.get("title", "无标题")[:60],
                article.get("url", "#"),
                score_info
            ))

            if article.get("summary"):
                summary = article["summary"][:120]
                lines.append("> {}".format(summary))

            lines.append("")

        total += min(len(articles), 8)
        lines.append("---")
        lines.append("")

    lines.append("")
    lines.append("*共收录 {} 条资讯 | 由 📰 每日简报生成器自动生成*".format(total))

    return "\n".join(lines)


def save_and_print(report_md, output_file=None):
    """保存到文件并打印到终端"""
    print("\n" + "=" * 60 + "\n")
    print(report_md)
    print("\n" + "=" * 60 + "\n")

    if output_file is None:
        out_dir = Path.home() / "daily-briefings"
        out_dir.mkdir(exist_ok=True)
        date_str = datetime.now().strftime("%Y%m%d_%H%M")
        output_file = out_dir / "briefing_{}.md".format(date_str)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report_md)

    print("[OK] 简报已保存至: {}".format(output_file))
    return output_file


def main():
    import argparse
    parser = argparse.ArgumentParser(description="每日简报 - 真实数据抓取版")
    parser.add_argument("--keywords", "-k", nargs="+", help="关键词过滤")
    parser.add_argument("--output", "-o", help="输出文件路径")
    parser.add_argument("--sources", "-s", choices=["all", "tech", "news"], default="all",
                        help="信息源范围")
    args = parser.parse_args()

    print("=" * 50)
    print("📰 每日简报生成器 — 正在抓取最新资讯...")
    print("=" * 50)

    sources = DEFAULT_SOURCES
    if args.sources == "tech":
        sources = [s for s in sources if s["category"] in ("tech", "dev")]
    elif args.sources == "news":
        sources = [s for s in sources if s["category"] in ("business", "finance", "news")]

    articles = fetch_all(sources=sources, keywords=args.keywords)
    report = generate_report(articles)
    save_and_print(report, output_file=args.output)


if __name__ == "__main__":
    main()
