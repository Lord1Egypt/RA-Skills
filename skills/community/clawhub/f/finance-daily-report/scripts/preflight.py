#!/usr/bin/env python3
"""
Pre-flight check: verify which data sources are reachable.
Returns a JSON report of URL availability for the agent to use.

Usage:
    python3 preflight.py [--timeout 10]

This script tests all Tier 1 and Tier 2 data sources and reports which ones
are accessible. The agent then uses web_fetch (which converts HTML to markdown)
to actually extract data from reachable sources.
"""

import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime

TIMEOUT = 10

SOURCES = [
    # Tier 1: Structured data (Trading Economics)
    {"key": "te_stocks", "url": "https://tradingeconomics.com/stocks", "tier": 1, "module": "股指"},
    {"key": "te_currencies", "url": "https://tradingeconomics.com/currencies", "tier": 1, "module": "汇率"},
    {"key": "te_commodities", "url": "https://tradingeconomics.com/commodities", "tier": 1, "module": "商品"},
    {"key": "te_bonds", "url": "https://tradingeconomics.com/bonds", "tier": 1, "module": "利率"},
    {"key": "te_us_market", "url": "https://tradingeconomics.com/united-states/stock-market", "tier": 1, "module": "美股分析"},
    {"key": "te_us_dollar", "url": "https://tradingeconomics.com/united-states/currency", "tier": 1, "module": "美元分析"},
    {"key": "te_oil", "url": "https://tradingeconomics.com/commodity/crude-oil", "tier": 1, "module": "原油分析"},
    {"key": "te_gold", "url": "https://tradingeconomics.com/commodity/gold", "tier": 1, "module": "黄金分析"},
    {"key": "te_cny", "url": "https://tradingeconomics.com/china/currency", "tier": 1, "module": "人民币分析"},
    {"key": "te_silver", "url": "https://tradingeconomics.com/commodity/silver", "tier": 1, "module": "白银分析"},
    # Tier 2: News & Calendar
    {"key": "jin10", "url": "https://www.jin10.com/", "tier": 2, "module": "新闻/快讯"},
    {"key": "cls", "url": "https://www.cls.cn/", "tier": 2, "module": "日历/前瞻"},
    {"key": "eastmoney", "url": "https://www.eastmoney.com/", "tier": 2, "module": "A股/基金"},
    # Tier 3: Search
    {"key": "cnbc_dji", "url": "https://www.cnbc.com/quotes/.DJI/", "tier": 2, "module": "道琼斯"},
]


def check_url(url):
    """Check if a URL is reachable. Returns (status_code, response_length, error)."""
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; FinanceBot/1.0)",
        "Accept": "text/html",
    }
    req = urllib.request.Request(url, headers=headers, method="HEAD")
    try:
        # Try HEAD first (faster)
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return resp.status, 0, None
    except Exception:
        # Fall back to GET
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                body = resp.read()
                return resp.status, len(body), None
        except urllib.error.HTTPError as e:
            return e.code, 0, str(e)
        except Exception as e:
            return 0, 0, str(e)


def main():
    global TIMEOUT
    import argparse
    parser = argparse.ArgumentParser(description="Pre-flight source availability check")
    parser.add_argument("--timeout", type=int, default=TIMEOUT, help="Timeout per URL")
    args = parser.parse_args()
    TIMEOUT = args.timeout

    results = []
    reachable = 0
    failed = 0

    print("=" * 60)
    print("Finance Daily Report — Source Pre-flight Check")
    print("=" * 60)

    for src in SOURCES:
        sys.stdout.write(f"  [{src['tier']}] {src['key']:20s} ... ")
        sys.stdout.flush()
        status, size, error = check_url(src["url"])
        ok = 200 <= status < 400
        if ok:
            reachable += 1
            print(f"✅ {status}")
        else:
            failed += 1
            print(f"❌ {status} {error or ''}")

        results.append({
            "key": src["key"],
            "url": src["url"],
            "tier": src["tier"],
            "module": src["module"],
            "reachable": ok,
            "status": status,
            "error": error,
        })

    print("=" * 60)
    print(f"Result: {reachable}/{len(SOURCES)} reachable, {failed} failed")
    print("=" * 60)

    # Output recommendation
    reachable_urls = [r for r in results if r["reachable"]]
    failed_urls = [r for r in results if not r["reachable"]]

    report = {
        "check_time": datetime.now().isoformat(),
        "total": len(SOURCES),
        "reachable": reachable,
        "failed": failed,
        "recommendation": "proceed" if reachable >= 8 else ("partial" if reachable >= 4 else "manual"),
        "reachable_sources": reachable_urls,
        "failed_sources": failed_urls,
    }

    # Print recommendation
    if report["recommendation"] == "proceed":
        print("\n✅ Recommendation: PROCEED with automated collection")
        print("   Use web_fetch on all reachable URLs")
    elif report["recommendation"] == "partial":
        print("\n⚠️ Recommendation: PARTIAL — some sources down")
        print("   Use available sources, mark missing modules as 数据暂缺")
    else:
        print("\n❌ Recommendation: MANUAL fallback needed")
        print("   Most sources unreachable, agent should try web_search or skip")

    # Print fetch plan
    print("\nFetch plan (reachable URLs):")
    for r in reachable_urls:
        print(f"  web_fetch(\"{r['url']}\") → {r['module']}")

    # Save report
    os.makedirs("/tmp/finance-data", exist_ok=True)
    with open("/tmp/finance-data/preflight.json", "w") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\nSaved: /tmp/finance-data/preflight.json")
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
