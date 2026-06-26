#!/usr/bin/env python3
"""
机场数据库管理模块
提供省份、城市、机场之间的映射查询功能
"""

import json
import os
from typing import List, Dict, Set, Optional, Tuple

# 获取当前模块目录
_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_DATA_DIR = os.path.join(os.path.dirname(_CURRENT_DIR), 'data')
_AIRPORTS_FILE = os.path.join(_DATA_DIR, 'airports.json')


class AirportDatabase:
    """机场数据库类"""

    _instance = None
    _data = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_data()
        return cls._instance

    def _load_data(self):
        """加载机场数据"""
        if os.path.exists(_AIRPORTS_FILE):
            with open(_AIRPORTS_FILE, 'r', encoding='utf-8') as f:
                self._data = json.load(f)
        else:
            # 如果文件不存在，使用内置数据
            self._data = self._get_builtin_data()

    def _get_builtin_data(self) -> Dict:
        """获取内置数据（备用）"""
        return {
            "airports": [],
            "provinces": {}
        }

    def get_airport_by_code(self, code: str) -> Optional[Dict]:
        """根据机场代码获取机场信息"""
        code = code.upper()
        for airport in self._data.get("airports", []):
            if airport.get("code", "").upper() == code:
                return airport
        return None

    def get_city_airports(self, city: str) -> List[Dict]:
        """获取某城市的所有机场"""
        city_normalized = city.replace("市", "").replace("的", "")
        results = []
        for airport in self._data.get("airports", []):
            airport_city = airport.get("city", "").replace("市", "")
            if airport_city == city_normalized:
                # 排除已废弃的机场
                if not airport.get("deprecated", False):
                    results.append(airport)
        return results

    def get_province_cities(self, province: str) -> List[str]:
        """获取某省份的所有城市（仅限有机场的城市）"""
        province_normalized = province.replace("省", "").replace("市", "").replace("自治区", "").replace("的", "")
        cities = set()

        for airport in self._data.get("airports", []):
            airport_province = airport.get("province", "").replace("省", "").replace("市", "").replace("自治区", "")

            # 精确匹配或包含匹配
            if (province_normalized in airport_province or
                airport_province in province_normalized):
                city = airport.get("city", "").replace("市", "")
                if city and not airport.get("deprecated", False):
                    cities.add(city)

        return sorted(list(cities))

    def get_city_code(self, city: str) -> Optional[str]:
        """获取城市的携程代码（通常是主机场代码）"""
        airports = self.get_city_airports(city)
        if airports:
            # 返回第一个机场的城市代码
            return airports[0].get("cityCode")

        # 尝试模糊匹配
        city_normalized = city.replace("市", "").replace("的", "")
        for airport in self._data.get("airports", []):
            airport_city = airport.get("city", "").replace("市", "")
            if airport_city == city_normalized:
                return airport.get("cityCode")

        return None

    def is_province(self, name: str) -> bool:
        """判断是否为省份名称"""
        name_normalized = name.replace("省", "").replace("市", "").replace("自治区", "").replace("的", "")
        provinces = self._data.get("provinces", {})

        for province_name in provinces.keys():
            province_normalized = province_name.replace("省", "").replace("市", "").replace("自治区", "")
            if name_normalized in province_normalized or province_normalized in name_normalized:
                return True
        return False

    def resolve_destination(self, destination: str) -> Tuple[str, List[str]]:
        """解析目的地，返回类型和具体城市列表

        Args:
            destination: 目的地字符串，可能是城市名或省份名

        Returns:
            (type, cities) - type 为 "city" 或 "province"，cities 为城市名列表
        """
        destination = destination.strip().rstrip('的')

        # 首先尝试作为城市处理
        airports = self.get_city_airports(destination)
        if airports:
            return ("city", [airports[0].get("city", "").replace("市", "")])

        # 尝试作为省份处理
        if self.is_province(destination):
            cities = self.get_province_cities(destination)
            if cities:
                return ("province", cities)

        # 无法识别
        return ("unknown", [])

    def get_all_cities_with_airports(self) -> List[str]:
        """获取所有有机场的城市列表"""
        cities = set()
        for airport in self._data.get("airports", []):
            if not airport.get("deprecated", False):
                city = airport.get("city", "").replace("市", "")
                cities.add(city)
        return sorted(list(cities))

    def get_all_provinces(self) -> List[str]:
        """获取所有省份列表"""
        return list(self._data.get("provinces", {}).keys())

    def search_city(self, query: str) -> List[Dict]:
        """模糊搜索城市"""
        query_normalized = query.replace("市", "").replace("省", "").lower()
        results = []

        for airport in self._data.get("airports", []):
            if airport.get("deprecated", False):
                continue

            city = airport.get("city", "").replace("市", "")
            province = airport.get("province", "")

            if query_normalized in city.lower() or query_normalized in province.lower():
                results.append({
                    "city": city,
                    "province": province,
                    "code": airport.get("cityCode"),
                    "airport_code": airport.get("code"),
                    "airport_name": airport.get("name")
                })

        # 去重
        seen = set()
        unique_results = []
        for r in results:
            key = r["city"]
            if key not in seen:
                seen.add(key)
                unique_results.append(r)

        return unique_results


# 全局实例
_db = None


def get_db() -> AirportDatabase:
    """获取数据库单例"""
    global _db
    if _db is None:
        _db = AirportDatabase()
    return _db


def test():
    """测试函数"""
    db = get_db()

    print("=== 测试省份解析 ===")

    # 测试新疆
    cities = db.get_province_cities("新疆")
    print(f"新疆有机场的城市: {cities}")

    # 测试四川
    cities = db.get_province_cities("四川")
    print(f"四川有机场的城市: {cities}")

    # 测试云南
    cities = db.get_province_cities("云南")
    print(f"云南有机场的城市: {cities}")

    # 测试海南
    cities = db.get_province_cities("海南")
    print(f"海南有机场的城市: {cities}")

    print("\n=== 测试目的地解析 ===")

    # 测试省份解析
    dest_type, cities = db.resolve_destination("新疆省")
    print(f"新疆省 -> type: {dest_type}, cities: {cities}")

    dest_type, cities = db.resolve_destination("四川")
    print(f"四川 -> type: {dest_type}, cities: {cities}")

    # 测试城市解析
    dest_type, cities = db.resolve_destination("上海")
    print(f"上海 -> type: {dest_type}, cities: {cities}")

    print("\n=== 测试城市搜索 ===")

    # 搜索
    results = db.search_city("乌鲁木齐")
    print(f"搜索'乌鲁木齐': {results}")


if __name__ == "__main__":
    test()
