# -*- coding: utf-8 -*-
"""
国内航班查询 - ClawHub技能脚本
数据源：途牛旅行（SCF代理），零配置
"""
import os
import json
import urllib.request
import urllib.error

# ============ 配置 ============
TUNIU_PROXY = "https://1439498936-0junm3maxj.ap-guangzhou.tencentscf.com"
PROXY_TOKEN = os.environ.get("PROXY_TOKEN", "")
TIMEOUT = 60


# ============ 代理调用 ============
def _call_tuniu(rtype, params):
    """调用途牛SCF代理"""
    url = TUNIU_PROXY
    headers = {"Content-Type": "application/json", "X-Proxy-Token": PROXY_TOKEN}
    body = {"type": rtype, "params": params}
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"error": str(e)}
# ============ 格式化 ============
def _format_duration(minutes_str):
    try:
        minutes = int(minutes_str)
        h = minutes // 60
        m = minutes % 60
        return str(h) + "h" + str(m) + "m" if m else str(h) + "h"
    except (ValueError, TypeError):
        return str(minutes_str)


def _format_datetime(dt_str):
    try:
        return dt_str.split(" ")[1][:5] if " " in dt_str else dt_str
    except (IndexError, TypeError):
        return str(dt_str)


def _format_flights(data, origin_label, dest_label):
    if isinstance(data, dict) and "error" in data:
        return "查询失败: " + data["error"]

    item_list = None
    if isinstance(data, dict):
        inner = data.get("data", data)
        if inner is None: inner = {}
        item_list = inner.get("itemList", []) if isinstance(inner, dict) else []

    d = dest_label or "目的地"
    tips = "\n\n📋 附加服务：🏨推荐" + d + "酒店 | 🎫推荐" + d + "景点 | 🚇" + d + "市内交通"

    if not item_list:
        route = origin_label + "->" + dest_label if origin_label and dest_label else ""
        return "未找到符合条件的航班" + route + "。建议调整日期或出发/到达城市后重试。" + tips

    route_info = " " + origin_label + "->" + dest_label if origin_label and dest_label else ""
    lines = ["找到 " + str(len(item_list)) + " 个航班方案" + route_info + "：", ""]

    direct_flights = []
    transit_flights = []
    for item in item_list:
        journeys = item.get("journeys", [])
        if journeys:
            jtype = journeys[0].get("journeyType", "")
            if jtype == "直达":
                direct_flights.append(item)
            else:
                transit_flights.append(item)

    if direct_flights:
        lines.append("--- 直飞航班 (" + str(len(direct_flights)) + "个) ---")
        lines.append("")
        for i, item in enumerate(direct_flights, 1):
            _format_single_flight(lines, i, item)

    if transit_flights:
        lines.append("--- 中转航班 (" + str(len(transit_flights)) + "个) ---")
        lines.append("")
        for i, item in enumerate(transit_flights, 1):
            _format_single_flight(lines, len(direct_flights) + i, item)

    lines.append("价格和库存实时变动，以实际下单为准")
    lines.append("数据来源：途牛旅行")
    return "\n".join(lines) + tips


def _format_single_flight(lines, idx, item):
    journeys = item.get("journeys", [])
    if not journeys: return
    journey = journeys[0]
    segments = journey.get("segments", [])
    if not segments: return

    price = item.get("ticketPrice", "")
    jump_url = item.get("jumpUrl", "")
    total_duration = item.get("totalDuration", "")

    seg = segments[0]
    airline = seg.get("marketingTransportName", "")
    flight_no = seg.get("marketingTransportNo", "")
    dep_short = seg.get("depStationShortName", seg.get("depStationName", ""))
    dep_time = _format_datetime(seg.get("depDateTime", ""))
    dep_term = seg.get("depTerm", "")

    last_seg = segments[-1]
    arr_short = last_seg.get("arrStationShortName", last_seg.get("arrStationName", ""))
    arr_time = _format_datetime(last_seg.get("arrDateTime", ""))
    arr_term = last_seg.get("arrTerm", "")

    seat_class = seg.get("seatClassName", "")
    journey_type = journey.get("journeyType", "")

    lines.append(str(idx) + ". " + airline + " " + flight_no + " [" + journey_type + "]")

    dep_info = dep_short
    if dep_term: dep_info += dep_term
    arr_info = arr_short
    if arr_term: arr_info += arr_term
    duration_str = _format_duration(total_duration) if total_duration else ""
    lines.append("   " + dep_time + " " + dep_info + " -> " + arr_time + " " + arr_info + " (" + duration_str + ")")

    price_str = "¥" + str(price) if price else "价格待查"
    seat_str = " | " + seat_class if seat_class else ""
    lines.append("   " + price_str + seat_str)

    if len(segments) > 1:
        for j, s in enumerate(segments, 1):
            s_airline = s.get("marketingTransportName", "")
            s_flight = s.get("marketingTransportNo", "")
            s_dep = _format_datetime(s.get("depDateTime", ""))
            s_arr = _format_datetime(s.get("arrDateTime", ""))
            s_dep_city = s.get("depCityName", "")
            s_arr_city = s.get("arrCityName", "")
            lines.append("   + 第" + str(j) + "段: " + s_airline + " " + s_flight + " " + s_dep_city + s_dep + "->" + s_arr_city + s_arr)

    if jump_url:
        lines.append("   预订: " + jump_url)
    lines.append("")


# ============ 工具函数 ============

def search_flight(params):
    """机票查询：搜索途牛平台机票，返回航班、时间、票价和购票链接。"""
    query = params.get("query", "")
    # 解析查询词
    parts = query.split()
    if len(parts) >= 3:
        dep = parts[0]
        arr = parts[1]
        date = parts[2]
    else:
        return _search_flight_ai(query)

    result = _call_tuniu("tuniu_flight_search", {
        "departureCityName": dep,
        "arrivalCityName": arr,
        "departureDate": date,
    })

    if isinstance(result, dict) and "error" in result:
        return _search_flight_ai(query)

    data = result.get("data", {})
    if isinstance(data, dict) and data.get("error"):
        return _search_flight_ai(query)

    flight_list = data.get("data", []) if isinstance(data, dict) else data
    if not isinstance(flight_list, list):
        flight_list = []

    lines = [f"🛫 查询到 {len(flight_list)} 个航班\n"]
    for i, f in enumerate(flight_list[:15]):
        fn = f.get("flightNo", f.get("flight_no", ""))
        dep_t = f.get("departTime", f.get("depart_time", ""))
        arr_t = f.get("arriveTime", f.get("arrive_time", ""))
        price = f.get("price", "")
        airline = f.get("airlineName", f.get("airline", ""))
        lines.append(f"{i+1}. {airline} {fn}")
        lines.append(f"   {dep_t} → {arr_t}  💰¥{price}")
    return "\n".join(lines) + "\n\n数据来源：途牛旅行"

def _search_flight_ai(query):
    """AI兜底搜索"""
    result = _call_tuniu("tuniu_flight_search", {
        "departureCityName": query.split()[0] if query.split() else query,
        "arrivalCityName": query.split()[1] if len(query.split()) > 1 else "",
        "departureDate": "",
    })
    if isinstance(result, dict) and result.get("error"):
        return "暂无航班数据，请稍后重试"
    return str(result) + "\n\n数据来源：途牛旅行"