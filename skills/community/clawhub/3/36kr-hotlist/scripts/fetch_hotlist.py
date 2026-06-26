#!/usr/bin/env python3
"""
fetch_hotlist.py — 36kr 24小时热榜查询工具

用法:
    python fetch_hotlist.py                     # 查询今日热榜
    python fetch_hotlist.py 2026-03-10          # 查询指定日期
    python fetch_hotlist.py --top 5             # 只显示前 5 名
    python fetch_hotlist.py --json              # 输出原始 JSON
    python fetch_hotlist.py --csv out.csv       # 导出 CSV

依赖:
    pip install httpx
"""

import argparse
import csv
import datetime
import json
import sys

try:
    import httpx
except ImportError:
    print("[ERROR] 缺少依赖，请先执行: pip install httpx")
    sys.exit(1)

BASE_URL = "https://openclaw.36krcdn.com/media/hotlist/{date}/24h_hot_list.json"
DEFAULT_TIMEOUT = 10
MAX_FALLBACK_DAYS = 3


def build_url(date: str) -> str:
    return BASE_URL.format(date=date)


def fetch(date: str = None, auto_fallback: bool = True) -> dict | None:
    """
    获取热榜数据。
    
    Args:
        date: YYYY-MM-DD 格式日期，默认今日
        auto_fallback: 若当日 404 则自动回退到前一天，最多回退 MAX_FALLBACK_DAYS 天
    Returns:
        热榜 dict，或 None（获取失败）
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
        try:
            resp = httpx.get(url, timeout=DEFAULT_TIMEOUT)
            if resp.status_code == 200:
                if i > 0:
                    print(f"[INFO] 当日无数据，已回退至 {query_date}")
                return resp.json()
            elif resp.status_code == 404:
                if auto_fallback:
                    print(f"[WARN] {query_date} 无数据，尝试前一天...")
                else:
                    print(f"[WARN] {query_date} 的热榜数据不存在（404）")
                    return None
            else:
                print(f"[ERROR] HTTP {resp.status_code}: {url}")
                return None
        except httpx.TimeoutException:
            print(f"[ERROR] 请求超时: {url}")
            return None
        except httpx.RequestError as e:
            print(f"[ERROR] 请求失败: {e}")
            return None

    print(f"[ERROR] 连续 {attempts} 天均无数据，放弃查询")
    return None


def print_table(data: dict, top: int = None):
    """格式化打印热榜表格。"""
    articles = data.get("data", [])
    if top:
        articles = articles[:top]

    print(f"\n┌{'─' * 70}┐")
    print(f"│  36kr 24小时热榜  {data.get('date', '?'):>48} │")
    print(f"├{'─' * 70}┤")

    for item in articles:
        rank = item.get("rank", "?")
        title = item.get("title", "")[:38]
        author = item.get("author", "")[:12]
        pub_time = item.get("publishTime", "")
        url = item.get("url", "")

        print(f"│  #{rank:<3} {title:<40} │")
        print(f"│       作者: {author:<12}  发布: {pub_time}    │")
        print(f"│       {url[:62]:<62} │")
        print(f"├{'─' * 70}┤")

    gen_ts = data.get("time", 0)
    gen_time = datetime.datetime.fromtimestamp(gen_ts / 1000).strftime("%Y-%m-%d %H:%M:%S") if gen_ts else "?"
    print(f"│  数据生成时间: {gen_time:<54} │")
    print(f"└{'─' * 70}┘")
    print(f"\n共 {len(articles)} 篇文章")


def export_csv(data: dict, filepath: str):
    """将热榜导出为 CSV 文件。"""
    articles = data.get("data", [])
    fields = ["rank", "title", "author", "publishTime", "url"]

    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(articles)

    print(f"[OK] 已导出 {len(articles)} 条记录 → {filepath}")


def main():
    parser = argparse.ArgumentParser(
        description="36kr 24小时热榜查询工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python fetch_hotlist.py                  # 今日热榜
  python fetch_hotlist.py 2026-03-10       # 指定日期
  python fetch_hotlist.py --top 5          # 前 5 名
  python fetch_hotlist.py --json           # 输出 JSON
  python fetch_hotlist.py --csv hot.csv    # 导出 CSV
        """,
    )
    parser.add_argument("date", nargs="?", default=None, help="日期 YYYY-MM-DD，默认今日")
    parser.add_argument("--top", type=int, default=None, help="只显示前 N 名")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    parser.add_argument("--csv", metavar="FILE", help="导出 CSV 到指定文件")
    parser.add_argument("--no-fallback", action="store_true", help="不自动回退到前一天")

    args = parser.parse_args()

    data = fetch(date=args.date, auto_fallback=not args.no_fallback)
    if data is None:
        sys.exit(1)

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    elif args.csv:
        export_csv(data, args.csv)
    else:
        print_table(data, top=args.top)


if __name__ == "__main__":
    main()


# ─────────────────────────────────────────────
# 内嵌 Demo（直接运行时也可通过 import 调用）
# ─────────────────────────────────────────────

def demo_basic():
    """Demo 1: 最简单的查询"""
    import datetime
    today = datetime.date.today().isoformat()
    url = BASE_URL.format(date=today)
    resp = httpx.get(url, timeout=10)
    articles = resp.json()["data"]
    for a in articles:
        print(f"#{a['rank']} {a['title']} — {a['author']}")


def demo_top3():
    """Demo 2: 只取前 3 名"""
    data = fetch()
    if data:
        for item in data["data"][:3]:
            print(f"TOP{item['rank']}: {item['title']}")
            print(f"  {item['url']}")


def demo_date_range():
    """Demo 3: 查询最近 7 天的第 1 名标题"""
    today = datetime.date.today()
    for i in range(7):
        day = (today - datetime.timedelta(days=i)).isoformat()
        data = fetch(date=day, auto_fallback=False)
        if data and data.get("data"):
            top1 = data["data"][0]
            print(f"{day}  #{top1['rank']} {top1['title']}")
        else:
            print(f"{day}  [无数据]")
