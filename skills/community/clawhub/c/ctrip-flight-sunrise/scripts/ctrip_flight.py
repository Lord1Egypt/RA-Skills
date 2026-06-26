#!/usr/bin/env python3
"""
携程机票查询脚本 - 使用真实Cookie获取数据
用于从携程网站搜索航班信息并输出结构化数据
"""

import requests
import json
import re
import sys
import argparse
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any

# 城市代码映射
CITY_CODES = {
    # 一线城市
    "北京": "BJS", "PEK": "BJS", "BJS": "BJS",
    "上海": "SHA", "PVG": "SHA", "SHA": "SHA", "PVG": "SHA",
    "广州": "CAN", "CAN": "CAN",
    "深圳": "SZX", "SZX": "SZX",
    # 四川省 - 机场数据来源: skills/ctrip-flight/data/airports.json
    "成都": "CTU", "CTU": "CTU", "TFU": "TFU",
    "绵阳": "MIG", "MIG": "MIG",
    "广元": "GYS", "GYS": "GYS",
    "达州": "DZH", "DZH": "DZH",
    "泸州": "LZO", "LZO": "LZO",
    "宜宾": "YBP", "YBP": "YBP",
    "南充": "NAO", "NAO": "NAO",
    "攀枝花": "PZI", "PZI": "PZI",
    "西昌": "XIC", "XIC": "XIC",
    "遂宁": "XFS", "XFS": "XFS",
    "九寨沟": "JZH", "JZH": "JZH",
    "稻城": "DCY", "DCY": "DCY",
    "红原": "HDO", "HDO": "HDO",
    "石渠": "SQE", "SQE": "SQE",
    # 其他城市
    "杭州": "HGH", "HGH": "HGH",
    "南京": "NKG", "NKG": "NKG",
    "武汉": "WUH", "WUH": "WUH",
    "西安": "XIY", "XIY": "XIY",
    "重庆": "CKG", "CKG": "CKG",
    "厦门": "XMN", "XMN": "XMN",
    "长沙": "CSX", "CSX": "CSX",
    "昆明": "KMG", "KMG": "KMG",
    "大连": "DLC", "DLC": "DLC",
    "青岛": "TAO", "TAO": "TAO",
    "天津": "TSN", "TSN": "TSN",
    "郑州": "CGO", "CGO": "CGO",
    "福州": "FOC", "FOC": "FOC",
    "沈阳": "SHE", "SHE": "SHE",
    "哈尔滨": "HRB", "HRB": "HRB",
    "南昌": "KHN", "KHN": "KHN",
    "贵阳": "KWE", "KWE": "KWE",
    "太原": "TYN", "TYN": "TYN",
    "济南": "TNA", "TNA": "TNA",
    "石家庄": "SJW", "SJW": "SJW",
    "长春": "CGQ", "CGQ": "CGQ",
    "兰州": "LHW", "LHW": "LHW",
    "南宁": "NNG", "NNG": "NNG",
    "宁波": "NGB", "NGB": "NGB",
    "珠海": "ZUH", "ZUH": "ZUH",
    "海口": "HAK", "HAK": "HAK",
    "乌鲁木齐": "URC", "URC": "URC",
    "拉萨": "LXA", "LXA": "LXA",
    "三亚": "SYX", "SYX": "SYX",
    "丽江": "LJG", "LJG": "LJG",
    "桂林": "KWL", "KWL": "KWL",
}

# 城市对应的主要机场代码映射
CITY_AIRPORTS = {
    "北京": ["PEK", "PKX", "NAY", "BJS"],
    "上海": ["PVG", "SHA", "JGN"],
    "广州": ["CAN"],
    "深圳": ["SZX"],
    "成都": ["CTU", "TFU"],
    "杭州": ["HGH"],
    "南京": ["NKG"],
    "武汉": ["WUH"],
    "西安": ["XIY"],
    "重庆": ["CKG"],
    "厦门": ["XMN"],
    "长沙": ["CSX"],
    "昆明": ["KMG"],
    "贵阳": ["KWE"],
    "大连": ["DLC"],
    "青岛": ["TAO"],
    "天津": ["TSN"],
    "郑州": ["CGO"],
    "福州": ["FOC"],
    "沈阳": ["SHE"],
    "哈尔滨": ["HRB"],
}

# 航空公司代码
AIRLINES = {
    "CA": "中国国航", "MU": "中国东航", "CZ": "中国南航",
    "HU": "海南航空", "MF": "厦门航空", "KN": "中国联航",
    "9C": "春秋航空", "BK": "奥凯航空", "3U": "四川航空",
    "JD": "首都航空", "HO": "吉祥航空", "EU": "成都航空",
    "PN": "西部航空", "G5": "华夏航空", "JR": "幸福航空",
    "NS": "河北航空", "KY": "昆明航空", "FM": "上海航空",
    "SC": "山东航空", "8L": "祥鹏航空", "ZH": "深圳航空",
}


class CtripFlightSearch:
    """携程机票搜索类"""

    def __init__(self, cookie: str = None):
        self.session = requests.Session()
        self.cookie = cookie or "M54SVyflV33bjZLIbe1jqABxPaAadUl80g7W%2FVPYC5QUz%2BhPwoDG2h4P1AY%2BtiwCO4w9XOdGXDIZ8ZuGcmxiwF%2BRsryGRYcGQUA3vZK0CcFBJToWfdMd7bTwnQbml%2F0Q6SI4BCM7LNYedy9axjiFBCXzZq7p69CrtGZm2TuUXGLI4XpyZQirL9KMbFaKwNNY"
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Cookie': f'FVP={self.cookie}',
        })
        self.base_url = "https://flights.ctrip.com"

    def get_city_code(self, city: str) -> str:
        """获取城市代码"""
        city = city.strip().rstrip('的')
        if len(city) == 3 and city.isalpha():
            return city.upper()
        return CITY_CODES.get(city, city.upper())

    def get_city_name(self, code: str) -> str:
        """从代码获取城市名"""
        for name, c in CITY_CODES.items():
            if c == code.upper():
                return name
        return code

    def _is_airport_in_city(self, airport_code: str, city: str) -> bool:
        """检查机场是否属于城市（备用方法，当 depCity/arrCity 不可用时使用）"""
        city_codes = CITY_AIRPORTS.get(city, [])
        return airport_code.upper() in [c.upper() for c in city_codes]

    def _has_flights_for_date(self, flights: List[Dict], target_date: str) -> bool:
        """检查航班列表中是否有匹配目标日期的航班"""
        for f in flights:
            dep_time = f.get('depTime', '')
            if dep_time.startswith(target_date):
                return True
        return False

    def _filter_valid_routes(self, flights: List[Dict], dep_city: str, arr_city: str) -> List[Dict]:
        """过滤出出发地和目的地正确的航班（去除联程航班的中间段）

        通用性设计：优先使用航班数据本身的 depCity/arrCity 字段，
        如果不可用则降级使用 CITY_AIRPORTS 映射表
        """
        valid_flights = []
        dep_city_normalized = dep_city.strip().rstrip('的')

        for f in flights:
            # 优先使用航班数据本身的城市信息（更通用，不依赖预定义映射）
            flight_dep_city = f.get('depCity', '')
            flight_arr_city = f.get('arrCity', '')

            # 如果航班数据包含城市信息，直接使用
            if flight_dep_city and flight_arr_city:
                # 忽略城市名中的"市"字进行比较
                dep_match = dep_city_normalized.replace('市', '') in flight_dep_city.replace('市', '')
                arr_match = arr_city.strip().replace('市', '') in flight_arr_city.replace('市', '')

                if dep_match and arr_match:
                    valid_flights.append(f)
                continue

            # 降级方案：使用机场代码匹配
            dep_code = f.get('depAirportCode', '')
            arr_code = f.get('arrAirportCode', '')

            if self._is_airport_in_city(dep_code, dep_city_normalized) and \
               self._is_airport_in_city(arr_code, arr_city):
                valid_flights.append(f)

        return valid_flights

    def search_flights(self, departure: str, arrival: str, date: str,
                       cabin: str = "y") -> Dict[str, Any]:
        """
        搜索航班

        Args:
            departure: 出发城市
            arrival: 到达城市
            date: 出发日期 YYYY-MM-DD
            cabin: 舱位类型 y=经济舱 c=公务舱 f=头等舱

        Returns:
            搜索结果字典
        """
        dep_code = self.get_city_code(departure)
        arr_code = self.get_city_code(arrival)

        result = {
            "searchParams": {
                "departure": dep_code,
                "departureName": self.get_city_name(dep_code),
                "arrival": arr_code,
                "arrivalName": self.get_city_name(arr_code),
                "date": date,
                "cabin": cabin,
            },
            "flights": [],
            "statistics": {},
            "searchTime": datetime.now().isoformat(),
            "error": None
        }

        try:
            # 构建URL (day 不要补零)
            day = str(int(date.split("-")[2]))  # "01" -> 1

            # 获取出发城市的所有机场代码（支持多机场城市如上海、北京）
            dep_airports = CITY_AIRPORTS.get(departure.strip().rstrip('的'), [dep_code])

            # 尝试多个 day 值，因为携程的 day 参数可能有偏移
            # 先试 day，再试 day+1
            all_flights = []

            for day_offset in [0, 1, 2]:
                current_day = str(int(day) + day_offset)

                # 尝试每个出发机场
                for current_dep_code in dep_airports:
                    # 尝试桌面版
                    url = f"{self.base_url}/booking/{current_dep_code}-{arr_code}-day-{current_day}.html"
                    params = {
                        "depdate": date,
                        "cabin": cabin,
                        "adult": 1,
                        "child": 0,
                        "infant": 0,
                    }

                    # 【优先使用移动版】因为移动版的价格与航班数据绑定更准确
                    mobile_url = f"https://m.ctrip.com/html5/flight/{current_dep_code}-{arr_code}-day-{current_day}.html"
                    mobile_response = self.session.get(
                        mobile_url,
                        headers={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15'},
                        timeout=15
                    )
                    flights = []
                    if mobile_response.status_code == 200:
                        flights = self._parse_mobile_flights(mobile_response.text)

                    # 如果移动版没有数据，尝试桌面版
                    if not flights:
                        response = self.session.get(url, params=params, timeout=15)
                        response.raise_for_status()
                        flights = self._parse_html_flights(response.text)

                    if flights:
                        all_flights.extend(flights)

                # 如果已经找到了目标日期的航班，停止尝试
                if self._has_flights_for_date(all_flights, date):
                    break

            if all_flights:
                # 过滤出从出发城市飞往目的地城市的航班（去除联程航班的中间段）
                valid_flights = self._filter_valid_routes(all_flights, departure, arrival)
                # 进一步过滤，只保留匹配目标日期的航班
                valid_flights = [f for f in valid_flights if f.get('depTime', '').startswith(date)]
                result["flights"] = valid_flights
                result["statistics"] = self._calculate_statistics(valid_flights)
                if not valid_flights:
                    result["error"] = "未找到航班数据"
            else:
                result["error"] = "未找到航班数据"

        except requests.RequestException as e:
            result["error"] = f"网络请求失败: {str(e)}"
        except Exception as e:
            result["error"] = f"解析失败: {str(e)}"

        return result

    def _parse_html_flights(self, html: str) -> List[Dict]:
        """从HTML中解析航班数据（支持桌面版）"""
        flights = []

        # 查找script标签中的JSON数据
        scripts = re.findall(r'<script[^>]*>([^<]+)</script>', html)

        all_flights = []
        all_prices = []

        for script in scripts:
            try:
                data = json.loads(script.strip())
                # 提取所有航班
                all_flights.extend(self._extract_flights(data))
                # 提取所有价格
                all_prices.extend(self._extract_prices(data))
            except (json.JSONDecodeError, Exception):
                continue

        # 合并航班和价格（按顺序对应）
        for i, flight in enumerate(all_flights):
            if i < len(all_prices):
                flight["price"] = all_prices[i]
            else:
                flight["price"] = 0
            flights.append(flight)

        return flights

    def _parse_mobile_flights(self, html: str) -> List[Dict]:
        """从移动版HTML中解析航班数据"""
        flights = []

        # 提取 transitCount, dfltnoFlgno (主航班号), price
        # 格式: "transitCount":0,"dfltnoFlgno":"9C7117","policy":{"price":573}
        transit_price_pattern = r'"transitCount":(\d+).*?"dfltnoFlgno":"([^"]+)","policy":\{"price":(\d+)'
        transit_prices = re.findall(transit_price_pattern, html, re.DOTALL)

        # 建立主航班号到 (transitCount, price) 的映射
        main_flight_info = {}
        for tc, fn, price in transit_prices:
            if fn not in main_flight_info:
                main_flight_info[fn] = (int(tc), int(price))

        # 提取每个航段的详细信息
        # 每个航班详情包含 flightNo, dtime, atime, dport, aport, airline, craft
        flight_blocks = re.findall(
            r'"flightNo":"([^"]+)","dtime":"([^"]+)","atime":"([^"]+)","duration":(\d+).*?"airline":\{"code":"([^"]*)","name":"([^"]*)"[^}]*\}.*?"dport":\{"code":"([^"]*)","name":"([^"]*)","cityName":"([^"]*)","cityCode":"([^"]*)"[^}]*\}.*?"aport":\{"code":"([^"]*)","name":"([^"]*)","cityName":"([^"]*)","cityCode":"([^"]*)"[^}]*\}.*?"craft":\{"name":"([^"]*)"',
            html, re.DOTALL
        )

        # 按主航班号组织航段
        # 对于直飞航班：只有一段，主航班号=该段航班号
        # 对于联程航班：有多段，主航班号=第一段航班号
        segments_by_main = {}
        for block in flight_blocks:
            fn = block[0]
            segments_by_main.setdefault(fn, []).append({
                "flightNo": fn,
                "depTime": block[1],
                "arrTime": block[2],
                "duration": int(block[3]),
                "airlineCode": block[4],
                "airline": block[5],
                "depAirportCode": block[6],
                "depAirport": block[7],
                "depCity": block[8],
                "arrAirportCode": block[10],
                "arrAirport": block[11],
                "arrCity": block[12],
                "planeType": block[13],
            })

        # 重组为完整航班
        for main_fn, (tc, price) in main_flight_info.items():
            segments = segments_by_main.get(main_fn, [])
            if not segments:
                continue

            if tc == 0:
                # 直飞航班：只有一段
                seg = segments[0]
                flights.append({
                    "flightNo": main_fn,
                    "airlineCode": seg["airlineCode"],
                    "airline": seg["airline"],
                    "depTime": seg["depTime"],
                    "arrTime": seg["arrTime"],
                    "duration": seg["duration"],
                    "depAirport": seg["depAirport"],
                    "depAirportCode": seg["depAirportCode"],
                    "depCity": seg.get("depCity", ""),
                    "arrAirport": seg["arrAirport"],
                    "arrAirportCode": seg["arrAirportCode"],
                    "arrCity": seg.get("arrCity", ""),
                    "planeType": seg["planeType"],
                    "stops": 0,
                    "isDirect": True,
                    "price": price,
                })
            else:
                # 联程航班：取第一段作为出发，最后一段作为到达
                first_seg = segments[0]
                last_seg = segments[-1]
                total_duration = sum(int(s["duration"]) for s in segments)

                flights.append({
                    "flightNo": main_fn,
                    "airlineCode": first_seg["airlineCode"],
                    "airline": first_seg["airline"],
                    "depTime": first_seg["depTime"],
                    "arrTime": last_seg["arrTime"],
                    "duration": total_duration,
                    "depAirport": first_seg["depAirport"],
                    "depAirportCode": first_seg["depAirportCode"],
                    "depCity": first_seg.get("depCity", ""),
                    "arrAirport": last_seg["arrAirport"],
                    "arrAirportCode": last_seg["arrAirportCode"],
                    "arrCity": last_seg.get("arrCity", ""),
                    "planeType": first_seg["planeType"],
                    "stops": tc,
                    "isDirect": False,
                    "price": price,
                })

        return flights

    def _extract_flights(self, obj, flights=None) -> List[Dict]:
        """递归提取所有航班"""
        if flights is None:
            flights = []

        if isinstance(obj, dict):
            if 'flightNo' in obj and 'dtime' in obj and 'airline' in obj:
                flight = {
                    "flightNo": obj.get('flightNo', ''),
                    "airline": obj.get('airline', {}).get('name', ''),
                    "airlineCode": obj.get('airline', {}).get('code', ''),
                    "depTime": obj.get('dtime', ''),
                    "arrTime": obj.get('atime', ''),
                    "duration": obj.get('duration', 0),
                    "depAirport": obj.get('dport', {}).get('name', ''),
                    "depAirportCode": obj.get('dport', {}).get('code', ''),
                    "depCity": obj.get('dport', {}).get('cityName', ''),
                    "arrAirport": obj.get('aport', {}).get('name', ''),
                    "arrAirportCode": obj.get('aport', {}).get('code', ''),
                    "arrCity": obj.get('aport', {}).get('cityName', ''),
                    "planeType": obj.get('craft', {}).get('name', ''),
                    "stops": len(obj.get('stops', [])),
                    "isDirect": len(obj.get('stops', [])) == 0,
                }
                flights.append(flight)
            for v in obj.values():
                if isinstance(v, (dict, list)):
                    self._extract_flights(v, flights)
        elif isinstance(obj, list):
            for item in obj:
                if isinstance(item, (dict, list)):
                    self._extract_flights(item, flights)

        return flights

    def _extract_prices(self, obj, prices=None) -> List[int]:
        """递归提取所有价格"""
        if prices is None:
            prices = []

        if isinstance(obj, dict):
            if 'price' in obj and 'departDate' in obj:
                prices.append(int(obj['price']))
            for v in obj.values():
                if isinstance(v, (dict, list)):
                    self._extract_prices(v, prices)
        elif isinstance(obj, list):
            for item in obj:
                if isinstance(item, (dict, list)):
                    self._extract_prices(item, prices)

        return prices

    def _calculate_statistics(self, flights: List[Dict]) -> Dict:
        """计算统计数据"""
        if not flights:
            return {}

        prices = [f['price'] for f in flights if f.get('price', 0) > 0]
        direct_flights = [f for f in flights if f.get('isDirect', False)]

        stats = {
            "totalFlights": len(flights),
            "directFlights": len(direct_flights),
            "transitFlights": len(flights) - len(direct_flights),
        }

        if prices:
            stats["lowestPrice"] = min(prices)
            stats["highestPrice"] = max(prices)
            stats["avgPrice"] = int(sum(prices) / len(prices))

        return stats

    def format_flights(self, result: Dict) -> str:
        """格式化输出航班列表"""
        if result.get("error"):
            return f"错误: {result['error']}"

        flights = result.get("flights", [])
        stats = result.get("statistics", {})

        if not flights:
            return "未找到航班"

        params = result.get("searchParams", {})
        output = []
        output.append("=" * 90)
        output.append(f"  {params.get('departureName', '')} → {params.get('arrivalName', '')}  "
                     f"日期: {params.get('date', '')}")
        output.append("=" * 90)

        # 统计信息
        if stats:
            output.append(f"\n共 {stats.get('totalFlights', 0)} 个航班  "
                         f"直飞: {stats.get('directFlights', 0)}  "
                         f"价格: ¥{stats.get('lowestPrice', 'N/A')} - ¥{stats.get('highestPrice', 'N/A')}")
        output.append("")

        # 表头
        output.append(f"{'航班号':<10} {'航空公司':<10} {'起飞时间':<18} {'到达时间':<18} {'飞行':<8} {'类型':<10} {'价格':<8}")
        output.append("-" * 90)

        # 按价格排序
        sorted_flights = sorted(flights, key=lambda x: x.get('price', 0) or 999999)

        for f in sorted_flights:
            dep_time = f.get('depTime', 'N/A')
            arr_time = f.get('arrTime', 'N/A')
            if ' ' in dep_time:
                dep_time = dep_time.split(' ')[1][:5]
            if ' ' in arr_time:
                arr_time = arr_time.split(' ')[1][:5]

            duration = f.get('duration', 0)
            if isinstance(duration, int):
                duration = f"{duration}min"

            stops = f.get('stops', 0)
            flight_type = "直飞" if stops == 0 else f"经停{stops}次"

            price = f.get('price', 0)
            price_str = f"¥{price}" if price > 0 else "N/A"

            output.append(f"{f.get('flightNo', ''):<10} {f.get('airline', ''):<10} "
                         f"{dep_time:<18} {arr_time:<18} {duration:<8} {flight_type:<10} {price_str:<8}")

        output.append("")
        return "\n".join(output)

    def compare_dates(self, departure: str, arrival: str, dates: List[str]) -> Dict:
        """多日期价格对比"""
        results = {
            "departure": departure,
            "arrival": arrival,
            "dates": [],
            "error": None
        }

        for date in dates:
            result = self.search_flights(departure, arrival, date)
            if result['flights']:
                stats = result['statistics']
                results['dates'].append({
                    "date": date,
                    "lowestPrice": stats.get('lowestPrice'),
                    "avgPrice": stats.get('avgPrice'),
                    "totalFlights": stats.get('totalFlights'),
                    "directFlights": stats.get('directFlights'),
                })

        if not results['dates']:
            results['error'] = "未找到航班数据"

        return results

    def format_compare(self, result: Dict) -> str:
        """格式化多日期对比输出"""
        if result.get("error"):
            return f"错误: {result['error']}"

        dates = result.get("dates", [])
        if not dates:
            return "未找到对比数据"

        params = result.get("departure", ""), result.get("arrival", "")
        output = []
        output.append("=" * 60)
        output.append(f"  价格对比: {params[0]} → {params[1]}")
        output.append("=" * 60)
        output.append("")
        output.append(f"{'日期':<15} {'最低价':<12} {'均价':<12} {'航班数':<10} {'直飞':<10}")
        output.append("-" * 60)

        for d in dates:
            output.append(f"{d['date']:<15} ¥{d.get('lowestPrice', 'N/A'):<10} "
                        f"¥{d.get('avgPrice', 'N/A'):<10} {d.get('totalFlights', 0):<10} {d.get('directFlights', 0)}")

        # 找出最低价日期
        if dates:
            cheapest = min(dates, key=lambda x: x.get('lowestPrice', 999999))
            output.append("")
            output.append(f"💡 最优惠: {cheapest['date']} 最低价 ¥{cheapest.get('lowestPrice')}")

        return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description='携程机票搜索')
    parser.add_argument('--departure', '-d', required=True, help='出发城市')
    parser.add_argument('--arrival', '-a', required=True, help='到达城市')
    parser.add_argument('--date', '-t', required=True, help='出发日期 YYYY-MM-DD')
    parser.add_argument('--cabin', '-c', default='y', choices=['y', 'c', 'f'],
                        help='舱位类型: y=经济舱 c=公务舱 f=头等舱')
    parser.add_argument('--output', '-o', help='输出JSON文件路径')
    parser.add_argument('--compare', help='多日期对比，逗号分隔的日期列表')

    args = parser.parse_args()

    searcher = CtripFlightSearch()

    if args.compare:
        dates = [d.strip() for d in args.compare.split(',')]
        result = searcher.compare_dates(args.departure, args.arrival, dates)
        print(searcher.format_compare(result))
    else:
        result = searcher.search_flights(args.departure, args.arrival, args.date, args.cabin)
        print(searcher.format_flights(result))

        # 如果有统计数据，输出JSON统计
        if result.get('statistics'):
            print("\n结构化数据:")
            print(json.dumps(result, ensure_ascii=False, indent=2))

    # 输出结果到文件
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n结果已保存到: {args.output}")


if __name__ == "__main__":
    main()
