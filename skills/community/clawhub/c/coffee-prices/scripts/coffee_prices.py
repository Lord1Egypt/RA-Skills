import argparse
import csv
import json
import os
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional

import requests


# 简单的城市分级配置，可根据需要自行扩展或调整
CITY_TIERS: Dict[str, str] = {
    # tier1
    "北京": "tier1",
    "上海": "tier1",
    "广州": "tier1",
    "深圳": "tier1",
    "杭州": "tier1",
    "南京": "tier1",
    "成都": "tier1",
    "重庆": "tier1",
    "苏州": "tier1",
    "武汉": "tier1",
    # tier2（示例，实际可按需调整）
    "西安": "tier2",
    "天津": "tier2",
    "青岛": "tier2",
    "宁波": "tier2",
    "厦门": "tier2",
    "郑州": "tier2",
    "长沙": "tier2",
    "合肥": "tier2",
    "佛山": "tier2",
    # 其他城市默认 tier2
}


TIER_MULTIPLIER: Dict[str, float] = {
    "tier1": 1.05,
    "tier2": 1.00,
    "tier3": 0.95,
}


# 品牌基础价格（单位：人民币，标准中杯、无折扣参考价）
BASE_PRICES: Dict[str, Dict[str, object]] = {
    "starbucks": {
        "display_name": "星巴克",
        "drinks": {
            "latte": 36.0,
            "americano": 30.0,
            "cappuccino": 36.0,
            "mocha": 38.0,
        },
    },
    "luckin": {
        "display_name": "瑞幸",
        "drinks": {
            "latte": 24.0,
            "americano": 20.0,
            "cappuccino": 24.0,
            "mocha": 26.0,
        },
    },
    "cotti": {
        "display_name": "库迪",
        "drinks": {
            "latte": 22.0,
            "americano": 18.0,
            "cappuccino": 22.0,
            "mocha": 24.0,
        },
    },
}


SUPPORTED_DRINKS = {
    "latte": "拿铁",
    "americano": "美式",
    "cappuccino": "卡布奇诺",
    "mocha": "摩卡",
}


@dataclass
class CoffeePriceRow:
    brand: str
    brand_en: str
    city: str
    drink: str
    drink_en: str
    price: float
    currency: str = "CNY"


def infer_city_from_ip(timeout: float = 3.0) -> Optional[str]:
    """
    尝试通过 IP 定位推断城市。
    使用 ipinfo.io 免费接口，仅作示意，不能保证在所有环境下可用。
    """
    try:
        resp = requests.get("https://ipinfo.io/json", timeout=timeout)
        if resp.status_code != 200:
            return None
        data = resp.json()
        city = data.get("city")
        if isinstance(city, str) and city:
            # ipinfo 返回的是英文城市名（如 Shanghai），此处简单去掉空格后返回
            return city.strip()
    except Exception:
        return None
    return None


def normalize_city_name(city: Optional[str]) -> Optional[str]:
    if not city:
        return None
    return city.strip()


def get_city_tier(city: str) -> str:
    if not city:
        return "tier2"
    if city in CITY_TIERS:
        return CITY_TIERS[city]
    # 简单规则：名称结尾带「市」时去掉再查一次
    if city.endswith("市"):
        base = city[:-1]
        if base in CITY_TIERS:
            return CITY_TIERS[base]
    # 对于英文城市名做一个非常粗糙的映射示例
    lower = city.lower()
    if any(k in lower for k in ["shanghai", "beijing", "guangzhou", "shenzhen", "hangzhou"]):
        return "tier1"
    return "tier2"


def get_multiplier_for_city(city: str) -> float:
    tier = get_city_tier(city)
    return TIER_MULTIPLIER.get(tier, 1.0)


def compute_price(brand_key: str, drink_key: str, city: str) -> Optional[float]:
    brand_data = BASE_PRICES.get(brand_key)
    if not brand_data:
        return None
    drinks = brand_data.get("drinks", {})
    base_price = drinks.get(drink_key)
    if base_price is None:
        return None
    multiplier = get_multiplier_for_city(city)
    raw_price = float(base_price) * multiplier
    # 四舍五入到 0.5 元，符合日常菜单价格习惯
    rounded = round(raw_price * 2) / 2.0
    return rounded


def build_rows(city: str, brands: List[str], drinks: List[str]) -> List[CoffeePriceRow]:
    rows: List[CoffeePriceRow] = []
    city_normalized = normalize_city_name(city) or "未知城市"
    for brand_key in brands:
        brand_data = BASE_PRICES.get(brand_key)
        if not brand_data:
            continue
        display_name = str(brand_data.get("display_name", brand_key))
        for drink_key in drinks:
            drink_cn = SUPPORTED_DRINKS.get(drink_key)
            if not drink_cn:
                continue
            price = compute_price(brand_key, drink_key, city_normalized)
            if price is None:
                continue
            rows.append(
                CoffeePriceRow(
                    brand=display_name,
                    brand_en=brand_key,
                    city=city_normalized,
                    drink=drink_cn,
                    drink_en=drink_key,
                    price=price,
                )
            )
    return rows


def output_markdown(rows: List[CoffeePriceRow]) -> None:
    if not rows:
        print("没有可用的价格数据。")
        return

    headers = ["品牌", "品牌英文", "城市", "品类", "参考价格(元)"]
    print("| " + " | ".join(headers) + " |")
    print("| " + " | ".join(["----"] * len(headers)) + " |")
    for row in rows:
        print(
            f"| {row.brand} | {row.brand_en} | {row.city} | {row.drink} | {row.price:.1f} |"
        )


def output_json(rows: List[CoffeePriceRow]) -> None:
    data = [asdict(r) for r in rows]
    print(json.dumps(data, ensure_ascii=False, indent=2))


def output_csv(rows: List[CoffeePriceRow]) -> None:
    writer = csv.writer(os.sys.stdout)
    writer.writerow(
        ["brand", "brand_en", "city", "drink", "drink_en", "price", "currency"]
    )
    for row in rows:
        writer.writerow(
            [row.brand, row.brand_en, row.city, row.drink, row.drink_en, row.price, row.currency]
        )


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="获取指定城市主流连锁咖啡（星巴克、瑞幸、库迪等）的参考价格，并以表格形式输出。"
    )
    parser.add_argument(
        "--city",
        type=str,
        help="城市名称（中文，如：上海、北京、成都）。省略时将尝试从环境变量 OPENCLAW_CITY 或 IP 自动推断。",
    )
    parser.add_argument(
        "--brands",
        type=str,
        default="starbucks,luckin,cotti",
        help="要查询的品牌，逗号分隔，例如：starbucks,luckin,cotti。",
    )
    parser.add_argument(
        "--drinks",
        type=str,
        default="latte,americano,cappuccino,mocha",
        help="要查询的咖啡品类，逗号分隔，例如：latte,americano,cappuccino,mocha。",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="markdown",
        choices=["markdown", "json", "csv"],
        help="输出格式：markdown（默认）、json、csv。",
    )
    return parser.parse_args(argv)


def resolve_city(cli_city: Optional[str]) -> str:
    # 1) CLI 直接传入
    if cli_city:
        return normalize_city_name(cli_city) or "未知城市"

    # 2) 环境变量
    env_city = os.getenv("OPENCLAW_CITY")
    if env_city:
        return normalize_city_name(env_city) or "未知城市"

    # 3) IP 自动推断
    ip_city = infer_city_from_ip()
    if ip_city:
        return normalize_city_name(ip_city) or "未知城市"

    return "未知城市"


def main(argv: Optional[List[str]] = None) -> None:
    args = parse_args(argv)
    city = resolve_city(args.city)

    brands = [b.strip() for b in args.brands.split(",") if b.strip()]
    drinks = [d.strip() for d in args.drinks.split(",") if d.strip()]

    rows = build_rows(city, brands, drinks)

    if args.output == "markdown":
        output_markdown(rows)
    elif args.output == "json":
        output_json(rows)
    elif args.output == "csv":
        output_csv(rows)
    else:
        # 理论上不会走到这里，因为 argparse 做了 choices 限定
        output_markdown(rows)


if __name__ == "__main__":
    main()

