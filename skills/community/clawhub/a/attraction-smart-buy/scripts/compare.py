#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
景点门票比价 v2.0.3 - 美团+途牛双平台景点门票比价 + 购票决策建议
通过SCF代理查询美团CPS//途牛实时景点门票价格
v2.0.3: 输入预处理、严格匹配、途牛过滤、多票型引导、重试机制

用法:
  python3 compare.py --city "北京" [--keyword "故宫"] [--level 5A] [--category 博物馆]
  python3 compare.py --city "北京" --name "故宫博物院"
  python3 compare.py --city "北京" --name "故宫博物院" --advisor
"""

import os
import argparse
import json
import re
import sys
import threading
import time
import urllib.request
import urllib.error
from datetime import datetime

# ============================================================
# 配置
# ============================================================

PROXY_TOKEN = os.environ.get("PROXY_TOKEN", "")
SCF_TUNIU_URL = "https://1439498936-0junm3maxj.ap-guangzhou.tencentscf.com"
SCF_MEITUAN_URL = "https://1439498936-cltb2hszg7.ap-guangzhou.tencentscf.com"

HEADERS = {
    "Content-Type": "application/json",
    "X-Proxy-Token": PROXY_TOKEN,
}

MAX_RETRIES = 2
RETRY_DELAY = 1.0

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
# v2.0.3: 移入_parse_meituan_search作为局部变量
EXCLUDE_KEYWORDS = [
    "讲解", "导览", "精讲", "大咖", "讲师", "陪玩", "夜游", "日游", "亲子",
    "家庭", "套票", "跟团", "一日游", "半日游", "多日游", "接送", "包车",
    "直通车", "大巴", "自驾", "自由行", "酒店", "小团", "纯玩团", "晚·", "天晚",
    "套餐", "摄影", "旅拍", "跟拍", "直通车", "接驳", "摆渡", "游船", "门票+",
    "+门票", "+导览", "+精讲", "3h", "3小时", "2h", "2小时", "打卡", "升旗",
    "观光巴士", "铛铛车", "漫游", "小团", "年卡", "月卡", "次卡", "平日卡",
    "周末卡", "贵宾卡", "双人", "2人", "三人", "3人", "多人",
    "通玩卡", "畅玩卡", "通卡", "皮划艇", "划船", "游艇", "漂流", "温泉",
    "滑雪", "演出", "实景",
]

# 途牛票项排除关键词
_TUNIU_EXCLUDE_KEYWORDS = [
    "直通车", "接驳", "摆渡", "观光车", "游船", "游艇", "牧场", "农庄", "农场",
    "温泉", "演出", "足道", "康养", "spa", "SPA", "按摩", "理疗", "沙滩泳场",
    "森林温泉", "游泳", "漂流", "露营", "帐篷", "烧烤", "野餐", "研学",
    "太阳岛", "蓝挚", "爱喵屋", "泰生", "夜游", "夜航", "江翠", "入岛", "离岛",
    "环岛", "套餐",
]

# ============================================================
# HTTP 请求（v2.0.3: 带重试机制）
# ============================================================

def _post(url, data, timeout=15):
    """标准 urllib POST 请求，支持自动重试"""
    body = json.dumps(data, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers=HEADERS, method="POST")
    last_error = None
    for attempt in range(MAX_RETRIES + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                return result if result is not None else {}
        except Exception as e:
            last_error = e
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY * (attempt + 1))
    return {"error": f"请求失败(重试{MAX_RETRIES}次): {last_error}"}


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
        t.join(timeout=25)
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
# v2.0.3: 输入预处理 & 名称匹配
# ============================================================

def _preprocess_input_name(name, city):
    """去掉city前缀和噪音词"""
    clean = name.strip()
    if city and clean.startswith(city):
        clean = clean[len(city):]
    noise_words = ["那个", "附近的", "那里的", "里面的", "旁边的"]
    for w in noise_words:
        clean = clean.replace(w, "")
    if clean.startswith("的"):
        clean = clean[1:]
    return clean.strip()


def _is_in_city(address, city):
    """校验地址是否在指定城市"""
    if not address:
        return False
    city_clean = city.replace("市", "").replace("省", "").replace("县", "").replace("区", "")
    addr_clean = address.replace("省", "").replace("市", "").replace("区", "").replace("县", "")
    return city_clean in addr_clean or city_clean in address


def _name_match(api_name, user_name):
    """名称匹配校验（v2.0.3改进版：更完善的后缀去除逻辑）"""
    if not api_name or not user_name:
        return False
    a = api_name.strip()
    b = user_name.strip()
    # 完全相等
    if a == b:
        return True
    # 直接包含
    if b in a or a in b:
        return True
    # 去除常见后缀再比较
    suffixes = ["风景名胜区", "风景区", "景区", "度假区", "公园", "旅游区", "博物苑", "博物馆", "纪念馆"]
    a_s, b_s = a, b
    for sf in suffixes:
        a_s = a_s.replace(sf, "")
        b_s = b_s.replace(sf, "")
    if a_s and b_s and (b_s in a_s or a_s in b_s):
        return True
    return False


# ============================================================
# v2.0.3: 途牛票项过滤 & 景区匹配
# ============================================================

def _tuniu_is_valid_ticket(res_name, scenic_name, target_name):
    """途牛票项过滤：排除非门票类票项"""
    name_lower = res_name.lower()
    for kw in _TUNIU_EXCLUDE_KEYWORDS:
        if kw.lower() in name_lower:
            return False
    if scenic_name and target_name:
        overlap = sum(1 for c in target_name if c in scenic_name)
        if overlap < min(2, len(target_name)):
            return False
    return True


def _tuniu_scenic_match(scenic_name, target_name):
    """途牛景区名称匹配校验"""
    if not scenic_name or not target_name:
        return False
    if target_name in scenic_name or scenic_name in target_name:
        return True
    overlap = sum(1 for c in target_name if c in scenic_name)
    min_len = min(len(target_name), len(scenic_name))
    required = max(3, int(min_len * 0.5))
    return overlap >= required


# ============================================================
# 数据提取（v2.0.3: 使用_name_match，无匹配返回None）
# ============================================================


def _parse_tuniu_result(data, name):
    if not data or "error" in data:
        return None
    tickets = data.get("data", {}).get("tickets", [])
    if tickets is None:
        tickets = []
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

    scenic_name = tickets[0].get("scenicName", "") if tickets and tickets[0] else ""
    # v2.0.3: scenic_name匹配校验
    if not _tuniu_scenic_match(scenic_name, name):
        return None

    # 找成人单票最低价（v2.0.3: 增加票项过滤）
    adult_price = None
    for t in tickets:
        if t is None:
            continue
        if not _tuniu_is_valid_ticket(t.get("resName", ""), scenic_name, name):
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
            if not _tuniu_is_valid_ticket(t.get("resName", ""), scenic_name, name):
                continue
            p = _parse_price(t.get("startPrice", ""))
            if p and (adult_price is None or p < adult_price):
                adult_price = p

    product_id = str(tickets[0].get("productId", "")) if tickets[0] else ""
    tuniu_url = f"https://m.tuniu.com/tour/{product_id}" if product_id else ""

    # 交叉验证
    name_mismatch = False
    if scenic_name and name:
        overlap = sum(1 for c in name if c in scenic_name)
        if overlap < min(2, len(name)):
            name_mismatch = True

    # v2.0.3: 全部票型（含discount、satisfaction等字段）
    all_tickets = []
    for t in tickets:
        if t is None:
            continue
        if not _tuniu_is_valid_ticket(t.get("resName", ""), scenic_name, name):
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
            "loss_name": t.get("lossName", ""),
        })

    # v2.0.3: 去重排序
    seen = set()
    unique_tickets = []
    for t in all_tickets:
        key = (t.get("name", ""), t.get("price"))
        if key not in seen:
            seen.add(key)
            unique_tickets.append(t)
    all_tickets = unique_tickets

    def _sort_key(x):
        pt_order = {"成人票": 0, "不限人群": 1, "儿童票": 2, "老人票": 3, "亲子家庭票": 4}.get(x.get("person_type", ""), 5)
        return (pt_order, x.get("price") or 9999)
    all_tickets.sort(key=_sort_key)

    return {
        "platform": "途牛",
        "scenic_name": scenic_name,
        "price": adult_price,
        "url": tuniu_url,
        "name_mismatch": name_mismatch,
        "all_tickets": all_tickets,
    }


# ============================================================
# 美团CPS数据提取（v2.0.3: 局部匹配+排除词+改进搜索逻辑）
# ============================================================

def _parse_meituan_search(data, name):
    """从美团CPS搜索结果中提取比价数据（v2.0.3改进搜索逻辑）"""
    if not data or "error" in data:
        return None
    products = data.get("data", {}).get("products", [])
    if not products:
        return None

    # v2.0.3: 局部排除关键词
    EXCLUDE_KW = [
        "讲解", "导览", "精讲", "大咖", "讲师", "陪玩", "夜游", "日游", "亲子",
        "家庭", "套票", "跟团", "一日游", "半日游", "多日游", "接送", "包车",
        "直通车", "大巴", "自驾", "自由行", "酒店", "小团", "纯玩团", "晚·", "天晚",
        "套餐", "摄影", "旅拍", "跟拍", "直通车", "接驳", "摆渡", "游船", "门票+",
        "+门票", "+导览", "+精讲", "3h", "3小时", "2h", "2小时", "打卡", "升旗",
        "观光巴士", "铛铛车", "漫游", "小团", "年卡", "月卡", "次卡", "平日卡",
        "周末卡", "贵宾卡", "双人", "2人", "三人", "3人", "多人",
        "通玩卡", "畅玩卡", "通卡", "皮划艇", "划船", "游艇", "漂流", "温泉",
        "滑雪", "演出", "实景",
    ]

    # v2.0.3: 局部名称匹配（逻辑同_name_match）
    def _poi_name_match(poi_name, target_name):
        if not poi_name or not target_name:
            return False
        if target_name in poi_name or poi_name in target_name:
            return True
        for suffix in ["风景名胜区", "风景区", "景区", "度假区", "公园", "旅游区"]:
            poi_name = poi_name.replace(suffix, "")
            target_name = target_name.replace(suffix, "")
        if target_name in poi_name or poi_name in target_name:
            return True
        overlap = sum(1 for c in target_name if c in poi_name)
        min_len = min(len(target_name), len(poi_name))
        return overlap >= max(2, int(min_len * 0.5))

    # v2.0.3: 优先成人票关键词匹配
    adult_product = None
    is_package = False
    for p in products:
        pname = p.get("name", "")
        poi_name = p.get("poiName", "")
        if not _poi_name_match(poi_name, name):
            continue
        skip = any(kw in pname for kw in EXCLUDE_KW)
        if skip:
            continue
        if pname.count("+") >= 2:
            continue
        if any(kw in pname for kw in ["成人", "全价", "标准", "通票", "大通票"]):
            adult_product = p
            break

    # v2.0.3: fallback
    if not adult_product:
        for p in products:
            pname = p.get("name", "")
            poi_name = p.get("poiName", "")
            if not _poi_name_match(poi_name, name):
                continue
            if not any(kw in pname for kw in EXCLUDE_KW):
                if pname.count("+") >= 2:
                    continue
                adult_product = p
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
# v2.0.3: 多票型引导提示
# ============================================================

def _build_ticket_tips(tuniu):
    """根据途牛多票型数据生成引导提示。
    因美团接口数据限制，仅途牛可返回多票型信息。
    """
    if not tuniu:
        return ""
    all_tickets = tuniu.get("all_tickets", [])
    if not all_tickets:
        return ""
    # 提取非成人票的其他票型
    other_tickets = []
    for t in all_tickets:
        pt = t.get("person_type", "")
        if pt and pt not in ("成人票", "不限人群") and t.get("price"):
            other_tickets.append(t)
    if not other_tickets:
        return ""
    # 构建票型摘要（最多取3个）
    parts = []
    for t in other_tickets[:3]:
        pt = t["person_type"]
        price = t["price"]
        parts.append(f"{pt}¥{int(price)}")
    ticket_summary = "、".join(parts)
    return f"💡 途牛另有{ticket_summary}等多种票型可选。美团未返回多票型数据，如需更多票型建议前往对应APP查看。"


# ============================================================
# 命令实现
# ============================================================

def cmd_search(city, keyword="", level="", category=""):
    """搜索景点（美团数据源）"""
    search_key = keyword if keyword else city + "景点"
    data = _post(SCF_MEITUAN_URL, {
        "type": "query_coupon",
        "params": {"searchText": search_key, "platform": 2, "bizLine": 4}
    })

    if "error" in data:
        return {"success": False, "message": f"查询失败: {data.get('error')}", "attractions": []}

    products = data.get("data", {}).get("products", [])
    if not products:
        return {"success": True, "city": city, "keyword": keyword, "total": 0, "attractions": []}

    # 去重：按 poiName 聚合
    seen_pois = {}
    for p in products:
        poi_name = p.get("poiName", "")
        if not poi_name:
            continue
        if poi_name not in seen_pois:
            seen_pois[poi_name] = p

    attractions = []
    for poi_name, item in seen_pois.items():
        cat = item.get("category", "")
        address = item.get("address", "")

        if level and level not in item.get("poiLevel", ""):
            continue
        if category and category not in cat:
            continue

        ticket_price = _parse_price(item.get("sellPrice"))
        price_display = f"¥{ticket_price:.0f}" if ticket_price else "待查询"
        image = _clean_img_url(item.get("headUrl", ""))

        attractions.append({
            "name": poi_name,
            "category": cat,
            "level": item.get("poiLevel", "未评级"),
            "ticket_price": ticket_price,
            "price_display": price_display,
            "ticket_name": item.get("name", ""),
            "is_free": False,
            "jump_url": "",
            "address": address,
            "image": image,
            "description": "",
        })

    def _sort_key(x):
        price = x["ticket_price"] if x["ticket_price"] is not None else 99999
        return price
    attractions.sort(key=_sort_key)

    return {
        "success": True,
        "city": city,
        "keyword": keyword,
        "total": len(attractions),
        "attractions": attractions[:20],
    }


def cmd_compare(name, city):
    """双平台门票比价"""
    # v2.0.3: 输入预处理
    clean_name = _preprocess_input_name(name, city)

    # 并发调用双平台
    results = _parallel_fetch([
        ("tuniu", SCF_TUNIU_URL, {"type": "tuniu_ticket_query", "params": {"scenic_name": name}}),
        ("meituan", SCF_MEITUAN_URL, {"type": "query_coupon", "params": {"searchText": name, "platform": 2, "bizLine": 4}}),
    ])

    # 解析途牛（v2.0.3: 使用clean_name）
    tuniu_raw = results.get("tuniu", {})
    tuniu = None
    if "error" not in tuniu_raw:
        tuniu = _parse_tuniu_result(tuniu_raw, clean_name)

    # 解析美团搜索（v2.0.3: 使用clean_name）
    meituan_raw = results.get("meituan", {})
    meituan = _parse_meituan_search(meituan_raw, clean_name)

    # 美团获取推广链接（需二次调用）
    if meituan and meituan.get("product_view_sign"):
        meituan["url"] = _fetch_meituan_referral_link(meituan["product_view_sign"])

    # 图片：优先美团图片，其次途牛图片
    image = ""
    if meituan and meituan.get("image"):
        image = meituan["image"]
    elif tuniu and tuniu.get("image"):
        image = tuniu.get("image", "")

    # 景点基础信息（取自途牛和美团）
    poi_level = tuniu.get("level", "") if tuniu else ""
    poi_category = tuniu.get("category", "") if tuniu else ""
    poi_address = tuniu.get("address", "") if tuniu else ""
    # v2.0.3: poi_name回退优先级：美团 > 途牛 > clean_name
    poi_name = ""
    if meituan:
        poi_name = meituan.get("poi_name", "")
    if not poi_name and tuniu:
        poi_name = tuniu.get("scenic_name", "")
    if not poi_name:
        poi_name = clean_name

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

    # 途牛数据
    if tuniu:
        comparison.append({
            "platform": "途牛",
            "price": tuniu.get("price"),
            "ticket_name": "成人票",
            "url": tuniu.get("url", ""),
            "note": "⚠️匹配可能有误" if tuniu.get("name_mismatch") else "",
        })

    # 排序：有价格按价格升序，同价优先（有佣金）
    def _cmp_sort(x):
        p = x["price"] if x["price"] is not None else 99999
        platform_order = {"美团": 0, "途牛": 1}.get(x["platform"], 2)
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

    # v2.0.3: 多票型引导提示
    ticket_tips = _build_ticket_tips(tuniu)

    # v2.0.3: 未匹配平台列表
    no_match_platforms = []
    if not meituan:
        no_match_platforms.append("美团")
    if not tuniu:
        no_match_platforms.append("途牛")

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
        "ticket_tips": ticket_tips,
        "no_match_platforms": no_match_platforms,
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
    parser = argparse.ArgumentParser(description="景点门票比价 v2.0.3 - 美团+途牛双平台比价")
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
