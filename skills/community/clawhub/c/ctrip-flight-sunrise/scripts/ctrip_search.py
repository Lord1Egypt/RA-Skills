#!/usr/bin/env python3
"""
携程机票搜索脚本
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
    # 二线城市
    "成都": "CTU", "CTU": "CTU",
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
    "常州": "CZX", "CZX": "CZX",
    "温州": "WNZ", "WNZ": "WNZ",
    "珠海": "ZUH", "ZUH": "ZUH",
    "海口": "HAK", "HAK": "HAK",
    "兰州": "LHW", "LHW": "LHW",
    "无锡": "WUX", "WUX": "WUX",
    "南宁": "NNG", "NNG": "NNG",
    "徐州": "XUZ", "XUZ": "XUZ",
    "宁波": "NGB", "NGB": "NGB",
    "佛山": "FUO", "FUO": "FUO",
    "苏州": "SZV", "SZV": "SZV",
    "东莞": "DGM", "DGM": "DGM",
    "无锡": "WUX", "WUX": "WUX",
}

# 航空公司代码
AIRLINES = {
    "CA": "中国国航",
    "MU": "中国东航",
    "CZ": "中国南航",
    "HU": "海南航空",
    "MF": "厦门航空",
    "KN": "中国联航",
    "9C": "春秋航空",
    "BK": "奥凯航空",
    "3U": "四川航空",
    "JD": "首都航空",
    "HO": "吉祥航空",
    "EU": "成都航空",
    "PN": "西部航空",
    "G5": "华夏航空",
    "JR": "幸福航空",
    "NS": "河北航空",
    "KY": "昆明航空",
    "ZD": "东北航空",
    "5J": "宿务航空",
    "TG": "泰国航空",
    "NH": "全日空",
    "JL": "日本航空",
    "KE": "大韩航空",
    "OZ": "韩亚航空",
    "SQ": "新加坡航空",
    "MH": "马来西亚航空",
}

# 舱位类型
CABIN_TYPES = {
    "y": "经济舱",
    "c": "公务舱",
    "f": "头等舱",
    "Y": "经济舱",
    "C": "公务舱",
    "F": "头等舱",
}


class CtripFlightSearch:
    """携程机票搜索类"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        self.base_url = "https://flights.ctrip.com"

    def get_city_code(self, city: str) -> str:
        """获取城市代码"""
        if len(city) == 3 and city.isalpha():
            return city.upper()
        return CITY_CODES.get(city, city.upper())

    def search_flights(self, departure: str, arrival: str, date: str,
                       cabin: str = "y", adult: int = 1) -> Dict[str, Any]:
        """
        搜索航班

        Args:
            departure: 出发城市
            arrival: 到达城市
            date: 出发日期 YYYY-MM-DD
            cabin: 舱位类型 y=经济舱 c=公务舱 f=头等舱
            adult: 成人数量

        Returns:
            搜索结果字典
        """
        dep_code = self.get_city_code(departure)
        arr_code = self.get_city_code(arrival)

        result = {
            "searchParams": {
                "departure": dep_code,
                "departureName": departure,
                "arrival": arr_code,
                "arrivalName": arrival,
                "date": date,
                "cabin": cabin,
                "adult": adult,
            },
            "flights": [],
            "statistics": {},
            "searchTime": datetime.now().isoformat(),
            "error": None
        }

        try:
            # 尝试方式1: 直接请求booking页面
            url = f"{self.base_url}/booking/{dep_code}-{arr_code}-day-1.html"
            params = {
                "depdate": date,
                "cabin": cabin,
                "adult": adult,
                "child": 0,
                "infant": 0,
            }

            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()

            # 解析页面中的航班数据
            flights = self._parse_html_flights(response.text)

            if flights:
                result["flights"] = flights
                result["statistics"] = self._calculate_statistics(flights)
            else:
                # 尝试方式2: 尝试API调用
                flights = self._try_api_search(dep_code, arr_code, date, cabin, adult)
                if flights:
                    result["flights"] = flights
                    result["statistics"] = self._calculate_statistics(flights)
                else:
                    result["error"] = "未找到航班数据，请尝试其他日期或航线"

        except requests.RequestException as e:
            result["error"] = f"网络请求失败: {str(e)}"
        except Exception as e:
            result["error"] = f"解析失败: {str(e)}"

        return result

    def _parse_html_flights(self, html: str) -> List[Dict]:
        """从HTML中解析航班数据"""
        flights = []

        # 尝试从window.__INITIAL_STATE__中提取数据
        initial_state_match = re.search(
            r'window\.__INITIAL_STATE__\s*=\s*({.*?})\s*;?\s*(?:</script|$)',
            html,
            re.DOTALL
        )

        if initial_state_match:
            try:
                data = json.loads(initial_state_match.group(1))
                # 尝试解析数据
                flights = self._extract_from_state(data)
            except json.JSONDecodeError:
                pass

        # 尝试从__OoO__中提取数据
        ooo_match = re.search(r'window\.__OoO__\s*=\s*({.*?})\s*;?\s*(?:</script|$)', html, re.DOTALL)
        if ooo_match and not flights:
            try:
                data = json.loads(ooo_match.group(1))
                flights = self._extract_from_ooo(data)
            except:
                pass

        return flights

    def _extract_from_state(self, data: Dict) -> List[Dict]:
        """从INITIAL_STATE中提取航班数据"""
        flights = []

        # 递归搜索flightList或类似的key
        def search_flights(obj):
            if isinstance(obj, dict):
                if 'flightList' in obj:
                    return obj['flightList']
                for v in obj.values():
                    result = search_flights(v)
                    if result:
                        return result
            elif isinstance(obj, list):
                for item in obj:
                    result = search_flights(item)
                    if result:
                        return result
            return None

        flight_list = search_flights(data)
        if flight_list and isinstance(flight_list, list):
            for f in flight_list:
                flight = self._parse_flight_item(f)
                if flight:
                    flights.append(flight)

        return flights

    def _extract_from_ooo(self, data: Dict) -> List[Dict]:
        """从__OoO__数据中提取航班信息"""
        flights = []

        def search_deep(obj, depth=0):
            if depth > 10:
                return
            if isinstance(obj, dict):
                if 'airlineName' in obj or 'flightNo' in obj:
                    flight = self._parse_flight_item(obj)
                    if flight:
                        flights.append(flight)
                for v in obj.values():
                    search_deep(v, depth + 1)
            elif isinstance(obj, list):
                for item in obj:
                    search_deep(item, depth + 1)

        search_deep(data)
        return flights

    def _parse_flight_item(self, item: Dict) -> Optional[Dict]:
        """解析单个航班数据项"""
        try:
            # 提取航空公司信息
            airline_code = item.get('airlineCode', item.get('airline', 'UNKNOWN'))
            airline_name = AIRLINES.get(airline_code, airline_code)

            # 提取航班号
            flight_no = item.get('flightNo', item.get('flightNumber', ''))

            # 提取时间信息
            dep_time = item.get('depTime', item.get('departureTime', '00:00'))
            arr_time = item.get('arrTime', item.get('arrivalTime', '00:00'))

            # 提取机场信息
            dep_airport = item.get('depAirport', item.get('departureAirport', ''))
            arr_airport = item.get('arrAirport', item.get('arrivalAirport', ''))

            # 提取价格
            price = item.get('price', item.get('adultPrice', 0))
            tax = item.get('tax', item.get('机场税', 0))
            total_price = price + tax

            # 提取航班类型
            stops = item.get('stops', item.get('stopCount', 0))
            is_direct = stops == 0 or stops == "0"

            # 飞行时长
            duration = item.get('duration', item.get('flyTime', ''))

            # 机型
            plane_type = item.get('planeType', item.get('aircraft', ''))

            # 剩余座位
            seats_left = item.get('seatsLeft', item.get('remainSeats', 0))

            return {
                "airline": airline_name,
                "airlineCode": airline_code,
                "flightNo": flight_no,
                "planeType": plane_type,
                "depTime": dep_time,
                "arrTime": arr_time,
                "depAirport": dep_airport,
                "arrAirport": arr_airport,
                "duration": duration,
                "isDirect": is_direct,
                "stops": int(stops) if stops != "0" else 0,
                "price": int(price),
                "tax": int(tax),
                "totalPrice": int(total_price),
                "seatsLeft": int(seats_left) if seats_left else None
            }
        except Exception as e:
            return None

    def _try_api_search(self, dep_code: str, arr_code: str, date: str,
                        cabin: str, adult: int) -> List[Dict]:
        """尝试API方式搜索"""
        flights = []

        # Ctrip的搜索API端点
        api_url = f"{self.base_url}/f Domestic/Search"

        payload = {
            "searchIndex": 1,
            "flightWay": "Oneway",
            "classType": "ALL" if cabin == "y" else cabin.upper(),
            "hasChild": False,
            "hasBaby": False,
            "airportParams": [{
                "dcity": dep_code,
                "acity": arr_code,
                "dcityname": dep_code,
                "acityname": arr_code,
                "date": date
            }]
        }

        try:
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Referer': f'{self.base_url}/',
                'X-Requested-With': 'XMLHttpRequest'
            }

            response = self.session.post(api_url, json=payload, headers=headers, timeout=10)

            if response.status_code == 200:
                try:
                    data = response.json()
                    if 'flightList' in data:
                        for f in data['flightList']:
                            flight = self._parse_flight_item(f)
                            if flight:
                                flights.append(flight)
                except json.JSONDecodeError:
                    pass
        except:
            pass

        return flights

    def _calculate_statistics(self, flights: List[Dict]) -> Dict:
        """计算统计数据"""
        if not flights:
            return {}

        prices = [f['price'] for f in flights]
        direct_flights = [f for f in flights if f['isDirect']]

        return {
            "totalFlights": len(flights),
            "directFlights": len(direct_flights),
            "transitFlights": len(flights) - len(direct_flights),
            "lowestPrice": min(prices),
            "highestPrice": max(prices),
            "avgPrice": int(sum(prices) / len(prices)),
        }

    def compare_prices(self, departure: str, arrival: str, dates: List[str],
                       cabin: str = "y") -> Dict:
        """多日期价格对比"""
        results = {
            "departure": departure,
            "arrival": arrival,
            "dates": []
        }

        for date in dates:
            result = self.search_flights(departure, arrival, date, cabin)
            if result['flights']:
                stats = result['statistics']
                results['dates'].append({
                    "date": date,
                    "lowestPrice": stats.get('lowestPrice'),
                    "avgPrice": stats.get('avgPrice'),
                    "totalFlights": stats.get('totalFlights'),
                    "directFlights": stats.get('directFlights'),
                })

        return results


def main():
    parser = argparse.ArgumentParser(description='携程机票搜索')
    parser.add_argument('--departure', '-d', required=True, help='出发城市')
    parser.add_argument('--arrival', '-a', required=True, help='到达城市')
    parser.add_argument('--date', '-t', required=True, help='出发日期 YYYY-MM-DD')
    parser.add_argument('--cabin', '-c', default='y', choices=['y', 'c', 'f'],
                        help='舱位类型: y=经济舱 c=公务舱 f=头等舱')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--compare', help='多日期对比，逗号分隔的日期列表')

    args = parser.parse_args()

    searcher = CtripFlightSearch()

    if args.compare:
        dates = [d.strip() for d in args.compare.split(',')]
        result = searcher.compare_prices(args.departure, args.arrival, dates, args.cabin)
    else:
        result = searcher.search_flights(args.departure, args.arrival, args.date, args.cabin)

    # 输出结果
    output = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"结果已保存到: {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
