#!/usr/bin/env python3
"""
fetch_ainotes.py — 36kr AI 测评笔记查询工具

用法:
    python fetch_ainotes.py                     # 查询今日测评笔记
    python fetch_ainotes.py 2026-03-18          # 查询指定日期
    python fetch_ainotes.py --top 5             # 只显示前 5 篇
    python fetch_ainotes.py --json              # 输出原始 JSON
    python fetch_ainotes.py --no-fallback       # 不自动回退到前一天

依赖: Python 3 标准库（无需额外安装）
"""

import argparse
import datetime
import json
import sys
import urllib.error
import urllib.request

BASE_URL = "https://openclaw.36krcdn.com/media/ainotes/{date}/ai_notes.json"
DEFAULT_TIMEOUT = 10
MAX_FALLBACK_DAYS = 3


def build_url(date: str) -> str:
    """构造指定日期的 API URL。"""
    return BASE_URL.format(date=date)


def _http_get(url: str, timeout: int = DEFAULT_TIMEOUT):
    """通过标准库 urllib 发起 GET 请求，返回 (status_code, data_or_none)。"""
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception:
        return None, None


def fetch(date: str = None, auto_fallback: bool = True):
    """
    获取 AI 测评笔记数据。

    Args:
        date: YYYY-MM-DD 格式日期，默认今日
        auto_fallback: 若当日 404 则自动回退到前一天，最多回退 MAX_FALLBACK_DAYS 天
    Returns:
        笔记列表 list，或 None（获取失败）
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
                print(f"[WARN] {query_date} 的测评笔记数据不存在（404）")
                return None
        else:
            print(f"[ERROR] HTTP {status}: {url}")
            return None

    print(f"[ERROR] 连续 {attempts} 天均无数据，放弃查询")
    return None


def format_time(ts_ms):
    """将毫秒时间戳转为可读时间字符串。"""
    if not ts_ms:
        return "?"
    try:
        return datetime.datetime.fromtimestamp(ts_ms / 1000).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return str(ts_ms)


def print_table(notes: list, top: int = None):
    """格式化打印测评笔记表格。"""
    if top:
        notes = notes[:top]

    print(f"\n{'─' * 72}")
    print(f"  36kr AI 测评笔记  共 {len(notes)} 篇")
    print(f"{'─' * 72}")

    for idx, item in enumerate(notes, 1):
        title = item.get("title", "")
        author = item.get("authorName", "")
        url = item.get("noteUrl", "")
        circles = "、".join(c.get("circleName", "") for c in (item.get("circleNames") or [])) or "—"
        products = "、".join(p.get("productName", "") for p in (item.get("productNames") or [])) or "—"
        pub_time = format_time(item.get("publishTime"))

        print(f"  #{idx:<3} {title}")
        print(f"       作者: {author}  |  发布: {pub_time}")
        print(f"       圈子: {circles}")
        print(f"       产品: {products}")
        print(f"       {url}")
        print()

    print(f"{'─' * 72}")


def main():
    parser = argparse.ArgumentParser(
        description="36kr AI 测评笔记查询工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python fetch_ainotes.py                  # 今日测评笔记
  python fetch_ainotes.py 2026-03-18       # 指定日期
  python fetch_ainotes.py --top 5          # 前 5 篇
  python fetch_ainotes.py --json           # 输出 JSON
  python fetch_ainotes.py --no-fallback    # 不自动回退
        """,
    )
    parser.add_argument("date", nargs="?", default=None, help="日期 YYYY-MM-DD，默认今日")
    parser.add_argument("--top", type=int, default=None, help="只显示前 N 篇")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    parser.add_argument("--no-fallback", action="store_true", help="不自动回退到前一天")

    args = parser.parse_args()

    notes = fetch(date=args.date, auto_fallback=not args.no_fallback)
    if notes is None:
        sys.exit(1)

    if args.json:
        print(json.dumps(notes, ensure_ascii=False, indent=2))
    else:
        print_table(notes, top=args.top)


if __name__ == "__main__":
    main()


# ─────────────────────────────────────────────
# 内嵌 Demo（直接运行时也可通过 import 调用）
# ─────────────────────────────────────────────

def demo_basic():
    """Demo 1: 最简单的查询"""
    today = datetime.date.today().isoformat()
    url = BASE_URL.format(date=today)
    _, notes = _http_get(url)
    if notes:
        for i, n in enumerate(notes, 1):
            print(f"#{i} {n['title']} — {n['authorName']}")


def demo_top3():
    """Demo 2: 只取前 3 篇"""
    notes = fetch()
    if notes:
        for item in notes[:3]:
            print(f"{item['title']} — {item['authorName']}")
            print(f"  {item['url']}")


def demo_with_products():
    """Demo 3: 展示有关联产品的笔记"""
    notes = fetch()
    if notes:
        for item in notes:
            products = item.get("productNames") or []
            if products:
                names = ", ".join(p.get("productName", "") for p in products)
                print(f"[{names}] {item['title']} — {item['authorName']}")
                print(f"  {item['noteUrl']}")


def demo_date_range():
    """Demo 4: 查询最近 7 天各天第 1 篇标题"""
    today = datetime.date.today()
    for i in range(7):
        day = (today - datetime.timedelta(days=i)).isoformat()
        notes = fetch(date=day, auto_fallback=False)
        if notes:
            top1 = notes[0]
            print(f"{day}  #1 {top1['title']} — {top1['authorName']}")
        else:
            print(f"{day}  [无数据]")
