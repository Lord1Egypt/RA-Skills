"""
城市经纬度查询模块
从 data/cities.json 加载中国主要城市经纬度数据
"""

import json
import os

_CITIES_DATA = None
_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "cities.json")


def _load_cities():
    """懒加载城市数据"""
    global _CITIES_DATA
    if _CITIES_DATA is None:
        with open(_DATA_PATH, "r", encoding="utf-8") as f:
            _CITIES_DATA = json.load(f)
    return _CITIES_DATA


def get_city_coords(city_name):
    """
    根据城市名查询经纬度
    支持模糊匹配（包含关系）
    
    Args:
        city_name: 城市名（如"上海"、"北京"）
    
    Returns:
        (latitude, longitude) 或 None
    """
    cities = _load_cities()
    
    # 精确匹配
    if city_name in cities:
        c = cities[city_name]
        return (c["lat"], c["lon"])
    
    # 模糊匹配：城市名包含输入，或输入包含城市名
    for name, c in cities.items():
        if city_name in name or name in city_name:
            return (c["lat"], c["lon"])
    
    return None


def list_cities():
    """列出所有支持的城市"""
    cities = _load_cities()
    return list(cities.keys())
