#!/usr/bin/env python3
"""每日竞品 ASIN 价格监控 — 抓取 Amazon 详情页并输出报告到 stdout。
用 OpenClaw automation 的 command 定时跑，不另起一轮模型。stdout 可推到 Discord/Telegram。

用法:
  python3 asin_price_monitor.py

定时任务（北京时间每天 9:00）:
  openclaw automations create "0 9 * * *" \\
    --name "竞品价格监控" --tz Asia/Shanghai \\
    --command "python3 ~/.openclaw/skills/amazon-scraper/scripts/asin_price_monitor.py" \\
    --session isolated --announce

自定义: 修改 ASINS 列表增删监控目标。
"""
import json, sys, os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scraper_client import scrape_detail as _scrape_detail, ScrapeError

# ─── 监控ASIN列表（在此增删） ───
ASINS = [
    "B0D1XD1ZV3",  # Apple AirPods Pro 2
    "B0CHWRXH8B",  # Bose QC Ultra
    "B09XS7NSWH",  # Sony WF-1000XM4
]

# ─── 历史数据文件（用于对比变化） ───
HISTORY_FILE = os.path.expanduser("~/.openclaw/amazon-scraper/asin-price-history.json")


def scrape_asin(asin: str) -> dict:
    """用 amazon-scraper Docker 镜像抓取单个 ASIN 详情页。"""
    try:
        p = _scrape_detail(asin)
    except ScrapeError as e:
        return {"asin": asin, "error": str(e)}
    return {
        "asin": asin,
        "title": (p.get("title") or "")[:80],
        "price": p.get("price"),
        "priceStr": p.get("priceStr"),
        "rating": p.get("rating"),
        "reviews": p.get("reviews"),
        "bullets_count": len(p.get("bullets", [])),
        "boughtPastMonth": p.get("boughtPastMonth"),
    }


def load_history() -> dict:
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE) as f:
            return json.load(f)
    return {}


def save_history(history: dict):
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def format_report(results: list, history: dict) -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    lines = [f"📊 **每日竞品价格监控报告** ({today})", ""]

    for r in results:
        asin = r["asin"]
        if "error" in r:
            lines.append(f"❌ `{asin}` — 抓取失败: {r['error']}")
            continue

        price = r.get("priceStr") or "N/A"
        rating = r.get("rating") or "N/A"
        reviews = r.get("reviews")
        reviews_str = f"{reviews:,}" if reviews else "N/A"
        bought = r.get("boughtPastMonth") or "N/A"

        prev = history.get(asin, {})
        prev_price = prev.get("priceStr", "")
        change_indicator = ""
        if prev_price and prev_price != price:
            change_indicator = f" ⚡was {prev_price}"

        lines.append(f"**`{asin}`** {r['title']}")
        lines.append(f"  💰 {price}{change_indicator} | ⭐ {rating} | 💬 {reviews_str} | 📦 {bought}/月")
        lines.append("")

    # Merge, don't replace. Rebuilding the file from this run alone dropped every
    # ASIN that failed today, so the next run reported it as a brand-new listing.
    new_history = dict(history)
    for r in results:
        if "error" not in r:
            new_history[r["asin"]] = {
                "priceStr": r.get("priceStr"),
                "price": r.get("price"),
                "date": today,
            }
    save_history(new_history)

    lines.append(f"_下次监控将对比今日价格变化_")
    return "\n".join(lines)


def main():
    results = []
    for asin in ASINS:
        r = scrape_asin(asin)
        results.append(r)
        status = "✅" if "error" not in r else "❌"
        print(f"{status} {asin}", file=sys.stderr)

    history = load_history()
    report = format_report(results, history)
    print(report)


if __name__ == "__main__":
    main()
