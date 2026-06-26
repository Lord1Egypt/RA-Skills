#!/usr/bin/env python3
"""Fetch listing details and search for keywords (parking, basement, renovation).

Usage:
    python3 scripts/details.py /tmp/airbnb_candidates.json --top 15
    python3 scripts/details.py /tmp/airbnb_candidates.json --top 15 --output /tmp/airbnb_results.json
"""

import argparse
import json
import re
import sys

from curl_cffi import requests


def main():
    p = argparse.ArgumentParser()
    p.add_argument("input", default="/tmp/airbnb_candidates.json")
    p.add_argument("--top", type=int, default=10)
    p.add_argument("--output", default="/tmp/airbnb_results.json")
    p.add_argument("--check-in", default="")
    p.add_argument("--check-out", default="")
    p.add_argument("--guests", type=int, default=2)
    args = p.parse_args()

    with open(args.input, encoding="utf-8") as f:
        candidates = json.load(f)

    top = candidates[: args.top]
    print(f"📄 Fetching details for top {len(top)} listings...", file=sys.stderr)

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }

    parking_kw = ["free parking", "parking", "driveway", "garage", "parking space", "off-street parking",
                  "免费停车", "停车位", "可选停车", "车位"]
    basement_kw = ["basement", "semi-basement", "garden level", "lower ground", "lower floor",
                   "地下室", "半地下室", "地下"]
    renovate_kw = ["newly renovated", "recently renovated", "newly refurbished", "recently updated",
                   "brand new", "newly decorated", "modern renovation",
                   "新装修", "翻新", "全新"]

    results = []
    for i, c in enumerate(top):
        url = f"https://www.airbnb.com/rooms/{c['room_id']}?check_in={args.check_in}&check_out={args.check_out}&adults={args.guests}"
        print(f"  [{i+1}/{len(top)}] {c['name']}...", file=sys.stderr)

        try:
            resp = requests.get(url, headers=headers, timeout=15, impersonate="chrome131")
            html = resp.text

            # JSON-LD
            ld = None
            m = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
            if m:
                ld = json.loads(m.group(1))

            room_type = ""
            m = re.search(r'"roomType":"([^"]+)"', html)
            if m:
                room_type = m.group(1)

            property_type = ""
            m = re.search(r'"propertyType":"([^"]+)"', html)
            if m:
                property_type = m.group(1)

            desc = ld.get("description", "") if ld else ""
            all_text = desc + " " + html

            def find_kws(kws):
                found = []
                for kw in kws:
                    if kw.lower() in all_text.lower():
                        idx = all_text.lower().index(kw.lower())
                        ctx = all_text[max(0, idx - 30):idx + len(kw) + 30].strip()
                        found.append({"keyword": kw, "context": ctx[:100]})
                return found

            c["description"] = desc[:300]
            c["room_type"] = room_type
            c["property_type"] = property_type
            c["parking"] = find_kws(parking_kw)
            c["basement"] = find_kws(basement_kw)
            c["renovated"] = find_kws(renovate_kw)
            results.append(c)

        except Exception as e:
            c["detail_error"] = str(e)[:200]
            results.append(c)
            print(f"    ✗ {e}", file=sys.stderr)

    # Sort: parking first, then distance
    with_parking = sorted([r for r in results if r.get("parking") and "detail_error" not in r],
                          key=lambda x: x["distance_km"])
    without = sorted([r for r in results if not r.get("parking") or "detail_error" in r],
                     key=lambda x: x["distance_km"])
    all_sorted = with_parking + without

    print(f"\n{'=' * 60}")
    print("📋 Airbnb Search Results (with detail analysis)")
    print(f"{'=' * 60}")

    for i, r in enumerate(all_sorted):
        pt = "🅿️ 有停车" if r.get("parking") else "❌ 无停车信息"
        bt = "✅ 非地下室"
        if r.get("basement"):
            bt = "⚠️ 地下室风险"
        rt = "🔨 新装修" if r.get("renovated") else ""
        tags = f"{pt} | {bt}"
        if rt:
            tags += f" | {rt}"

        print(f"\n--- #{i+1}: {r['name']} ---")
        print(f"  {tags}")
        print(f"  📍 {r['distance_km']}km | 💰 ￥{r.get('total_price', 0):.0f}/8晚 | ⭐ {r['rating']} ({r.get('reviewCount', '?')}条)")
        if r.get("bedrooms"):
            print(f"  🛏️ {r['bedrooms']}卧 | {r.get('property_type', '')} ({r.get('room_type', '')})")
        if r.get("description"):
            print(f"  📝 {r['description'][:150]}")
        if r.get("parking"):
            for pf in r["parking"][:2]:
                print(f"  🅿️ {pf['keyword']}: {pf['context']}")
        if r.get("basement"):
            for bf in r["basement"][:2]:
                print(f"  ⚠️ {bf['keyword']}: {bf['context']}")
        if r.get("renovated"):
            for rf in r["renovated"][:2]:
                print(f"  🔨 {rf['keyword']}: {rf['context']}")
        print(f"  🔗 {r['url']}")

    # Summary
    print(f"\n{'=' * 60}")
    pc = sum(1 for r in all_sorted if r.get("parking"))
    bc = sum(1 for r in all_sorted if r.get("basement"))
    rc = sum(1 for r in all_sorted if r.get("renovated"))
    print(f"📊 {len(all_sorted)} analyzed | {pc} parking | {bc} basement risk | {rc} renovated")

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(all_sorted, f, ensure_ascii=False, indent=2)
    print(f"💾 Saved to {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
