#!/usr/bin/env python3
"""
Freelance Job Scraper — HN + YC Jobs + Remote Boards
Usage: python scan_jobs.py [--keyword KW] [--min-pay USD] [--output FILE]
"""

import json
import subprocess
import re
import sys
import argparse
from datetime import datetime, timezone

KEYWORDS_AI = ["ai", "automation", "python", "scraping", "llm", "gpt", "agent", "bot", "api", "data"]
KEYWORDS_PAY = ["$", "usd", "hour", "fixed", "budget", "pay"]

def gh(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return []
    try:
        return json.loads(result.stdout)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return []

def score_job(text, reply_count=0):
    text_lower = text.lower()
    score = 0
    reasons = []
    for kw in KEYWORDS_AI:
        if kw in text_lower:
            score += 3
            reasons.append(f"AI keyword: {kw}")
            break
    for kw in KEYWORDS_PAY:
        if kw in text_lower:
            m = re.search(r'\$[\d,]+', text)
            if m:
                amt = int(m.group().replace('$', '').replace(',', ''))
                if amt >= 100:
                    score += 3
                    reasons.append(f"High payout: ${amt}")
                elif amt >= 25:
                    score += 1
                    reasons.append(f"Pay: ${amt}")
            break
    if "yc" in text_lower or "y combinator" in text_lower:
        score += 2
        reasons.append("YC company")
    if "remote" in text_lower or "async" in text_lower:
        score += 1
        reasons.append("Remote OK")
    if reply_count < 5:
        score += 2
        reasons.append(f"Low competition ({reply_count} replies)")
    elif reply_count < 15:
        score += 1
    return score, reasons

def scan_hn_jobs(month=None, year=2026):
    if not month:
        now = datetime.now(timezone.utc)
        month = now.month
    results = []
    query = f'"{month} who is hiring" site:news.ycombinator.com'
    items = gh(["gh", "api", "search/issues", "-X", "GET",
                 "-f", f"q={query}", "-F", "per_page=5"])
    for item in (items.get("items", []) if isinstance(items, dict) else [])[:3]:
        title = item.get("title", "")
        url = item.get("html_url", "")
        if "who is hiring" in title.lower():
            score, reasons = score_job(title)
            results.append({
                "source": "HN Who is Hiring",
                "title": title,
                "url": url,
                "score": score,
                "reasons": reasons
            })
    return results

def main():
    parser = argparse.ArgumentParser(description="Freelance Job Scraper")
    parser.add_argument("--keyword", "-k", default=None)
    parser.add_argument("--min-pay", "-m", type=int, default=0)
    parser.add_argument("--output", "-o", default=None)
    args = parser.parse_args()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    print(f"## Freelance Lead Digest — {today}")
    print()
    hn_jobs = scan_hn_jobs()
    all_jobs = sorted(hn_jobs, key=lambda x: x["score"], reverse=True)
    hot = [j for j in all_jobs if j["score"] >= 7]
    medium = [j for j in all_jobs if 4 <= j["score"] < 7]
    low = [j for j in all_jobs if j["score"] < 4]
    if hot:
        print("### Hot Leads (score >= 7)")
        for j in hot:
            print(f"- [{j['source']}] {j['title']} | score: {j['score']} | {', '.join(j['reasons'])}")
            print(f"  {j['url']}")
        print()
    if medium:
        print("### Medium Leads (score 4-6)")
        for j in medium:
            print(f"- [{j['source']}] {j['title']} | score: {j['score']}")
            print(f"  {j['url']}")
        print()
    if low:
        print("### Low Priority (score < 4)")
        for j in low[:3]:
            print(f"- [{j['source']}] {j['title']}")
        print()
    if not all_jobs:
        print("No relevant jobs found. Check back tomorrow.")
    report = sys.stdout.getvalue() if hasattr(sys.stdout, 'getvalue') else ""
    if args.output:
        with open(args.output, "w") as f:
            f.write(report)
        print(f"Report written to {args.output}")

if __name__ == "__main__":
    main()
