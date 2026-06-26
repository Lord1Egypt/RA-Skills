#!/usr/bin/env python3
import argparse
import json
import sys
from typing import Dict, List, Tuple

import requests

INDEX_URL = "http://map.amap.com/subway/index.html?&1100"
DETAIL_URL = "http://map.amap.com/service/subway?srhdata={city_id}_drw_{cityname}.json"
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36"
}


def fetch_index() -> str:
    resp = requests.get(INDEX_URL, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    resp.encoding = "utf-8"
    return resp.text


def parse_city_index(html: str) -> List[Tuple[str, str, str]]:
    import re

    matches = re.findall(r'<a[^>]+id="(\d+)"[^>]+cityname="([^"]+)"[^>]*>([^<]+)</a>', html)
    seen = set()
    result = []
    for city_id, cityname, display_name in matches:
        key = (city_id, cityname, display_name.strip())
        if key in seen:
            continue
        seen.add(key)
        result.append(key)
    return result


def find_city(city_query: str, cities: List[Tuple[str, str, str]]) -> Tuple[str, str, str]:
    q = city_query.strip().lower()
    for city_id, cityname, display_name in cities:
        if q == display_name.lower() or q == cityname.lower() or q == city_id:
            return city_id, cityname, display_name
    # contains fallback
    for city_id, cityname, display_name in cities:
        if q in display_name.lower() or q in cityname.lower():
            return city_id, cityname, display_name
    raise ValueError(f"City not found in AMap subway index: {city_query}")


def fetch_city_detail(city_id: str, cityname: str) -> Dict:
    url = DETAIL_URL.format(city_id=city_id, cityname=cityname)
    resp = requests.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    data = resp.json()
    return data


def normalize_city_data(display_name: str, data: Dict) -> Dict:
    lines_out = []
    for line in data.get("l", []):
        line_name = line.get("ln", "")
        branch = line.get("la", "")
        full_name = f"{line_name}({branch})" if branch else line_name
        stations = []
        for st in line.get("st", []):
            stations.append(
                {
                    "name": st.get("n", ""),
                    "id": st.get("sid", ""),
                }
            )
        lines_out.append(
            {
                "name": full_name,
                "raw_name": line_name,
                "branch": branch,
                "station_count": len(stations),
                "stations": stations,
            }
        )

    return {
        "city": display_name,
        "source": "AMap subway",
        "network_name": data.get("s", ""),
        "city_id": data.get("i", ""),
        "line_count": len(lines_out),
        "lines": lines_out,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch subway / metro line and station data from AMap.")
    parser.add_argument("city", help="City name, pinyin cityname, or AMap city id, e.g. 长沙 / changsha / 4301")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON")
    parser.add_argument("--stations-only", action="store_true", help="Output only line names and station names")
    args = parser.parse_args()

    try:
        html = fetch_index()
        cities = parse_city_index(html)
        city_id, cityname, display_name = find_city(args.city, cities)
        raw = fetch_city_detail(city_id, cityname)
        normalized = normalize_city_data(display_name, raw)

        if args.stations_only:
            simplified = {
                "city": normalized["city"],
                "line_count": normalized["line_count"],
                "lines": [
                    {
                        "name": line["name"],
                        "stations": [s["name"] for s in line["stations"]],
                    }
                    for line in normalized["lines"]
                ],
            }
            payload = simplified
        else:
            payload = normalized

        if args.pretty:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print(json.dumps(payload, ensure_ascii=False))
        return 0
    except Exception as e:
        print(json.dumps({"error": str(e), "city": args.city}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
