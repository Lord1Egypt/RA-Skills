"""Shared city data (platform-agnostic).

Platform-specific mappings (adcode, abbreviations, pinyin slugs) live in
each adapter's own cities.py module.
"""

CITY_NAMES: list[str] = [
    # Tier-1
    "北京", "上海", "广州", "深圳",
    # New Tier-1
    "成都", "杭州", "重庆", "武汉", "苏州", "南京",
    "天津", "西安", "长沙", "郑州", "东莞", "青岛",
    "合肥", "佛山", "宁波", "昆明", "沈阳", "大连",
    # Tier-2
    "厦门", "济南", "无锡", "福州", "哈尔滨", "石家庄",
    "烟台", "珠海", "惠州", "中山", "太原", "南昌",
    "贵阳", "南宁", "温州", "常州", "徐州", "兰州",
]


def is_valid_city(city: str) -> bool:
    return city in CITY_NAMES or city == "全国"
