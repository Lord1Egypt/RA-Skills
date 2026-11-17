#!/usr/bin/env python3
"""邮轮实时搜索 v3.0 — 接入途牛实时API，支持搜索+详情+舱位+船舶信息"""

import sys
import json
import os
import ssl
import urllib.request
import urllib.error
from datetime import datetime, timedelta

_ALLOWED_PROXY_HOSTS = [
    "ap-guangzhou.tencentscf.com",
]

PROXY_URL = os.environ.get("PROXY_URL", "https://1439498936-0junm3maxj.ap-guangzhou.tencentscf.com")
PROXY_TOKEN = os.environ.get("PROXY_TOKEN", "")


def _validate_proxy_url(url):
    if not url:
        return False
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        host = parsed.hostname or ""
        return any(host.endswith(allowed) for allowed in _ALLOWED_PROXY_HOSTS)
    except Exception:
        return False


def _post(type_name, params):
    if not _validate_proxy_url(PROXY_URL):
        return {"error": "PROXY_URL未配置或指向未授权主机，仅允许腾讯云SCF代理端点"}
    if not PROXY_TOKEN:
        return {"error": "PROXY_TOKEN未配置"}

    ctx = ssl.create_default_context()
    ctx.verify_mode = ssl.CERT_REQUIRED
    ctx.check_hostname = True

    body = json.dumps({"type": type_name, "params": params}, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    req = urllib.request.Request(PROXY_URL, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("X-Proxy-Token", PROXY_TOKEN)
    try:
        with urllib.request.urlopen(req, timeout=120, context=ctx) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("code") == 0:
                return data.get("data", {})
            return data
    except urllib.error.HTTPError as e:
        err = ""
        try:
            err = e.read().decode("utf-8")[:300]
        except Exception:
            pass
        return {"error": "HTTP " + str(e.code) + ": " + err}
    except Exception as e:
        return {"error": str(e)}


def _is_valid_product(row):
    name = row.get("productName", "")
    if "请勿下单" in name or "内部使用" in name:
        return False
    return True


def _compute_score(row):
    satisfaction = row.get("satisfaction", 0) / 100.0
    people = min(row.get("peopleNum", 0), 10000) / 10000.0
    price = row.get("price", 99999)
    price_score = max(0, 1 - (price - 1000) / 50000)
    return satisfaction * 0.4 + people * 0.3 + price_score * 0.3


def _format_cruise(row):
    depart_list = row.get("departCityName", [])
    depart_city = depart_list[0] if depart_list else "未知"
    route_list = row.get("cruiseLineName", [])
    route = route_list[0] if route_list else "未知"
    product_id = row.get("productId", "")
    return {
        "productId": str(product_id),
        "name": row.get("productName", ""),
        "brand": row.get("cruiseBrand", ""),
        "price": row.get("price", 0),
        "days": row.get("tourDay", 0),
        "departure": depart_city,
        "port": row.get("departurePortName", ""),
        "route": route,
        "satisfaction": row.get("satisfaction", 0),
        "popularity": row.get("peopleNum", 0),
        "ticketType": row.get("ticketTypeName", ""),
        "tags": row.get("customConditionName", []),
        "picUrl": row.get("picUrl", ""),
        "bookingUrl": "https://m.tuniu.com/cruise/" + str(product_id) if product_id else "",
    }


# ========== 辅助：在搜索中定位产品 ==========
def _find_product_in_search(product_id, date_begin, date_end, route_hint=""):
    """在搜索结果中查找指定产品，支持航线提示和多页搜索"""
    search_targets = []
    if route_hint:
        search_targets.append({"cruiseLineName": route_hint})
    for route in ["日本", "韩国", "东南亚", "地中海", "长江三峡", "加勒比"]:
        if route != route_hint:
            search_targets.append({"cruiseLineName": route})
    search_targets.append({})  # 兜底：不限航线

    for st in search_targets:
        for page in range(1, 4):
            params = {"departsDateBegin": date_begin, "departsDateEnd": date_end, "pageNum": page}
            params.update(st)
            result = _post("tuniu_cruise_search", params)
            real_data = result.get("data", {}) if isinstance(result, dict) else {}
            rows = real_data.get("rows", []) if isinstance(real_data, dict) else []
            if not rows:
                break
            for r in rows:
                if str(r.get("productId", "")) == str(product_id):
                    return r
    return None


# ========== 工具1：搜索邮轮 ==========
def search_cruise(destination, departure, date_begin, date_end):
    params = {"departsDateBegin": date_begin, "departsDateEnd": date_end}
    if destination:
        params["cruiseLineName"] = destination
    if departure:
        params["departureCity"] = departure

    result = _post("tuniu_cruise_search", params)
    if isinstance(result, dict) and result.get("error"):
        return result

    real_data = result.get("data", {}) if isinstance(result, dict) else {}
    rows = real_data.get("rows", []) if isinstance(real_data, dict) else []
    count = real_data.get("count", 0) if isinstance(real_data, dict) else 0

    valid_rows = [r for r in rows if _is_valid_product(r)]
    valid_rows.sort(key=lambda r: _compute_score(r), reverse=True)

    formatted = [_format_cruise(r) for r in valid_rows[:15]]
    return {
        "total": count,
        "showing": len(formatted),
        "filters": {"destination": destination, "departure": departure, "dateRange": date_begin + " ~ " + date_end},
        "cruises": formatted
    }


# ========== 工具2：推荐邮轮 ==========
def recommend_cruise(date_begin, date_end):
    params = {"departsDateBegin": date_begin, "departsDateEnd": date_end}
    result = _post("tuniu_cruise_search", params)
    if isinstance(result, dict) and result.get("error"):
        return result

    real_data = result.get("data", {}) if isinstance(result, dict) else {}
    rows = real_data.get("rows", []) if isinstance(real_data, dict) else []
    valid_rows = [r for r in rows if _is_valid_product(r)]

    route_groups = {}
    for r in valid_rows:
        route_list = r.get("cruiseLineName", [])
        route = route_list[0] if route_list else "其他"
        if route not in route_groups:
            route_groups[route] = []
        route_groups[route].append(r)

    categories = {}

    high_sat = [r for r in valid_rows if r.get("satisfaction", 0) >= 97 and r.get("peopleNum", 0) >= 100]
    high_sat.sort(key=lambda r: (r.get("satisfaction", 0), r.get("peopleNum", 0)), reverse=True)
    categories["🏆 口碑之选"] = [_format_cruise(r) for r in high_sat[:5]]

    budget = [r for r in valid_rows if r.get("satisfaction", 0) >= 90]
    budget.sort(key=lambda r: r.get("price", 99999))
    categories["💰 性价比首选"] = [_format_cruise(r) for r in budget[:5]]

    popular = sorted(valid_rows, key=lambda r: r.get("peopleNum", 0), reverse=True)
    categories["🔥 热门推荐"] = [_format_cruise(r) for r in popular[:5]]

    route_picks = []
    for route, cruises in route_groups.items():
        best = max(cruises, key=lambda r: _compute_score(r))
        score = _compute_score(best)
        route_picks.append((route, _format_cruise(best), score))
    route_picks.sort(key=lambda x: x[2], reverse=True)
    categories["🌊 航线精选"] = [p[1] for p in route_picks[:8]]

    return {
        "total": len(valid_rows),
        "dateRange": date_begin + " ~ " + date_end,
        "categories": categories
    }


# ========== 工具3：产品详情 + 预订须知 ==========
def cruise_detail(product_id, date_begin, date_end, route_hint=""):
    target = _find_product_in_search(product_id, date_begin, date_end, route_hint)
    if not target:
        return {"error": "未找到产品 " + str(product_id) + "，请提供航线关键词(--route)辅助定位"}

    detail_params = {
        "productId": str(product_id),
        "departsDateBegin": date_begin,
        "departsDateEnd": date_end,
        "departCityCode": target.get("departCityCode", []),
        "classBrandParentId": target.get("classBrandId", 0),
        "proMode": target.get("proMode", 1)
    }
    result = _post("tuniu_cruise_product_detail", detail_params)

    d = result
    if isinstance(d, dict) and "data" in d:
        d = d["data"]
    if isinstance(d, dict) and "text" in d:
        try:
            d = json.loads(d["text"]).get("data", {})
        except Exception:
            pass

    if d is None or (isinstance(d, dict) and d.get("errorCode")):
        msg = d.get("msg", "查询失败") if isinstance(d, dict) else "查询失败"
        return {"error": "产品详情查询失败: " + msg}

    output = {
        "productId": str(d.get("productId", product_id)),
        "productName": d.get("productName", ""),
        "cruiseName": d.get("cruiseName", ""),
        "departureCity": d.get("departureCityName", ""),
        "departurePort": d.get("departurePortName", ""),
        "arrivalPort": d.get("arrivalPortName", ""),
        "duration": d.get("duration", 0),
        "nights": d.get("productNight", 0),
        "saleMode": d.get("saleModeName", ""),
        "bookNotice": d.get("bookNotice", ""),
        "images": [],
        "promotions": [],
        "journeySummary": [],
    }

    for p in d.get("productPicList", []):
        if isinstance(p, dict) and p.get("path"):
            output["images"].append({"name": p.get("name", ""), "url": p["path"]})

    for p in d.get("productPromotionInfo", []):
        if isinstance(p, dict):
            output["promotions"].append({"name": p.get("name", ""), "desc": p.get("desc", "")})

    for j in d.get("journeySummary", []):
        if isinstance(j, dict):
            output["journeySummary"].append({
                "day": j.get("dayNum", ""),
                "title": j.get("title", ""),
                "summary": j.get("summary", "")
            })

    return output


# ========== 工具4：舱位房型 + 价格 ==========
def cruise_cabin(product_id, depart_date):
    result = _post("tuniu_cruise_cabin_and_room", {
        "productId": str(product_id),
        "departDate": depart_date
    })

    d = result
    if isinstance(d, dict) and "data" in d:
        d = d["data"]
    if isinstance(d, dict) and "text" in d:
        try:
            d = json.loads(d["text"]).get("data", {})
        except Exception:
            pass

    if d is None or (isinstance(d, dict) and d.get("errorCode")):
        msg = d.get("msg", "查询失败") if isinstance(d, dict) else "未找到可用舱位"
        return {"error": "舱位查询失败: " + msg + "（请确认出发日期是否有可售）"}

    output = {
        "productId": str(product_id),
        "departDate": depart_date,
        "vendorId": "",
        "cabins": []
    }

    base = d.get("base", {})
    if base:
        output["vendorId"] = str(base.get("vendorId", ""))
        output["departDate"] = base.get("beginDate", depart_date)

    for cabin in d.get("cabinList", []):
        cabin_info = {
            "cabinName": cabin.get("cabinName", ""),
            "startPrice": cabin.get("startPrice", 0),
            "unit": cabin.get("unit", "起/人"),
            "image": cabin.get("cruiseCabinPicPath", ""),
            "rooms": []
        }
        for room in cabin.get("roomList", []):
            room_info = {
                "roomName": room.get("roomName", ""),
                "area": room.get("roomArea", ""),
                "floor": room.get("floor", ""),
                "hasBalcony": bool(room.get("hasBalcony", 0)),
                "maxPersons": room.get("maxCapacity", 0),
                "startPrice": room.get("startPrice", 0),
                "unit": room.get("unit", "起/人"),
                "facility": room.get("facilityDesc", ""),
                "description": room.get("roomDesc", ""),
                "bookNotice": room.get("bookNotice", ""),
                "priceDetails": []
            }
            for pr in room.get("priceRes", []):
                if isinstance(pr, dict):
                    room_info["priceDetails"].append({
                        "resId": pr.get("resId", ""),
                        "adultPrice": pr.get("adultPrice", 0),
                        "childPrice": pr.get("childPrice", 0),
                        "vendorId": pr.get("vendorId", "")
                    })
            cabin_info["rooms"].append(room_info)
        output["cabins"].append(cabin_info)

    return output


# ========== 工具5：船舶信息 + 餐饮 + 娱乐 ==========
def cruise_ship_info(product_id):
    result = _post("tuniu_cruise_base_info", {"productId": str(product_id)})

    d = result
    if isinstance(d, dict) and "data" in d:
        d = d["data"]
    if isinstance(d, dict) and "text" in d:
        try:
            d = json.loads(d["text"]).get("data", {})
        except Exception:
            pass

    if d is None or (isinstance(d, dict) and d.get("errorCode")):
        msg = d.get("msg", "查询失败") if isinstance(d, dict) else "查询失败"
        return {"error": "船舶信息查询失败: " + msg}

    output = {
        "productId": str(product_id),
        "ship": {},
        "cabins": [],
        "restaurants": [],
        "amuses": []
    }

    basic = d.get("basicInfo", {})
    if basic:
        output["ship"] = {
            "cruiseNameZh": basic.get("cruiseNameZh", ""),
            "cruiseNameEn": basic.get("cruiseNameEn", ""),
            "companyName": basic.get("companyName", ""),
            "firstSail": basic.get("firstSail", ""),
            "cruiseFeature": basic.get("cruiseFeature", "")
        }

    stat = d.get("shipStatInfo", {})
    if stat:
        output["ship"].update({
            "weight": str(stat.get("cruiseWeight", "")) + "吨" if stat.get("cruiseWeight") else "",
            "length": str(stat.get("cruiseLength", "")) + "米" if stat.get("cruiseLength") else "",
            "width": str(stat.get("cruiseWidth", "")) + "米" if stat.get("cruiseWidth") else "",
            "decks": stat.get("deckCount", ""),
            "rooms": stat.get("roomCount", ""),
            "passengers": stat.get("clientCount", ""),
            "crew": stat.get("sailorCount", ""),
            "speed": str(stat.get("avgSpeed", "")) + "节" if stat.get("avgSpeed") else "",
            "voltage": stat.get("powerVolt", "")
        })

    for c in d.get("cabinTypes", []):
        if isinstance(c, dict):
            output["cabins"].append({"name": c.get("cabinName", ""), "desc": c.get("cabinDesc", "")})

    for r in d.get("restaurants", []):
        if isinstance(r, dict):
            output["restaurants"].append({
                "name": r.get("name", ""),
                "floor": r.get("floorName", ""),
                "feature": r.get("feature", ""),
                "openTime": r.get("openTime", ""),
                "price": r.get("freeOrPrice", ""),
                "description": r.get("description", "")
            })

    for a in d.get("amuses", []):
        if isinstance(a, dict):
            output["amuses"].append({
                "name": a.get("name", ""),
                "floor": a.get("floorName", ""),
                "feature": a.get("feature", ""),
                "openTime": a.get("openTime", ""),
                "price": a.get("freeOrPrice", ""),
                "description": a.get("description", "")
            })

    return output


# ========== 渲染函数 ==========

def _render_search_result(data):
    if data.get("error"):
        return "❌ 查询失败：" + data["error"]

    total = data.get("total", 0)
    filters = data.get("filters", {})
    cruises = data.get("cruises", [])

    lines = ["为你找到 **" + str(total) + "** 个邮轮产品（" + filters.get("dateRange", "") + "）：\n"]
    if filters.get("destination"):
        lines.append("🎯 目的地：" + filters["destination"])
    if filters.get("departure"):
        lines.append("🚀 出发地：" + filters["departure"])
    lines.append("")

    for i, c in enumerate(cruises[:10], 1):
        details = []
        if c["price"]:
            details.append("¥" + str(int(c["price"])) + "起")
        if c["days"]:
            details.append(str(c["days"]) + "天")
        if c["brand"]:
            details.append(c["brand"])

        sat_str = ""
        if c["satisfaction"]:
            sat_str = " | 满意度" + str(c["satisfaction"]) + "%"
            if c["satisfaction"] >= 97:
                sat_str += " 👍口碑好"

        line = "**" + str(i) + ". " + c["name"] + "**"
        if details:
            line += "\n   " + " | ".join(details)
        line += "\n   📍 " + c["departure"] + "出发 · " + c["port"] + " · 航线：" + c["route"]
        line += sat_str
        if c["popularity"]:
            line += " | " + str(c["popularity"]) + "人已预订"
        if c.get("bookingUrl"):
            line += "\n   🔗 [点击预订](" + c["bookingUrl"] + ")"
        if c.get("picUrl"):
            line += "\n   ![邮轮图片](" + c["picUrl"] + ")"
        lines.append(line)
        lines.append("")

    lines.append("---")
    lines.append("💡 输入产品编号可查看详情、舱位价格、船舶设施")
    lines.append("🏠 房型参考：内舱房最经济 | 海景房有窗无阳台 | 阳台房体验最佳 | 套房适合蜜月/庆祝")
    return "\n".join(lines)


def _render_recommend_result(data):
    if data.get("error"):
        return "❌ 查询失败：" + data["error"]

    total = data.get("total", 0)
    date_range = data.get("dateRange", "")
    categories = data.get("categories", {})

    lines = ["🚢 邮轮智能推荐（" + date_range + "，共" + str(total) + "条可选）\n"]

    for cat_name, cruises in categories.items():
        if not cruises:
            continue
        lines.append("### " + cat_name + "\n")
        for i, c in enumerate(cruises[:3], 1):
            details = []
            if c["price"]:
                details.append("¥" + str(int(c["price"])) + "起")
            if c["days"]:
                details.append(str(c["days"]) + "天")
            if c["satisfaction"]:
                details.append("满意度" + str(c["satisfaction"]) + "%")

            line = str(i) + ". **" + c["brand"] + "** — " + c["route"]
            if details:
                line += " | " + " | ".join(details)
            line += " | " + c["departure"] + "出发"
            if c.get("bookingUrl"):
                line += " | [预订](" + c["bookingUrl"] + ")"
            lines.append(line)
        lines.append("")

    lines.append("---")
    lines.append("💡 输入产品编号可查看详情、舱位价格、船舶设施")
    return "\n".join(lines)


def _render_detail_result(data):
    if data.get("error"):
        return "❌ 查询失败：" + data["error"]

    lines = []
    lines.append("## 🚢 " + data.get("productName", "") + "\n")

    info = []
    if data.get("cruiseName"):
        info.append("邮轮：" + data["cruiseName"])
    if data.get("duration"):
        info.append(str(data["duration"]) + "天" + str(data.get("nights", "")) + "晚")
    if data.get("departureCity"):
        info.append("出发：" + data["departureCity"] + " · " + data.get("departurePort", ""))
    if info:
        lines.append(" | ".join(info) + "\n")

    promos = data.get("promotions", [])
    if promos:
        lines.append("### 🎁 当前促销")
        for p in promos:
            name = p.get("name", "")
            if name:
                lines.append("- " + name)
        lines.append("")

    notice = data.get("bookNotice", "")
    if notice:
        lines.append("### 📋 预订须知")
        notice_lines = notice.strip().split("\n")
        for nl in notice_lines[:15]:
            nl = nl.strip()
            if nl:
                lines.append(nl)
        if len(notice_lines) > 15:
            lines.append("...（更多条款请查看预订页面）")
        lines.append("")

    journey = data.get("journeySummary", [])
    if journey:
        lines.append("### 🗺️ 行程概览")
        for j in journey:
            day = j.get("day", "")
            title = j.get("title", "")
            summary = j.get("summary", "")
            if title or summary:
                lines.append("- 第" + str(day) + "天：" + (title or summary or ""))
        lines.append("")

    pid = data.get("productId", "")
    if pid:
        lines.append("🔗 [前往预订](https://m.tuniu.com/cruise/" + str(pid) + ")")

    return "\n".join(lines)


def _render_cabin_result(data):
    if data.get("error"):
        return "❌ 查询失败：" + data["error"]

    lines = []
    lines.append("## 🛏️ 舱位房型（出发日期：" + data.get("departDate", "") + "）\n")

    cabins = data.get("cabins", [])
    if not cabins:
        lines.append("暂无可售舱位，请尝试其他出发日期。")
        return "\n".join(lines)

    for cabin in cabins:
        name = cabin.get("cabinName", "")
        start_price = cabin.get("startPrice", 0)
        unit = cabin.get("unit", "起/人")
        img = cabin.get("image", "")

        price_str = " ¥" + str(start_price) + unit if start_price else ""
        lines.append("### " + name + price_str)
        if img:
            lines.append("![舱位图片](" + img + ")")

        rooms = cabin.get("rooms", [])
        for room in rooms:
            rname = room.get("roomName", "")
            area = room.get("area", "")
            floor = room.get("floor", "")
            balcony = "🌅有阳台" if room.get("hasBalcony") else ""
            maxp = room.get("maxPersons", 0)
            rprice = room.get("startPrice", 0)

            info_parts = []
            if area:
                info_parts.append(area)
            if floor:
                info_parts.append(str(floor) + "层")
            if balcony:
                info_parts.append(balcony)
            if maxp:
                info_parts.append("最多" + str(maxp) + "人")
            if rprice:
                info_parts.append("¥" + str(rprice) + unit)

            lines.append("- **" + rname + "** " + " | ".join(info_parts))

            prices = room.get("priceDetails", [])
            if prices:
                p = prices[0]
                lines.append("  成人 ¥" + str(p.get("adultPrice", "")) + "/人 | 儿童 ¥" + str(p.get("childPrice", "")) + "/人")

        lines.append("")

    lines.append("---")
    lines.append("💡 价格为人均价，实际以预订时为准。点击预订链接选择舱位下单。")
    pid = data.get("productId", "")
    if pid:
        lines.append("🔗 [前往预订](https://m.tuniu.com/cruise/" + str(pid) + ")")
    return "\n".join(lines)


def _render_ship_info(data):
    if data.get("error"):
        return "❌ 查询失败：" + data["error"]

    lines = []
    ship = data.get("ship", {})
    lines.append("## 🚢 " + ship.get("cruiseNameZh", "") + "\n")

    if ship.get("cruiseNameEn"):
        lines.append("**英文名：** " + ship["cruiseNameEn"])
    if ship.get("companyName"):
        lines.append("**所属公司：** " + ship["companyName"])
    if ship.get("firstSail"):
        lines.append("**首航时间：** " + ship["firstSail"])

    params = []
    if ship.get("weight"):
        params.append("吨位：" + ship["weight"])
    if ship.get("length") and ship.get("width"):
        params.append("尺寸：" + ship["length"] + " × " + ship["width"])
    if ship.get("decks"):
        params.append("甲板：" + str(ship["decks"]) + "层")
    if ship.get("rooms"):
        params.append("客房：" + str(ship["rooms"]) + "间")
    if ship.get("passengers"):
        params.append("载客：" + str(ship["passengers"]) + "人")
    if ship.get("crew"):
        params.append("船员：" + str(ship["crew"]) + "人")
    if ship.get("speed"):
        params.append("航速：" + ship["speed"])
    if ship.get("voltage"):
        params.append("电压：" + ship["voltage"])
    if params:
        lines.append("\n### 📊 船舶参数")
        lines.append(" | ".join(params))

    feature = ship.get("cruiseFeature", "")
    if feature:
        lines.append("\n### ✨ 特色介绍")
        lines.append(feature[:300])
        if len(feature) > 300:
            lines.append("...")

    cabin_types = data.get("cabins", [])
    if cabin_types:
        lines.append("\n### 🛏️ 舱型说明")
        for ct in cabin_types:
            lines.append("- **" + ct.get("name", "") + "**：" + ct.get("desc", "")[:80])

    restaurants = data.get("restaurants", [])
    if restaurants:
        lines.append("\n### 🍽️ 餐饮设施（" + str(len(restaurants)) + "家）")
        for r in restaurants[:10]:
            name = r.get("name", "")
            floor = r.get("floor", "")
            price = r.get("price", "")
            feat = r.get("feature", "")
            info = []
            if floor:
                info.append(floor)
            if feat:
                info.append(feat)
            if price:
                info.append(str(price))
            lines.append("- **" + name + "** " + " | ".join(info))
        if len(restaurants) > 10:
            lines.append("- ...还有" + str(len(restaurants) - 10) + "家餐厅")

    amuses = data.get("amuses", [])
    if amuses:
        lines.append("\n### 🎢 娱乐设施（" + str(len(amuses)) + "项）")
        for a in amuses[:10]:
            name = a.get("name", "")
            floor = a.get("floor", "")
            price = a.get("price", "")
            info = []
            if floor:
                info.append(floor)
            if price:
                info.append(str(price))
            lines.append("- **" + name + "** " + (" | ".join(info) if info else ""))
        if len(amuses) > 10:
            lines.append("- ...还有" + str(len(amuses) - 10) + "个娱乐项目")

    lines.append("")
    return "\n".join(lines)


# ========== 主入口 ==========
def main():
    import argparse
    parser = argparse.ArgumentParser(description="邮轮实时搜索与智能推荐 v3.0")
    parser.add_argument("--mode", choices=["search", "recommend", "detail", "cabin", "ship"],
                        default="search",
                        help="search=条件搜索, recommend=智能推荐, detail=产品详情, cabin=舱位查询, ship=船舶信息")
    parser.add_argument("--product-id", default="", help="产品ID（detail/cabin/ship模式必填）")
    parser.add_argument("--destination", default="", help="目的地/航线关键词（search/detail模式）")
    parser.add_argument("--departure", default="", help="出发城市（search模式）")
    parser.add_argument("--days", type=int, default=90, help="搜索未来天数（默认90）")
    parser.add_argument("--depart-date", default="", help="出发日期 YYYY-MM-DD（cabin模式必填）")
    parser.add_argument("--price-max", type=int, default=0, help="最高价格筛选")
    parser.add_argument("--tag", default="", help="标签筛选")
    parser.add_argument("--route", default="", help="航线关键词，辅助定位产品（detail模式）")
    parser.add_argument("--output", default="text", choices=["json", "text"], help="输出格式")

    args = parser.parse_args()

    today = datetime.now()
    date_begin = today.strftime("%Y-%m-%d")
    date_end = (today + timedelta(days=args.days)).strftime("%Y-%m-%d")

    if args.mode == "detail":
        if not args.product_id:
            print("❌ 请提供 --product-id")
            return
        result = cruise_detail(args.product_id, date_begin, date_end, args.route)
        print(_render_detail_result(result) if args.output == "text" else json.dumps(result, ensure_ascii=False, indent=2))

    elif args.mode == "cabin":
        if not args.product_id:
            print("❌ 请提供 --product-id")
            return
        depart_date = args.depart_date or date_begin
        result = cruise_cabin(args.product_id, depart_date)
        print(_render_cabin_result(result) if args.output == "text" else json.dumps(result, ensure_ascii=False, indent=2))

    elif args.mode == "ship":
        if not args.product_id:
            print("❌ 请提供 --product-id")
            return
        result = cruise_ship_info(args.product_id)
        print(_render_ship_info(result) if args.output == "text" else json.dumps(result, ensure_ascii=False, indent=2))

    elif args.mode == "recommend":
        result = recommend_cruise(date_begin, date_end)
        print(_render_recommend_result(result) if args.output == "text" else json.dumps(result, ensure_ascii=False, indent=2))

    else:  # search
        result = search_cruise(args.destination, args.departure, date_begin, date_end)
        if "cruises" in result and args.price_max > 0:
            result["cruises"] = [c for c in result["cruises"] if c["price"] <= args.price_max]
            result["showing"] = len(result["cruises"])
        if "cruises" in result and args.tag:
            result["cruises"] = [c for c in result["cruises"] if any(args.tag in t for t in c.get("tags", []))]
            result["showing"] = len(result["cruises"])
        print(_render_search_result(result) if args.output == "text" else json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
