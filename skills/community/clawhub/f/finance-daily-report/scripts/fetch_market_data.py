#!/usr/bin/env python3
"""
Fetch market data from reliable, tested sources using web_fetch-compatible HTTP.
Outputs structured JSON for each module.

Usage:
    python3 fetch_market_data.py [--date 2026-03-13] [--out-dir /tmp/finance-data]

Data Sources (tested & reliable, no auth required):
    - Trading Economics: stocks, currencies, commodities, bonds (structured tables)
    - 金十数据 (jin10.com): Chinese market news, calendar
    - 财联社 (cls.cn): Economic calendar, events
    - 东方财富 (eastmoney.com): A-share data
    - CNBC: Individual index quotes (e.g. /quotes/.DJI/)
"""

import json
import os
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime, timedelta

DEFAULT_OUT = "/tmp/finance-data"
TIMEOUT = 15

# ── Reliable data source URLs ──
SOURCES = {
    "te_stocks": {
        "url": "https://tradingeconomics.com/stocks",
        "desc": "Global stock indices",
        "module": "核心股市表现"
    },
    "te_currencies": {
        "url": "https://tradingeconomics.com/currencies",
        "desc": "Major currency pairs + DXY",
        "module": "汇率与美元"
    },
    "te_commodities": {
        "url": "https://tradingeconomics.com/commodities",
        "desc": "Oil, gold, silver, copper, iron ore",
        "module": "商品与核心资产"
    },
    "te_us_bonds": {
        "url": "https://tradingeconomics.com/united-states/government-bond-yield",
        "desc": "US 10Y Treasury yield + analysis",
        "module": "全球利率与美债"
    },
    "te_us_stocks": {
        "url": "https://tradingeconomics.com/united-states/stock-market",
        "desc": "S&P 500 detailed analysis",
        "module": "市场主线"
    },
    "te_us_dollar": {
        "url": "https://tradingeconomics.com/united-states/currency",
        "desc": "DXY detailed analysis",
        "module": "汇率与美元"
    },
    "te_gold": {
        "url": "https://tradingeconomics.com/commodity/gold",
        "desc": "Gold detailed analysis",
        "module": "商品与核心资产"
    },
    "te_oil": {
        "url": "https://tradingeconomics.com/commodity/crude-oil",
        "desc": "WTI crude oil detailed analysis",
        "module": "商品与核心资产"
    },
    "te_cny": {
        "url": "https://tradingeconomics.com/china/currency",
        "desc": "USD/CNY detailed analysis",
        "module": "汇率与美元"
    },
    "jin10": {
        "url": "https://www.jin10.com/",
        "desc": "Chinese financial news feed",
        "module": "市场主线"
    },
    "cls_calendar": {
        "url": "https://www.cls.cn/",
        "desc": "Economic calendar & events",
        "module": "明日重点前瞻"
    },
    "eastmoney": {
        "url": "https://www.eastmoney.com/",
        "desc": "A-share market summary",
        "module": "核心股市表现"
    }
}


def fetch_url(url, max_chars=8000):
    """Fetch a URL and return text content."""
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; FinanceBot/1.0)",
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            content = resp.read().decode("utf-8", errors="replace")
            return content[:max_chars]
    except (urllib.error.HTTPError, urllib.error.URLError) as e:
        return f"ERROR: {e}"
    except Exception as e:
        return f"ERROR: {e}"


def extract_te_table(html, source_key):
    """Extract structured data from Trading Economics table pages.
    Returns list of dicts with name, price, day_change, pct_change, monthly, date."""
    results = []
    # TE tables have pattern: [Name](link)\n\nPrice\n\nDayChange\n\n%Change\n\nMonthly\n\nDate
    # We look for rows in the text
    lines = html.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # Look for lines with trading economics links
        match = re.search(r'\[([^\]]+)\]\(/([^)]+)\)', line)
        if match:
            name = match.group(1)
            # Try to get next numeric values
            values = []
            j = i + 1
            while j < len(lines) and len(values) < 5:
                val = lines[j].strip()
                if val and val not in ('', 'Price', 'Day', '%', 'Monthly', 'Date',
                                        'Major', 'Europe', 'Asia', 'Americas', 'Energy',
                                        'Metals', 'Agricultural', 'Industrials'):
                    values.append(val)
                j += 1
            if len(values) >= 4:
                results.append({
                    "name": name,
                    "price": values[0],
                    "day_change": values[1],
                    "pct_change": values[2],
                    "monthly_change": values[3],
                    "date": values[4] if len(values) > 4 else "",
                    "source_url": SOURCES[source_key]["url"],
                    "source_name": "Trading Economics"
                })
        i += 1
    # Deduplicate by name
    seen = set()
    unique = []
    for r in results:
        if r["name"] not in seen:
            seen.add(r["name"])
            unique.append(r)
    return unique


def extract_te_analysis(html):
    """Extract analysis paragraphs from TE detail pages."""
    # Find paragraphs starting with ## that contain analysis
    paragraphs = []
    for match in re.finditer(r'## (.+?)(?=\n##|\nRelated|\nActual|\Z)', html, re.DOTALL):
        text = match.group(1).strip()
        if len(text) > 50 and not text.startswith("The main stock"):
            paragraphs.append(text)
    return paragraphs


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Fetch market data from reliable sources")
    parser.add_argument("--date", default=None, help="Report date (YYYY-MM-DD)")
    parser.add_argument("--out-dir", default=DEFAULT_OUT, help="Output directory")
    parser.add_argument("--sources", default="all", help="Comma-separated source keys or 'all'")
    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)

    source_keys = list(SOURCES.keys()) if args.sources == "all" else args.sources.split(",")

    results = {}
    errors = []

    for key in source_keys:
        if key not in SOURCES:
            print(f"Unknown source: {key}", file=sys.stderr)
            continue

        src = SOURCES[key]
        print(f"Fetching {key}: {src['url']}...")
        html = fetch_url(src["url"])

        if html.startswith("ERROR:"):
            errors.append({"source": key, "url": src["url"], "error": html})
            print(f"  FAILED: {html}")
            continue

        # Parse structured data from table pages
        data = {"source": key, "module": src["module"], "url": src["url"]}

        if key.startswith("te_") and key in ("te_stocks", "te_currencies", "te_commodities"):
            data["table"] = extract_te_table(html, key)
            data["type"] = "table"
        elif key.startswith("te_"):
            data["analysis"] = extract_te_analysis(html)
            data["raw_text"] = html[:5000]
            data["type"] = "analysis"
        else:
            data["raw_text"] = html[:5000]
            data["type"] = "news"

        results[key] = data
        row_count = len(data.get("table", [])) or len(data.get("analysis", []))
        print(f"  OK: {row_count} items extracted")

    # Save results
    output = {
        "fetch_time": datetime.now().isoformat(),
        "report_date": args.date or "auto",
        "sources_attempted": len(source_keys),
        "sources_ok": len(results),
        "sources_failed": len(errors),
        "data": results,
        "errors": errors
    }

    out_path = os.path.join(args.out_dir, "market_data.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nSaved to: {out_path}")
    print(f"Success: {len(results)}/{len(source_keys)} sources")
    if errors:
        print(f"Failed: {len(errors)} sources")
        for e in errors:
            print(f"  - {e['source']}: {e['error']}")

    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main() or 0)
