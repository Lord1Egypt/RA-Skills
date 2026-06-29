# -*- coding: utf-8 -*-
"""
游轮船票查询 - ClawHub技能脚本
零配置即装即用，通过SCF代理调用途牛+高德+飞猪API
4个工具：游轮船票查询、市内交通、景点推荐、酒店推荐
"""
import json
import re
import urllib.request
import urllib.error
from datetime import datetime, timedelta

# ============ 配置 ============
TUNIU_PROXY = "https://1439498936-0junm3maxj.ap-guangzhou.tencentscf.com"
GAODE_PROXY = "https://1439498936-bl10af74fl.ap-guangzhou.tencentscf.com"
FLIGGY_PROXY = "https://1439498936-6sysdjjt99.ap-guangzhou.tencentscf.com"
PROXY_TOKEN = "tp_8k2mX9vQ4z"
TIMEOUT = 30

# 游轮热门关键词提示
CRUISE_HINTS = [
    "长江三峡游轮", "黄浦江游船", "重庆游船", "三峡游轮",
    "长江游轮", "三峡大坝游轮", "两江游船", "珠江夜游",
    "夜游长江", "夜游黄浦江", "朝天门游船", "维多利亚游轮",
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


def _call_tuniu(rtype, params):
    return _call_proxy(TUNIU_PROXY, rtype, params)


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
        default_date = today + timedelta(days=1)
        return (default_date.strftime("%Y-%m-%d"), f"已默认查询明天（{default_date.strftime('%m月%d日')}）的船票")

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
                if next_year <= today + timedelta(days=60):
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
                if next_year <= today + timedelta(days=60):
                    return (next_year.strftime("%Y-%m-%d"), f"已自动调整为明年{mo}月{d}日")
            except ValueError: pass
        return _validate_date(parsed, today, date_str)

    if s == "今天": return (today.strftime("%Y-%m-%d"), "")
    if s == "明天": return ((today + timedelta(days=1)).strftime("%Y-%m-%d"), "")
    if s == "后天": return ((today + timedelta(days=2)).strftime("%Y-%m-%d"), "")

    return ("", f"无法识别日期格式：{date_str}，请输入如\"6月15日\"、\"6-15\"、\"明天\"等格式")


def _validate_date(parsed, today, date_str):
    if parsed < today:
        return (today.strftime("%Y-%m-%d"), f"您输入的{date_str}已过，已自动为您查询今天（{today.strftime('%m月%d日')}）的船票")
    if parsed > today + timedelta(days=90):
        return ("", f"暂无法查询{parsed.strftime('%m月%d日')}的船票，目前可查询未来90天内的船票")
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


# ============ 工具1：游轮船票查询 ============
def _extract_direction(res_name):
    """从resName提取上下水方向"""
    if not res_name:
        return ""
    s = res_name.lower()
    if "下水" in s:
        return "⬇️ 下水（顺流）"
    if "上水" in s:
        return "⬆️ 上水（逆流）"
    # 常见城市方向推断
    if "渝宜" in s or "重庆宜昌" in s:
        return "⬇️ 下水（重庆→宜昌）"
    if "宜渝" in s or "宜昌重庆" in s:
        return "⬆️ 上水（宜昌→重庆）"
    return ""


def _clean_res_name(res_name, scenic_name):
    """清理resName，去掉与scenicName重复的部分和成人票等后缀"""
    if not res_name:
        return scenic_name or ""
    name = res_name
    # 去掉< >包裹
    name = re.sub(r'[<>]', '', name)
    # 去掉scenicName重复
    if scenic_name and scenic_name in name:
        name = name.replace(scenic_name, "").strip("_").strip("-").strip()
    return name if name else scenic_name or ""


def search_cruise(params):
    """查询游轮船票信息，包括游轮名、价格、航线方向和退改政策。"""
    scenic_name = params.get("scenic_name", "")
    if not scenic_name:
        hint_list = "、".join(CRUISE_HINTS[:8])
        return f"请提供游轮线路名称，如：{hint_list}\n\n💡 提示：搜索需要精确关键词，如\"长江三峡游轮\"比\"三峡\"更准确"

    result = _call_tuniu("tuniu_ticket_query", {"scenic_name": scenic_name})
    if isinstance(result, dict) and "error" in result:
        return "游轮船票查询失败: " + result["error"]

    inner = result.get("data", result) if isinstance(result, dict) else result
    if inner is None or not isinstance(inner, dict):
        return f"😔 未找到「{scenic_name}」的游轮船票。建议尝试更精确的关键词，如\"长江三峡游轮\"、\"黄浦江游船\""

    tickets = inner.get("tickets", [])
    if not tickets:
        return f"😔 未找到「{scenic_name}」的游轮船票。建议尝试更精确的关键词，如\"长江三峡游轮\"、\"黄浦江游船\""

    lines = [f"🚢 找到 {len(tickets)} 个游轮船票「{scenic_name}」：", ""]

    for i, t in enumerate(tickets[:15], 1):
        scenic_name_val = t.get("scenicName", "")
        res_name = t.get("resName", "")
        start_price = t.get("startPrice", "")
        price_market = t.get("priceMarket", "0")
        loss_name = t.get("lossName", "")
        detail_addr = t.get("detailAddr", "")
        person_type = t.get("personTypeName", "")
        enter_type = t.get("enterTypeName", "")
        admission_desc = t.get("admissionVoucherDesc", "")
        satisfaction = t.get("satisfaction", 0)
        start_date = t.get("startDate", "")
        end_date = t.get("endDate", "")
        product_id = t.get("productId", "")
        direction = _extract_direction(res_name)

        # 显示名 = resName清理后的版本
        display_name = _clean_res_name(res_name, scenic_name_val)

        lines.append(f"**{i}. {display_name}**")
        if direction:
            lines.append(f"   🧭 {direction}")

        # 价格
        if start_price:
            try:
                p = int(float(start_price))
                price_str = f"💰 ¥{p}起"
            except (ValueError, TypeError):
                price_str = f"💰 {start_price}起"
            if price_market and price_market != "0.0" and price_market != "0":
                try:
                    mp = int(float(price_market))
                    if mp != p:
                        price_str += f"（门市¥{mp}）"
                except: pass
            lines.append(f"   {price_str}")

        # 预售期
        if start_date and end_date:
            lines.append(f"   📅 售期：{start_date} ~ {end_date}")

        # 地址
        if detail_addr:
            lines.append(f"   📍 {detail_addr}")

        # 入园方式
        if enter_type:
            entry_line = f"   🎫 {enter_type}"
            if admission_desc:
                entry_line += f"（{admission_desc}）"
            lines.append(entry_line)

        # 退改
        if loss_name:
            lines.append(f"   🔄 退改：{loss_name}")

        # 满意度
        if satisfaction and float(satisfaction) > 0:
            lines.append(f"   ⭐ 满意度{int(float(satisfaction))}%")

        # 预订链接
        if product_id:
            url = f"https://m.tuniu.com/ticket/p-{product_id}"
            lines.append(f"   🔗 [查看详情/预订→]({url})")

        lines.append("")

    lines.append("⚠️ 价格实时变动，以实际下单页面为准")
    lines.append("💡 点击链接可直接跳转途牛查看详情和预订")
    lines.append("")
    lines.append("📋 附加服务：1、查去码头交通 2、推荐附近景点 3、推荐住宿，回复数字即可")

    return "\n".join(lines)


# ============ 工具2：市内交通 ============
def query_transport(params):
    """查询从出发地到游轮码头的地铁、公交和打车路线，地铁优先展示。"""
    origin = params.get("origin", "")
    destination = params.get("destination", "")
    city = params.get("city", "")

    if not origin: return "请提供出发地，如：重庆北站、解放碑"
    if not destination: return "请提供目的地（码头名），如：朝天门码头、宜昌游客中心"
    if not city: return "请提供城市名，如：重庆、宜昌"

    lines = [f"📍 {origin} → {destination} 交通方式", ""]

    # 先查公交地铁
    transit_routes = _gaode_transit(origin, destination, city)

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
    driving = _gaode_driving(origin, destination, city)
    if driving:
        lines.append("━━━ 🚗 打车/驾车 ━━━")
        lines.append(f"距离{driving['distance_km']}公里 | 约{driving['duration_min']}分钟 | {driving['taxi_cost']}")
        lines.append("💡 可打开微信/支付宝「滴滴出行」小程序叫车")
        lines.append("")

    if not metro_routes and not bus_routes and not driving:
        return "未找到合适的交通方案，建议使用地图APP导航。"

    lines.append("💡 以上时间和费用为预估值，实际可能因路况变化")
    return "\n".join(lines)


# ============ 工具3：景点推荐 ============
def recommend_attraction(params):
    """推荐游轮出发地或目的地城市的热门景点，含门票价格和预订链接。"""
    city = params.get("city", "")
    keyword = params.get("keyword", "")

    if not city: return "请提供城市名，如：重庆、宜昌、上海"

    # 飞猪search_poi用具体关键词效果更好，没keyword时用城市名
    search_keyword = keyword if keyword else city

    result = _call_fliggy("search_poi", {"keyword": search_keyword, "city": city})
    if isinstance(result, dict) and "error" in result:
        return "景点推荐失败: " + result["error"]

    inner = result.get("data", result) if isinstance(result, dict) else result
    if inner is None or not isinstance(inner, dict):
        return f"😔 未找到{city}的景点推荐，建议尝试其他城市或关键词"

    pois = inner.get("itemList", [])
    if not pois:
        return f"😔 未找到{city}的景点推荐，建议尝试其他城市或关键词"

    lines = [f"🎡 {city}热门景点推荐：", ""]

    for i, poi in enumerate(pois[:10], 1):
        name = poi.get("name", "")
        category = poi.get("category", "")
        address = poi.get("address", "")
        desc = poi.get("description", "")
        url = poi.get("jumpUrl", "")
        free_status = poi.get("freePoiStatus", "")
        poi_level = poi.get("poiLevel", "")
        ticket_info = poi.get("ticketInfo", "")

        lines.append(f"**{i}. {name}**")

        detail_parts = []
        # 景区等级
        if poi_level:
            try:
                lv = int(poi_level)
                detail_parts.append(f"🏆 {lv}A景区")
            except: pass
        # 免费标识
        if free_status == "FREE":
            detail_parts.append("🆓 免费入园")
        elif ticket_info:
            # ticket_info可能是dict或字符串
            if isinstance(ticket_info, dict):
                price_val = ticket_info.get("price", "")
                if price_val:
                    detail_parts.append(f"💰 {price_val}起")
            elif ticket_info:
                detail_parts.append(f"💰 {ticket_info}")
        if category:
            detail_parts.append(category)
        if detail_parts:
            lines.append(f"   {' | '.join(detail_parts)}")

        if address:
            lines.append(f"   📍 {address}")
        # 描述截取前60字
        if desc:
            desc_short = desc.strip().replace("\n", " ")[:60]
            if len(desc.strip()) > 60:
                desc_short += "…"
            lines.append(f"   📝 {desc_short}")
        if url:
            lines.append(f"   🔗 [查看/购票→]({url})")
        lines.append("")

    lines.append("💡 点击链接可查看景点详情和购买门票")
    return "\n".join(lines)


# ============ 工具4：酒店推荐 ============
def recommend_hotel(params):
    """用自然语言描述住宿需求，AI智能匹配高分酒店并返回推荐和预订链接。"""
    query = params.get("query", "")
    if not query: return "请描述你的住宿需求，如：重庆朝天门附近酒店，300左右"

    result = _call_fliggy("fliggy_ai_search", {"query": query}, timeout=60)
    if isinstance(result, dict) and "error" in result:
        return "酒店推荐失败: " + result["error"]

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

    content_text += "\n\n📋 附加服务：回复「查游轮票」可查询游轮船票"
    return content_text
