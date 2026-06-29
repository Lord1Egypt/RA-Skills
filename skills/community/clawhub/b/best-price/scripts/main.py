#!/usr/bin/env python3
"""购物比价助手 - 京东/淘宝/拼多多跨平台比价"""

import sys
import json
import re
import urllib.request
import urllib.parse
import urllib.error

PROXIES = {
    "jd": {
        "url": "https://1439498936-9n7zsjnaif.ap-guangzhou.tencentscf.com",
        "token": "tp_8k2mX9vQ4z",
    },
    "taobao": {
        "url": "https://1439498936-lofjio3yzf.ap-guangzhou.tencentscf.com",
        "token": "tp_8k2mX9vQ4z",
    },
    "pdd": {
        "url": "https://1439498936-1iog1h3lb1.ap-guangzhou.tencentscf.com",
        "token": "tp_8k2mX9vQ4z",
    },
}

KNOWN_BRANDS = {
    "apple", "iphone", "ipad", "macbook", "airpods", "imac",
    "samsung", "galaxy", "huawei", "xiaomi", "redmi", "oppo", "vivo",
    "sony", "dell", "lenovo", "hp", "asus", "acer",
    "nike", "adidas", "puma", "lining", "anta",
    "dyson", "philips", "panasonic", "midea", "haier", "gree",
    "louis vuitton", "gucci", "chanel", "prada", "dior",
    "l'oreal", "estee lauder", "shiseido", "sk-ii", "la mer",
    "honda", "toyota", "byd", "tesla", "bmw", "benz", "audi",
    "ysl", "tom ford", "givenchy", "armani", "burberry",
    "logitech", "razer", "corsair", "steelseries",
    "canon", "nikon", "fuji", "boe", "hisense", "tcl", "skyworth",
}


def _scf_call(proxy_key, req_type, params):
    """Call a SCF proxy and return the parsed JSON response."""
    proxy = PROXIES[proxy_key]
    payload = json.dumps({"type": req_type, "params": params}).encode("utf-8")
    req = urllib.request.Request(
        proxy["url"], data=payload,
        headers={"Content-Type": "application/json", "X-Proxy-Token": proxy["token"]},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"ok": False, "error": str(e)}


def _extract_items(data):
    if not isinstance(data, dict):
        return []
    if not data.get("ok"):
        return []
    items = data.get("data", [])
    if isinstance(items, list):
        return items
    if isinstance(items, dict):
        for key in ("result", "items", "list"):
            val = items.get(key, [])
            if isinstance(val, list):
                return val
    return []


def _follow_redirect(url, max_hops=5):
    for _ in range(max_hops):
        try:
            req = urllib.request.Request(url, method="GET")
            req.add_header("User-Agent", "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)")
            resp = urllib.request.urlopen(req, timeout=10)
            final = resp.url
            if final == url:
                break
            url = final
        except urllib.error.HTTPError as e:
            location = e.headers.get("Location")
            if location:
                url = location
            else:
                break
        except Exception:
            break
    return url


def _is_category_word(query):
    q = query.strip().lower()
    if len(q) >= 4:
        return False
    if re.search(r"\d", q):
        return False
    for brand in KNOWN_BRANDS:
        if brand in q:
            return False
    return True


def _parse_jd_url(query):
    m = re.search(r"item\.jd\.com/(\d+)", query)
    if m:
        return m.group(1)
    m = re.search(r"item\.m\.jd\.com/product/(\d+)", query)
    if m:
        return m.group(1)
    return None


def _parse_taobao_url(query):
    if not ("m.tb.cn" in query or "taobao.com" in query or "tb.cn" in query):
        return None
    final_url = _follow_redirect(query)
    parsed = urllib.parse.urlparse(final_url)
    qs = urllib.parse.parse_qs(parsed.query)
    if "id" in qs:
        return qs["id"][0]
    m = re.search(r"/i(\d{8,})", parsed.path)
    if m:
        return m.group(1)
    m = re.search(r"item-(\d+)", parsed.path)
    if m:
        return m.group(1)
    return None


def _parse_pdd_url(query):
    if not ("p.pinduoduo.com" in query or "yangkeduo.com" in query):
        return None
    final_url = _follow_redirect(query)
    parsed = urllib.parse.urlparse(final_url)
    qs = urllib.parse.parse_qs(parsed.query)
    if "goods_sign" in qs:
        return qs["goods_sign"][0]
    return None


def _search_jd(keyword, sku_id=None):
    search_kw = sku_id if sku_id else keyword
    data = _scf_call("jd", "goods_query", {
        "keyword": search_kw, "pageIndex": 1, "pageSize": 20, "isSelf": True,
    })
    items_raw = _extract_items(data)
    results = []
    for item in items_raw:
        if not isinstance(item, dict):
            continue
        if item.get("isJdSale") != 1:
            continue
        rating = item.get("goodCommentsShare")
        if rating is not None and rating < 90:
            continue

        price = item.get("price")
        final_price = item.get("lowestCouponPrice")
        coupon_text = ""
        discount = item.get("bestCouponDiscount")
        if discount:
            coupon_text = f"限时优惠{int(discount)}元"

        item_id = item.get("itemId", "")
        buy_url = f"https://item.jd.com/{item_id}.html"
        results.append({
            "name": item.get("skuName", ""), "brand": item.get("brandName", ""),
            "shop": item.get("shopName", ""), "shop_type": "自营",
            "price": price, "final_price": final_price,
            "coupon": coupon_text if coupon_text else None,
            "sales": item.get("inOrderCount30Days"), "rating": rating,
            "image": item.get("imageUrl", ""), "buy_url": buy_url,
        })
    return results


def _simplify_keyword(keyword):
    k = re.sub(r"\s*\d+(G|GB|TB|T)\b", "", keyword, flags=re.IGNORECASE)
    k = re.sub(r"[（(][^）)]*[）)]", "", k)
    k = re.sub(r"\s+", "", k)
    return k.strip()


def _search_taobao(keyword):
    for kw in [keyword, _simplify_keyword(keyword)]:
        if not kw:
            continue
        data = _scf_call("taobao", "search", {
            "keyword": kw, "is_tmall": True, "page_no": 1, "page_size": 20,
        })
        items_raw = _extract_items(data)
        if items_raw:
            break

    results = []
    for item in items_raw:
        if not isinstance(item, dict):
            continue
        if item.get("user_type") == "C店":
            continue
        coupon_info = item.get("coupon_info", "")
        coupon_text = coupon_info if coupon_info else None
        results.append({
            "name": item.get("title", ""), "brand": item.get("brand_name", ""),
            "shop": item.get("shop_title", ""), "shop_type": "天猫",
            "price": item.get("price"), "final_price": item.get("final_price"),
            "coupon": coupon_text, "sales": item.get("sales"), "rating": None,
            "image": item.get("pict_url", ""), "buy_url": item.get("click_url", ""),
        })
    return results


def _search_pdd(keyword):
    data = _scf_call("pdd", "search", {"keyword": keyword, "with_coupon": True})
    items_raw = _extract_items(data)
    results = []
    for item in items_raw:
        if not isinstance(item, dict):
            continue
        if not item.get("goods_image_url"):
            continue

        goods_sign = item.get("goods_sign", "")
        coupon_discount = item.get("coupon_discount")
        coupon_min_order = item.get("coupon_min_order")
        coupon_text = None
        if coupon_discount:
            if coupon_min_order:
                coupon_text = f"优惠券满{coupon_min_order}减{coupon_discount}"
            else:
                coupon_text = f"优惠券减{coupon_discount}"

        buy_url = f"https://mobile.yangkeduo.com/goods.html?goods_sign={goods_sign}"
        if goods_sign:
            url_data = _scf_call("pdd", "generate_url", {"goods_sign_list": [goods_sign]})
            if isinstance(url_data, dict) and url_data.get("ok"):
                url_info = url_data.get("data")
                if isinstance(url_info, dict):
                    generated = url_info.get("short_url", "") or url_info.get("mobile_url", "")
                    if generated:
                        buy_url = generated
                elif isinstance(url_info, list) and url_info:
                    first = url_info[0] if isinstance(url_info[0], dict) else {}
                    generated = first.get("short_url", "") or first.get("mobile_url", "")
                    if generated:
                        buy_url = generated

        results.append({
            "name": item.get("goods_name", ""), "brand": item.get("brand_name", ""),
            "shop": item.get("mall_name", ""), "shop_type": "拼多多",
            "price": item.get("min_normal_price") or item.get("min_group_price"),
            "final_price": item.get("final_price"), "coupon": coupon_text,
            "sales": item.get("sales_tip", ""), "rating": None,
            "image": item.get("goods_image_url", ""), "buy_url": buy_url,
        })
    return results


def _lookup_jd_by_sku(sku_id):
    return _search_jd(keyword="", sku_id=sku_id)


def _lookup_taobao_by_item_id(item_id):
    data = _scf_call("taobao", "item_info", {"item_id": item_id})
    if isinstance(data, dict) and data.get("ok"):
        info = data.get("data", data)
        if isinstance(info, dict):
            title = info.get("title", "")
            brand = info.get("brand_name", "")
            keyword = f"{brand} {title}".strip() if brand else title
            return keyword if keyword else None
    return None


def _lookup_pdd_by_goods_sign(goods_sign):
    data = _scf_call("pdd", "detail", {"goods_sign": goods_sign})
    if isinstance(data, dict) and data.get("ok"):
        info = data.get("data", data)
        if isinstance(info, dict):
            name = info.get("goods_name", "")
            brand = info.get("brand_name", "")
            keyword = f"{brand} {name}".strip() if brand else name
            return keyword if keyword else None
    return None


def _check_pdd_brand_match(items, query_brand):
    if not items:
        return "拼多多未找到旗舰店/专卖店/专营店同款"
    if not query_brand:
        return None
    query_brand_lower = query_brand.lower()
    for item in items:
        item_brand = (item.get("brand") or "").lower()
        if item_brand and (query_brand_lower in item_brand or item_brand in query_brand_lower):
            return None
    return "拼多多未找到旗舰店/专卖店/专营店同款"


def tool_compare_prices(params):
    query = params.get("query", "").strip()
    platform = params.get("platform", "all")

    if not query:
        return json.dumps({"query": query, "results": None, "hint": "请输入商品关键词或链接"}, ensure_ascii=False)

    if _is_category_word(query):
        return json.dumps({
            "query": query, "results": None,
            "hint": "请提供具体的品牌型号或商品链接，我帮您全网比价。例如：iPhone 17 Pro Max 256G、戴森V15吹风机",
        }, ensure_ascii=False)

    search_keyword = query
    url_platform = None

    jd_sku = _parse_jd_url(query)
    tb_item_id = _parse_taobao_url(query)
    pdd_goods_sign = _parse_pdd_url(query)

    if jd_sku:
        url_platform = "jd"
    elif tb_item_id:
        url_platform = "taobao"
    elif pdd_goods_sign:
        url_platform = "pdd"

    if url_platform == "taobao" and tb_item_id:
        resolved = _lookup_taobao_by_item_id(tb_item_id)
        if resolved:
            search_keyword = resolved
    elif url_platform == "pdd" and pdd_goods_sign:
        resolved = _lookup_pdd_by_goods_sign(pdd_goods_sign)
        if resolved:
            search_keyword = resolved

    if platform == "all":
        platforms = ["jd", "taobao", "pdd"]
    else:
        platforms = [platform]

    results = {}
    query_brand = ""

    if "jd" in platforms:
        if jd_sku:
            jd_items = _lookup_jd_by_sku(jd_sku)
            if not jd_items:
                jd_items = _search_jd(search_keyword)
        else:
            jd_items = _search_jd(search_keyword)
        for it in jd_items:
            if it.get("brand"):
                query_brand = it["brand"]
                break
        results["jd"] = {"items": jd_items, "note": None}

    if "taobao" in platforms:
        tb_items = _search_taobao(search_keyword)
        if not query_brand:
            for it in tb_items:
                if it.get("brand"):
                    query_brand = it["brand"]
                    break
        results["taobao"] = {"items": tb_items, "note": None}

    if not query_brand:
        q_lower = query.lower()
        for brand in KNOWN_BRANDS:
            if brand in q_lower:
                query_brand = brand
                break

    if "pdd" in platforms:
        pdd_items = _search_pdd(search_keyword)
        pdd_note = _check_pdd_brand_match(pdd_items, query_brand)
        results["pdd"] = {"items": pdd_items, "note": pdd_note}

    output = {"query": query, "results": results, "hint": None}
    return json.dumps(output, ensure_ascii=False, default=str)


TOOLS = {
    "compare_prices": tool_compare_prices,
}


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({"error": "用法: python3 main.py <tool> '<json_params>'"}, ensure_ascii=False))
        sys.exit(1)

    tool = sys.argv[1]
    try:
        args = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"参数JSON解析失败: {e}"}, ensure_ascii=False))
        sys.exit(1)

    if tool not in TOOLS:
        print(json.dumps({"error": f"未知工具: {tool}，可用工具: {', '.join(TOOLS.keys())}"}, ensure_ascii=False))
        sys.exit(1)

    try:
        result = TOOLS[tool](args)
        print(result)
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)
