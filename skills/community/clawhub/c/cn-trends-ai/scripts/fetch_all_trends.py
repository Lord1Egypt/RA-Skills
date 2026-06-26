#!/usr/bin/env python3
"""
多平台热点聚合抓取引擎
支持：知乎热榜、微博热搜、百度热搜、B站排行榜

用法:
  python3 fetch_trends.py --all --limit 20
  python3 fetch_trends.py --platform zhihu --limit 10
  python3 fetch_trends.py --all --keyword "AI" --json
"""

import json
import os
import sys
import ssl
import argparse
import time
import certifi
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# SSL 配置：优先标准验证，失败才降级
# macOS Python 需要显式加载 certifi 根证书
_SAFE_SSL_CTX = ssl.create_default_context()
_SAFE_SSL_CTX.load_verify_locations(certifi.where())

def _urlopen(req, timeout=10):
    """标准SSL验证（certifi根证书）"""
    return urlopen(req, timeout=timeout, context=_SAFE_SSL_CTX)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

# ========== 知乎热榜 ==========

def fetch_zhihu(limit=20):
    """抓取知乎热榜"""
    url = "https://api.zhihu.com/topstory/hot-lists/total?limit={}".format(limit)
    try:
        req = Request(url, headers=HEADERS)
        with _urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print("  ⚠️ 知乎热榜抓取失败: {}".format(e), file=sys.stderr)
        return []

    results = []
    for item in data.get("data", []):
        target = item.get("target", {})
        title = target.get("title", "").strip()
        if not title:
            continue

        # 提取热度数值
        detail = item.get("detail_text", "")
        heat_num = 0
        if "万" in detail:
            try:
                heat_num = float(detail.replace("万热度", "").replace("万", "").strip()) * 10000
            except ValueError:
                pass
        elif "热度" in detail:
            try:
                heat_num = int(detail.replace("热度", "").strip())
            except ValueError:
                pass

        results.append({
            "title": title,
            "platform": "知乎",
            "heat": int(heat_num),
            "heat_display": detail,
            "url": "https://www.zhihu.com/question/{}".format(target.get("id", "")),
            "category": "",
            "excerpt": (target.get("excerpt", "") or "")[:100]
        })

    return results


# ========== 微博热搜 ==========

def fetch_weibo(limit=20):
    """抓取微博热搜"""
    url = "https://weibo.com/ajax/side/hotSearch"
    headers = {**HEADERS, "Referer": "https://weibo.com/"}
    try:
        req = Request(url, headers=headers)
        with _urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print("  ⚠️ 微博热搜抓取失败: {}".format(e), file=sys.stderr)
        return []

    results = []
    realtime = data.get("data", {}).get("realtime", [])
    for item in realtime[:limit]:
        note = item.get("note", "").strip()
        if not note:
            continue
        note = item.get("note", "").strip()
        if not note:
            continue

        label = item.get("label_name", "")
        if label:
            note = "[{}]{}".format(label, note)

        results.append({
            "title": note,
            "platform": "微博",
            "heat": int(item.get("num", 0)),
            "heat_display": str(item.get("num", 0)),
            "url": "https://s.weibo.com/weibo?q=%23{}%23".format(
                item.get("word", item.get("note", ""))
            ),
            "category": "",
            "excerpt": ""
        })

    return results


# ========== 百度热搜 ==========

def fetch_baidu(limit=20):
    """抓取百度热搜"""
    url = "https://top.baidu.com/api/board?platform=wise&tab=realtime"
    try:
        req = Request(url, headers=HEADERS)
        with _urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print("  ⚠️ 百度热搜抓取失败: {}".format(e), file=sys.stderr)
        return []

    results = []
    cards = data.get("data", {}).get("cards", [])
    if cards:
        content = cards[0].get("content", [])
        for item in content[:limit]:
            query = item.get("query", "").strip()
            if not query:
                continue

            desc = item.get("desc", "")
            heat_num = 0
            try:
                heat_num = int(item.get("hotScore", 0))
            except (ValueError, TypeError):
                pass

            results.append({
                "title": query,
                "platform": "百度",
                "heat": heat_num,
                "heat_display": desc[:30] if desc else "",
                "url": "https://www.baidu.com/s?wd={}".format(query),
                "category": item.get("tag", ""),
                "excerpt": desc[:100] if desc else ""
            })

    return results


# ========== B站排行榜 ==========

def fetch_bilibili(limit=20):
    """抓取B站排行榜"""
    url = "https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all"
    try:
        req = Request(url, headers=HEADERS)
        with _urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print("  ⚠️ B站排行榜抓取失败: {}".format(e), file=sys.stderr)
        return []

    results = []
    items = data.get("data", {}).get("list", [])
    for item in items[:limit]:
        title = item.get("title", "").strip()
        if not title:
            continue

        stat = item.get("stat", {})
        results.append({
            "title": title,
            "platform": "B站",
            "heat": int(stat.get("view", 0)),
            "heat_display": "{}播放".format(_format_num(stat.get("view", 0))),
            "url": item.get("short_link_v2", "https://www.bilibili.com/video/{}".format(
                item.get("bvid", "")
            )),
            "category": item.get("tname", ""),
            "excerpt": item.get("description", "")[:100] if item.get("description") else ""
        })

    return results


# ========== 工具函数 ==========

def _format_num(n):
    """格式化数字"""
    n = int(n)
    if n >= 10000:
        return "{:.1f}万".format(n / 10000)
    elif n >= 1000:
        return "{:.1f}k".format(n / 1000)
    return str(n)


def filter_by_keyword(items, keyword):
    """按关键词过滤"""
    kw = keyword.lower()
    return [item for item in items if kw in item["title"].lower()]


def print_report(items, keyword=None):
    """打印热点报告"""
    if not items:
        print("\n📭 未抓取到热点数据")
        return

    # 按平台分组
    by_platform = {}
    for item in items:
        p = item["platform"]
        by_platform.setdefault(p, []).append(item)

    print("\n" + "=" * 60)
    if keyword:
        print("📊 热点速览 | 关键词: 「{}」".format(keyword))
    else:
        print("📊 今日热点速览")
    print("=" * 60)

    for platform, topics in by_platform.items():
        print("\n🔥 {} | {} 条".format(platform, len(topics)))
        for i, t in enumerate(topics, 1):
            heat = t.get("heat_display", "")
            if heat:
                print("  {}. {}  🔥{}".format(i, t["title"][:48], heat))
            else:
                print("  {}. {}".format(i, t["title"][:48]))
            if t.get("excerpt"):
                print("     {}".format(t["excerpt"][:60]))

    print("\n" + "-" * 60)
    print("💡 AI 分析：输入「分析选题」获取内容机会评分")
    print("💡 输入「生成内容」直接改写为知乎/小红书文案")


# ========== 主入口 ==========

FETCHERS = {
    "zhihu": fetch_zhihu,
    "weibo": fetch_weibo,
    "baidu": fetch_baidu,
    "bilibili": fetch_bilibili,
}

PLATFORM_NAMES = {
    "zhihu": "知乎",
    "weibo": "微博",
    "baidu": "百度",
    "bilibili": "B站",
    "all": "全部平台",
}


def main():
    parser = argparse.ArgumentParser(description="多平台热点聚合")
    parser.add_argument("--platform", "-p",
                        choices=list(FETCHERS.keys()) + ["all"],
                        default="all",
                        help="抓取平台（默认全部）")
    parser.add_argument("--limit", "-n", type=int, default=15,
                        help="每个平台抓取条数（默认15）")
    parser.add_argument("--keyword", "-k",
                        help="按关键词过滤")
    parser.add_argument("--json", action="store_true",
                        help="输出 JSON 格式")
    args = parser.parse_args()

    # 确定要抓取的平台
    if args.platform == "all":
        platforms = list(FETCHERS.keys())
    else:
        platforms = [args.platform]

    # 依次抓取
    all_items = []
    for name in platforms:
        display_name = PLATFORM_NAMES.get(name, name)
        print("📡 抓取 {}...".format(display_name), file=sys.stderr)
        start = time.time()
        items = FETCHERS[name](args.limit)
        elapsed = time.time() - start
        if items:
            print("  ✅ {} 条 ({:.1f}s)".format(len(items), elapsed), file=sys.stderr)
        else:
            print("  ⚠️ 无数据 ({:.1f}s)".format(elapsed), file=sys.stderr)
        all_items.extend(items)

    # 关键词过滤
    if args.keyword:
        all_items = filter_by_keyword(all_items, args.keyword)

    # 按热度排序
    all_items.sort(key=lambda x: x.get("heat", 0), reverse=True)

    # 输出
    if args.json:
        print(json.dumps(all_items, ensure_ascii=False, indent=2))
    else:
        print_report(all_items, args.keyword)


if __name__ == "__main__":
    main()
