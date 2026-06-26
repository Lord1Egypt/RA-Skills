#!/usr/bin/env python3
"""
续程城市检索工具 (Drop Cities Lookup)

功能：根据出发地和目的地的三字代码，从 data/drop_routes.json 中查找可捡漏的续程城市列表。
定位：纯数据检索工具，不做航班搜索、不做价格对比、不做流程编排。

输入：优先使用三字代码（如 BJS-SHE），支持中文名称兜底映射。
输出：JSON 格式的续程城市列表（三字码）。

使用方法：
    python3 bargain_flights.py --origin BJS --destination SHE
    python3 bargain_flights.py --origin 北京 --destination 沈阳    # 中文兜底
"""

import argparse
import json
import sys
import os

# 中文名称 → 三字码 映射（兜底用）
CITY_CODE_MAP = {
    # 国内城市
    "北京": "BJS", "上海": "SHA", "广州": "CAN", "深圳": "SZX",
    "成都": "CTU", "重庆": "CKG", "杭州": "HGH", "南京": "NKG",
    "武汉": "WUH", "西安": "XIY", "昆明": "KMG", "丽江": "LJG",
    "大理": "DLY", "三亚": "SYX", "海口": "HAK", "桂林": "KWL",
    "澳门": "MFM", "香港": "HKG", "东京": "TYO", "首尔": "SEL",
    "大阪": "OSA", "曼谷": "BKK", "新加坡": "SIN", "台北": "TPE",
    "厦门": "XMN", "吉隆坡": "KUL", "马尼拉": "MNL", "迪拜": "DXB",
    "伊斯坦布尔": "IST", "开罗": "CAI", "内罗毕": "NBO",
    "约翰内斯堡": "JNB", "伦敦": "LON", "巴黎": "PAR",
    "法兰克福": "FRA", "悉尼": "SYD", "墨尔本": "MEL",
    "纽约": "NYC", "洛杉矶": "LAX", "旧金山": "SFO",
    "青岛": "TAO", "天津": "TSN", "长沙": "CSX", "郑州": "CGO",
    "乌鲁木齐": "URC", "兰州": "LHW", "银川": "INC", "呼和浩特": "HET",
    "南宁": "NNG", "南昌": "KHN", "福州": "FOC", "大连": "DLC",
    "石家庄": "SJW", "太原": "TYN", "烟台": "YNT", "济南": "TNA",
    "长春": "CGQ", "哈尔滨": "HRB", "沈阳": "SHE", "宁波": "NBO",
    "无锡": "WUX", "珠海": "ZUH", "汕头": "SWA", "拉萨": "LXA",
    "西宁": "XNN", "高雄": "KHH", "胡志明": "SGN", "河内": "HAN",
    "雅加达": "JKT", "巴厘岛": "DPS", "仰光": "RGN", "金边": "PNH",
    "阿布扎比": "AUH", "多哈": "DOH", "德里": "DEL", "孟买": "BOM",
    "马累": "MLE", "科伦坡": "CMB", "达卡": "DAC", "吉达": "JED",
    "利雅得": "RUH", "安曼": "AMM", "亚的斯亚贝巴": "ADD",
    "开普敦": "CPT", "慕尼黑": "MUC", "柏林": "BER", "阿姆斯特丹": "AMS",
    "布鲁塞尔": "BRU", "马德里": "MAD", "罗马": "FCO", "米兰": "MIL",
    "维也纳": "VIE", "苏黎世": "ZRH", "日内瓦": "GVA", "哥本哈根": "CPH",
    "斯德哥尔摩": "STO", "奥斯陆": "OSL", "赫尔辛基": "HEL", "雅典": "ATH",
    "莫斯科": "MOW", "布里斯班": "BNE", "奥克兰": "AKL", "惠灵顿": "WLG",
    "珀斯": "PER", "温哥华": "YVR", "多伦多": "YYZ", "蒙特利尔": "YUL",
    "西雅图": "SEA", "休斯顿": "IAH", "达拉斯": "DFW", "波士顿": "BOS",
    "迈阿密": "MIA", "亚特兰大": "ATL", "芝加哥": "ORD",
}


def resolve_city_code(city: str) -> str:
    """
    解析城市输入，返回三字代码。
    输入已是三字码（全大写字母，长度 3）直接返回，否则尝试中文映射兜底。
    """
    if len(city) == 3 and city.isupper():
        return city
    return CITY_CODE_MAP.get(city, city)


def load_drop_routes(data_file: str = None) -> list:
    """加载 data/drop_routes.json"""
    if data_file is None:
        data_file = os.path.join(os.path.dirname(__file__), "..", "data", "drop_routes.json")

    try:
        with open(data_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️ 配置文件不存在: {data_file}", file=sys.stderr)
        return []


def lookup_drop_cities(origin_code: str, destination_code: str, routes: list) -> list:
    """根据航线三字码查找续程城市列表"""
    for route in routes:
        if route["o"] == origin_code and route["d"] == destination_code:
            return route.get("drop", [])
    return []


def main():
    parser = argparse.ArgumentParser(
        description="续程城市检索工具 — 根据航线三字码查找 drop_routes.json 中的续程城市"
    )
    parser.add_argument("--origin", required=True, help="出发城市三字码（中文兜底）")
    parser.add_argument("--destination", required=True, help="目的地城市三字码（中文兜底）")
    parser.add_argument("--data-file", help="自定义续程城市配置文件路径")

    args = parser.parse_args()

    # 解析三字码（中文兜底映射）
    o_code = resolve_city_code(args.origin)
    d_code = resolve_city_code(args.destination)

    # 加载配置
    routes = load_drop_routes(args.data_file)
    if not routes:
        print(json.dumps({
            "status": 1,
            "message": "未加载到续程城市配置",
            "data": None
        }, ensure_ascii=False))
        return 1

    # 查找续程城市
    drop_cities = lookup_drop_cities(o_code, d_code, routes)

    if not drop_cities:
        print(f"⚠️ 未配置 {o_code} → {d_code} 的续程城市", file=sys.stderr)
        print(json.dumps({
            "status": 0,
            "message": f"未配置 {o_code} → {d_code} 的续程城市",
            "data": {
                "origin": o_code,
                "destination": d_code,
                "drop_cities": []
            }
        }, ensure_ascii=False))
        return 0

    print(json.dumps({
        "status": 0,
        "message": "success",
        "data": {
            "origin": o_code,
            "destination": d_code,
            "drop_cities": drop_cities
        }
    }, ensure_ascii=False))

    return 0


if __name__ == "__main__":
    exit(main())
