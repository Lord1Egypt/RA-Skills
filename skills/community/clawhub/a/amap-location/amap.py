#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
高德地图 Location Skill - 路径规划、POI 搜索等
"""

import argparse
import sys
import os
import json
import urllib.request
import urllib.parse
from datetime import datetime

# 加载 API Key
API_KEY = os.getenv("AMAP_API_KEY")
if not API_KEY:
    print("❌ 错误：请设置环境变量 AMAP_API_KEY")
    sys.exit(1)

BASE_URL = "https://restapi.amap.com/v3"

def make_request(url, params=None):
    """发送 HTTP 请求"""
    if params is None:
        params = {}
    params['key'] = API_KEY
    
    query_string = urllib.parse.urlencode(params)
    full_url = f"{url}?{query_string}"
    
    try:
        with urllib.request.urlopen(full_url, timeout=10) as response:
            data = response.read().decode('utf-8')
            return json.loads(data)
    except Exception as e:
        return {"status": "0", "info": f"请求失败：{str(e)}"}

def geocode(address):
    """地理编码：地址转坐标"""
    url = f"{BASE_URL}/geocode/geo"
    params = {
        'address': address,
        'output': 'json'
    }
    result = make_request(url, params)
    if result.get('status') == '1' and result.get('geocodes'):
        geocode = result['geocodes'][0]
        return {
            'address': geocode.get('formatted_address', ''),
            'location': geocode.get('location', '')
        }
    return None

def regeocode(location):
    """逆地理编码：坐标转地址"""
    url = f"{BASE_URL}/geocode/regeo"
    params = {
        'location': location,
        'output': 'json'
    }
    result = make_request(url, params)
    if result.get('status') == '1':
        regeo = result.get('regeocode', {})
        return regeo.get('formatted_address', '')
    return None

def direction_driving(origin, destination):
    """驾车路径规划"""
    url = f"{BASE_URL}/direction/driving"
    params = {
        'origin': origin,
        'destination': destination,
        'output': 'json',
        'extensions': 'all'
    }
    result = make_request(url, params)
    if result.get('status') == '1' and result.get('route'):
        route = result['route']
        paths = route.get('paths', [])
        if paths:
            path = paths[0]  # 推荐路线
            return {
                'distance': path.get('distance', '0'),
                'duration': path.get('duration', '0'),
                'strategy': path.get('strategy', ''),
                'steps': path.get('steps', [])
            }
    return None

def direction_walk(origin, destination):
    """步行路径规划"""
    url = f"{BASE_URL}/direction/walking"
    params = {
        'origin': origin,
        'destination': destination,
        'output': 'json'
    }
    result = make_request(url, params)
    if result.get('status') == '1' and result.get('route'):
        route = result['route']
        paths = route.get('paths', [])
        if paths:
            path = paths[0]
            return {
                'distance': path.get('distance', '0'),
                'duration': path.get('duration', '0'),
                'steps': path.get('steps', [])
            }
    return None

def direction_transit(origin, destination):
    """公交路径规划"""
    url = f"{BASE_URL}/direction/transit/integrated"
    params = {
        'origin': origin,
        'destination': destination,
        'output': 'json',
        'city': '广州'
    }
    result = make_request(url, params)
    if result.get('status') == '1' and result.get('route'):
        route = result['route']
        transit = route.get('transits', [])
        if transit:
            t = transit[0]
            return {
                'distance': t.get('distance', '0'),
                'duration': t.get('duration', '0'),
                'transit_lines': t.get('transits', [])
            }
    return None

def search_poi(keywords, location=None, types='', radius=1000):
    """POI 搜索（美食、酒店等）"""
    url = f"{BASE_URL}/place/text"
    params = {
        'keywords': keywords,
        'output': 'json',
        'radius': radius,
        'offset': 10,
        'page': 1,
        'extensions': 'all'
    }
    if location:
        params['location'] = location
    if types:
        params['types'] = types
    
    result = make_request(url, params)
    if result.get('status') == '1':
        pois = result.get('pois', [])
        return pois
    return []

def format_distance(meters):
    """格式化距离"""
    meters = float(meters)
    if meters >= 1000:
        return f"{meters/1000:.1f}公里"
    return f"{int(meters)}米"

def format_duration(seconds):
    """格式化时间"""
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    
    if hours > 0:
        return f"{hours}小时{minutes}分钟"
    return f"{minutes}分钟"

def main():
    parser = argparse.ArgumentParser(description="高德地图 Location Skill")
    subparsers = parser.add_subparsers(dest='command', help='命令类型')
    
    # geocode 命令
    geo_parser = subparsers.add_parser('geocode', help='地理编码')
    geo_parser.add_argument('--address', required=True, help='地址')
    
    # regeocode 命令
    regeo_parser = subparsers.add_parser('regeocode', help='逆地理编码')
    regeo_parser.add_argument('--location', required=True, help='坐标 (lng,lat)')
    
    # driving 命令
    drive_parser = subparsers.add_parser('driving', help='驾车路径规划')
    drive_parser.add_argument('--origin', required=True, help='起点坐标')
    drive_parser.add_argument('--destination', required=True, help='终点坐标')
    
    # walking 命令
    walk_parser = subparsers.add_parser('walking', help='步行路径规划')
    walk_parser.add_argument('--origin', required=True, help='起点坐标')
    walk_parser.add_argument('--destination', required=True, help='终点坐标')
    
    # transit 命令
    transit_parser = subparsers.add_parser('transit', help='公交路径规划')
    transit_parser.add_argument('--origin', required=True, help='起点坐标')
    transit_parser.add_argument('--destination', required=True, help='终点坐标')
    
    # search 命令
    search_parser = subparsers.add_parser('search', help='POI 搜索')
    search_parser.add_argument('--keywords', required=True, help='搜索关键词')
    search_parser.add_argument('--location', help='中心坐标')
    search_parser.add_argument('--types', help='POI 类型')
    search_parser.add_argument('--radius', type=int, default=1000, help='搜索半径 (米)')
    
    args = parser.parse_args()
    
    if args.command == 'geocode':
        result = geocode(args.address)
        if result:
            print(f"📍 地址：{result['address']}")
            print(f"🗺️  坐标：{result['location']}")
        else:
            print("❌ 地理编码失败")
    
    elif args.command == 'regeocode':
        result = regeocode(args.location)
        if result:
            print(f"📍 地址：{result}")
        else:
            print("❌ 逆地理编码失败")
    
    elif args.command == 'driving':
        result = direction_driving(args.origin, args.destination)
        if result:
            print(f"🚗 驾车路线")
            print(f"   距离：{format_distance(result['distance'])}")
            print(f"   预计：{format_duration(result['duration'])}")
        else:
            print("❌ 路径规划失败")
    
    elif args.command == 'walking':
        result = direction_walk(args.origin, args.destination)
        if result:
            print(f"🚶 步行路线")
            print(f"   距离：{format_distance(result['distance'])}")
            print(f"   预计：{format_duration(result['duration'])}")
        else:
            print("❌ 路径规划失败")
    
    elif args.command == 'transit':
        result = direction_transit(args.origin, args.destination)
        if result:
            print(f"🚌 公交路线")
            print(f"   距离：{format_distance(result['distance'])}")
            print(f"   预计：{format_duration(result['duration'])}")
        else:
            print("❌ 路径规划失败")
    
    elif args.command == 'search':
        results = search_poi(args.keywords, args.location, args.types, args.radius)
        if results:
            print(f"📊 找到 {len(results)} 个结果:")
            for i, poi in enumerate(results[:5], 1):
                print(f"\n{i}. {poi.get('name', '未知')}")
                print(f"   地址：{poi.get('address', '未知')}")
                if poi.get('distance'):
                    print(f"   距离：{poi.get('distance')}米")
                if poi.get('tel'):
                    print(f"   电话：{poi.get('tel')}")
        else:
            print("❌ 未找到结果")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
