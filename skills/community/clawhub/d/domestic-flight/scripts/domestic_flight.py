# -*- coding: utf-8 -*-
"""
国内航班查询 - ClawHub技能脚本
数据源：飞猪旅行（SCF代理），零配置
"""
import json
import urllib.request
import urllib.error

# ============ 配置 ============
FLIGGY_PROXY = "https://1439498936-6sysdjjt99.ap-guangzhou.tencentscf.com"
PROXY_TOKEN = "tp_8k2mX9vQ4z"
TIMEOUT = 60


# ============ 代理调用 ============
def _call_fliggy(rtype, params):
    body = json.dumps({"type": rtype, "params": params}, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    req = urllib.request.Request(
        FLIGGY_PROXY, data=body,
        headers={"Content-Type": "application/json", "X-Proxy-Token": PROXY_TOKEN},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            raw = json.loads(r.read().decode("utf-8"))
            if isinstance(raw, dict) and "code" in raw:
                if raw.get("code") == 0:
                    return raw.get("data", raw)
                else:
                    return {"error": "SCF proxy error: " + str(raw.get("message", raw))}
            return raw
    except urllib.error.HTTPError as e:
        err = ""
        try: err = e.read().decode("utf-8", errors="replace")[:200]
        except: pass
        return {"error": "proxy error " + str(e.code) + ": " + err}
    except Exception as e:
        return {"error": "request error: " + str(e)}


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
    lines.append("数据来源：飞猪旅行")
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
    """国内航班查询：查询国内航班实时价格与时刻表，返回航班号、起降时间、价格及预订链接。"""
    origin = params.get("origin", "")
    destination = params.get("destination", "")
    dep_date = params.get("dep_date", "")

    # 也支持自然语言query
    query = params.get("query", "")
    if query and (not origin or not destination or not dep_date):
        return _search_flight_ai(query)

    if not origin: return "请输入出发城市，如：上海"
    if not destination: return "请输入到达城市，如：北京"
    if not dep_date: return "请输入出发日期，格式：YYYY-MM-DD"

    arguments = {
        "origin": origin.strip(),
        "destination": destination.strip(),
        "depDate": dep_date.strip(),
        "limit": 10,
    }
    if params.get("seat_class"): arguments["seatClassName"] = params["seat_class"]
    if params.get("sort_type"): arguments["sortType"] = int(params["sort_type"])
    if params.get("max_price", 0) > 0: arguments["maxPrice"] = int(params["max_price"])
    if params.get("journey_type"): arguments["journeyType"] = int(params["journey_type"])
    if params.get("transport_no"): arguments["transportNo"] = params["transport_no"]

    data = _call_fliggy("search_flight", arguments)
    return _format_flights(data, origin.strip(), destination.strip())


def _search_flight_ai(query):
    """自然语言搜索航班（回退方案）"""
    result = _call_fliggy("fliggy_ai_search", {"query": query})
    if isinstance(result, dict) and "error" in result:
        return "航班查询失败: " + result["error"]
    inner = result.get("data", result)
    if isinstance(inner, str):
        return inner + "\n\n数据来源：飞猪旅行"
    if isinstance(inner, dict):
        item_list = inner.get("itemList", [])
        if item_list:
            return _format_flights(result, "", "")
    return "未找到符合条件的航班，建议调整查询条件"
