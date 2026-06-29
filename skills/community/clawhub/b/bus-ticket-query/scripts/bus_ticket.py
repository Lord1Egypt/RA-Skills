import os
# -*- coding: utf-8 -*-
"""
汽车票查询与预订 - ClawHub技能脚本
零配置即装即用，通过SCF代理调用同程+高德+飞猪API
3个工具：汽车票查询、去汽车站交通、住宿推荐
"""
import json
import re
import urllib.request
import urllib.error
from datetime import datetime, timedelta

# ============ 配置 ============
TC_PROXY = "https://1439498936-7vqpkiipef.ap-guangzhou.tencentscf.com"
GAODE_PROXY = "https://1439498936-bl10af74fl.ap-guangzhou.tencentscf.com"
FLIGGY_PROXY = "https://1439498936-6sysdjjt99.ap-guangzhou.tencentscf.com"
PROXY_TOKEN = os.environ.get("PROXY_TOKEN", "")
TIMEOUT = 30

_CITIES = [
    "北京", "上海", "广州", "深圳", "成都", "杭州", "南京", "武汉", "长沙", "重庆",
    "西安", "厦门", "青岛", "大连", "昆明", "丽江", "桂林", "苏州", "珠海", "海口",
    "三亚", "天津", "济南", "沈阳", "哈尔滨", "长春", "郑州", "合肥", "福州", "南昌",
    "太原", "石家庄", "贵阳", "南宁", "兰州", "银川", "呼和浩特", "乌鲁木齐", "拉萨",
    "无锡", "宁波", "温州", "烟台", "威海", "佛山", "东莞", "中山", "惠州", "扬州",
]


# ============ 代理调用 ============
def _call_proxy(url, rtype, params, timeout=None):
    body = json.dumps({"type": rtype, "params": params}, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    req = urllib.request.Request(
        url, data=body,
        headers={"Content-Type": "application/json", "X-Proxy-Token": PROXY_TOKEN},
        method="POST",
    )
    _timeout = timeout or TIMEOUT
    try:
        with urllib.request.urlopen(req, timeout=_timeout) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err = ""
        try: err = e.read().decode("utf-8", errors="replace")[:300]
        except: pass
        return {"error": "proxy error " + str(e.code) + ": " + err}
    except Exception as e:
        return {"error": "request error: " + str(e)}


def _call_tc(rtype, params):
    return _call_proxy(TC_PROXY, rtype, params)


def _call_fliggy(rtype, params, timeout=None):
    return _call_proxy(FLIGGY_PROXY, rtype, params, timeout=timeout)


def _call_gaode(api, params):
    data = _call_proxy(GAODE_PROXY, api, params, timeout=15)
    if isinstance(data, dict) and data.get("code") == 0 and "data" in data:
        return data["data"]
    return data


# ============ 日期智能解析 ============
def _smart_parse_date(date_str):
    now = datetime.now()
    today = now.date()
    if not date_str or not date_str.strip():
        if now.hour >= 20:
            default_date = today + timedelta(days=1)
            return (default_date.strftime("%Y-%m-%d"), f"您未指定日期，已默认查询明天（{default_date.strftime('%m月%d日')}）的车票")
        else:
            return (today.strftime("%Y-%m-%d"), f"您未指定日期，已默认查询今天（{today.strftime('%m月%d日')}）的车票")

    s = date_str.strip()
    year = now.year

    m = re.match(r'^(\d{4})[-/](\d{1,2})[-/](\d{1,2})$', s)
    if m:
        y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
        try: parsed = datetime(y, mo, d).date()
        except ValueError: return ("", f"日期格式有误：{date_str}")
        return _validate_date(parsed, today, date_str)

    m = re.match(r'^(\d{1,2})月(\d{1,2})日?$', s)
    if m:
        mo, d = int(m.group(1)), int(m.group(2))
        try: parsed = datetime(year, mo, d).date()
        except ValueError: return ("", f"日期格式有误：{date_str}")
        if parsed < today:
            try:
                next_year = datetime(year + 1, mo, d).date()
                if next_year <= today + timedelta(days=30):
                    return (next_year.strftime("%Y-%m-%d"), f"已自动调整为明年{mo}月{d}日")
            except ValueError: pass
        return _validate_date(parsed, today, date_str)

    m = re.match(r'^(\d{1,2})[-/](\d{1,2})$', s)
    if m:
        mo, d = int(m.group(1)), int(m.group(2))
        try: parsed = datetime(year, mo, d).date()
        except ValueError: return ("", f"日期格式有误：{date_str}")
        if parsed < today:
            try:
                next_year = datetime(year + 1, mo, d).date()
                if next_year <= today + timedelta(days=30):
                    return (next_year.strftime("%Y-%m-%d"), f"已自动调整为明年{mo}月{d}日")
            except ValueError: pass
        return _validate_date(parsed, today, date_str)

    if s == "今天": return (today.strftime("%Y-%m-%d"), "")
    if s == "明天": return ((today + timedelta(days=1)).strftime("%Y-%m-%d"), "")
    if s == "后天": return ((today + timedelta(days=2)).strftime("%Y-%m-%d"), "")

    return ("", f"无法识别日期格式：{date_str}，请输入如\"6月15日\"、\"6-15\"、\"明天\"等格式")


def _validate_date(parsed, today, date_str):
    if parsed < today:
        return (today.strftime("%Y-%m-%d"), f"您输入的{date_str}已过，已自动为您查询今天（{today.strftime('%m月%d日')}）的车票")
    if parsed > today + timedelta(days=30):
        return ("", f"暂无法查询{parsed.strftime('%m月%d日')}的车票，目前可查询未来30天内的车票")
    return (parsed.strftime("%Y-%m-%d"), "")


# ============ 高德通用 ============
def _is_metro_line(line_name):
    metro_keywords = ["地铁", "号线", "城轨", "磁浮", "市域", "轻轨"]
    return any(kw in line_name for kw in metro_keywords)


def _estimate_taxi_cost(distance_m):
    distance_km = distance_m / 1000
    if distance_km <= 0: return "¥0"
    if distance_km <= 3: return "¥14左右"
    cost = 14 + (distance_km - 3) * 2.5
    return f"¥{int(cost)}左右"


def _gaode_driving(origin, destination, city):
    params = {"origin_address": origin, "origin_city": city, "destination_address": destination, "destination_city": city, "strategy": "0"}
    data = _call_gaode("driving_route_by_address", params)
    if isinstance(data, dict) and data.get("status") == "1":
        paths = data.get("route", {}).get("paths", [])
        if paths:
            path = paths[0]
            distance = int(float(path.get("distance", 0)))
            duration = int(float(path.get("duration", 0)))
            return {
                "distance_km": round(distance / 1000, 1),
                "duration_min": round(duration / 60),
                "taxi_cost": _estimate_taxi_cost(distance),
            }
    return {}


def _gaode_transit(origin, destination, city):
    params = {"origin_address": origin, "origin_city": city, "destination_address": destination, "destination_city": city, "city": city, "strategy": "0"}
    data = _call_gaode("transit_route_by_address", params)
    if isinstance(data, dict) and data.get("status") == "1":
        return data.get("route", {}).get("transits", [])
    return []


# ============ 工具1：汽车票查询 ============
def _format_left_ticket(num):
    if num is None:
        return "有余票"
    try:
        n = int(num)
        if n <= 0:
            return "❌ 无票"
        elif n <= 5:
            return f"🔥 仅剩{n}张"
        else:
            return f"余{n}张"
    except (ValueError, TypeError):
        return "有余票"


def search_bus(params):
    """查询汽车票班次、价格和余票信息，支持灵活日期输入。"""
    departure = params.get("departure", "")
    destination = params.get("destination", "")
    dep_date = params.get("dep_date", "")

    if not departure: return "请提供出发城市，如：上海、广州"
    if not destination: return "请提供到达城市，如：苏州、深圳"

    parsed_date, date_hint = _smart_parse_date(dep_date)
    if not parsed_date: return date_hint

    args = {"departure": departure, "destination": destination}

    result = _call_tc("tongcheng_bus_search", args)
    if isinstance(result, dict) and "error" in result:
        return "汽车票查询失败: " + result["error"]

    inner = result.get("data", result)
    if inner is None or not isinstance(inner, dict):
        return f"😔 未找到{departure}→{destination}的汽车票。可能该路线暂无班次，建议更换城市或调整日期。"

    buses = inner.get("buses", [])
    if not buses:
        return f"😔 未找到{departure}→{destination}的汽车票。可能该路线暂无班次，建议更换城市或调整日期。"

    buses.sort(key=lambda b: b.get("depTime", "99:99"))

    lines = [f"🚌 找到 {len(buses)} 个班次 {departure}→{destination}（{parsed_date}）：", ""]

    for i, bus in enumerate(buses, 1):
        dep_station = bus.get("depStationName", "")
        arr_station = bus.get("arrStationName", "")
        dep_time = bus.get("depTime", "")
        arr_time = bus.get("arrTime", "")
        price = bus.get("price", "")
        run_time = bus.get("runTimeDesc", "")
        distance = bus.get("distance", "")
        left_ticket = bus.get("leftTicketNum")
        coach_type = bus.get("coachType", "")
        trip_type = bus.get("tripType", "")
        redirect_url = bus.get("redirectUrl", bus.get("clawRedirectUrl", ""))

        dep_f = dep_time[:5] if dep_time and len(dep_time) >= 5 else dep_time
        arr_f = arr_time[:5] if arr_time and len(arr_time) >= 5 else arr_time
        ticket_status = _format_left_ticket(left_ticket)
        type_label = "直达" if trip_type == "DIRECT" else trip_type or ""

        lines.append(f"**{i}. {dep_f}出发** [{type_label}]")
        lines.append(f"   {dep_f} {dep_station} → {arr_f} {arr_station}")

        detail_parts = []
        if run_time: detail_parts.append(run_time)
        if distance:
            try: detail_parts.append(f"{int(float(distance))}km")
            except: pass
        if coach_type: detail_parts.append(coach_type)
        if detail_parts:
            lines.append(f"   🕐 {' | '.join(detail_parts)}")

        price_str = f"¥{price}" if price else "票价待查"
        lines.append(f"   💰 {price_str} | 🎫 {ticket_status}")

        if redirect_url:
            lines.append(f"   🔗 [预订→]({redirect_url})")
        lines.append("")

    lines.append("⚠️ 票价和余票实时变动，以实际下单为准")
    lines.append("💡 点击预订链接可直接跳转同程购买")
    lines.append("")
    lines.append("📋 附加服务：1、查去汽车站怎么走 2、推荐目的地住宿，回复数字即可")

    text = "\n".join(lines)
    if date_hint:
        text = f"📅 {date_hint}\n\n{text}"
    return text


# ============ 工具2：去汽车站交通 ============
def query_transport(params):
    """查询从出发地到汽车站的地铁、公交和打车路线，地铁优先展示。"""
    origin = params.get("origin", "")
    bus_station = params.get("bus_station", "")
    city = params.get("city", "")

    if not origin: return "请提供出发地，如：南京路、浦东机场"
    if not bus_station: return "请提供汽车站名，如：上海虹桥客运西站、苏州汽车南站"
    if not city: return "请提供城市名，如：上海、苏州"

    lines = [f"📍 {origin} → {bus_station} 交通方式", ""]

    # 先查公交地铁
    transit_routes = _gaode_transit(origin, bus_station, city)

    metro_routes = []
    bus_routes = []
    for route in transit_routes[:8]:
        is_metro = False
        for seg in route.get("segments", []):
            for bl in seg.get("bus", {}).get("buslines", []):
                if _is_metro_line(bl.get("name", "")): is_metro = True; break
        if is_metro:
            metro_routes.append(route)
        else:
            bus_routes.append(route)

    # 地铁优先
    if metro_routes:
        lines.append("━━━ 🚇 地铁/城轨（推荐·省钱） ━━━")
        for i, route in enumerate(metro_routes[:3], 1):
            duration = int(route.get("duration", 0) or 0)
            cost = route.get("cost", "0")
            all_lines = []
            for seg in route.get("segments", []):
                for bl in seg.get("bus", {}).get("buslines", []):
                    name = bl.get("name", "").split("(")[0]
                    dep = bl.get("departure_stop", {}).get("name", "")
                    arr = bl.get("arrival_stop", {}).get("name", "")
                    all_lines.append({"name": name, "dep": dep, "arr": arr})
            cost_str = f"¥{cost}" if cost and cost != "0" else ""
            line_names = " → ".join(l["name"] for l in all_lines)
            detail_parts = [f"约{round(duration / 60)}分钟"]
            if cost_str: detail_parts.append(cost_str)
            lines.append(f"方案{i}: {line_names} | {' '.join(detail_parts)}")
            for l in all_lines:
                if l["dep"] or l["arr"]:
                    lines.append(f"  {l['name']}: {l['dep']}→{l['arr']}")
        lines.append("")

    # 公交次之
    if bus_routes:
        lines.append("━━━ 🚌 公交 ━━━")
        for i, route in enumerate(bus_routes[:2], 1):
            duration = int(route.get("duration", 0) or 0)
            cost = route.get("cost", "0")
            all_lines = []
            for seg in route.get("segments", []):
                for bl in seg.get("bus", {}).get("buslines", []):
                    all_lines.append(bl.get("name", "").split("(")[0])
            cost_str = f"¥{cost}" if cost and cost != "0" else ""
            line_names = " → ".join(all_lines)
            detail_parts = [f"约{round(duration / 60)}分钟"]
            if cost_str: detail_parts.append(cost_str)
            lines.append(f"方案{i}: {line_names} | {' '.join(detail_parts)}")
        lines.append("")

    # 打车最后
    driving = _gaode_driving(origin, bus_station, city)
    if driving:
        lines.append("━━━ 🚗 打车/驾车 ━━━")
        lines.append(f"距离{driving['distance_km']}公里 | 约{driving['duration_min']}分钟 | {driving['taxi_cost']}")
        lines.append("💡 可打开微信/支付宝「滴滴出行」小程序叫车")
        lines.append("")

    if not metro_routes and not bus_routes and not driving:
        return "未找到合适的交通方案，建议使用地图APP导航。"

    lines.append("💡 以上时间和费用为预估值，实际可能因路况变化")
    return "\n".join(lines)


# ============ 工具3：住宿推荐 ============
def _extract_city(text):
    for city in _CITIES:
        if city in text: return city
    return ""


def recommend_hotel(params):
    """用自然语言描述住宿需求，AI智能匹配高分酒店并返回推荐和预订链接。"""
    query = params.get("query", "")
    if not query: return "请描述你的住宿需求，如：住哪个区域，预算多少，有什么偏好？"

    result = _call_fliggy("fliggy_ai_search", {"query": query}, timeout=60)
    if isinstance(result, dict) and "error" in result:
        return "住宿推荐失败: " + result["error"]

    inner = result.get("data", result) if isinstance(result, dict) else result
    if inner is None:
        return "😔 未找到符合条件的酒店。建议调整搜索条件后重试。"

    if isinstance(inner, str):
        content_text = inner
    elif isinstance(inner, dict):
        data_inner = inner.get("data")
        if isinstance(data_inner, str):
            content_text = data_inner
            sys_msg = inner.get("systemMessage")
            if sys_msg:
                content_text += f"\n\n📌 {sys_msg}"
        elif isinstance(data_inner, dict):
            items = data_inner.get("itemList", [])
            if items:
                lines = [f"🏨 找到 {len(items)} 家酒店：", ""]
                for i, h in enumerate(items[:10], 1):
                    info = h.get("info", h)
                    name = info.get("title", h.get("name", ""))
                    price = info.get("price", h.get("price", ""))
                    url = info.get("detailUrl", h.get("detailUrl", "")) or info.get("jumpUrl", "")
                    lines.append(f"**{i}. {name}**")
                    if price: lines.append(f"   💰 {price}")
                    if url: lines.append(f"   🔗 [预订→]({url})")
                    lines.append("")
                content_text = "\n".join(lines)
            else:
                content_text = "😔 未找到符合条件的酒店。建议调整搜索条件后重试。"
        else:
            content_text = "😔 未找到符合条件的酒店。"
    else:
        content_text = str(inner)

    content_text += "\n\n📋 附加服务：回复「查汽车票」可查询返程汽车票"
    return content_text
