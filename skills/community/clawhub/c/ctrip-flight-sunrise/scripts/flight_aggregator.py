#!/usr/bin/env python3
"""
航班聚合搜索模块
支持复杂查询：多省份、多日期范围、价格筛选、直飞筛选、周末筛选
"""

import sys
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import json

# 导入相关模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from airport_db import get_db
from ctrip_flight import CtripFlightSearch


class FlightQueryParser:
    """航班查询解析器 - 将自然语言查询解析为结构化搜索条件"""

    def __init__(self):
        self.db = get_db()

    def parse(self, query: str, departure: str, date_range: str = None) -> Dict:
        """解析查询

        Args:
            query: 自然语言查询，如 "四川、云南和海南三个省" 或 "5月1日到5月7日"
            departure: 出发地
            date_range: 日期范围描述

        Returns:
            结构化的查询条件
        """
        result = {
            "departure": departure,
            "destinations": [],  # [(type, city_name), ...]
            "date_range": None,  # {"start": "2026-05-01", "end": "2026-05-07"}
            "price_max": None,
            "direct_only": True,
            "weekend_only": False
        }

        # 解析目的地
        result["destinations"] = self._parse_destinations(query)

        # 解析日期范围
        if date_range:
            result["date_range"] = self._parse_date_range(date_range)
        else:
            result["date_range"] = self._parse_date_range_from_query(query)

        # 解析价格
        result["price_max"] = self._extract_price(query)

        # 周末
        result["weekend_only"] = "周末" in query

        return result

    def _parse_destinations(self, query: str) -> List[Tuple[str, str]]:
        """解析目的地列表"""
        destinations = []
        seen_cities = set()

        # 移除量词和助词，但保留省份标记
        cleaned = query.replace("三个省", "").replace("三个城市", "").replace("的", "")
        cleaned = cleaned.replace("和", ",").replace("及", ",").replace("与", ",")

        # 按逗号或顿号分割
        parts = cleaned.replace("，", ",").replace("、", ",").split(",")

        # 需要过滤掉的关键词
        filter_keywords = [
            "价格低于", "元以下", "元以内", "价格", "元",
            "周末", "工作日", "直飞", "经停", "中转",
            "低于", "不超过", "不超过", "以上", "以下",
            "时间", "起飞", "到达", "航班"
        ]

        for part in parts:
            part = part.strip()
            if not part:
                continue

            # 检查是否包含过滤关键词
            is_filter = False
            for keyword in filter_keywords:
                if keyword in part and len(part) < 15:  # 关键词较短，如果整个part是关键词则跳过
                    is_filter = True
                    break

            if is_filter:
                continue

            # 移除常见后缀
            part_clean = part.replace("省", "").replace("市", "").replace("县", "")

            # 跳过空字符串
            if not part_clean:
                continue

            # 使用数据库解析
            dest_type, cities = self.db.resolve_destination(part_clean)

            if dest_type == "province":
                for city in cities:
                    if city not in seen_cities:
                        seen_cities.add(city)
                        destinations.append(("province", city))
            elif dest_type == "city":
                for city in cities:
                    if city not in seen_cities:
                        seen_cities.add(city)
                        destinations.append(("city", city))

        return destinations

    def _parse_date_range(self, date_str: str) -> Dict:
        """解析日期范围字符串"""
        result = {"start": None, "end": None, "weekends": []}

        # 解析 "5月1日到5月7日" 或 "2026-05-01到2026-05-07"
        import re

        # 匹配 X月X日 格式
        month_day_pattern = r'(\d+)月(\d+)日'
        matches = re.findall(month_day_pattern, date_str)

        if len(matches) >= 2:
            year = datetime.now().year
            start_month, start_day = int(matches[0][0]), int(matches[0][1])
            end_month, end_day = int(matches[1][0]), int(matches[1][1])

            start_date = datetime(year, start_month, start_day)
            end_date = datetime(year, end_month, end_day)
        else:
            # 假设是未来一周
            start_date = datetime.now()
            end_date = start_date + timedelta(days=7)

        result["start"] = start_date.strftime("%Y-%m-%d")
        result["end"] = end_date.strftime("%Y-%m-%d")

        # 计算周末日期
        current = start_date
        while current <= end_date:
            if current.weekday() in [5, 6]:  # 周六、周日
                result["weekends"].append(current.strftime("%Y-%m-%d"))
            current += timedelta(days=1)

        return result

    def _parse_date_range_from_query(self, query: str) -> Dict:
        """从查询中提取日期范围"""
        # 检查是否有明确的日期描述
        if "五一" in query or "5月1日" in query:
            return self._parse_date_range("5月1日到5月7日")
        elif "清明" in query:
            return self._parse_date_range("4月4日到4月6日")
        elif "端午" in query:
            return self._parse_date_range("5月28日到5月30日")
        elif "中秋" in query:
            return self._parse_date_range("9月15日到9月17日")
        elif "国庆" in query:
            return self._parse_date_range("10月1日到10月7日")
        elif "一周" in query or "接下来一周" in query:
            # 未来一周
            start = datetime.now()
            end = start + timedelta(days=7)
            return {
                "start": start.strftime("%Y-%m-%d"),
                "end": end.strftime("%Y-%m-%d"),
                "weekends": self._get_weekends(start, end)
            }

        # 默认：未来一周
        return self._parse_date_range("接下来一周")

    def _get_weekends(self, start: datetime, end: datetime) -> List[str]:
        """获取日期范围内的周末"""
        weekends = []
        current = start
        while current <= end:
            if current.weekday() in [5, 6]:
                weekends.append(current.strftime("%Y-%m-%d"))
            current += timedelta(days=1)
        return weekends

    def _extract_price(self, query: str) -> Optional[int]:
        """从查询中提取价格上限"""
        import re
        patterns = [
            r'低于(\d+)元',
            r'不超过(\d+)元',
            r'(\d+)元以下',
            r'价格.*?(\d+)',
            r'.*?(\d{3,4})元'
        ]

        for pattern in patterns:
            match = re.search(pattern, query)
            if match:
                return int(match.group(1))

        return None


class FlightAggregator:
    """航班聚合器 - 执行多次搜索并聚合结果"""

    def __init__(self):
        self.searcher = CtripFlightSearch()
        self.db = get_db()
        self.query_parser = FlightQueryParser()

    def search(self, query: str, departure: str, date_range: str = None) -> Dict:
        """执行聚合搜索

        Args:
            query: 查询描述，如 "四川、云南和海南三个省"
            departure: 出发地
            date_range: 日期范围

        Returns:
            聚合结果
        """
        # 解析查询
        conditions = self.query_parser.parse(query, departure, date_range)

        print(f"解析查询条件:")
        print(f"  出发地: {conditions['departure']}")
        print(f"  目的地类型: {set(t for t, _ in conditions['destinations'])}")
        print(f"  目的地城市: {[c for _, c in conditions['destinations']]}")
        print(f"  日期范围: {conditions['date_range']}")
        print(f"  价格上限: {conditions['price_max']}")
        print(f"  仅周末: {conditions['weekend_only']}")
        print(f"  仅直飞: {conditions['direct_only']}")
        print()

        # 执行搜索
        all_flights = []
        date_range = conditions['date_range']

        # 对每个目的地城市执行搜索
        searched_cities = set()

        for dest_type, city in conditions['destinations']:
            if city in searched_cities:
                continue
            searched_cities.add(city)

            print(f"搜索: {departure} -> {city}...")

            # 获取该城市的机场代码
            city_code = self.db.get_city_code(city)
            if not city_code:
                print(f"  警告: 无法获取 {city} 的城市代码")
                continue

            # 如果是日期范围，搜索每一天
            dates_to_search = []

            if date_range and date_range.get("weekends") and conditions["weekend_only"]:
                dates_to_search = date_range["weekends"]
            elif date_range:
                # 生成日期范围内的所有日期
                start = datetime.strptime(date_range["start"], "%Y-%m-%d")
                end = datetime.strptime(date_range["end"], "%Y-%m-%d")
                current = start
                while current <= end:
                    dates_to_search.append(current.strftime("%Y-%m-%d"))
                    current += timedelta(days=1)
            else:
                dates_to_search.append(datetime.now().strftime("%Y-%m-%d"))

            for date in dates_to_search:
                try:
                    result = self.searcher.search_flights(departure, city, date)

                    if result.get("flights"):
                        for flight in result["flights"]:
                            flight["searchDate"] = date
                            flight["destCity"] = city
                            flight["destType"] = dest_type
                            all_flights.append(flight)
                except Exception as e:
                    print(f"  搜索 {date} 失败: {e}")
                    continue

        print(f"\n共找到 {len(all_flights)} 个航班")
        print()

        # 过滤结果
        filtered_flights = self._apply_filters(all_flights, conditions)

        print(f"过滤后: {len(filtered_flights)} 个航班")

        # 生成报告
        return self._generate_report(filtered_flights, conditions)

    def _apply_filters(self, flights: List[Dict], conditions: Dict) -> List[Dict]:
        """应用各种过滤器"""
        result = flights

        # 仅直飞
        if conditions["direct_only"]:
            before = len(result)
            result = [f for f in result if f.get("isDirect", False)]
            print(f"直飞过滤: {before} -> {len(result)}")

        # 价格过滤
        if conditions["price_max"]:
            before = len(result)
            result = [f for f in result if f.get("price", 0) <= conditions["price_max"]]
            print(f"价格<={conditions['price_max']}过滤: {before} -> {len(result)}")

        return result

    def _generate_report(self, flights: List[Dict], conditions: Dict) -> Dict:
        """生成分析报告"""
        if not flights:
            return {
                "summary": "未找到符合条件的航班",
                "flights": [],
                "statistics": {}
            }

        # 按目的地分组
        by_dest = {}
        for f in flights:
            city = f.get("destCity", "未知")
            if city not in by_dest:
                by_dest[city] = []
            by_dest[city].append(f)

        # 按价格排序
        sorted_flights = sorted(flights, key=lambda x: x.get("price", 99999))

        # 统计
        prices = [f.get("price", 0) for f in flights if f.get("price", 0) > 0]

        report = {
            "summary": {
                "total_flights": len(flights),
                "total_cities": len(by_dest),
                "price_range": f"¥{min(prices)} - ¥{max(prices)}" if prices else "N/A",
                "lowest_price": min(prices) if prices else 0,
                "conditions": conditions
            },
            "by_destination": {
                city: {
                    "count": len(flights),
                    "lowest_price": min(f.get("price", 99999) for f in flights if f.get("price", 0) > 0),
                    "weekend_flights": [f for f in flights if self._is_weekend(f.get("depTime", ""))]
                }
                for city, flights in by_dest.items()
            },
            "flights": sorted_flights[:50],  # 最多返回50个
            "statistics": {
                "min_price": min(prices) if prices else 0,
                "max_price": max(prices) if prices else 0,
                "avg_price": int(sum(prices) / len(prices)) if prices else 0,
                "direct_count": len([f for f in flights if f.get("isDirect")]),
                "weekend_count": len([f for f in flights if self._is_weekend(f.get("depTime", ""))])
            }
        }

        return report

    def _is_weekend(self, datetime_str: str) -> bool:
        """判断是否为周末"""
        if not datetime_str:
            return False
        try:
            if " " in datetime_str:
                date_str = datetime_str.split(" ")[0]
            else:
                date_str = datetime_str[:10]

            dt = datetime.strptime(date_str, "%Y-%m-%d")
            return dt.weekday() in [5, 6]
        except:
            return False


def format_report(report: Dict) -> str:
    """格式化输出报告"""
    output = []
    output.append("=" * 80)
    output.append("航班搜索结果报告")
    output.append("=" * 80)
    output.append("")

    summary = report.get("summary", {})
    conditions = summary.get("conditions", {})

    output.append(f"查询条件:")
    output.append(f"  出发地: {conditions.get('departure', 'N/A')}")
    output.append(f"  目的地: {[c for _, c in conditions.get('destinations', [])]}")
    output.append(f"  日期范围: {conditions.get('date_range', {}).get('start', 'N/A')} - {conditions.get('date_range', {}).get('end', 'N/A')}")
    output.append(f"  价格上限: {conditions.get('price_max', '无')}")
    output.append(f"  仅周末: {conditions.get('weekend_only', False)}")
    output.append(f"  仅直飞: {conditions.get('direct_only', True)}")
    output.append("")

    stats = report.get("statistics", {})
    output.append(f"统计结果:")
    output.append(f"  总航班数: {summary.get('total_flights', 0)}")
    output.append(f"  涉及城市数: {summary.get('total_cities', 0)}")
    output.append(f"  价格范围: {summary.get('price_range', 'N/A')}")
    output.append(f"  最低价: ¥{stats.get('min_price', 0)}")
    output.append(f"  平均价: ¥{stats.get('avg_price', 0)}")
    output.append(f"  直飞航班: {stats.get('direct_count', 0)}")
    output.append(f"  周末航班: {stats.get('weekend_count', 0)}")
    output.append("")

    # 按目的地显示
    by_dest = report.get("by_destination", {})
    if by_dest:
        output.append("按目的地明细:")
        output.append("-" * 80)

        for city, city_data in sorted(by_dest.items(), key=lambda x: x[1].get("lowest_price", 99999)):
            output.append(f"\n{city} (共 {city_data['count']} 个航班, 最低 ¥{city_data['lowest_price']}):")
            weekend = city_data.get("weekend_flights", [])
            if weekend:
                output.append(f"  周末可飞: {len(weekend)} 个")

            # 显示最低价的前3个
            sorted_city_flights = sorted(city_data.get("weekend_flights", []) or city_data.get("flights", [])[:3],
                                        key=lambda x: x.get("price", 99999))[:3]
            for f in sorted_city_flights:
                dep_time = f.get("depTime", "N/A")
                if " " in dep_time:
                    dep_time = dep_time.split(" ")[1][:5]
                price = f.get("price", 0)
                flight_no = f.get("flightNo", "N/A")
                airline = f.get("airline", "N/A")
                is_direct = "直飞" if f.get("isDirect") else "经停"
                output.append(f"    {flight_no} {airline} {dep_time} ¥{price} {is_direct}")

    output.append("")
    output.append("=" * 80)

    return "\n".join(output)


# 测试
if __name__ == "__main__":
    aggregator = FlightAggregator()

    # 测试解析
    parser = FlightQueryParser()
    conditions = parser.parse("四川、云南和海南", "上海", "5月1日到5月7日")
    print("解析结果:", json.dumps(conditions, ensure_ascii=False, indent=2))
