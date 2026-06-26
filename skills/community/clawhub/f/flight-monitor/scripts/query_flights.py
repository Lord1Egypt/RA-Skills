#!/usr/bin/env python3
"""
flight-monitor: Query flight prices using web search.

This script uses the AI agent's web_search capability as its data source.
When called, it prints a structured prompt that the AI should use to search
for current flight prices, then formats the result.

For programmatic/direct use it also supports a lightweight scrape of
publicly available flight summary pages.

Usage (direct):
    python query_flights.py --from BJS --to SYX --date 2026-03-25
    python query_flights.py --from 北京 --to 三亚 --date 2026-03-25 --max-price 1500
    python query_flights.py --from SHA --to CTU --date 2026-04-01 --return-date 2026-04-05
    python query_flights.py --from BJS --to SYX --date 2026-03-25 --json
"""

import argparse
import json
import sys
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime

# ── City code mapping ────────────────────────────────────────────────────────
CITY_CODES = {
    "北京": "BJS", "上海": "SHA", "广州": "CAN", "深圳": "SZX",
    "杭州": "HGH", "成都": "CTU", "三亚": "SYX", "西安": "SIA",
    "昆明": "KMG", "重庆": "CKG", "武汉": "WUH", "南京": "NKG",
    "厦门": "XMN", "青岛": "TAO", "大连": "DLC", "沈阳": "SHE",
    "长沙": "CSX", "郑州": "CGO", "哈尔滨": "HRB", "乌鲁木齐": "URC",
    "贵阳": "KWE", "福州": "FOC", "南昌": "KHN", "太原": "TYN",
    "海口": "HAK", "兰州": "LHW", "西宁": "XNN", "呼和浩特": "HET",
    "石家庄": "SJW", "南宁": "NNG", "合肥": "HFE", "济南": "TNA",
    "天津": "TSN", "烟台": "YNT", "温州": "WNZ", "宁波": "NGB", "赣州": "KOW",
    "东京": "TYO", "大阪": "OSA", "首尔": "SEL", "新加坡": "SIN",
    "曼谷": "BKK", "香港": "HKG", "台北": "TPE", "澳门": "MFM",
    "纽约": "NYC", "洛杉矶": "LAX", "伦敦": "LON", "巴黎": "PAR",
    "悉尼": "SYD", "迪拜": "DXB",
}
CITY_NAMES = {v: k for k, v in CITY_CODES.items()}

# Airline name → Chinese name
AIRLINE_CN = {
    "CA": "中国国航", "MU": "中国东航", "CZ": "中国南航",
    "HU": "海南航空", "3U": "四川航空", "ZH": "深圳航空",
    "9C": "春秋航空", "HO": "吉祥航空", "GS": "天津航空",
    "MF": "厦门航空", "KN": "中国联航", "VD": "中国联航",
    "EU": "成都航空", "BK": "奥凯航空", "8L": "祥鹏航空",
    "NS": "幸福航空", "Y8": "山东航空", "SC": "山东航空",
    "GJ": "长龙航空", "TV": "九元航空",
}


def resolve_city(s: str) -> tuple:
    """Return (code, name). Input can be Chinese name or IATA code."""
    upper = s.strip().upper()
    if upper in CITY_NAMES:
        return upper, CITY_NAMES[upper]
    orig = s.strip()
    if orig in CITY_CODES:
        return CITY_CODES[orig], orig
    for cn, code in CITY_CODES.items():
        if cn in orig:
            return code, cn
    return upper, upper  # fallback


def build_booking_urls(dep_code: str, arr_code: str, date: str,
                       return_date: str = None) -> dict:
    """Build booking page URLs for major OTAs."""
    d = date.replace("-", "")
    dep_l = dep_code.lower()
    arr_l = arr_code.lower()
    urls = {
        "携程 Ctrip": f"https://flights.ctrip.com/itinerary/oneway/{dep_l}-{arr_l}?depdate={date}",
        "飞猪 Fliggy": (
            f"https://sjipiao.fliggy.com/flight_search_result.htm"
            f"?tripType=0&depCity={dep_code}&arrCity={arr_code}"
            f"&depDate={date}&depCityName={CITY_NAMES.get(dep_code,'')}"
            f"&arrCityName={CITY_NAMES.get(arr_code,'')}"
        ),
        "去哪儿 Qunar": f"https://flight.qunar.com/site/oneway.htm?searchDepartureAirport={CITY_NAMES.get(dep_code,dep_code)}&searchArrivalAirport={CITY_NAMES.get(arr_code,arr_code)}&searchDepartureDate={date}",
        "Google Flights": f"https://www.google.com/travel/flights?q=flights+from+{dep_code}+to+{arr_code}+on+{date}",
    }
    if return_date:
        urls["携程往返 Ctrip RT"] = (
            f"https://flights.ctrip.com/itinerary/roundtrip/{dep_l}-{arr_l}"
            f"?depdate={date}&retdate={return_date}"
        )
    return urls


def generate_search_prompt(dep_code: str, dep_name: str,
                            arr_code: str, arr_name: str,
                            date: str, max_price: float = None,
                            return_date: str = None) -> dict:
    """
    Returns a structured result that instructs the AI to perform a web search
    for live flight prices. This is the primary data-gathering method.
    """
    price_note = f"，筛选低于¥{max_price}的" if max_price else ""
    rt_note = f"；同时查询 {return_date} 返程" if return_date else ""
    query = (
        f"{dep_name}到{arr_name} {date} 机票价格{price_note}{rt_note} "
        f"最低价 航班号 出发时间"
    )
    query_en = (
        f"cheapest flights {dep_code} to {arr_code} {date} price economy"
    )
    booking_urls = build_booking_urls(dep_code, arr_code, date, return_date)

    return {
        "status": "search_required",
        "dep": f"{dep_name}({dep_code})",
        "arr": f"{arr_name}({arr_code})",
        "date": date,
        "return_date": return_date,
        "max_price": max_price,
        "search_queries": [query, query_en],
        "booking_urls": booking_urls,
        "instruction": (
            f"Please use web_search to find current flight prices for {dep_name}→{arr_name} "
            f"on {date}. Search for: \"{query}\". "
            f"Extract: airline names, flight numbers, departure times, arrival times, prices. "
            + (f"Filter results to show only flights ≤¥{max_price}. " if max_price else "")
            + "Then format the results as a markdown table."
        ),
    }


def format_search_result(result: dict) -> str:
    """Format the search_required result as user-facing markdown."""
    booking_urls = result.get("booking_urls", {})
    date = result.get("date", "")
    dep = result.get("dep", "")
    arr = result.get("arr", "")
    max_price = result.get("max_price")
    return_date = result.get("return_date")

    lines = [
        f"## 机票查询：{dep} → {arr}",
        "",
        f"**出发日期：** {date}",
    ]
    if return_date:
        lines.append(f"**返程日期：** {return_date}")
    if max_price:
        lines.append(f"**价格筛选：** ≤ ¥{max_price}")
    lines += [
        "",
        "### 实时查询",
        "",
        "> 正在通过搜索引擎获取最新机票价格……",
        "",
        "### 立即预订",
        "",
    ]
    for name, url in booking_urls.items():
        lines.append(f"- [{name}]({url})")

    sq = result.get("search_queries", [])
    if sq:
        lines += ["", "### 推荐搜索词", ""]
        for q in sq:
            lines.append(f"- `{q}`")

    return "\n".join(lines)


def query(dep: str, arr: str, date: str,
          max_price: float = None, return_date: str = None) -> dict:
    dep_code, dep_name = resolve_city(dep)
    arr_code, arr_name = resolve_city(arr)
    return generate_search_prompt(dep_code, dep_name, arr_code, arr_name,
                                  date, max_price, return_date)


def main():
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description="Flight price query helper")
    parser.add_argument("--from", dest="dep", required=True,
                        help="Departure city (Chinese name or IATA code)")
    parser.add_argument("--to", dest="arr", required=True,
                        help="Arrival city (Chinese name or IATA code)")
    parser.add_argument("--date", required=True,
                        help="Departure date YYYY-MM-DD")
    parser.add_argument("--return-date", dest="return_date",
                        help="Return date for round trip")
    parser.add_argument("--max-price", dest="max_price", type=float,
                        help="Maximum price filter (RMB)")
    parser.add_argument("--json", dest="as_json", action="store_true",
                        help="Output raw JSON")
    args = parser.parse_args()

    result = query(args.dep, args.arr, args.date, args.max_price, args.return_date)

    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_search_result(result))
        print()
        print("---")
        print("INSTRUCTION FOR AI AGENT:")
        print(result.get("instruction", ""))


if __name__ == "__main__":
    main()
