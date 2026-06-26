#!/usr/bin/env python3
"""
fetch_aireport.py — 36kr 自助报道栏目文章查询工具

用法:
    python fetch_aireport.py                     # 查询今日自助报道
    python fetch_aireport.py 2026-03-10          # 查询指定日期
    python fetch_aireport.py --top 5             # 只显示前 5 篇
    python fetch_aireport.py --json              # 输出原始 JSON
    python fetch_aireport.py --recent 7          # 查询最近 7 天去重汇总

依赖: Python 3 标准库（无需额外安装）
"""

import argparse
import datetime
import json
import sys
import urllib.error
import urllib.request

BASE_URL = "https://openclaw.36krcdn.com/media/aireport/{date}/ai_report_articles.json"
DEFAULT_TIMEOUT = 10
MAX_FALLBACK_DAYS = 3


def build_url(date: str) -> str:
    """构造指定日期的 API URL。"""
    return BASE_URL.format(date=date)


def _http_get(url: str, timeout: int = DEFAULT_TIMEOUT):
    """通过标准库 urllib 发起 GET 请求，返回 (status_code, json_data_or_none)。"""
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception:
        return None, None


def fetch(date: str = None, auto_fallback: bool = True) -> dict | None:
    """
    获取自助报道文章数据。

    Args:
        date: YYYY-MM-DD 格式日期，默认今日
        auto_fallback: 若当日 404 则自动回退到前一天，最多回退 MAX_FALLBACK_DAYS 天
    Returns:
        自助报道 dict，或 None（获取失败）
    """
    if date is None:
        check_date = datetime.date.today()
    else:
        try:
            check_date = datetime.date.fromisoformat(date)
        except ValueError:
            print(f"[ERROR] 日期格式错误: {date}，应为 YYYY-MM-DD")
            return None

    attempts = MAX_FALLBACK_DAYS + 1 if auto_fallback else 1

    for i in range(attempts):
        query_date = check_date - datetime.timedelta(days=i)
        url = build_url(query_date.isoformat())
        status, data = _http_get(url)
        if status is None:
            print(f"[ERROR] 请求失败或超时: {url}")
            return None
        if status == 200:
            if i > 0:
                print(f"[INFO] 当日无数据，已回退至 {query_date}")
            return data
        elif status == 404:
            if auto_fallback:
                print(f"[WARN] {query_date} 无数据，尝试前一天...")
            else:
                print(f"[WARN] {query_date} 的自助报道数据不存在（404）")
                return None
        else:
            print(f"[ERROR] HTTP {status}: {url}")
            return None

    print(f"[ERROR] 连续 {attempts} 天均无数据，放弃查询")
    return None


def fetch_recent(days: int = 7) -> list:
    """
    查询最近 days 天的自助报道文章，去重后按发布时间倒序返回。

    Args:
        days: 向前查询的天数
    Returns:
        去重后的文章列表
    """
    today = datetime.date.today()
    seen_urls = set()
    all_articles = []

    for i in range(days):
        date = (today - datetime.timedelta(days=i)).isoformat()
        url = build_url(date)
        status, data = _http_get(url)
        if status == 200 and data:
            for article in data.get("data", []):
                if article.get("url") not in seen_urls:
                    seen_urls.add(article["url"])
                    all_articles.append(article)

    # 按发布时间倒序
    all_articles.sort(key=lambda x: x.get("publishTime", ""), reverse=True)
    return all_articles


def print_table(data: dict, top: int = None):
    """格式化打印自助报道文章表格。"""
    articles = data.get("data", [])
    if top:
        articles = articles[:top]

    print(f"\n┌{'─' * 72}┐")
    print(f"│  36kr 自助报道  {data.get('date', '?'):>52} │")
    print(f"├{'─' * 72}┤")

    for item in articles:
        rank = item.get("rank", "?")
        title = item.get("title", "")[:40]
        author = item.get("author", "")[:14]
        pub_time = item.get("publishTime", "")
        url = item.get("url", "")

        print(f"│  #{rank:<3} {title:<42} │")
        print(f"│       作者: {author:<14}  发布: {pub_time}      │")
        print(f"│       {url[:64]:<64} │")
        print(f"├{'─' * 72}┤")

    gen_ts = data.get("time", 0)
    gen_time = datetime.datetime.fromtimestamp(gen_ts / 1000).strftime("%Y-%m-%d %H:%M:%S") if gen_ts else "?"
    print(f"│  数据生成时间: {gen_time:<56} │")
    print(f"└{'─' * 72}┘")
    print(f"\n共 {len(articles)} 篇文章")


def print_recent_table(articles: list, top: int = None):
    """格式化打印近期去重汇总结果。"""
    if top:
        articles = articles[:top]

    print(f"\n{'─' * 70}")
    print(f"  36kr 自助报道 · 近期汇总（共 {len(articles)} 篇，已去重）")
    print(f"{'─' * 70}")
    for item in articles:
        rank = item.get("rank", "-")
        title = item.get("title", "")
        author = item.get("author", "")
        pub = item.get("publishTime", "")
        url = item.get("url", "")
        print(f"  [{pub}] #{rank} {title} — {author}")
        print(f"         {url}")
        print()
    print(f"{'─' * 70}")



def main():
    parser = argparse.ArgumentParser(
        description="36kr 自助报道栏目文章查询工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python fetch_aireport.py                  # 今日自助报道
  python fetch_aireport.py 2026-03-10       # 指定日期
  python fetch_aireport.py --top 5          # 前 5 篇
  python fetch_aireport.py --json           # 输出 JSON
  python fetch_aireport.py --csv ai.csv     # 导出 CSV
  python fetch_aireport.py --recent 7       # 最近 7 天汇总
        """,
    )
    parser.add_argument("date", nargs="?", default=None, help="日期 YYYY-MM-DD，默认今日")
    parser.add_argument("--top", type=int, default=None, help="只显示前 N 篇")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    parser.add_argument("--no-fallback", action="store_true", help="不自动回退到前一天")
    parser.add_argument("--recent", type=int, metavar="DAYS", help="查询最近 N 天去重汇总")

    args = parser.parse_args()

    # 近期汇总模式
    if args.recent:
        articles = fetch_recent(days=args.recent)
        if not articles:
            print(f"[WARN] 最近 {args.recent} 天均无数据")
            sys.exit(1)
        print_recent_table(articles, top=args.top)
        return

    # 单日查询模式
    data = fetch(date=args.date, auto_fallback=not args.no_fallback)
    if data is None:
        sys.exit(1)

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print_table(data, top=args.top)


if __name__ == "__main__":
    main()


# ─────────────────────────────────────────────
# 内嵌 Demo（直接运行时也可通过 import 调用）
# ─────────────────────────────────────────────

def demo_basic():
    """Demo 1: 最简单的查询"""
    today = datetime.date.today().isoformat()
    url = BASE_URL.format(date=today)
    _, data = _http_get(url)
    if data:
        for a in data["data"]:
            print(f"#{a['rank']} {a['title']} — {a['author']}")


def demo_top3():
    """Demo 2: 只取前 3 篇"""
    data = fetch()
    if data:
        for item in data["data"][:3]:
            print(f"TOP{item['rank']}: {item['title']}")
            print(f"  {item['url']}")


def demo_recent_unique():
    """Demo 3: 查询最近 3 天的去重文章列表"""
    articles = fetch_recent(days=3)
    print(f"最近 3 天共 {len(articles)} 篇自助报道：")
    for a in articles[:5]:
        print(f"  [{a['publishTime']}] {a['title']} — {a['author']}")


def demo_date_range():
    """Demo 4: 查询最近 7 天各天第 1 篇标题"""
    today = datetime.date.today()
    for i in range(7):
        day = (today - datetime.timedelta(days=i)).isoformat()
        data = fetch(date=day, auto_fallback=False)
        if data and data.get("data"):
            top1 = data["data"][0]
            print(f"{day}  #1 {top1['title']}")
        else:
            print(f"{day}  [无数据]")
