#!/usr/bin/env python3
"""Search Airbnb and filter by basic criteria.

Usage:
    python3 scripts/search.py "Brighton" --check-in 2026-08-27 --check-out 2026-09-04 \
        --guests 3 --currency CNY --bedrooms 2 --max-price 20000 --min-rating 4.8 \
        --max-distance-km 2.5 --center-lat 50.8225 --center-lng -0.1373
"""

import argparse
import json
import math
import re
import sys
from datetime import date, timedelta


def main():
    p = argparse.ArgumentParser()
    p.add_argument("location", nargs="?", default="Brighton")
    p.add_argument("--check-in", default=None)
    p.add_argument("--check-out", default=None)
    p.add_argument("--guests", type=int, default=2)
    p.add_argument("--currency", default="CNY")
    p.add_argument("--language", default="zh")
    p.add_argument("--bedrooms", type=int, default=0)
    p.add_argument("--max-price", type=float, default=0)
    p.add_argument("--min-rating", type=float, default=0)
    p.add_argument("--max-distance-km", type=float, default=5)
    p.add_argument("--center-lat", type=float, default=50.8225)
    p.add_argument("--center-lng", type=float, default=-0.1373)
    p.add_argument("--proxy", default="")
    p.add_argument("--output", default="/tmp/airbnb_candidates.json")
    args = p.parse_args()

    import pyairbnb

    # Defaults
    check_in = args.check_in or (date.today() + timedelta(days=7)).isoformat()
    check_out = args.check_out or (date.today() + timedelta(days=14)).isoformat()

    # Search box
    delta = args.max_distance_km / 111.0
    ne_lat = args.center_lat + delta
    ne_long = args.center_lng + delta
    sw_lat = args.center_lat - delta
    sw_long = args.center_lng - delta
    zoom = 13 if args.max_distance_km <= 3 else 12

    print(f"🔍 {args.location}: {check_in}→{check_out}, {args.guests} guests, {args.currency}", file=sys.stderr)

    results = pyairbnb.search_all(
        check_in=check_in, check_out=check_out,
        ne_lat=ne_lat, ne_long=ne_long, sw_lat=sw_lat, sw_long=sw_long,
        zoom_value=zoom, price_min=0, price_max=0, place_type="",
        amenities=[], free_cancellation=False,
        currency=args.currency, language=args.language, proxy_url=args.proxy,
    )
    print(f"✅ Found {len(results)} listings", file=sys.stderr)

    # Filter
    candidates = []
    for r in results:
        pl = r.get("structuredContent", {}).get("primaryLine", [])
        bedrooms = 0
        for item in pl:
            if item.get("type") == "BEDINFO":
                body = item.get("body", "")
                m = re.search(r"(\d+)\s*(?:间卧室|卧室|bedrooms?|br)", body, re.IGNORECASE)
                if m:
                    bedrooms = int(m.group(1))
                    break

        bp = r.get("price", {}).get("break_down", [])
        total = next((b.get("amount", 0) for b in bp if "折后" in b.get("description", "")),
                     r.get("price", {}).get("unit", {}).get("amount", 0))

        rating = r.get("rating", {}).get("value", 0)
        coord = r.get("coordinates", {})
        clat = coord.get("latitude", 0)
        clng = coord.get("longitud", coord.get("longitude", 0))
        dist = math.sqrt(((clat - args.center_lat) * 111) ** 2 + ((clng - args.center_lng) * 111 * math.cos(math.radians(args.center_lat))) ** 2)

        if args.bedrooms > 0 and bedrooms < args.bedrooms:
            continue
        if args.max_price > 0 and total > args.max_price:
            continue
        if args.min_rating > 0 and rating < args.min_rating:
            continue
        if dist > args.max_distance_km:
            continue

        rs = (r.get("structuredContent", {}).get("reviewSnippet") or [{}])[0]
        candidates.append({
            "room_id": str(r.get("room_id")),
            "name": r.get("name", ""),
            "bedrooms": bedrooms,
            "total_price": total,
            "rating": rating,
            "reviewCount": r.get("rating", {}).get("reviewCount", "0"),
            "distance_km": round(dist, 2),
            "badges": r.get("badges", []),
            "reviewSnippet": (rs.get("body", "") or "")[:80],
            "price_unit": r.get("price", {}).get("unit", {}).get("amount", 0),
            "url": f"https://www.airbnb.com/rooms/{r.get('room_id')}",
        })

    candidates.sort(key=lambda x: x["distance_km"])
    print(f"🎯 Filtered to {len(candidates)}", file=sys.stderr)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(candidates, f, ensure_ascii=False, indent=2)
    print(f"💾 Saved to {args.output}", file=sys.stderr)

    # Print summary
    for i, c in enumerate(candidates[:20]):
        b = "⭐".join([b.replace("TOP_X_GUEST_FAVORITE", "热门").replace("GUEST_FAVORITE", "好评") for b in c["badges"]])
        bt = f" [{b}]" if b else ""
        print(f"#{i+1}: {c['name']}{bt} | {c['bedrooms']}卧 ￥{c['total_price']:.0f} ⭐{c['rating']} {c['distance_km']}km | {c['reviewSnippet']}")


if __name__ == "__main__":
    main()
