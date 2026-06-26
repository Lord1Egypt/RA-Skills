#!/usr/bin/env python3
import argparse
import json
import math
import sys
from typing import Any, Dict, List, Optional


def normalize_text(s: Optional[str]) -> str:
    return (s or "").strip().lower()


def collect_station_names(subway_data: Dict[str, Any]) -> List[Dict[str, str]]:
    items = []
    for line in subway_data.get("lines", []):
        line_name = line.get("name", "")
        for station in line.get("stations", []):
            station_name = station["name"] if isinstance(station, dict) else str(station)
            items.append({"line": line_name, "station": station_name})
    return items


def score_hotel(hotel: Dict[str, Any], subway_data: Dict[str, Any], target_line: Optional[str], target_station: Optional[str]) -> Dict[str, Any]:
    text_parts = [
        hotel.get("name", ""),
        hotel.get("address", ""),
        hotel.get("interestsPoi", ""),
        hotel.get("review", ""),
        hotel.get("brandName", ""),
    ]
    blob = " ".join([x for x in text_parts if x])
    blob_norm = normalize_text(blob)

    score = 0
    matched_station = None
    matched_line = None
    reasons: List[str] = []

    # target station has highest weight
    if target_station and normalize_text(target_station) in blob_norm:
        score += 60
        matched_station = target_station
        reasons.append(f"命中目标站点：{target_station}")

    # station mentions from subway dataset
    for item in collect_station_names(subway_data):
        station = item["station"]
        line = item["line"]
        if normalize_text(station) and normalize_text(station) in blob_norm:
            if not matched_station:
                matched_station = station
                matched_line = line
            score += 18
            reasons.append(f"文本提到地铁站：{station}（{line}）")
            break

    # target line mention
    if target_line and normalize_text(target_line) in blob_norm:
        score += 28
        matched_line = target_line
        reasons.append(f"命中目标线路：{target_line}")

    # interchange / transport convenience hints
    hint_words = [
        ("地铁", 10),
        ("地铁站", 10),
        ("换乘", 10),
        ("火车站", 8),
        ("高铁站", 8),
        ("机场", 6),
        ("步行", 6),
        ("近", 3),
    ]
    for word, pts in hint_words:
        if word in blob:
            score += pts
            reasons.append(f"包含便利性关键词：{word}")

    # mild preference for stronger rating when transit fit is close
    try:
        rating = float(str(hotel.get("score", "0") or "0"))
        score += rating * 2
    except Exception:
        pass

    return {
        "name": hotel.get("name", ""),
        "address": hotel.get("address", ""),
        "price": hotel.get("price", ""),
        "score_desc": hotel.get("scoreDesc", ""),
        "review": hotel.get("review", ""),
        "matched_station": matched_station,
        "matched_line": matched_line,
        "transit_score": round(score, 2),
        "reasons": reasons,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Score hotels by metro convenience using subway data + hotel JSON.")
    parser.add_argument("--subway", required=True, help="Path to subway JSON from fetch_subway_data.py")
    parser.add_argument("--hotels", required=True, help="Path to hotel JSON (list or flyai payload)")
    parser.add_argument("--target-line", help="Preferred line name, e.g. 1号线")
    parser.add_argument("--target-station", help="Preferred station name, e.g. 黄土岭")
    parser.add_argument("--top", type=int, default=5, help="Number of top hotels to output")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    try:
        with open(args.subway, "r", encoding="utf-8") as f:
            subway_data = json.load(f)
        with open(args.hotels, "r", encoding="utf-8") as f:
            hotel_payload = json.load(f)

        if isinstance(hotel_payload, list):
            hotels = hotel_payload
        else:
            hotels = hotel_payload.get("data", {}).get("itemList", hotel_payload.get("itemList", []))

        ranked = [
            score_hotel(h, subway_data, args.target_line, args.target_station)
            for h in hotels
        ]
        ranked.sort(key=lambda x: x["transit_score"], reverse=True)
        output = {
            "target_line": args.target_line,
            "target_station": args.target_station,
            "count": min(args.top, len(ranked)),
            "results": ranked[: args.top],
        }
        if args.pretty:
            print(json.dumps(output, ensure_ascii=False, indent=2))
        else:
            print(json.dumps(output, ensure_ascii=False))
        return 0
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
