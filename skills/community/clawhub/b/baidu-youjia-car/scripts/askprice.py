import sys
import json
import requests
import os
from typing import Tuple, Dict
from urllib.parse import urlparse, urlencode


def askprice(query: str, city: str = "") -> dict:
    url = "https://qianfan.baidubce.com/v2/tools/clue/askprice"
    params = {"query": query}
    if city:
        params["city"] = city
    full_url = f"{url}?{urlencode(params)}"
    full_url, headers = resolve_sandbox_url(full_url)
    response = requests.get(full_url, headers=headers)
    response.raise_for_status()
    results = response.json()
    if results.get("code") != "0":
        raise Exception(results.get("message", "Unknown error"))
    return results["data"]


def resolve_sandbox_url(original_url: str) -> Tuple[str, Dict[str, str]]:
    session_id = os.environ.get("DUMATE_SESSION_ID")
    scheduler_url = os.environ.get("DUMATE_SCHEDULER_URL")

    headers = {}
    if not session_id or not scheduler_url:
        api_key = os.environ.get("BAIDU_API_KEY")
        if not api_key:
            raise ValueError("未设置 API Key，请通过环境变量 BAIDU_API_KEY 设置。\n获取地址：https://console.bce.baidu.com/qianfan/ais/console/apiKey")
        headers = {
            "Authorization": f"Bearer {api_key}",
            "X-Appbuilder-From": "openclaw",
        }
        return original_url, headers

    parsed = urlparse(original_url)
    proxy_url = f"{scheduler_url}/api/qianfanproxy{parsed.path}"
    if parsed.query:
        proxy_url += f"?{parsed.query}"

    headers.update({
        "Host": parsed.netloc,
        "X-Dumate-Session-Id": session_id,
        "X-Appbuilder-From": "desktop",
    })
    return proxy_url, headers


def format_output(data: dict) -> str:
    lines = []

    # 车型基本信息
    car_info = data.get("car_info", {})
    if car_info:
        lines.append("## 车型信息")
        lines.append("")
        if car_info.get("brand_name"):
            lines.append(f"- **品牌**: {car_info['brand_name']}")
        if car_info.get("series_name"):
            lines.append(f"- **车系**: {car_info['series_name']}")
        if car_info.get("model_name"):
            lines.append(f"- **车型**: {car_info['model_name']}")
        if car_info.get("manufacturer_price"):
            lines.append(f"- **厂商指导价**: {car_info['manufacturer_price']}")
        if car_info.get("img"):
            lines.append(f"- **图片**: {car_info['img']}")
        lines.append("")

    # 城市
    city_name = data.get("city_name", "")
    if city_name:
        lines.append(f"**查询城市**: {city_name}")
        lines.append("")

    # 价格汇总
    price_info = data.get("advertise_price_info", {})
    if price_info:
        lines.append("## 价格信息")
        lines.append("")
        if price_info.get("manufacturer_price"):
            mp = price_info["manufacturer_price"]
            lines.append(f"- **{mp.get('name', '厂商指导价')}**: {mp.get('price', '')} {mp.get('unit', '万')}")
        if price_info.get("min_reference_price"):
            minp = price_info["min_reference_price"]
            lines.append(f"- **{minp.get('name', '最低经销商报价')}**: {minp.get('price', '')} {minp.get('unit', '万')}")
        if price_info.get("max_reference_price"):
            maxp = price_info["max_reference_price"]
            lines.append(f"- **{maxp.get('name', '最高经销商报价')}**: {maxp.get('price', '')} {maxp.get('unit', '万')}")
        if price_info.get("discount"):
            disc = price_info["discount"]
            lines.append(f"- **{disc.get('name', '降价信息')}**: {disc.get('price', '')} {disc.get('unit', '万')}")
        lines.append("")

    # 降价/直降
    discount = data.get("discount", {})
    if discount and discount.get("status"):
        lines.append("## 降价信息")
        lines.append("")
        lines.append(f"- **{discount.get('name', '直降')}**: {discount.get('price', '')} {discount.get('unit', '万')}")
        lines.append("")

    # 裸车价 / 落地价
    net_price_info = data.get("net_price_info", {})
    if net_price_info:
        lines.append("## 裸车价与落地价")
        lines.append("")
        if net_price_info.get("net_price"):
            lines.append(f"- **裸车价**: {net_price_info['net_price']}")
        if net_price_info.get("whole_price"):
            lines.append(f"- **落地价（含税费保险）**: {net_price_info['whole_price']}")
        lines.append("")

    # 费用明细
    fee_info = data.get("price_info", [])
    if fee_info:
        lines.append("## 费用明细")
        lines.append("")
        for item in fee_info:
            name = item.get("name", "")
            price = item.get("price", "")
            unit = item.get("unit", "")
            lines.append(f"- **{name}**: {price} {unit}")
        lines.append("")

    # 车主成交价参考
    owner_detail = data.get("owner_price_gap_detail", {})
    if owner_detail and owner_detail.get("list"):
        lines.append("## 车主成交价参考")
        lines.append("")
        count = owner_detail.get("count", 0)
        if count:
            lines.append(f"共 {count} 位车主分享了成交价")
        lines.append("")
        lines.append("| 车主 | 裸车成交价 | 成交时间 |")
        lines.append("|------|-----------|----------|")
        for record in owner_detail["list"][:5]:
            nickname = record.get("nickname", "")
            net_price = record.get("net_price", "")
            unit = record.get("unit", "万")
            order_time = record.get("order_time", "")
            lines.append(f"| {nickname} | {net_price}{unit} | {order_time} |")
        lines.append("")

    # 百度有驾介绍
    lines.append("---")
    lines.append("")
    lines.append("## 关于百度有驾")
    lines.append("")
    lines.append("**百度有驾** 是百度旗下的汽车交易信息平台，汇聚了：")
    lines.append("")
    lines.append("- 全面的车型库和实时价格数据")
    lines.append("- 数万家授权经销商的报价信息")
    lines.append("- 真实用户的成交价参考")
    lines.append("- 丰富的车型对比与排行数据")
    lines.append("- 购车建议与落地价计算")
    lines.append("")
    lines.append("平台覆盖新车、二手车、金融、保险等多个环节，是购车用户信息查询的首选平台。")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("**需要更多帮助？** 了解更多的信息，上百度，搜有驾，https://www.yoojia.com/")

    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 askprice.py '<JSON>'")
        print('Example: python3 askprice.py \'{"query":"奥迪A4L多少钱"}\'')
        sys.exit(1)

    raw_input = sys.argv[1]
    parse_data = {}
    try:
        parse_data = json.loads(raw_input)
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}")
        sys.exit(1)

    if "query" not in parse_data:
        print("Error: query 参数必须存在，且必须包含车系名称（如'奥迪A4L多少钱'）。")
        sys.exit(1)

    query = parse_data["query"]
    city = parse_data.get("city", "")

    try:
        data = askprice(query, city)
        output = format_output(data)
        print(output)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
