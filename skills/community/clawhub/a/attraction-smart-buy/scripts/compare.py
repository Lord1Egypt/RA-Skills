#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
景点门票比价 v2.0.1 - 美团+飞猪+途牛三平台景点门票比价 + 购票决策建议
通过SCF代理查询美团CPS/飞猪/途牛实时景点门票价格

用法:
  python3 compare.py --city "北京" [--keyword "故宫"] [--level 5A] [--category 博物馆]
  python3 compare.py --city "北京" --name "故宫博物院"
  python3 compare.py --city "北京" --name "故宫博物院" --advisor
"""

import argparse
import json
import re
import sys
import threading
import urllib.request
import urllib.error
from datetime import datetime

# ============================================================
# 配置
# ============================================================

PROXY_TOKEN = ""

SCF_FLIGGY_URL = "https://1439498936-6sysdjjt99.ap-guangzhou.tencentscf.com"
SCF_TUNIU_URL = "https://1439498936-0junm3maxj.ap-guangzhou.tencentscf.com"
SCF_MEITUAN_URL = "https://1439498936-cltb2hszg7.ap-guangzhou.tencentscf.com"

HEADERS = {
    "Content-Type": "application/json",
    "X-Proxy-Token": PROXY_TOKEN,
}

# 景点等级 -> 价格分位基准（门票价格，单位：元）
LEVEL_PRICE_REF = {
    "5A": (30, 120, 400),
    "4A": (15, 60, 200),
    "3A": (5, 30, 100),
    "无等级": (0, 50, 200),
}

# 景点类型 -> 价格偏移系数
CATEGORY_PRICE_FACTOR = {
    "主题乐园": 2.5, "水上乐园": 1.8, "动物园": 1.5, "海洋馆": 1.8,
    "博物馆": 0.6, "历史古迹": 0.8, "风景名胜": 1.0, "公园乐园": 1.2,
    "宗教场所": 0.5, "城市观光": 0.7, "沙滩海岛": 1.2, "温泉": 1.5,
    "滑雪场": 2.0, "剧院剧场": 1.5,
}

# 旺季月份（全国通用）
PEAK_MONTHS = {1, 2, 7, 8, 10}

# 美团CPS景点搜索排除关键词（非纯门票商品）
# v2.0.1: 扩展关键词列表
EXCLUDE_KEYWORDS = [
    "讲解", "导览", "夜游", "日游", "亲子", "家庭", "套票", "跟团",
    "一日游", "半日游", "接送", "包车", "直通车", "大巴", "自驾",
    "自由行", "多日游", "酒店", "小团", "纯玩团", "晚·", "天晚",
    "套餐", "摄影", "旅拍", "跟拍", "接驳", "摆渡", "游船",
    "门票+", "+门票", "+导览", "+精讲", "3h", "3小时", "2h", "2小时",
    "打卡", "升旗", "观光巴士", "铛铛车", "漫游", "年卡", "月卡",
    "次卡", "平日卡", "周末卡", "贵宾卡", "双人", "2人", "三人", "3人", "多人",
    # v2.0.1新增：通玩卡/皮划艇等
    "通玩卡", "畅玩卡", "通卡", "皮划艇", "划船", "游艇",
    "漂流", "温泉", "滑雪", "演出", "实景", "精讲", "大咖", "讲师", "陪玩",
]

# ============================================================
# HTTP 请求
# ============================================================

def _post(url, data, timeout=15):
    """标准 urllib POST 请求"""
    body = json.dumps(data, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers=HEADERS, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result if result is not None else {}
    except urllib.error.URLError as e:
        return {"error": f"请求失败: {e}"}
    except Exception as e:
        return {"error": f"解析失败: {e}"}


def _parallel_fetch(tasks):
    """并发调用多个SCF，tasks = [(key, url, body), ...]"""
    results = {}

    def _fetch(key, url, body):
        results[key] = _post(url, body)

    threads = []
    for key, url, body in tasks:
        t = threading.Thread(target=_fetch, args=(key, url, body))
        t.start()
        threads.append(t)
    for t in threads:
        t.join(timeout=20)
    return results


# ============================================================
# 价格解析与图片清洗
# ============================================================

def _parse_price(price_str):
    if not price_str:
        return None
    cleaned = re.sub(r"[¥￥,，]", "", str(price_str))
    try:
        return float(cleaned)
    except (ValueError, TypeError):
        return None


def _clean_img_url(url):
    if not url:
        return ""
    return url.split("@")[0].strip()


def _get_price_level(price, category="", level=""):
    level_key = level if level in LEVEL_PRICE_REF else "无等级"
    low, mid, high = LEVEL_PRICE_REF[level_key]
    factor = 1.0
    for cat_key, cat_factor in CATEGORY_PRICE_FACTOR.items():
        if cat_key in category:
            factor = cat_factor
            break
    low *= factor
    mid *= factor
    high *= factor
    if price <= low:
        return "低价", "🟢"
    elif price <= mid:
        return "均价", "🟡"
    elif price <= high:
        return "偏高", "🟠"
    else:
        return "偏贵", "🔴"


def _is_peak_season():
    return datetime.now().month in PEAK_MONTHS


# ============================================================
# v2.0.1: POI名称匹配校验
# ============================================================

def _poi_name_match(poi_name, target_name):
    """poiName匹配校验：确保美团的景点和目标景点一致"""
    if not poi_name or not target_name:
        return False
    # 直接包含
    if target_name in poi_name or poi_name in target_name:
        return True
    # 去除常见后缀再比较
    for suffix in ["风景名胜区", "风景区", "景区", "度假区", "公园", "旅游区"]:
        poi_name = poi_name.replace(suffix, "")
        target_name = target_name.replace(suffix, "")
    if target_name in poi_name or poi_name in target_name:
        return True
    # 字符重叠度
    overlap = sum(1 for c in target_name if c in poi_name)
    min_len = min(len(target_name), len(poi_name))
    return overlap >= max(2, int(min_len * 0.5))


# ============================================================
# 飞猪数据提取
# ============================================================

def _parse_fliggy_result(data, name):
    if not data or "error" in data:
        return None
    items = data.get("data", {}).get("itemList", [])
    if not items:
        return None
    # 精确匹配优先
    match = None
    for item in items:
        iname = item.get("name", "")
        if name in iname or iname in name:
            match = item
            break
    if not match:
        match = items[0]

    ticket_info = match.get("ticketInfo") or {}
    return {
        "platform": "飞猪",
        "poi_name": match.get("name", ""),
        "price": _parse_price(ticket_info.get("price", "")),
        "ticket_name": ticket_info.get("ticketName", ""),
        "url": match.get("jumpUrl", ""),
        "image": _clean_img_url(match.get("mainPic", "")),
        "level": match.get("poiLevel", ""),
        "category": match.get("category", ""),
        "address": match.get("address", ""),
    }


# ============================================================
# 途牛数据提取
# ============================================================

def _parse_tuniu_result(data, name):
    if not data or "error" in data:
        return None
    tickets = data.get("data", {}).get("tickets", [])
    if not tickets:
        for suffix in ["度假区", "风景名胜区", "旅游景区", "风景区", "景区", "旅游区"]:
            if name.endswith(suffix):
                short = name[:-len(suffix)]
                data2 = _post(SCF_TUNIU_URL, {
                    "type": "tuniu_ticket_query",
                    "params": {"scenic_name": short}
                })
                if "error" not in data2:
                    tickets = data2.get("data", {}).get("tickets", [])
                    if tickets:
                        break
    if not tickets:
        return None

    # 找成人单票最低价
    adult_price = None
    for t in tickets:
        if t is None:
            continue
        pt = t.get("personTypeName", "")
        tt = t.get("ticketTypeName", "")
        p = _parse_price(t.get("startPrice", ""))
        if pt == "成人票" and tt in ("单票", "门票"):
            if adult_price is None or (p and p < adult_price):
                adult_price = p
        elif pt == "不限人群" and tt in ("单票", "门票"):
            if adult_price is None or (p and p < adult_price):
                adult_price = p
    # 没有纯成人票取最低价
    if adult_price is None:
        for t in tickets:
            if t is None:
                continue
            p = _parse_price(t.get("startPrice", ""))
            if p and (adult_price is None or p < adult_price):
                adult_price = p

    scenic_name = tickets[0].get("scenicName", "") if tickets[0] else ""
    product_id = str(tickets[0].get("productId", "")) if tickets[0] else ""
    tuniu_url = f"https://www.tuniu.com/tour/{product_id}" if product_id else ""

    # 交叉验证
    name_mismatch = False
    if scenic_name and name:
        overlap = sum(1 for c in name if c in scenic_name)
        if overlap < min(2, len(name)):
            name_mismatch = True

    # 全部票型
    all_tickets = []
    for t in tickets:
        if t is None:
            continue
        price = _parse_price(t.get("startPrice", ""))
        market_price = _parse_price(t.get("priceMarket", ""))
        discount = None
        if price and market_price and market_price > 0:
            discount = round(price / market_price * 10, 1)
        all_tickets.append({
            "name": t.get("resName", ""),
            "person_type": t.get("personTypeName", ""),
            "ticket_type": t.get("ticketTypeName", ""),
            "price": price,
            "market_price": market_price,
            "discount": discount,
            "enter_type": t.get("enterTypeName", ""),
            "satisfaction": t.get("satisfaction"),
            "remark_num": t.get("remarkNum", 0),
        })

    def _sort_key(x):
        pt_order = {"成人票": 0, "不限人群": 1, "儿童票": 2, "老人票": 3, "亲子家庭票": 4}.get(x.get("person_type", ""), 5)
        return (pt_order, x.get("price") or 9999)
    all_tickets.sort(key=_sort_key)

    return {
        "platform": "途牛",
        "scenic_name": scenic_name,
        "price": adult_price,
        "url": tuniu_url,
        "image": "",
        "name_mismatch": name_mismatch,
        "all_tickets": all_tickets,
    }


# ============================================================
# 美团CPS数据提取（v2.0.1: 三层过滤 + _poi_name_match校验）
# ============================================================

def _parse_meituan_search(data, name):
    """从美团CPS搜索结果中提取比价数据（v2.0.1三层过滤）"""
    if not data or "error" in data:
        return None
    products = data.get("data", {}).get("products", [])
    if not products:
        return None

    # 三层过滤找成人纯门票
    adult_product = None
    is_package = False

    # 第一层：含成人/全价/标准且不含排除词，且poiName匹配
    for p in products:
        pname = p.get("name", "")
        poi_name = p.get("poiName", "")
        # v2.0.1新增：校验poiName是否匹配目标景点
        if not _poi_name_match(poi_name, name):
            continue
        if any(kw in pname for kw in EXCLUDE_KEYWORDS):
            continue
        if any(kw in pname for kw in ["成人", "全价", "标准", "大通票", "通票"]):
            adult_product = p
            break

    # 第二层：不含排除词的第一个，且poiName匹配
    if not adult_product:
        for p in products:
            pname = p.get("name", "")
            poi_name = p.get("poiName", "")
            # v2.0.1新增：校验poiName是否匹配目标景点
            if not _poi_name_match(poi_name, name):
                continue
            if not any(kw in pname for kw in EXCLUDE_KEYWORDS):
                adult_product = p
                break

    # 第三层：兜底取第一个poiName匹配的
    if not adult_product:
        for p in products:
            poi_name = p.get("poiName", "")
            if _poi_name_match(poi_name, name):
                adult_product = p
                is_package = True
                break

    if not adult_product:
        return None

    sell_price = _parse_price(adult_product.get("sellPrice"))
    product_view_sign = adult_product.get("productViewSign", "")

    return {
        "platform": "美团",
        "product_name": adult_product.get("name", ""),
        "poi_name": adult_product.get("poiName", ""),
        "price": sell_price,
        "url": "",
        "image": _clean_img_url(adult_product.get("headUrl", "")),
        "product_view_sign": product_view_sign,
        "is_package": is_package,
    }


def _fetch_meituan_referral_link(product_view_sign):
    """获取美团CPS推广链接"""
    if not product_view_sign:
        return ""
    link_data = _post(SCF_MEITUAN_URL, {
        "type": "get_referral_link",
        "params": {
            "productViewSign": product_view_sign,
            "platform": 2,
            "bizLine": 4,
            "linkType": 1,
        }
    })
    if "error" not in link_data:
        rmap = link_data.get("referralLinkMap", {})
        return rmap.get("1", rmap.get("2", ""))
    return ""


# ============================================================
# 命令实现
# ============================================================

def cmd_search(city, keyword="", level="", category=""):
    """搜索景点"""
    search_key = keyword if keyword else "景点"
    data = _post(SCF_FLIGGY_URL, {
        "type": "search_poi",
        "params": {"keyword": search_key, "city": city}
    })

    if "error" in data:
        return {"success": False, "message": f"查询失败: {data.get('error')}", "attractions": []}

    items = data.get("data", {}).get("itemList", [])
    if items is None:
        items = []

    attractions = []
    for item in items:
        name = item.get("name", "")
        cat = item.get("category", "")
        poi_level = item.get("poiLevel", "")
        ticket_info = item.get("ticketInfo")
        free_status = item.get("freePoiStatus", "")
        jump_url = item.get("jumpUrl", "")
        address = item.get("address", "")
        desc = item.get("description", "")
        main_pic = _clean_img_url(item.get("mainPic", ""))

        if level and poi_level != level:
            continue
        if category and category not in cat:
            continue

        ticket_price = None
        ticket_name = ""
        if ticket_info:
            ticket_price = _parse_price(ticket_info.get("price", ""))
            ticket_name = ticket_info.get("ticketName", "")

        is_free = free_status == "FREE"
        price_display = "免费" if is_free else (f"¥{ticket_price:.0f}" if ticket_price else "待查询")

        attractions.append({
            "name": name,
            "category": cat,
            "level": f"{poi_level}A" if poi_level else "未评级",
            "ticket_price": ticket_price,
            "price_display": price_display,
            "ticket_name": ticket_name,
            "is_free": is_free,
            "jump_url": jump_url,
            "address": address,
            "image": main_pic,
            "description": desc[:100] + "..." if len(desc) > 100 else desc,
        })

    def _sort_key(x):
        is_free_order = 0 if x["is_free"] else 1
        price = x["ticket_price"] if x["ticket_price"] is not None else 99999
        return (is_free_order, price)
    attractions.sort(key=_sort_key)

    return {
        "success": True,
        "city": city,
        "keyword": keyword,
        "total": len(attractions),
        "attractions": attractions[:20],
    }


def cmd_compare(name, city):
    """三平台门票比价"""
    # 并发调用三平台
    results = _parallel_fetch([
        ("fliggy", SCF_FLIGGY_URL, {"type": "search_poi", "params": {"keyword": name, "city": city}}),
        ("tuniu", SCF_TUNIU_URL, {"type": "tuniu_ticket_query", "params": {"scenic_name": name}}),
        ("meituan", SCF_MEITUAN_URL, {"type": "query_coupon", "params": {"searchText": name, "platform": 2, "bizLine": 4}}),
    ])

    # 解析飞猪
    fliggy_raw = results.get("fliggy", {})
    fliggy = None
    if "error" not in fliggy_raw:
        items = fliggy_raw.get("data", {}).get("itemList", [])
        if items:
            fliggy = _parse_fliggy_result(fliggy_raw, name)

    # 解析途牛
    tuniu_raw = results.get("tuniu", {})
    tuniu = None
    if "error" not in tuniu_raw:
        tuniu = _parse_tuniu_result(tuniu_raw, name)

    # 解析美团搜索
    meituan_raw = results.get("meituan", {})
    meituan = _parse_meituan_search(meituan_raw, name)

    # 美团获取推广链接（需二次调用）
    if meituan and meituan.get("product_view_sign"):
        meituan["url"] = _fetch_meituan_referral_link(meituan["product_view_sign"])

    # 图片：优先飞猪mainPic（景区实景图），其次美团headUrl
    image = ""
    if fliggy and fliggy.get("image"):
        image = fliggy["image"]
    elif meituan and meituan.get("image"):
        image = meituan["image"]

    # 景点基础信息（取飞猪的）
    poi_level = fliggy.get("level", "") if fliggy else ""
    poi_category = fliggy.get("category", "") if fliggy else ""
    poi_address = fliggy.get("address", "") if fliggy else ""
    poi_name = fliggy.get("poi_name", name) if fliggy else name

    # 汇总比价
    comparison = []

    # 美团数据
    if meituan:
        meituan_note = ""
        pname = meituan.get("product_name", "")
        if meituan.get("is_package"):
            meituan_note = "仅提供套餐/讲解"
        elif any(kw in pname for kw in ["讲解", "导览", "跟团", "自由行", "一日游", "多日游"]):
            meituan_note = "仅提供套餐/讲解"
        comparison.append({
            "platform": "美团",
            "price": meituan.get("price"),
            "ticket_name": pname[:30],
            "url": meituan.get("url", ""),
            "note": meituan_note,
        })

    # 飞猪数据
    if fliggy:
        comparison.append({
            "platform": "飞猪",
            "price": fliggy.get("price"),
            "ticket_name": fliggy.get("ticket_name", ""),
            "url": fliggy.get("url", ""),
            "note": "",
        })

    # 途牛数据
    if tuniu:
        comparison.append({
            "platform": "途牛",
            "price": tuniu.get("price"),
            "ticket_name": "成人票",
            "url": tuniu.get("url", ""),
            "note": "⚠️匹配可能有误" if tuniu.get("name_mismatch") else "",
        })

    # 排序：有价格按价格升序，同价飞猪优先（有佣金）
    def _cmp_sort(x):
        p = x["price"] if x["price"] is not None else 99999
        platform_order = {"飞猪": 0, "美团": 1, "途牛": 2}.get(x["platform"], 3)
        return (p, platform_order)
    comparison.sort(key=_cmp_sort)

    # 最低价和可省
    all_prices = [c["price"] for c in comparison if c["price"] is not None]
    lowest_price = min(all_prices) if all_prices else None
    savings = max(all_prices) - min(all_prices) if len(all_prices) >= 2 else None

    # 途牛全部票型
    tuniu_all_tickets = tuniu.get("all_tickets", []) if tuniu else []

    # 价格水平
    price_level = ""
    price_emoji = ""
    if lowest_price is not None:
        level_str = poi_level if poi_level in LEVEL_PRICE_REF else "无等级"
        price_level, price_emoji = _get_price_level(lowest_price, poi_category, level_str)

    return {
        "success": True,
        "attraction": name,
        "city": city,
        "poi_name": poi_name,
        "level": f"{poi_level}A" if poi_level else "未评级",
        "category": poi_category,
        "address": poi_address,
        "image": image,
        "comparison": comparison,
        "lowest_price": lowest_price,
        "savings": savings,
        "price_level": price_level,
        "price_emoji": price_emoji,
        "tuniu_tickets": tuniu_all_tickets[:30],
        "tuniu_total": len(tuniu_all_tickets),
    }


def cmd_advisor(name, city, ticket_type="成人票"):
    """购票决策建议"""
    compare_result = cmd_compare(name, city)

    if not compare_result["success"]:
        return compare_result

    lowest_price = compare_result.get("lowest_price")
    level = compare_result.get("level", "").replace("A", "")
    category = compare_result.get("category", "")
    tuniu_tickets = compare_result.get("tuniu_tickets", [])
    comparison = compare_result.get("comparison", [])
    savings = compare_result.get("savings")

    # 5维决策分析
    dimensions = {}

    # 维度1：价格水平
    if lowest_price is not None:
        price_level, price_emoji = _get_price_level(lowest_price, category, level)
        dimensions["price_level"] = {
            "label": "价格水平",
            "value": f"{price_emoji} {price_level}",
            "detail": f"当前最低价 ¥{lowest_price:.0f}",
        }
    else:
        dimensions["price_level"] = {"label": "价格水平", "value": "⚪ 无价格数据", "detail": "暂无实时报价"}

    # 维度2：平台价差
    if savings is not None and savings > 0:
        dimensions["platform_diff"] = {
            "label": "平台价差",
            "value": f"💰 可省 ¥{savings:.0f}",
            "detail": f"平台间差价 ¥{savings:.0f}，选最低价平台",
        }
    elif len(comparison) >= 2:
        dimensions["platform_diff"] = {"label": "平台价差", "value": "🟰 各平台同价", "detail": "各平台价格一致，任选即可"}
    else:
        dimensions["platform_diff"] = {"label": "平台价差", "value": "⚪ 仅单一平台", "detail": "只有一个平台报价"}

    # 维度3：折扣力度（先占位）
    dimensions["discount"] = {"label": "折扣力度", "value": "⚪ 无明显折扣", "detail": "当前无特殊优惠"}

    # 维度4：满意度
    avg_satisfaction = None
    max_remarks = 0
    for t in tuniu_tickets:
        s = t.get("satisfaction")
        r = t.get("remark_num", 0)
        if s is not None:
            if avg_satisfaction is None:
                avg_satisfaction = s
            else:
                avg_satisfaction = (avg_satisfaction + s) / 2
            max_remarks = max(max_remarks, r)

    if avg_satisfaction is not None:
        if avg_satisfaction >= 95:
            sat_label = "🌟 极高"
        elif avg_satisfaction >= 90:
            sat_label = "👍 较高"
        elif avg_satisfaction >= 80:
            sat_label = "👌 一般"
        else:
            sat_label = "⚠️ 偏低"
        dimensions["satisfaction"] = {
            "label": "游客满意度",
            "value": f"{sat_label} {avg_satisfaction:.0f}%",
            "detail": f"评价数 {max_remarks}",
        }
    else:
        dimensions["satisfaction"] = {"label": "游客满意度", "value": "⚪ 暂无数据", "detail": "无满意度评价"}

    # 维度5：季节建议
    peak = _is_peak_season()
    if peak:
        dimensions["season"] = {"label": "季节因素", "value": "旺季 🔥", "detail": "旅游旺季，建议提前购票，现场可能限流"}
    else:
        dimensions["season"] = {"label": "季节因素", "value": "淡季 ✅", "detail": "旅游淡季，票价稳定，入园压力小"}

    # 筛选指定票型
    if ticket_type == "成人票":
        matched_tickets = [t for t in tuniu_tickets if "成人" in t.get("person_type", "")]
        if not matched_tickets:
            matched_tickets = [t for t in tuniu_tickets if "不限" in t.get("person_type", "")]
    elif ticket_type:
        matched_tickets = [t for t in tuniu_tickets
                           if ticket_type in t.get("person_type", "") or ticket_type in t.get("name", "")]
    else:
        matched_tickets = tuniu_tickets
    if not matched_tickets:
        matched_tickets = tuniu_tickets[:5]

    # 更新折扣维度
    adult_discounts = [t for t in matched_tickets
                       if ("成人" in t.get("person_type", "") or "不限" in t.get("person_type", ""))
                       and t.get("discount") is not None and t.get("discount", 10) < 10]
    if adult_discounts:
        best_discount = min(t["discount"] for t in adult_discounts)
        best_name = [t["name"] for t in adult_discounts if t["discount"] == best_discount][0]
        dimensions["discount"] = {"label": "折扣力度", "value": f"🏷️ {best_discount}折", "detail": f"「{best_name}」折扣最优"}
    elif any(t.get("discount") is not None and t.get("discount", 10) < 10 for t in tuniu_tickets):
        other_discounts = [t["discount"] for t in tuniu_tickets if t.get("discount") is not None and t.get("discount", 10) < 10]
        if other_discounts:
            best_other = min(other_discounts)
            dimensions["discount"] = {"label": "折扣力度", "value": f"🏷️ {best_other}折(儿童/老人)", "detail": "成人票无折扣，儿童/老人票有优惠"}

    # 综合决策
    signal = "🟢 建议购买"
    reason_parts = []

    if lowest_price is not None:
        price_level_val, _ = _get_price_level(lowest_price, category, level)
        if price_level_val == "低价":
            signal = "🟢 建议购买"
            reason_parts.append("价格处于低位")
        elif price_level_val == "均价":
            signal = "🟡 价格适中"
            reason_parts.append("价格处于正常水平")
        elif price_level_val == "偏高":
            signal = "🟠 建议观望"
            reason_parts.append("价格偏高，可关注优惠")
        else:
            signal = "🔴 暂不建议"
            reason_parts.append("价格偏贵，建议等优惠或选替代景点")

    if savings and savings > 20:
        reason_parts.append(f"平台间可省¥{savings:.0f}")

    if peak:
        reason_parts.append("旺季建议提前购票")

    reason = "；".join(reason_parts) if reason_parts else "建议按需购买"

    return {
        "success": True,
        "attraction": name,
        "city": city,
        "level": compare_result.get("level", ""),
        "signal": signal,
        "reason": reason,
        "dimensions": dimensions,
        "recommended_tickets": matched_tickets[:5],
        "lowest_price": lowest_price,
        "best_platform": comparison[0]["platform"] if comparison else "",
        "best_url": comparison[0].get("url", "") if comparison else "",
    }


# ============================================================
# CLI 入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="景点门票比价 v2.0.1 - 美团+飞猪+途牛三平台比价")
    parser.add_argument("--city", required=True, help="城市名，如：北京、上海")
    parser.add_argument("--keyword", default="", help="搜索关键词，如：故宫、迪士尼")
    parser.add_argument("--level", default="", help="景区等级，5A/4A/3A")
    parser.add_argument("--category", default="", help="景点类型，如：博物馆、主题乐园")
    parser.add_argument("--name", default="", help="景点名称（用于比价模式），如：故宫博物院")
    parser.add_argument("--advisor", action="store_true", help="输出购票决策建议（需配合--name使用）")
    parser.add_argument("--ticket-type", default="成人票", help="票型筛选（advisor模式），默认成人票")

    args = parser.parse_args()

    if args.name:
        # 比价模式
        if args.advisor:
            result = cmd_advisor(args.name, args.city, args.ticket_type)
        else:
            result = cmd_compare(args.name, args.city)
    else:
        # 搜索模式
        result = cmd_search(args.city, args.keyword, args.level, args.category)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
