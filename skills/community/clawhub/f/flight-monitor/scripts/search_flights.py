#!/usr/bin/env python3
"""
search_flights.py — Flight search via direct API calls.

Priority order:
  1. Ctrip (携程) internal AJAX API  — richest data, no key needed
  2. zbape.com cheapest-price API    — requires API key in config
  3. Fallback                        — returns booking deep-links + search query
                                       for the AI to do a single web_search

Usage:
    python search_flights.py --from SHA --to CTU --date 2026-03-21
    python search_flights.py --from 上海 --to 成都 --date 2026-03-21 --return-date 2026-03-28
    python search_flights.py --from BJS --to SYX --date 2026-04-10 --max-price 800
    python search_flights.py --from SHA --to CTU --date 2026-03-21 --json
    python search_flights.py --setup-zbape <YOUR_KEY>
"""

import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.parse
import urllib.error
import io
from datetime import datetime, date

# ── Config file path ─────────────────────────────────────────────────────────
CONFIG_DIR = os.path.expanduser("~/.workbuddy/flight-monitor")
CONFIG_FILE = os.path.join(CONFIG_DIR, "api_config.json")

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
    "天津": "TSN", "烟台": "YNT", "温州": "WNZ", "宁波": "NGB",
    "赣州": "KOW", "珠海": "ZUH", "汕头": "SWA", "湛江": "ZHA",
    "拉萨": "LXA", "林芝": "LZY", "日喀则": "RKZ", "银川": "INC",
    "包头": "BAV", "赤峰": "CIF", "通辽": "TGO", "满洲里": "NZH",
    "丽江": "LJG", "西双版纳": "JHG", "大理": "DLU", "腾冲": "TCZ",
    "三明": "SML", "龙岩": "LCX", "泉州": "JJN", "南平": "NPE",
    "东京": "TYO", "大阪": "OSA", "首尔": "SEL", "新加坡": "SIN",
    "曼谷": "BKK", "香港": "HKG", "台北": "TPE", "澳门": "MFM",
    "纽约": "NYC", "洛杉矶": "LAX", "伦敦": "LON", "巴黎": "PAR",
    "悉尼": "SYD", "迪拜": "DXB",
}
CITY_NAMES = {v: k for k, v in CITY_CODES.items()}

# Airline code → full name
AIRLINE_CN = {
    "CA": "中国国航", "MU": "中国东航", "CZ": "中国南航",
    "HU": "海南航空", "3U": "四川航空", "ZH": "深圳航空",
    "9C": "春秋航空", "HO": "吉祥航空", "GS": "天津航空",
    "MF": "厦门航空", "KN": "中国联航", "EU": "成都航空",
    "BK": "奥凯航空", "8L": "祥鹏航空", "NS": "幸福航空",
    "SC": "山东航空", "GJ": "长龙航空", "TV": "九元航空",
    "FM": "上海航空", "OQ": "中国快运", "G5": "西部航空",
}


# ── Helpers ──────────────────────────────────────────────────────────────────

def load_config() -> dict:
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_config(cfg: dict):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)


def resolve_city(s: str) -> tuple:
    """Return (iata_code, chinese_name)."""
    upper = s.strip().upper()
    if upper in CITY_NAMES:
        return upper, CITY_NAMES[upper]
    orig = s.strip()
    if orig in CITY_CODES:
        return CITY_CODES[orig], orig
    for cn, code in CITY_CODES.items():
        if cn in orig:
            return code, cn
    # Unknown city: return as-is
    return upper, upper


def airline_name(code: str) -> str:
    prefix = code[:2].upper()
    return AIRLINE_CN.get(prefix, code)


def fmt_duration(dep_str: str, arr_str: str) -> str:
    """Calculate HhMm from two 'HH:MM' or 'YYYY-MM-DD HH:MM:SS' strings."""
    try:
        fmt_long = "%Y-%m-%d %H:%M:%S"
        fmt_short = "%H:%M"
        def parse_t(s):
            s = s.strip()
            if len(s) > 8:
                return datetime.strptime(s[:19], fmt_long)
            return datetime.strptime(s, fmt_short)
        d = parse_t(dep_str)
        a = parse_t(arr_str)
        if a < d:
            # next day arrival
            from datetime import timedelta
            a += timedelta(days=1)
        mins = int((a - d).total_seconds() // 60)
        return f"{mins // 60}h{mins % 60:02d}m"
    except Exception:
        return "—"


def build_booking_urls(dep_code: str, arr_code: str, dep_date: str,
                       return_date: str = None) -> dict:
    # Only use ASCII IATA codes in URLs; fall back to city name search if unknown
    dep_l = dep_code.lower() if dep_code.isascii() else ""
    arr_l = arr_code.lower() if arr_code.isascii() else ""
    dep_cn = CITY_NAMES.get(dep_code, dep_code)
    arr_cn = CITY_NAMES.get(arr_code, arr_code)

    if dep_l and arr_l:
        ctrip_url = f"https://flights.ctrip.com/itinerary/oneway/{dep_l}-{arr_l}?depdate={dep_date}"
    else:
        ctrip_url = (
            f"https://flights.ctrip.com/itinerary/oneway/"
            f"?depdate={dep_date}&dcity={dep_cn}&acitiy={arr_cn}"
        )
    urls = {
        "携程": ctrip_url,
        "去哪儿": (
            f"https://flight.qunar.com/site/oneway.htm"
            f"?searchDepartureAirport={dep_cn}&searchArrivalAirport={arr_cn}"
            f"&searchDepartureDate={dep_date}"
        ),
        "飞猪": (
            f"https://sjipiao.fliggy.com/flight_search_result.htm"
            f"?tripType=0&depCity={dep_code if dep_code.isascii() else dep_cn}"
            f"&arrCity={arr_code if arr_code.isascii() else arr_cn}&depDate={dep_date}"
        ),
    }
    if return_date:
        if dep_l and arr_l:
            urls["携程往返"] = (
                f"https://flights.ctrip.com/itinerary/roundtrip/{dep_l}-{arr_l}"
                f"?depdate={dep_date}&retdate={return_date}"
            )
        else:
            urls["携程往返"] = ctrip_url  # fallback to one-way link
    return urls


# ── Source 1: Ctrip AJAX API ─────────────────────────────────────────────────

CTRIP_API = "https://flights.ctrip.com/itinerary/api/12808/products"

def _ctrip_payload(dep_code: str, arr_code: str, dep_date: str,
                   dep_name: str = "", arr_name: str = "") -> dict:
    return {
        "flightWay": "Oneway",
        "classType": "ALL",
        "hasChild": False,
        "hasBaby": False,
        "searchIndex": 1,
        "airportParams": [
            {
                "dcity": dep_code,
                "acity": arr_code,
                "dcityname": dep_name or CITY_NAMES.get(dep_code, dep_code),
                "acityname": arr_name or CITY_NAMES.get(arr_code, arr_code),
                "date": dep_date,
            }
        ],
        "selectedInfos": None,
    }


def _ctrip_headers(dep_code: str, arr_code: str, dep_date: str) -> dict:
    if dep_code.isascii() and arr_code.isascii():
        referer = (
            f"https://flights.ctrip.com/itinerary/oneway/"
            f"{dep_code.lower()}-{arr_code.lower()}?depdate={dep_date}"
        )
    else:
        referer = "https://flights.ctrip.com/"
    return {
        "Content-Type": "application/json",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Referer": referer,
        "Origin": "https://flights.ctrip.com",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }


def _parse_ctrip_response(data: dict) -> list:
    """
    Extract flight list from Ctrip API response.
    Returns list of dicts with keys:
      flight_no, airline, dep_time, arr_time, duration,
      dep_airport, arr_airport, stops, price, cabin
    """
    flights = []
    try:
        itineraries = (
            data.get("data", {})
                .get("flightItineraryList", [])
        )
        # fallback key variants
        if not itineraries:
            itineraries = data.get("data", {}).get("itineraryList", [])

        for itin in itineraries:
            # ── Price ──
            price_list = itin.get("priceList", [])
            min_price = None
            cabin_name = "经济舱"
            for p in price_list:
                cabin = p.get("cabin", "")
                # Only economy (Y/S/M/...) or lowest
                price_val = p.get("price") or p.get("adultPrice")
                if price_val is not None:
                    if min_price is None or price_val < min_price:
                        min_price = price_val
                        cabin_name = p.get("cabinTypeName", "经济舱")

            # ── Flight legs ──
            legs = itin.get("flightSegments", []) or itin.get("legs", [])
            if not legs:
                continue

            leg = legs[0]
            flight_list = leg.get("flightList", leg.get("flights", [leg]))

            if not flight_list:
                continue

            first = flight_list[0]
            last = flight_list[-1]

            fn = first.get("flightNumber", first.get("flightNo", ""))
            airline_code = fn[:2] if fn else ""
            dep_time = first.get("departureDate", first.get("dtime", ""))
            arr_time = last.get("arrivalDate", last.get("atime", ""))
            dep_ap = first.get("departureAirportInfo", {})
            arr_ap = last.get("arrivalAirportInfo", {})
            dep_airport_name = (
                dep_ap.get("airportName", "")
                if isinstance(dep_ap, dict) else ""
            )
            arr_airport_name = (
                arr_ap.get("airportName", "")
                if isinstance(arr_ap, dict) else ""
            )

            stops = "直飞" if len(flight_list) == 1 else f"经停({len(flight_list)-1}次)"

            # Extract HH:MM from datetime string
            def hhmm(s):
                if not s:
                    return "—"
                s = str(s).strip()
                if "T" in s:
                    s = s.split("T")[1][:5]
                elif " " in s:
                    s = s.split(" ")[1][:5]
                return s[:5]

            flights.append({
                "flight_no": fn,
                "airline": airline_name(fn) if fn else "—",
                "dep_time": hhmm(dep_time),
                "arr_time": hhmm(arr_time),
                "duration": fmt_duration(dep_time, arr_time),
                "dep_airport": dep_airport_name,
                "arr_airport": arr_airport_name,
                "stops": stops,
                "price": min_price,
                "cabin": cabin_name,
            })

    except Exception as e:
        pass  # Return whatever was collected

    # Sort by price ascending
    flights.sort(key=lambda x: x.get("price") or 99999)
    return flights


def fetch_ctrip(dep_code: str, arr_code: str, dep_date: str,
                dep_name: str = "", arr_name: str = "") -> dict:
    """
    Query Ctrip AJAX API.
    Returns {"source": "ctrip", "flights": [...], "error": None/str}
    """
    payload = _ctrip_payload(dep_code, arr_code, dep_date, dep_name, arr_name)
    headers = _ctrip_headers(dep_code, arr_code, dep_date)

    try:
        body = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            CTRIP_API,
            data=body,
            headers=headers,
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read().decode("utf-8")
        data = json.loads(raw)
        flights = _parse_ctrip_response(data)
        if flights:
            return {"source": "ctrip", "flights": flights, "error": None}
        # API returned but no parseable flights (may be JS challenge or empty)
        return {"source": "ctrip", "flights": [], "error": "empty_response"}
    except urllib.error.HTTPError as e:
        return {"source": "ctrip", "flights": [], "error": f"HTTP {e.code}"}
    except Exception as e:
        return {"source": "ctrip", "flights": [], "error": str(e)}


# ── Source 2: zbape.com cheapest-price API ───────────────────────────────────

ZBAPE_API = "https://api.zbape.com/api/plane/query"

def fetch_zbape(dep_name: str, arr_name: str, zbape_key: str) -> dict:
    """
    Query zbape cheapest-price API.
    Returns {"source": "zbape", "lowest_price": int, "error": None/str}
    Note: zbape only returns lowest price per date, not full flight list.
    """
    try:
        params = urllib.parse.urlencode({
            "key": zbape_key,
            "star": dep_name,
            "end": arr_name,
        })
        url = f"{ZBAPE_API}?{params}"
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw = resp.read().decode("utf-8")
        data = json.loads(raw)
        if data.get("code") == 200:
            return {
                "source": "zbape",
                "lowest_outbound": data["data"].get("lowest_outbound_price"),
                "lowest_return": data["data"].get("lowest_return_price"),
                "outbound_info": data["data"].get("outbound_info", {}),
                "error": None,
            }
        return {"source": "zbape", "error": data.get("msg", "unknown")}
    except Exception as e:
        return {"source": "zbape", "error": str(e)}


# ── Source 3: Fallback ───────────────────────────────────────────────────────

def make_fallback(dep_code: str, dep_name: str,
                  arr_code: str, arr_name: str,
                  dep_date: str, return_date: str = None,
                  max_price: float = None) -> dict:
    """
    Returns a single optimised web_search query string + booking URLs.
    The AI should do exactly ONE web_search with this query, then stop.
    """
    price_note = f" 低于{int(max_price)}元" if max_price else ""
    rt_note = f" 往返{return_date}" if return_date else ""
    # Favour ly.com snippets which tend to include price/flight data
    query = (
        f"{dep_name}到{arr_name} {dep_date}{rt_note} 机票{price_note} "
        f"最低价 航班号 出发时间 site:ly.com OR site:flights.ctrip.com"
    )
    urls = build_booking_urls(dep_code, arr_code, dep_date, return_date)
    return {
        "source": "fallback",
        "search_query": query,
        "booking_urls": urls,
        "instruction": (
            f"[FALLBACK] Direct API unavailable. "
            f"Do ONE web_search with this exact query: \"{query}\". "
            f"Extract flight numbers, prices, times from the snippets. "
            f"Do NOT fetch any URLs. Format results as a markdown table."
        ),
    }


# ── Main query orchestrator ──────────────────────────────────────────────────

def search(dep: str, arr: str, dep_date: str,
           return_date: str = None, max_price: float = None) -> dict:
    """
    Full flight search. Returns unified result dict:
    {
      "dep": "上海(SHA)", "arr": "成都(CTU)",
      "date": "2026-03-21", "return_date": "...",
      "max_price": 800,
      "source": "ctrip" | "zbape" | "fallback",
      "flights": [...],          # present for ctrip source
      "search_query": "...",     # present for fallback source
      "booking_urls": {...},
      "error": None | "..."
    }
    """
    dep_code, dep_name = resolve_city(dep)
    arr_code, arr_name = resolve_city(arr)
    cfg = load_config()

    result_base = {
        "dep": f"{dep_name}({dep_code})",
        "arr": f"{arr_name}({arr_code})",
        "date": dep_date,
        "return_date": return_date,
        "max_price": max_price,
        "booking_urls": build_booking_urls(dep_code, arr_code, dep_date, return_date),
    }

    # ── Try Source 1: Ctrip ──
    ctrip_result = fetch_ctrip(dep_code, arr_code, dep_date, dep_name, arr_name)
    if ctrip_result["flights"]:
        flights = ctrip_result["flights"]
        # Apply max_price filter
        if max_price:
            flights = [f for f in flights if f.get("price") and f["price"] <= max_price]
        result_base.update({
            "source": "ctrip",
            "flights": flights,
            "error": None,
        })
        # If round-trip, also fetch return leg
        if return_date:
            ret_result = fetch_ctrip(arr_code, dep_code, return_date, arr_name, dep_name)
            ret_flights = ret_result.get("flights", [])
            if max_price:
                ret_flights = [f for f in ret_flights
                               if f.get("price") and f["price"] <= max_price]
            result_base["return_flights"] = ret_flights
        return result_base

    # ── Try Source 2: zbape (price trend only, no schedule) ──
    zbape_key = cfg.get("zbape_key")
    if zbape_key:
        zb = fetch_zbape(dep_name, arr_name, zbape_key)
        if not zb.get("error"):
            result_base.update({
                "source": "zbape",
                "lowest_outbound": zb.get("lowest_outbound"),
                "lowest_return": zb.get("lowest_return"),
                "outbound_info": zb.get("outbound_info", {}),
                "note": (
                    "zbape API仅提供最低价格，不含具体航班时刻。"
                    "请点击下方预订链接查看完整航班。"
                ),
                "error": None,
            })
            return result_base

    # ── Source 3: Fallback ──
    fb = make_fallback(dep_code, dep_name, arr_code, arr_name,
                       dep_date, return_date, max_price)
    result_base.update(fb)
    return result_base


# ── Output formatters ────────────────────────────────────────────────────────

def format_flights_table(flights: list, title: str = "") -> str:
    if not flights:
        return f"{title}\n\n> 未找到符合条件的航班。\n"
    lines = []
    if title:
        lines.append(title)
        lines.append("")
    lines.append("| 航班 | 价格(含税) | 出发 | 到达 | 全程时长 | 中转 |")
    lines.append("|------|-----------|------|------|----------|------|")
    for f in flights:
        price_str = f"¥{f['price']}" if f.get("price") else "—"
        lines.append(
            f"| {f['airline']} {f['flight_no']} "
            f"| {price_str} "
            f"| {f['dep_time']} "
            f"| {f['arr_time']} "
            f"| {f['duration']} "
            f"| {f['stops']} |"
        )
    return "\n".join(lines)


def format_result(result: dict) -> str:
    dep = result["dep"]
    arr = result["arr"]
    dep_date = result["date"]
    return_date = result.get("return_date")
    max_price = result.get("max_price")
    source = result.get("source", "unknown")
    booking_urls = result.get("booking_urls", {})

    lines = [f"## 机票查询：{dep} → {arr}", ""]
    lines.append(f"**出发日期：** {dep_date}")
    if return_date:
        lines.append(f"**返程日期：** {return_date}")
    if max_price:
        lines.append(f"**价格筛选：** ≤ ¥{max_price}")
    lines.append(f"**数据来源：** {source}")
    lines.append("")

    if source == "ctrip":
        flights = result.get("flights", [])
        lines.append(
            format_flights_table(flights, f"### 去程：{dep} → {arr}，{dep_date}")
        )
        if flights:
            min_p = min(f["price"] for f in flights if f.get("price"))
            ctrip_url = booking_urls.get("携程", "#")
            lines.append(f"\n最低价：¥{min_p}  [立即预订 →]({ctrip_url})")

        if return_date:
            ret_flights = result.get("return_flights", [])
            lines.append("")
            lines.append(
                format_flights_table(ret_flights, f"### 返程：{arr} → {dep}，{return_date}")
            )
            if ret_flights:
                min_rp = min(f["price"] for f in ret_flights if f.get("price"))
                lines.append(f"\n返程最低价：¥{min_rp}")

    elif source == "zbape":
        low_out = result.get("lowest_outbound")
        low_ret = result.get("lowest_return")
        lines.append(f"### 价格概览")
        lines.append("")
        if low_out:
            lines.append(f"- 去程最低价（近期）：**¥{low_out}**")
        if low_ret:
            lines.append(f"- 返程最低价（近期）：**¥{low_ret}**")
        lines.append("")
        lines.append(f"> {result.get('note', '')}")

    elif source == "fallback":
        lines.append("### 搜索指引")
        lines.append("")
        lines.append(f"> {result.get('instruction', '')}")
        lines.append("")
        lines.append(f"**推荐搜索词：**")
        lines.append(f"```\n{result.get('search_query', '')}\n```")

    lines.append("")
    lines.append("### 立即预订")
    lines.append("")
    for name, url in booking_urls.items():
        lines.append(f"- [{name}]({url})")

    return "\n".join(lines)


# ── Setup helpers ────────────────────────────────────────────────────────────

def setup_zbape(key: str):
    cfg = load_config()
    cfg["zbape_key"] = key
    save_config(cfg)
    print(f"zbape API key 已保存到 {CONFIG_FILE}")


# ── CLI ──────────────────────────────────────────────────────────────────────

def main():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(
        description="search_flights: Query flight info via direct API calls"
    )
    parser.add_argument("--from", dest="dep",
                        help="Departure city (Chinese or IATA code)")
    parser.add_argument("--to", dest="arr",
                        help="Arrival city (Chinese or IATA code)")
    parser.add_argument("--date",
                        help="Departure date (YYYY-MM-DD)")
    parser.add_argument("--return-date", dest="return_date",
                        help="Return date for round trip (YYYY-MM-DD)")
    parser.add_argument("--max-price", dest="max_price", type=float,
                        help="Maximum price filter (RMB)")
    parser.add_argument("--json", dest="as_json", action="store_true",
                        help="Output raw JSON instead of formatted markdown")
    parser.add_argument("--setup-zbape", dest="zbape_key", metavar="KEY",
                        help="Save zbape API key to config")

    args = parser.parse_args()

    # Setup mode
    if args.zbape_key:
        setup_zbape(args.zbape_key)
        return

    if not (args.dep and args.arr and args.date):
        parser.print_help()
        sys.exit(1)

    result = search(
        dep=args.dep,
        arr=args.arr,
        dep_date=args.date,
        return_date=args.return_date,
        max_price=args.max_price,
    )

    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_result(result))

        # If fallback, print the AI instruction prominently
        if result.get("source") == "fallback":
            print()
            print("---")
            print("INSTRUCTION FOR AI AGENT:")
            print(result.get("instruction", ""))


if __name__ == "__main__":
    main()
