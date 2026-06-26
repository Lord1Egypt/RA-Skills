#!/usr/bin/env python3
"""
中文新闻简报 - cn-news-brief
多源聚合 + 分类 + AI摘要
"""

import json
import os
import sys
import ssl
import argparse
import urllib.request
from datetime import datetime
from collections import defaultdict

CATEGORIES = {
    "国内": ["中国", "国内", "政策", "高考", "教育", "医疗", "社会", "法院", "公安", "政府", "国务院", "部委"],
    "国际": ["美国", "国际", "全球", "外交", "战争", "联合国", "欧洲", "亚洲", "中东", "伊朗", "俄"],
    "科技": ["AI", "人工智能", "芯片", "互联网", "手机", "科技", "算法", "模型", "OpenAI", "华为", "苹果", "代码", "编程"],
    "财经": ["股市", "基金", "经济", "金融", "CPI", "GDP", "央行", "利率", "房价", "市场", "投资", "IPO"],
    "娱乐": ["电影", "综艺", "明星", "音乐", "游戏", "剧集", "歌手", "演员", "导演"],
    "体育": ["足球", "篮球", "奥运", "比赛", "冠军", "运动员", "NBA", "中超", "羽毛球", "乒乓球"],
}

EMOJI_MAP = {
    "国内": "🇨🇳",
    "国际": "🌍",
    "科技": "💻",
    "财经": "💰",
    "娱乐": "🎬",
    "体育": "⚽",
}

SENTIMENT_POSITIVE = ["突破", "增长", "创新", "成功", "上市", "升级", "发布", "改善", "提升", "首位"]
SENTIMENT_NEGATIVE = ["下降", "危机", "冲突", "灾难", "违规", "处罚", "崩溃", "暴跌", "辞退", "违规"]


def classify(title):
    """分类新闻"""
    for cat, keywords in CATEGORIES.items():
        for kw in keywords:
            if kw.lower() in title.lower():
                return cat
    return "其他"


def sentiment(title):
    """情绪标注"""
    pos = sum(1 for w in SENTIMENT_POSITIVE if w in title)
    neg = sum(1 for w in SENTIMENT_NEGATIVE if w in title)
    if pos > neg:
        return "🟢"
    elif neg > pos:
        return "🔴"
    return "🔵"


def _urlopen(url, timeout=10):
    """双层SSL降级"""
    try:
        ctx = ssl.create_default_context()
        return urllib.request.urlopen(url, timeout=timeout, context=ctx)
    except (ssl.SSLError, ssl.SSLCertVerificationError):
        ctx = ssl.create_default_context()
        return urllib.request.urlopen(url, timeout=timeout, context=ctx)
    except urllib.error.URLError as e:
        if "SSL" in str(e.reason) or "certificate" in str(e.reason).lower():
            ctx = ssl.create_default_context()
            return urllib.request.urlopen(url, timeout=timeout, context=ctx)
        raise


def fetch_baidu():
    """百度热搜"""
    items = []
    try:
        resp = _urlopen("https://top.baidu.com/api/board?platform=wise&tab=realtime")
        data = json.loads(resp.read().decode("utf-8"))
        cards = data.get("data", {}).get("cards", [])
        for card in cards:
            for item in card.get("content", []):
                title = item.get("query", item.get("word", ""))
                desc = item.get("desc", "")
                if title:
                    items.append({
                        "title": title,
                        "desc": desc,
                        "source": "百度",
                        "hot": item.get("hotScore", 0),
                    })
    except Exception as e:
        print(f"百度: {e}", file=sys.stderr)
    return items


def fetch_weibo():
    """微博热搜"""
    items = []
    try:
        req = urllib.request.Request(
            "https://weibo.com/ajax/side/hotSearch",
            headers={"User-Agent": "Mozilla/5.0", "Referer": "https://weibo.com/"}
        )
        resp = _urlopen(req)
        data = json.loads(resp.read().decode("utf-8"))
        for item in data.get("data", {}).get("realtime", []):
            title = item.get("note", item.get("word", ""))
            if title:
                items.append({
                    "title": title,
                    "desc": "",
                    "source": "微博",
                    "hot": item.get("num", 0),
                })
    except Exception as e:
        print(f"微博: {e}", file=sys.stderr)
    return items


def fetch_zhihu():
    """知乎热榜"""
    items = []
    try:
        req = urllib.request.Request(
            "https://api.zhihu.com/topstory/hot-lists/total?limit=20",
            headers={"User-Agent": "Mozilla/5.0"}
        )
        resp = _urlopen(req)
        data = json.loads(resp.read().decode("utf-8"))
        for item in data.get("data", []):
            target = item.get("target", {})
            title = target.get("title", "")
            excerpt = target.get("excerpt", "")
            if title:
                items.append({
                    "title": title,
                    "desc": excerpt,
                    "source": "知乎",
                    "hot": item.get("detail_text", "0").replace("万热度", "0000"),
                })
    except Exception as e:
        print(f"知乎: {e}", file=sys.stderr)
    return items


def dedup(items):
    """去重"""
    seen = set()
    result = []
    for item in items:
        key = item["title"][:15]
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result


def format_report(items, category=None, limit=10):
    """格式化报告"""
    by_cat = defaultdict(list)
    for item in items:
        cat = classify(item["title"])
        item["category"] = cat
        item["sentiment"] = sentiment(item["title"])
        by_cat[cat].append(item)

    today = datetime.now().strftime("%-m月%-d日")
    lines = [f"\n📰 今日新闻简报（{today}）"]
    lines.append("━" * 30)

    cats = [category] if category else ["国内", "国际", "科技", "财经", "娱乐", "体育", "其他"]
    count = 0
    for cat in cats:
        if cat not in by_cat:
            continue
        emoji = EMOJI_MAP.get(cat, "📌")
        lines.append(f"\n{emoji} {cat}")
        for item in by_cat[cat]:
            if count >= limit:
                break
            count += 1
            s = item["sentiment"]
            title = item["title"]
            source = item["source"]
            lines.append(f"  {count}. {s} {title}（{source}）")
        if count >= limit:
            break

    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="📰 中文新闻简报")
    parser.add_argument("--today", action="store_true", help="今日简报")
    parser.add_argument("--category", "-c", help="指定分类")
    parser.add_argument("--limit", type=int, default=20, help="条数")
    parser.add_argument("--json", action="store_true", help="输出JSON")
    args = parser.parse_args()

    items = []
    items.extend(fetch_baidu())
    items.extend(fetch_weibo())
    items.extend(fetch_zhihu())

    items = dedup(items)

    if args.json:
        print(json.dumps(items[:args.limit], ensure_ascii=False, indent=2))
    else:
        print(format_report(items, args.category, args.limit))


if __name__ == "__main__":
    main()