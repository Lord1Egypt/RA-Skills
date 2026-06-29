#!/usr/bin/env python3
import os
import sys
import json
import re
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime

def print_help():
    print("""
Bing Webmaster Tools Data Retrieval Script (Zero-Dependency)

Usage:
  python3 fetch_data.py --site-url <SITE_URL> --method <METHOD> [--api-key <API_KEY>]

Methods:
  rank_traffic : Fetch search ranking, impressions, clicks, and CTR stats.
  query_stats  : Fetch top keywords driving traffic, impressions, and rankings.
  crawl_stats  : Fetch search crawler crawl statistics and index issues.
  quota        : Fetch remaining URL submission quota.
  all          : Pull all statistics and output a comprehensive Markdown report.

Environment Variable:
  BING_WEBMASTER_API_KEY: Will be used if --api-key is not provided.
""")

def parse_bing_date(date_str):
    if not date_str:
        return "N/A"
    match = re.search(r'/Date\((\d+)(?:[+-]\d+)?\)/', str(date_str))
    if match:
        try:
            timestamp_ms = int(match.group(1))
            date_obj = datetime.fromtimestamp(timestamp_ms / 1000.0)
            return date_obj.strftime('%Y-%m-%d %H:%M:%S')
        except Exception:
            pass
    return str(date_str)

def call_bing_api(method_name, site_url, api_key):
    params = urllib.parse.urlencode({"siteUrl": site_url, "apikey": api_key})
    endpoint = f"https://ssl.bing.com/webmaster/api.svc/json/{method_name}?{params}"
    req = urllib.request.Request(
        endpoint,
        headers={"Accept": "application/json"}
    )
    try:
        with urllib.request.urlopen(req) as response:
            res_body = response.read().decode("utf-8")
            data = json.loads(res_body)
            # Bing JSON API typically wraps the actual array/object in a "d" key
            return data.get("d") if isinstance(data, dict) and "d" in data else data
    except urllib.error.HTTPError as e:
        print(f"❌ API Error calling {method_name}: {e.code} - {e.reason}", file=sys.stderr)
        try:
            print(f"Details: {e.read().decode('utf-8')}", file=sys.stderr)
        except Exception:
            pass
        return None
    except Exception as e:
        print(f"❌ Error calling {method_name}: {e}", file=sys.stderr)
        return None

def main():
    args = sys.argv[1:]
    if "--help" in args or "-h" in args or not args:
        print_help()
        sys.exit(0)

    site_url = None
    method = None
    api_key = os.environ.get("BING_WEBMASTER_API_KEY")

    # Simple argument parsing
    i = 0
    while i < len(args):
        if args[i] == "--site-url":
            site_url = args[i+1]
            i += 2
        elif args[i] == "--method":
            method = args[i+1]
            i += 2
        elif args[i] == "--api-key":
            api_key = args[i+1]
            i += 2
        else:
            print(f"Unknown argument: {args[i]}")
            print_help()
            sys.exit(1)

    if not site_url:
        print("Error: --site-url is required.")
        sys.exit(1)

    if not method:
        print("Error: --method is required.")
        sys.exit(1)

    if not api_key:
        print("Error: Bing Webmaster API Key is missing. Provide it via --api-key or set BING_WEBMASTER_API_KEY env variable.")
        sys.exit(1)

    valid_methods = ["rank_traffic", "query_stats", "crawl_stats", "quota", "all"]
    if method not in valid_methods:
        print(f"Error: Invalid method '{method}'. Choose from: {', '.join(valid_methods)}")
        sys.exit(1)

    # Dispatch based on method
    if method == "quota":
        res = call_bing_api("GetUrlSubmissionQuota", site_url, api_key)
        if res:
            print(json.dumps(res, indent=2))
        else:
            print("Failed to retrieve quota.")

    elif method == "rank_traffic":
        res = call_bing_api("GetRankAndTrafficStats", site_url, api_key)
        if res:
            if isinstance(res, list):
                print(f"--- Rank and Traffic Statistics for {site_url} ---")
                print(f"{'Date':<20} | {'Clicks':<10} | {'Impressions':<12} | {'Avg Rank':<10}")
                print("-" * 62)
                for item in res[:20]: # Show last 20 records
                    date_val = parse_bing_date(item.get("Date")) if "Date" in item else "N/A"
                    print(f"{date_val:<20} | {item.get('Clicks', 0):<10} | {item.get('Impressions', 0):<12} | {item.get('Rank', 0.0):<10.2f}")
            else:
                print(json.dumps(res, indent=2))
        else:
            print("Failed to retrieve rank & traffic stats.")

    elif method == "query_stats":
        res = call_bing_api("GetQueryStats", site_url, api_key)
        if res:
            if isinstance(res, list):
                print(f"--- Top Search Keywords for {site_url} ---")
                print(f"{'Query Keyword':<30} | {'Clicks':<8} | {'Impressions':<12} | {'CTR':<8} | {'Avg Pos':<10}")
                print("-" * 76)
                for item in res[:30]: # Show top 30 queries
                    q = item.get("Query", "N/A")
                    clicks = item.get("Clicks", 0)
                    imps = item.get("Impressions", 0)
                    ctr = (clicks / imps * 100) if imps > 0 else 0.0
                    pos = item.get("AvgClickPosition", 0.0)
                    print(f"{q:<30} | {clicks:<8} | {imps:<12} | {ctr:<6.2f}% | {pos:<10.2f}")
            else:
                print(json.dumps(res, indent=2))
        else:
            print("Failed to retrieve query statistics.")

    elif method == "crawl_stats":
        res = call_bing_api("GetCrawlStats", site_url, api_key)
        if res:
            if isinstance(res, list):
                print(f"--- Crawl Statistics for {site_url} ---")
                print(f"{'Date':<20} | {'Pages Crawled':<15} | {'Crawl Errors':<15}")
                print("-" * 56)
                for item in res[:20]:
                    date_val = parse_bing_date(item.get("Date")) if "Date" in item else "N/A"
                    print(f"{date_val:<20} | {item.get('PageCount', 0):<15} | {item.get('ErrorCount', 0):<15}")
            else:
                print(json.dumps(res, indent=2))
        else:
            print("Failed to retrieve crawl statistics.")

    elif method == "all":
        print(f"# Bing Webmaster SEO Report: {site_url}\n")
        print(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        # 1. Quota
        quota = call_bing_api("GetUrlSubmissionQuota", site_url, api_key)
        if quota:
            print("## 🚀 URL Submission Quota Status")
            print(f"- **Daily Quota (Remaining/Total)**: `{quota.get('DailyQuota', 'N/A')}`")
            print(f"- **Monthly Quota (Remaining/Total)**: `{quota.get('MonthlyQuota', 'N/A')}`\n")

        # 2. Rank & Traffic Summary
        traffic = call_bing_api("GetRankAndTrafficStats", site_url, api_key)
        if traffic and isinstance(traffic, list):
            print("## 📊 Recent Rank & Traffic (Last 10 Records)")
            print("| Date | Clicks | Impressions | Avg Rank |")
            print("| :--- | :---: | :---: | :---: |")
            for item in traffic[:10]:
                date_val = parse_bing_date(item.get("Date")).split()[0]
                print(f"| {date_val} | {item.get('Clicks', 0)} | {item.get('Impressions', 0)} | {item.get('Rank', 0.0):.2f} |")
            print()

        # 3. Keyword Performance
        queries = call_bing_api("GetQueryStats", site_url, api_key)
        if queries and isinstance(queries, list):
            print("## 🔑 Top Search Keywords (Driving Traffic)")
            print("| Query Keyword | Clicks | Impressions | CTR | Avg Click Position |")
            print("| :--- | :---: | :---: | :---: | :---: |")
            for item in queries[:15]:
                q = item.get("Query", "N/A")
                clicks = item.get("Clicks", 0)
                imps = item.get("Impressions", 0)
                ctr = (clicks / imps * 100) if imps > 0 else 0.0
                pos = item.get("AvgClickPosition", 0.0)
                print(f"| {q} | {clicks} | {imps} | {ctr:.2f}% | {pos:.2f} |")
            print()

        # 4. Crawl Stats
        crawl = call_bing_api("GetCrawlStats", site_url, api_key)
        if crawl and isinstance(crawl, list):
            print("## 🕷️ Crawl Health")
            print("| Date | Pages Crawled | Crawl Errors |")
            print("| :--- | :---: | :---: |")
            for item in crawl[:10]:
                date_val = parse_bing_date(item.get("Date")).split()[0]
                print(f"| {date_val} | {item.get('PageCount', 0)} | {item.get('ErrorCount', 0)} |")
            print()

if __name__ == "__main__":
    main()
