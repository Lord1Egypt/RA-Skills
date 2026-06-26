"""City name → youxinpai cityId mapping.

Loaded at import time from bundled city_list.json (scraped from youxinpai API).
The JSON format is a list of provinces, each containing a cityList with cityId/cityName.
"""

import json
from pathlib import Path

_CITY_DATA_FILE = Path(__file__).parent / "city_list.json"

_CITY_MAP: dict[str, int] = {}


def _load_city_map() -> dict[str, int]:
    if _CITY_MAP:
        return _CITY_MAP

    with open(_CITY_DATA_FILE, encoding="utf-8") as f:
        provinces = json.load(f)

    for province in provinces:
        province_name = province.get("provinceName", "")
        city_list = province.get("cityList", [])

        for city in city_list:
            city_name = city.get("cityName", "").strip()
            city_id = city.get("cityId")
            if city_name and city_id is not None:
                _CITY_MAP[city_name] = city_id

        # 直辖市：省名 == 城市名的情况已自动覆盖
        # 但需要确保省名也能匹配到第一个城市（如"广东"不应匹配到任何城市）
        if len(city_list) == 1 and city_list[0].get("cityName") == province_name:
            _CITY_MAP[province_name] = city_list[0]["cityId"]

    return _CITY_MAP


def get_city_id(city_name: str) -> int | None:
    """Return youxinpai cityId for a Chinese city name, or None if not found."""
    city_map = _load_city_map()
    return city_map.get(city_name)


def get_all_city_names() -> list[str]:
    """Return all supported city names."""
    city_map = _load_city_map()
    return list(city_map.keys())
