#!/usr/bin/env python3
"""
景点门票比价：美团+飞猪+途牛三平台景点门票比价 + 购票决策建议
通过SCF代理查询美团CPS/飞猪/途牛实时景点门票价格

用法:
  python3 compare.py search --city "北京" [--keyword "故宫"] [--level 5A] [--category 博物馆]
  python3 compare.py compare --name "故宫博物院" --city "北京"

"""

import os
import argparse
import json
import re
import sys
import threading
import urllib.request
import urllib.error


# ============================================================
# 配置
# ============================================================

PROXY_TOKEN = os.environ.get("PROXY_TOKEN", "")

SCF_FLIGGY_URL = "https://1439498936-6sysdjjt99.ap-guangzhou.tencentscf.com"
SCF_TUNIU_URL = "https://1439498936-0junm3maxj.ap-guangzhou.tencentscf.com"
SCF_MEITUAN_URL = "https://1439498936-cltb2hszg7.ap-guangzhou.tencentscf.com"

HEADERS = {
    "Content-Type": "application/json",
    "X-Proxy-Token": PROXY_TOKEN,
}

# 美团CPS排除关键词（非门票商品）
MEITUAN_EXCLUDE_KEYWORDS = [
    "讲解", "导览", "精讲", "大咖", "讲师", "陪玩",
    "夜游", "日游", "亲子", "家庭", "套票", "跟团",
    "一日游", "半日游", "多日游", "接送", "包车", "直通车",
    "大巴", "自驾", "自由行", "酒店", "小团", "纯玩团",
    "晚·", "天晚", "套餐", "摄影", "旅拍", "跟拍",
    "接驳", "摆渡", "游船",
    "门票+", "+门票", "+导览", "+精讲",
    "3h", "3小时", "2h", "2小时",
    "打卡", "升旗", "观光巴士", "铛铛车", "漫游",
    "年卡", "月卡", "次卡", "平日卡", "周末卡", "贵宾卡",
    "双人", "2人", "三人", "3人", "多人",
    "通玩卡", "畅玩卡", "通卡", "皮划艇", "划船", "游艇",
    "漂流", "温泉", "滑雪", "演出", "实景",
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


# ============================================================
# 飞猪数据提取
# ============================================================

def _parse_fliggy_result(data, name):
    if not data or "error" in data:
        return None
    items = data.get("data", {}).get("itemList", [])
    if not items:
        return None
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
            "loss_name": t.get("lossName", ""),
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
# 美团CPS数据提取
# ============================================================

def _parse_meituan_search(data, name):
    if not data or "error" in data:
        return None
    products = data.get("data", {}).get("products", [])
    if not products:
        return None

    # poiName 匹配校验：确保美团的景点和目标景点一致
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

    adult_product = None
    is_package = False
    for p in products:
        pname = p.get("name", "")
        poi_name = p.get("poiName", "")
        if not _poi_name_match(poi_name, name):
            continue
        if any(kw in pname for kw in MEITUAN_EXCLUDE_KEYWORDS):
            continue
        if pname.count("+") >= 2:
            continue
        if any(kw in pname for kw in ["成人", "全价", "标准", "通票", "大通票"]):
            adult_product = p
            break
    if not adult_product:
        for p in products:
            pname = p.get("name", "")
            poi_name = p.get("poiName", "")
            if not _poi_name_match(poi_name, name):
                continue
            if not any(kw in pname for kw in MEITUAN_EXCLUDE_KEYWORDS):
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

    fliggy = _parse_fliggy_result(results.get("fliggy"), name)
    tuniu = _parse_tuniu_result(results.get("tuniu"), name)
    meituan = _parse_meituan_search(results.get("meituan"), name)

    # 美团获取推广链接
    if meituan and meituan.get("product_view_sign"):
        link_data = _post(SCF_MEITUAN_URL, {
            "type": "get_referral_link",
            "params": {
                "productViewSign": meituan["product_view_sign"],
                "platform": 2,
                "bizLine": 4,
                "linkType": 1,
            }
        })
        if "error" not in link_data:
            rmap = link_data.get("referralLinkMap", {})
            meituan["url"] = rmap.get("1", rmap.get("2", ""))

    # 图片：优先飞猪mainPic，美团备选
    image = ""
    if fliggy and fliggy.get("image"):
        image = fliggy["image"]
    elif meituan and meituan.get("image"):
        image = meituan["image"]

    # 景点基础信息
    poi_level = fliggy.get("level", "") if fliggy else ""
    poi_category = fliggy.get("category", "") if fliggy else ""
    poi_address = fliggy.get("address", "") if fliggy else ""
    poi_name = fliggy.get("poi_name", name) if fliggy else name

    # 汇总比价
    comparison = []
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
    if fliggy:
        comparison.append({
            "platform": "飞猪",
            "price": fliggy.get("price"),
            "ticket_name": fliggy.get("ticket_name", ""),
            "url": fliggy.get("url", ""),
            "note": "",
        })
    if tuniu:
        comparison.append({
            "platform": "途牛",
            "price": tuniu.get("price"),
            "ticket_name": "成人票",
            "url": tuniu.get("url", ""),
            "note": "⚠️ 匹配可能有误" if tuniu.get("name_mismatch") else "",
        })

    # 排序：价格升序，同价飞猪优先
    def _cmp_sort(x):
        p = x["price"] if x["price"] is not None else 99999
        platform_order = {"飞猪": 0, "美团": 1, "途牛": 2}.get(x["platform"], 3)
        return (p, platform_order)
    comparison.sort(key=_cmp_sort)

    all_prices = [c["price"] for c in comparison if c["price"] is not None]
    lowest_price = min(all_prices) if all_prices else None
    savings = max(all_prices) - min(all_prices) if len(all_prices) >= 2 else None

    tuniu_tickets = tuniu.get("all_tickets", []) if tuniu else []

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
        "tuniu_tickets": tuniu_tickets,
    }



# ============================================================
# CLI 入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="景点门票比价")
    subparsers = parser.add_subparsers(dest="command")

    # search
    p_search = subparsers.add_parser("search", help="搜索景点")
    p_search.add_argument("--city", required=True, help="城市")
    p_search.add_argument("--keyword", default="", help="关键词")
    p_search.add_argument("--level", default="", help="景区等级(5A/4A/3A)")
    p_search.add_argument("--category", default="", help="景点类型")

    # compare
    p_compare = subparsers.add_parser("compare", help="门票三平台比价")
    p_compare.add_argument("--name", required=True, help="景点名称")
    p_compare.add_argument("--city", required=True, help="城市")

    args = parser.parse_args()

    if args.command == "search":
        result = cmd_search(args.city, args.keyword, args.level, args.category)
    elif args.command == "compare":
        result = cmd_compare(args.name, args.city)
    else:
        parser.print_help()
        return

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
