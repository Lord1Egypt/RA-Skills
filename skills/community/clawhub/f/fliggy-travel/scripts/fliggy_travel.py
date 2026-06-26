# -*- coding: utf-8 -*-
"""
飞猪旅行助手 - ClawHub技能脚本
零配置即装即用，通过SCF代理调用飞猪+高德API
11个工具：行程规划、火车票、机票、酒店、景点、美食、交通、极速搜索、万豪搜索/详情/套餐
"""
import json
import re
import urllib.request
import urllib.error

# ============ 配置 ============
FLIGGY_PROXY = "https://1439498936-6sysdjjt99.ap-guangzhou.tencentscf.com"
GAODE_PROXY = "https://1439498936-bl10af74fl.ap-guangzhou.tencentscf.com"
PROXY_TOKEN = "tp_8k2mX9vQ4z"
TIMEOUT = 30

_CITIES = [
    "北京", "上海", "广州", "深圳", "成都", "杭州", "南京", "武汉", "长沙", "重庆",
    "西安", "厦门", "青岛", "大连", "昆明", "丽江", "桂林", "苏州", "珠海", "海口",
    "三亚", "天津", "济南", "沈阳", "哈尔滨", "长春", "郑州", "合肥", "福州", "南昌",
    "太原", "石家庄", "贵阳", "南宁", "兰州", "银川", "呼和浩特", "乌鲁木齐", "拉萨",
    "无锡", "宁波", "温州", "烟台", "威海", "佛山", "东莞", "中山", "惠州", "扬州",
]


# ============ 代理调用 ============
def _call_fliggy(rtype, params):
    """调用飞猪SCF代理"""
    body = json.dumps({"type": rtype, "params": params}, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    req = urllib.request.Request(
        FLIGGY_PROXY, data=body,
        headers={"Content-Type": "application/json", "X-Proxy-Token": PROXY_TOKEN},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err = ""
        try: err = e.read().decode("utf-8", errors="replace")[:300]
        except: pass
        return {"error": "proxy error " + str(e.code) + ": " + err}
    except Exception as e:
        return {"error": "request error: " + str(e)}


def _call_gaode(api, params):
    """调用高德SCF代理"""
    body = json.dumps({"type": api, "params": params}).encode("utf-8")
    req = urllib.request.Request(
        GAODE_PROXY, data=body,
        headers={"Content-Type": "application/json", "X-Proxy-Token": PROXY_TOKEN},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read().decode("utf-8"))
            # 高德代理返回 {"code":0,"data":{...},"type":"xxx"}，自动解包data层
            if isinstance(data, dict) and data.get("code") == 0 and "data" in data:
                return data["data"]
            return data
    except urllib.error.HTTPError as e:
        err = ""
        try: err = e.read().decode("utf-8", errors="replace")[:200]
        except: pass
        return {"error": "proxy error " + str(e.code) + ": " + err}
    except Exception as e:
        return {"error": "request error: " + str(e)}


# ============ 高德通用 ============
def _gaode_geocode(address, city=""):
    params = {"address": address}
    if city: params["city"] = city
    data = _call_gaode("geocode", params)
    if isinstance(data, dict) and data.get("status") == "1":
        geocodes = data.get("geocodes", [])
        if geocodes:
            loc = geocodes[0].get("location", "")
            if loc and "," in loc:
                parts = loc.split(",")
                return (parts[0], parts[1])
    return (None, None)


def _gaode_food_search(location, keywords="", city="", radius=3000, limit=10):
    params = {"location": location, "types": "050000", "radius": radius, "sortrule": "weight", "offset": limit, "page": 1, "extensions": "all"}
    if keywords: params["keywords"] = keywords
    if city: params["city"] = city
    data = _call_gaode("poi_around", params)
    if isinstance(data, dict) and data.get("status") == "1":
        return data.get("pois", [])
    return []


def _gaode_driving(origin, destination):
    data = _call_gaode("driving_route_by_address", {"origin_address": origin, "destination_address": destination})
    if isinstance(data, dict) and data.get("status") == "1":
        route = data.get("route", {})
        paths = route.get("paths", [])
        # 优先从taxi_cost取打车费
        taxi_cost_raw = route.get("taxi_cost", "0")
        if paths:
            path = paths[0]
            distance = int(path.get("distance", 0))
            duration = int(path.get("duration", 0))
            # 用高德返回的taxi_cost更准确
            try:
                taxi_cost = "¥" + str(int(taxi_cost_raw)) + "左右"
            except:
                taxi_cost = _estimate_taxi_cost(distance)
            return {"distance_km": round(distance / 1000, 1), "duration_min": round(duration / 60), "taxi_cost": taxi_cost}
    return {}


def _gaode_transit(origin, destination, city):
    data = _call_gaode("transit_route_by_address", {"origin_address": origin, "destination_address": destination, "city": city})
    if not isinstance(data, dict) or data.get("status") != "1":
        return []
    transits = data.get("route", {}).get("transits", [])
    results = []
    for transit in transits[:4]:
        duration = int(transit.get("duration", 0))
        cost = transit.get("cost", "0")
        walking = transit.get("walking_distance", "0")
        lines = []
        for seg in transit.get("segments", []):
            buslines = seg.get("bus", {}).get("buslines", [])
            if buslines:
                bl = buslines[0]
                lines.append({"name": bl.get("name", ""), "dep_stop": bl.get("departure_stop", {}).get("name", ""), "arr_stop": bl.get("arrival_stop", {}).get("name", ""), "duration_min": round(int(bl.get("duration", 0)) / 60)})
        is_metro = any(_is_metro_line(l["name"]) for l in lines)
        results.append({"duration_min": round(duration / 60), "cost": cost, "walking_distance": walking, "lines": lines, "is_metro": is_metro, "type": "地铁" if is_metro else "公交"})
    return results


# ============ 辅助 ============
def _estimate_taxi_cost(distance_m):
    distance_km = distance_m / 1000
    if distance_km <= 0: return "¥0"
    if distance_km <= 3: return "¥14左右"
    cost = 14 + (distance_km - 3) * 2.5
    return "¥" + str(int(cost)) + "左右"

def _is_metro_line(line_name):
    return any(kw in line_name for kw in ["地铁", "号线", "城轨", "磁浮", "市域", "轻轨"])

def _extract_city(query):
    for city in _CITIES:
        if city in query: return city
    return ""

def _extract_dest(query):
    m = re.search(r"去(.{2,8}?)(玩|旅游|旅行|度假|出差|住|的|几天)", query)
    if m:
        dest = re.sub(r"(的|了|一|两|附近|周边|景区|区域|一带)$", "", m.group(1).strip())
        if len(dest) >= 2: return dest
    m = re.search(r"(.{2,6}?)(旅游|旅行|度假|游玩|周末游|亲子游|蜜月游|自由行)", query)
    if m:
        dest = re.sub(r"(去|到|的|了|附近|周边|景区|一带)$", "", m.group(1).strip())
        if len(dest) >= 2: return dest
    return ""

def _build_tips(current_tool, dest=""):
    all_tools = [("行程规划", "🗺️行程规划"), ("火车票查询", "🚄火车票查询"), ("机票查询", "✈️机票查询"), ("酒店搜索", "🏨酒店搜索"), ("景点门票", "🎫景点门票"), ("美食推荐", "🍜美食推荐"), ("市内交通", "🚇市内交通"), ("极速搜索", "⚡极速搜索"), ("万豪酒店", "🏨万豪酒店")]
    tips = []
    for tool_key, label in all_tools:
        if tool_key == current_tool: continue
        if dest:
            mapping = {"行程规划": "🗺️规划" + dest + "行程", "火车票查询": "🚄查去" + dest + "的火车票", "机票查询": "✈️查去" + dest + "的机票", "酒店搜索": "🏨推荐" + dest + "酒店", "景点门票": "🎫推荐" + dest + "景点", "美食推荐": "🍜推荐" + dest + "美食", "市内交通": "🚇" + dest + "市内交通", "极速搜索": "⚡极速搜" + dest + "旅行信息", "万豪酒店": "🏨查" + dest + "万豪酒店"}
            tips.append(mapping.get(tool_key, label))
        else:
            tips.append(label)
    return "\n\n💡 我还能帮你：" + " | ".join(tips)

def _parse_flyai_text(data):
    if isinstance(data, str): return data
    if isinstance(data, dict):
        if "error" in data: return "搜索失败: " + data["error"]
        if "raw_text" in data: return data["raw_text"]
        inner = data.get("data", data)
        if inner is None: inner = {}
        if isinstance(inner, str): return inner
        if isinstance(inner, dict):
            item_list = inner.get("itemList", [])
            if item_list: return _format_items(item_list)
            return json.dumps(inner, ensure_ascii=False, indent=2)
    return str(data)

def _normalize_item(item):
    """统一item字段：兼容旧版平铺和fast_search的info嵌套"""
    info = item.get("info")
    if isinstance(info, dict):
        return {"name": info.get("title", ""), "price": info.get("price", ""), "jumpUrl": info.get("jumpUrl", ""), "rating": info.get("scoreDesc", ""), "star": info.get("star", ""), "address": info.get("address", ""), "mainPic": info.get("mainPic", "")}
    return item

def _format_items(item_list):
    lines = []
    for i, raw_item in enumerate(item_list[:10], 1):
        item = _normalize_item(raw_item)
        name = item.get("title", item.get("name", "未知"))
        price = item.get("price", item.get("ticketPrice", ""))
        jump_url = item.get("jumpUrl", item.get("detailUrl", ""))
        rating = item.get("rating", "")
        star = item.get("star", item.get("hotelStars", ""))
        address = item.get("address", "")
        main_pic = item.get("mainPic", item.get("picUrl", ""))
        lines.append(str(i) + ". " + name)
        detail_parts = []
        if price: detail_parts.append("💰 ¥" + str(price) + "起")
        if rating: detail_parts.append("⭐" + str(rating))
        if star and star not in ("", "0"): detail_parts.append("🏷️" + str(star))
        if detail_parts: lines.append("   " + " | ".join(detail_parts))
        if address: lines.append("   📍 " + address)
        if jump_url: lines.append("   🔗 " + jump_url)
        if main_pic: lines.append("   ![图片](" + str(main_pic) + ")")
        lines.append("")
    lines.append("⚠️ 价格实时变动，以实际下单为准")
    return "\n".join(lines)

def _format_train_items(item_list):
    lines = []
    for i, item in enumerate(item_list[:15], 1):
        for journey in item.get("journeys", []):
            for seg in journey.get("segments", []):
                transport = seg.get("marketingTransportName", "")
                transport_no = seg.get("marketingTransportNo", seg.get("transportNo", ""))
                dep_station = seg.get("depStationShortName", seg.get("depStationName", ""))
                arr_station = seg.get("arrStationShortName", seg.get("arrStationName", ""))
                dep_time = seg.get("depDateTime", "")
                arr_time = seg.get("arrDateTime", "")
                duration = seg.get("duration", "")
                lines.append(str(i) + ". " + transport + " " + str(transport_no))
                dep_t = dep_time.split(" ")[-1] if " " in dep_time else dep_time
                arr_t = arr_time.split(" ")[-1] if " " in arr_time else arr_time
                lines.append("   " + dep_station + " " + dep_t + " → " + arr_station + " " + arr_t)
                if duration:
                    try:
                        dur = int(duration)
                        lines.append("   ⏱️ " + str(dur // 60) + "时" + str(dur % 60) + "分")
                    except: pass
                seat_info = seg.get("seatInfos", [])
                if seat_info:
                    seat_parts = []
                    for s in seat_info[:4]:
                        sname = s.get("seatClassName", "")
                        sprice = s.get("price", "")
                        sstock = s.get("stock", "")
                        stock_str = "有票" if sstock and str(sstock) not in ("0", "") else ("无票" if str(sstock) == "0" else "")
                        part = sname + " ¥" + str(sprice)
                        if stock_str: part += "(" + stock_str + ")"
                        seat_parts.append(part)
                    if seat_parts: lines.append("   💺 " + " | ".join(seat_parts))
                detail_url = item.get("detailUrl", "")
                if detail_url: lines.append("   🔗 " + detail_url)
                lines.append("")
                break
    lines.append("⚠️ 余票和价格实时变动，以实际下单为准")
    return "\n".join(lines)

def _format_flight_items(item_list):
    lines = []
    for i, item in enumerate(item_list[:15], 1):
        for journey in item.get("journeys", []):
            for seg in journey.get("segments", []):
                transport = seg.get("marketingTransportName", "")
                transport_no = seg.get("marketingTransportNo", seg.get("transportNo", ""))
                dep_city = seg.get("depCityName", "")
                arr_city = seg.get("arrCityName", "")
                dep_station = seg.get("depStationShortName", seg.get("depStationName", ""))
                arr_station = seg.get("arrStationShortName", seg.get("arrStationName", ""))
                dep_time = seg.get("depDateTime", "")
                arr_time = seg.get("arrDateTime", "")
                duration = seg.get("duration", "")
                lines.append(str(i) + ". " + transport + str(transport_no) + " " + dep_city + "→" + arr_city)
                dep_t = dep_time.split(" ")[-1] if " " in dep_time else dep_time
                arr_t = arr_time.split(" ")[-1] if " " in arr_time else arr_time
                lines.append("   " + dep_station + " " + dep_t + " → " + arr_station + " " + arr_t)
                if duration:
                    try:
                        dur = int(duration)
                        lines.append("   ⏱️ " + str(dur // 60) + "时" + str(dur % 60) + "分")
                    except: pass
                cabin_info = seg.get("cabinInfos", [])
                if cabin_info:
                    price_parts = []
                    for c in cabin_info[:3]:
                        cname = c.get("cabinClassName", "")
                        cprice = c.get("price", "")
                        price_parts.append(cname + " ¥" + str(cprice))
                    if price_parts: lines.append("   💰 " + " | ".join(price_parts))
                detail_url = item.get("detailUrl", "")
                if detail_url: lines.append("   🔗 " + detail_url)
                lines.append("")
                break
    lines.append("⚠️ 票价实时变动，以实际下单为准")
    return "\n".join(lines)


# ============ 11个工具函数 ============

def travel_plan(params):
    """行程规划：用自然语言描述旅行需求，智能推荐行程方案。"""
    query = params.get("query", "")
    if not query: return "请描述你的旅行需求，如：三亚5天亲子游"
    result = _call_fliggy("fliggy_ai_search", {"query": query})
    text = _parse_flyai_text(result)
    dest = _extract_dest(query) or _extract_city(query)
    return text + _build_tips("行程规划", dest)


def search_train(params):
    """火车票查询：查询火车票/高铁票的余票、价格和时刻表。"""
    origin = params.get("origin", "")
    if not origin: return "请提供出发地"
    destination = params.get("destination", "")
    args = {"origin": origin}
    if destination: args["destination"] = destination
    if params.get("dep_date"): args["depDate"] = params["dep_date"]
    if params.get("seat_class"): args["seatClassName"] = params["seat_class"]
    if params.get("train_type"): args["trafficModel"] = params["train_type"]
    if params.get("only_has_stock"): args["limitHasStock"] = True
    result = _call_fliggy("search_domestic_train", args)
    if isinstance(result, dict) and "error" in result:
        return "火车票查询失败: " + result["error"]
    inner = result.get("data", result)
    if isinstance(inner, dict):
        item_list = inner.get("itemList", [])
        text = _format_train_items(item_list) if item_list else "未找到符合条件的火车票"
    else:
        text = _parse_flyai_text(result)
    return text + _build_tips("火车票查询", destination)


def search_flight(params):
    """机票查询：查询国内航班实时票价、航班号、起降时间。"""
    origin = params.get("origin", "")
    if not origin: return "请提供出发地"
    destination = params.get("destination", "")
    args = {"origin": origin}
    if destination: args["destination"] = destination
    if params.get("dep_date"): args["depDate"] = params["dep_date"]
    if params.get("back_date"): args["backDate"] = params["back_date"]
    if params.get("seat_class"): args["seatClassName"] = params["seat_class"]
    if params.get("direct_only"): args["journeyType"] = 1
    result = _call_fliggy("search_flight", args)
    if isinstance(result, dict) and "error" in result:
        return "机票查询失败: " + result["error"]
    inner = result.get("data", result)
    if isinstance(inner, dict):
        item_list = inner.get("itemList", [])
        text = _format_flight_items(item_list) if item_list else "未找到符合条件的航班"
    else:
        text = _parse_flyai_text(result)
    return text + _build_tips("机票查询", destination)


def search_hotel(params):
    """酒店搜索：搜索酒店，返回实时价格和预订链接。"""
    dest_name = params.get("dest_name", "")
    if not dest_name: return "请提供目的地"
    args = {"destName": dest_name}
    if params.get("check_in"): args["checkInDate"] = params["check_in"]
    if params.get("check_out"): args["checkOutDate"] = params["check_out"]
    if params.get("keywords"): args["keyWords"] = params["keywords"]
    if params.get("star"): args["hotelStars"] = params["star"]
    if params.get("max_price", 0) > 0: args["maxPrice"] = params["max_price"]
    if params.get("hotel_type"): args["hotelTypes"] = params["hotel_type"]
    if params.get("bed_type"): args["hotelBedTypes"] = params["bed_type"]
    result = _call_fliggy("search_hotels", args)
    text = _parse_flyai_text(result)
    return text + _build_tips("酒店搜索", dest_name)


def search_poi(params):
    """景点门票：搜索景点门票，返回门票价格和购票链接。"""
    keyword = params.get("keyword", "")
    city = params.get("city", "")
    if not keyword and not city: return "请至少提供景点关键词或城市名"
    args = {}
    if keyword: args["keyword"] = keyword
    if city: args["cityName"] = city
    if params.get("category"): args["category"] = params["category"]
    if params.get("poi_level", 0) > 0: args["poiLevel"] = params["poi_level"]
    args["showTicket"] = True
    result = _call_fliggy("search_poi", args)
    text = _parse_flyai_text(result)
    return text + _build_tips("景点门票", city or keyword)


def search_food(params):
    """美食推荐：基于位置搜索周边餐厅美食。"""
    query = params.get("query", "")
    if not query: return "请描述美食需求，如：上海南京路附近火锅"
    dest = _extract_dest(query) or _extract_city(query)
    city = _extract_city(query)
    if not dest: dest = query.strip()[:8]
    lng, lat = _gaode_geocode(dest, city)
    if not lng: return "无法解析「" + dest + "」的位置，请告诉我具体城市和地点"
    keywords = ""
    for kw in ["火锅", "日料", "粤菜", "烧烤", "咖啡", "甜品", "川菜", "湘菜", "西餐", "海鲜", "早茶", "小吃"]:
        if kw in query: keywords = kw; break
    pois = _gaode_food_search(location=lng + "," + lat, keywords=keywords, city=city or dest, radius=3000, limit=10)
    if not pois: return "未找到" + dest + "附近的餐厅" + _build_tips("美食推荐", dest)
    lines = ["🍜 找到 " + str(len(pois)) + " 家 " + dest + "附近餐厅：", ""]
    for i, poi in enumerate(pois, 1):
        name = poi.get("name", "未知")
        type_name = poi.get("type", "")
        cuisine = ""
        if type_name:
            parts = type_name.split(";")
            if len(parts) >= 2: cuisine = parts[1]
        cuisine_tag = " [" + cuisine + "]" if cuisine else ""
        rating = poi.get("rating", "") or (poi.get("biz_ext", {}) or {}).get("rating", "")
        cost = poi.get("cost", "") or (poi.get("biz_ext", {}) or {}).get("cost", "")
        address = poi.get("address", "")
        lines.append(str(i) + ". " + name + cuisine_tag)
        detail_parts = []
        if rating and rating not in ("0", "-1"): detail_parts.append("⭐" + str(rating))
        if cost and cost not in ("0", "-1"): detail_parts.append("人均¥" + str(cost))
        if detail_parts: lines.append("   " + " | ".join(detail_parts))
        if address: lines.append("   📍 " + address)
        lines.append("")
    lines.append("💡 评分和价格仅供参考，建议出发前电话确认")
    return "\n".join(lines) + _build_tips("美食推荐", city or dest)


def search_transport(params):
    """市内交通：查询从A到B的打车预估和公交地铁路线。"""
    query = params.get("query", "")
    if not query: return "请描述交通需求，如：上海浦东机场到外滩"
    city = _extract_city(query)
    m = re.search(r"(.{2,15}?)到(.{2,15})", query)
    if not m: return "请说明出发地和目的地，如：浦东机场到外滩（上海）" + _build_tips("市内交通")
    origin = m.group(1).strip()
    destination = m.group(2).strip()
    for c in _CITIES:
        if origin.startswith(c): origin = origin[len(c):].strip(); break
    if not city: return "请告诉我城市名" + _build_tips("市内交通")

    lines = ["📍 " + origin + " → " + destination + " 交通方式", ""]

    # 驾车路线（用地址直接调高德）
    driving_data = _call_gaode("driving_route_by_address", {"origin_address": city + origin, "destination_address": city + destination})
    driving = {}
    if isinstance(driving_data, dict) and driving_data.get("status") == "1":
        route = driving_data.get("route", {})
        paths = route.get("paths", [])
        taxi_cost_raw = route.get("taxi_cost", "0")
        if paths:
            path = paths[0]
            distance = int(path.get("distance", 0))
            duration = int(path.get("duration", 0))
            try:
                taxi_cost = "¥" + str(int(taxi_cost_raw)) + "左右"
            except:
                taxi_cost = _estimate_taxi_cost(distance)
            driving = {"distance_km": round(distance / 1000, 1), "duration_min": round(duration / 60), "taxi_cost": taxi_cost}

    if driving:
        lines.append("━━━ 🚗 打车/驾车 ━━━")
        lines.append("距离" + str(driving["distance_km"]) + "公里 | 约" + str(driving["duration_min"]) + "分钟 | " + driving["taxi_cost"])
        lines.append("💡 可打开微信/支付宝「滴滴出行」小程序叫车")
        lines.append("")

    # 公交地铁路线
    transit_data = _call_gaode("transit_route_by_address", {"origin_address": city + origin, "destination_address": city + destination, "city": city})
    transit_routes = []
    if isinstance(transit_data, dict) and transit_data.get("status") == "1":
        transits = transit_data.get("route", {}).get("transits", [])
        for transit in transits[:4]:
            duration = int(transit.get("duration", 0))
            cost = transit.get("cost", "0")
            walking = transit.get("walking_distance", "0")
            lines_info = []
            for seg in transit.get("segments", []):
                buslines = seg.get("bus", {}).get("buslines", [])
                if buslines:
                    bl = buslines[0]
                    lines_info.append({"name": bl.get("name", ""), "dep_stop": bl.get("departure_stop", {}).get("name", ""), "arr_stop": bl.get("arrival_stop", {}).get("name", "")})
            is_metro = any(_is_metro_line(l["name"]) for l in lines_info)
            transit_routes.append({"duration_min": round(duration / 60), "cost": cost, "walking_distance": walking, "lines": lines_info, "is_metro": is_metro, "type": "地铁" if is_metro else "公交"})

    if transit_routes:
        metro_routes = [r for r in transit_routes if r["is_metro"]]
        bus_routes = [r for r in transit_routes if not r["is_metro"]]
        if metro_routes:
            lines.append("━━━ 🚇 地铁/城轨 ━━━")
            for i, route in enumerate(metro_routes[:2], 1):
                cost_str = "¥" + route["cost"] if route["cost"] and route["cost"] != "0" else ""
                line_names = " → ".join(l["name"].split("(")[0] for l in route["lines"])
                detail_parts = ["约" + str(route["duration_min"]) + "分钟"]
                if cost_str: detail_parts.append(cost_str)
                lines.append("方案" + str(i) + ": " + line_names + " | " + " ".join(detail_parts))
                for l in route["lines"]:
                    lines.append("  " + l["name"].split("(")[0] + ": " + l["dep_stop"] + "→" + l["arr_stop"])
            lines.append("")
        if bus_routes:
            lines.append("━━━ 🚌 公交 ━━━")
            for i, route in enumerate(bus_routes[:2], 1):
                cost_str = "¥" + route["cost"] if route["cost"] and route["cost"] != "0" else ""
                line_names = " → ".join(l["name"].split("(")[0] for l in route["lines"])
                detail_parts = ["约" + str(route["duration_min"]) + "分钟"]
                if cost_str: detail_parts.append(cost_str)
                lines.append("方案" + str(i) + ": " + line_names + " | " + " ".join(detail_parts))
            lines.append("")

    if not driving and not transit_routes:
        return "未找到合适的交通方案，建议使用地图APP导航。" + _build_tips("市内交通", city)
    lines.append("💡 以上时间和费用为预估值，实际可能因路况变化")
    return "\n".join(lines) + _build_tips("市内交通", city)


def search_fast(params):
    """极速搜索：飞猪通用搜索极速版，快速查询旅行信息。"""
    query = params.get("query", "")
    if not query: return "请输入搜索词"
    result = _call_fliggy("fliggy_fast_search", {"query": query})
    text = _parse_flyai_text(result)
    dest = _extract_city(query) or _extract_dest(query) or ""
    return text + _build_tips("极速搜索", dest)


def search_marriott_hotel(params):
    """万豪酒店搜索：搜索万豪集团旗下酒店。"""
    dest_name = params.get("dest_name", "")
    if not dest_name: return "请提供目的地"
    args = {"destName": dest_name}
    if params.get("check_in"): args["checkInDate"] = params["check_in"]
    if params.get("check_out"): args["checkOutDate"] = params["check_out"]
    if params.get("keywords"): args["keyWords"] = params["keywords"]
    if params.get("max_price", 0) > 0: args["maxPrice"] = params["max_price"]
    if params.get("bed_type"): args["hotelBedTypes"] = params["bed_type"]
    result = _call_fliggy("search_marriott_hotels", args)
    text = _parse_flyai_text(result)
    return text + _build_tips("万豪酒店", dest_name)


def get_marriott_hotel_info(params):
    """万豪酒店详情：获取万豪酒店详细信息。"""
    hotel_name = params.get("hotel_name", "")
    shid = params.get("shid", 0)
    if not hotel_name and not shid: return "请提供酒店名称或酒店ID"
    args = {}
    if hotel_name: args["hotelName"] = hotel_name
    if shid: args["shid"] = shid
    if params.get("review_keyword"): args["reviewKeyword"] = params["review_keyword"]
    result = _call_fliggy("get_marriott_hotel_info", args)
    text = _parse_flyai_text(result)
    return text + _build_tips("万豪酒店", hotel_name)


def search_marriott_package(params):
    """万豪套餐搜索：搜索万豪集团在售套餐商品。"""
    keyword = params.get("keyword", "")
    hotel_name = params.get("hotel_name", "")
    province_or_city = params.get("province_or_city", "")
    if not keyword and not hotel_name and not province_or_city: return "请提供搜索关键词、酒店名称或城市"
    args = {}
    if keyword: args["keyword"] = keyword
    if hotel_name: args["hotelName"] = hotel_name
    if province_or_city: args["provinceOrCity"] = province_or_city
    result = _call_fliggy("search_marriott_packages", args)
    text = _parse_flyai_text(result)
    return text + _build_tips("万豪酒店", province_or_city or hotel_name)
