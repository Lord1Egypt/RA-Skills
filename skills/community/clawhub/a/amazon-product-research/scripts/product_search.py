#!/usr/bin/env python3
"""
Amazon产品搜索模块
自然语言搜索Amazon产品，支持RapidAPI + Mock回退
"""

import random
import sys
import io
import requests

# Windows GBK encoding fix
try:
    if sys.stdout.encoding != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
from typing import List, Dict, Optional


def search_products(
    query: str,
    market: str = "US",
    max_products: int = 5,
    rapidapi_key: Optional[str] = None,
    debug: bool = False
) -> List[Dict]:
    """
    搜索Amazon产品

    Args:
        query: 搜索关键词（自然语言）
        market: 市场代码 (US/UK/DE/JP/FR/CA/IT/ES)
        max_products: 最多返回产品数
        rapidapi_key: RapidAPI Key
        debug: 调试模式

    Returns:
        产品列表 [{"asin", "title", "price", "rating", "total_reviews", "image_url", "url"}, ...]
    """
    print(f"🔍 搜索关键词: \"{query}\" (Market: {market})")

    # 尝试真实搜索
    if rapidapi_key:
        products = _search_rapidapi(query, market, max_products, rapidapi_key, debug)
        if products:
            print(f"✅ 找到 {len(products)} 个产品（RapidAPI）")
            return products
        print("⚠️ RapidAPI搜索失败，回退到模拟数据")

    # 模拟数据回退
    products = _search_mock(query, market, max_products, debug)
    print(f"✅ 生成 {len(products)} 个模拟产品")
    return products


def _search_rapidapi(
    query: str,
    market: str,
    max_products: int,
    api_key: str,
    debug: bool
) -> List[Dict]:
    """通过RapidAPI搜索产品"""
    url = "https://amazon-products-and-reviews.p.rapidapi.com/products/search"

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "amazon-products-and-reviews.p.rapidapi.com"
    }

    # 市场代码映射
    market_country = {
        "US": "US", "UK": "GB", "DE": "DE", "JP": "JP",
        "FR": "FR", "CA": "CA", "IT": "IT", "ES": "ES"
    }

    params = {
        "keyword": query,
        "country": market_country.get(market.upper(), "US"),
        "page": 1
    }

    if debug:
        print(f"  API URL: {url}")
        print(f"  Params: {params}")

    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)

        if debug:
            print(f"  Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            products = []

            # 解析搜索结果
            items = data.get("products", data.get("data", data.get("results", [])))
            if isinstance(data, list):
                items = data

            for item in items[:max_products]:
                asin = item.get("asin", item.get("product_id", ""))
                if not asin:
                    continue

                host = _get_market_host(market)
                products.append({
                    "asin": asin,
                    "title": item.get("title", f"Product {asin}"),
                    "price": str(item.get("price", {}).get("current_price", item.get("price", "N/A"))),
                    "rating": float(item.get("rating", item.get("star_rating", 0))),
                    "total_reviews": int(item.get("reviews_count", item.get("total_reviews", 0))),
                    "image_url": item.get("image", item.get("thumbnail", "")),
                    "url": f"https://www.{host}/dp/{asin}"
                })

            return products
        else:
            print(f"  ⚠️ 搜索失败: HTTP {response.status_code}")
            return []
    except Exception as e:
        print(f"  ⚠️ 搜索异常: {e}")
        return []


def _search_mock(query: str, market: str, max_products: int, debug: bool) -> List[Dict]:
    """生成模拟产品数据"""

    # 基于查询词生成合理的产品名
    mock_products = _generate_mock_products(query, market, max_products)

    if debug:
        for p in mock_products:
            print(f"  Mock: [{p['asin']}] {p['title'][:50]}... ⭐{p['rating']}")

    return mock_products


def _generate_mock_products(query: str, market: str, count: int) -> List[Dict]:
    """根据查询词智能生成模拟产品"""

    # 从查询词提取品牌和品类线索
    q_lower = query.lower()
    host = _get_market_host(market)

    # 预定义品类模板
    category_hints = {
        "bluetooth": {"category": "Wireless Earbuds", "brands": ["SoundCore", "JBL", "TOZO", "Bmani", "SoundPEATS"]},
        "headphone": {"category": "Headphones", "brands": ["Sony", "Bose", "Sennheiser", "Audio-Technica", "Beats"]},
        "speaker": {"category": "Bluetooth Speakers", "brands": ["JBL", "Ultimate Ears", "Bose", "Anker", "Tribit"]},
        "yoga": {"category": "Yoga Mats", "brands": ["Gaiam", "BalanceFrom", "Manduka", "Jade", "Liforme"]},
        "mat": {"category": "Exercise Mats", "brands": ["Gaiam", "BalanceFrom", "Manduka", "Jade", "Liforme"]},
        "camera": {"category": "Cameras", "brands": ["Canon", "Sony", "Nikon", "Fujifilm", "Panasonic"]},
        "phone": {"category": "Smartphones", "brands": ["Samsung", "Apple", "Google", "OnePlus", "Xiaomi"]},
        "charger": {"category": "Chargers", "brands": ["Anker", "RAVPower", "Aukey", "Belkin", "Spigen"]},
        "lamp": {"category": "Desk Lamps", "brands": ["TaoTronics", "BenQ", "Philips", "Lepro", "Globe Electric"]},
        "keyboard": {"category": "Keyboards", "brands": ["Logitech", "Razer", "Corsair", "Keychron", "SteelSeries"]},
        "mouse": {"category": "Computer Mice", "brands": ["Logitech", "Razer", "Microsoft", "SteelSeries", "Corsair"]},
        "watch": {"category": "Smartwatches", "brands": ["Apple", "Samsung", "Garmin", "Fitbit", "Amazfit"]},
        "water bottle": {"category": "Water Bottles", "brands": ["Hydro Flask", "Yeti", "Nalgene", "Contigo", "CamelBak"]},
        "coffee": {"category": "Coffee Makers", "brands": ["Keurig", "Nespresso", "Breville", "Mr. Coffee", "Hamilton Beach"]},
    }

    # 模糊匹配品类
    brands = ["GenericPro", "BestChoice", "PrimePick", "ValueMax", "TopDeal"]
    category = "Consumer Electronics"

    for hint, info in category_hints.items():
        if hint in q_lower:
            brands = info["brands"]
            category = info["category"]
            break

    # 生成产品
    suffix_map = {
        "US": "com", "UK": "co.uk", "DE": "de", "JP": "co.jp",
        "FR": "fr", "CA": "ca", "IT": "it", "ES": "es"
    }
    tld = suffix_map.get(market.upper(), "com")

    products = []
    for i in range(count):
        brand = brands[i % len(brands)]
        model = f"Pro-{random.randint(1000, 9999)}"
        rating = round(random.uniform(3.2, 4.8), 1)
        reviews = random.randint(50, 15000)
        price = f"${random.randint(9, 299)}.{random.randint(0,99):02d}"

        asin = f"B{''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=9))}"

        products.append({
            "asin": asin,
            "title": f"{brand} {model} {category} - {['2024','2025','New','Pro','Plus','Ultra'][i]} Edition",
            "price": price,
            "rating": rating,
            "total_reviews": reviews,
            "image_url": f"https://via.placeholder.com/300x300/EEE/999?text={brand.replace(' ', '+')}",
            "url": f"https://www.amazon.{tld}/dp/{asin}"
        })

    return products


def _get_market_host(market: str) -> str:
    """获取市场Host"""
    market_hosts = {
        "US": "amazon.com", "UK": "amazon.co.uk", "DE": "amazon.de",
        "JP": "amazon.co.jp", "FR": "amazon.fr", "CA": "amazon.ca",
        "IT": "amazon.it", "ES": "amazon.es"
    }
    return market_hosts.get(market.upper(), "amazon.com")


if __name__ == "__main__":
    # 快速测试
    results = search_products("bluetooth headphones noise cancelling", "US", 5, debug=True)
    print(f"\n找到 {len(results)} 个产品:")
    for p in results:
        print(f"  [{p['asin']}] {p['title'][:60]} | ⭐{p['rating']} | {p['price']}")
