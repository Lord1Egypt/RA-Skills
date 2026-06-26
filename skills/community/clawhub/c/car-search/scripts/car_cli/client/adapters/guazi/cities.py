"""Guazi city name → URL abbreviation mapping.

Guazi uses pinyin abbreviations in URLs: /bj/buy/, /sh/buy/.
"""

CITY_ABBR: dict[str, str] = {
    "北京": "bj", "上海": "sh", "广州": "gz", "深圳": "sz",
    "成都": "cd", "杭州": "hz", "重庆": "cq", "武汉": "wh",
    "苏州": "su", "南京": "nj", "天津": "tj", "西安": "xa",
    "长沙": "cs", "郑州": "zz", "东莞": "dg", "青岛": "qd",
    "合肥": "hf", "佛山": "fs", "宁波": "nb", "昆明": "km",
    "沈阳": "sy", "大连": "dl", "厦门": "xm", "济南": "jn",
    "无锡": "wx", "福州": "fz", "哈尔滨": "hrb", "石家庄": "sjz",
    "烟台": "yt", "珠海": "zh", "惠州": "hui", "中山": "zs",
    "太原": "ty", "南昌": "nc", "贵阳": "gy", "南宁": "nn",
    "温州": "wz", "常州": "cz", "徐州": "xz", "兰州": "lz",
}


def get_city_abbr(city: str) -> str:
    """Get pinyin abbreviation for a city (e.g. 北京 -> bj). Empty string for unknown."""
    return CITY_ABBR.get(city, "")
