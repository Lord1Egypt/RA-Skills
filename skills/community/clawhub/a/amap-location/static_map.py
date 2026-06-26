#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
高德地图静态地图生成器（带自定义标记）
"""

import argparse
import sys
import os
import json
import urllib.request
import urllib.parse
import io
from datetime import datetime

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("❌ 错误：请安装 PIL/Pillow: pip install Pillow")
    sys.exit(1)

# 加载 API Key
API_KEY = os.getenv("AMAP_API_KEY")
if not API_KEY:
    print("❌ 错误：请设置环境变量 AMAP_API_KEY")
    sys.exit(1)

BASE_URL = "https://restapi.amap.com/v3"
STATIC_MAP_URL = "https://restapi.amap.com/v3/staticmap"

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

def search_poi(keywords, location=None, types='', radius=1000, offset=10):
    """POI 搜索"""
    url = f"{BASE_URL}/place/text"
    params = {
        'keywords': keywords,
        'output': 'json',
        'radius': radius,
        'offset': offset,
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

def calculate_distance(loc1, loc2):
    """计算两点距离（简化版）"""
    lat1, lng1 = map(float, loc1.split(','))
    lat2, lng2 = map(float, loc2.split(','))
    
    lat_diff = abs(lat1 - lat2) * 111000
    lng_diff = abs(lng1 - lng2) * 85000
    
    return ((lat_diff ** 2) + (lng_diff ** 2)) ** 0.5

def calculate_bounds(user_location, poi_list):
    """计算包含所有点的边界和中心点 - 以用户位置为中心"""
    user_lng, user_lat = map(float, user_location.split(','))
    
    # 以用户位置为中心（这样用户位置一定在图片正中心）
    center = f"{user_lng},{user_lat}"
    center_lng, center_lat = user_lng, user_lat
    
    # 收集所有点计算边界
    all_lats = [user_lat]
    all_lngs = [user_lng]
    
    for poi in poi_list:
        poi_lng, poi_lat = map(float, poi['location'].split(','))
        all_lats.append(poi_lat)
        all_lngs.append(poi_lng)
    
    min_lat, max_lat = min(all_lats), max(all_lats)
    min_lng, max_lng = min(all_lngs), max(all_lngs)
    
    # 计算跨度
    lat_diff = max_lat - min_lat
    lng_diff = max_lng - min_lng
    
    # 使用更大的 zoom 值，显示范围更小
    if lat_diff > 0.05 or lng_diff > 0.05:
        zoom = 13
    elif lat_diff > 0.02 or lng_diff > 0.02:
        zoom = 14
    elif lat_diff > 0.01 or lng_diff > 0.01:
        zoom = 15
    elif lat_diff > 0.005 or lng_diff > 0.005:
        zoom = 16
    else:
        zoom = 17  # 更近的距离用更大 zoom
    
    return center, zoom, (min_lng, max_lng, min_lat, max_lat)

def download_base_map(center, zoom, width, height):
    """下载基础地图"""
    params = {
        'location': center,
        'zoom': zoom,
        'size': f'{width}*{height}',
        'scale': 2
    }
    
    query_string = urllib.parse.urlencode(params)
    map_url = f"{STATIC_MAP_URL}?{query_string}&key={API_KEY}"
    
    try:
        with urllib.request.urlopen(map_url, timeout=15) as response:
            img_data = response.read()
            if img_data[:8] == b'\x89PNG\r\n\x1a\n' or img_data[:2] == b'\xff\xd8':
                return Image.open(io.BytesIO(img_data))
            else:
                print(f"❌ 无效的地图图片：{img_data[:100]}")
                return None
    except Exception as e:
        print(f"❌ 地图下载失败：{str(e)}")
        return None

def lng_lat_to_pixel(lng, lat, center_lng, center_lat, zoom, width, height):
    """将经纬度转换为像素坐标（墨卡托投影）"""
    import math
    
    # 墨卡托投影 X
    def mercator_x(lng):
        return (lng + 180) / 360
    
    # 墨卡托投影 Y
    def mercator_y(lat):
        lat_rad = math.radians(lat)
        return (1 - math.log(math.tan(lat_rad) + 1/math.cos(lat_rad)) / math.pi) / 2
    
    # 计算中心点的瓦片坐标
    center_x = mercator_x(center_lng) * (2 ** zoom)
    center_y = mercator_y(center_lat) * (2 ** zoom)
    
    # 计算目标点的瓦片坐标
    x = mercator_x(lng) * (2 ** zoom)
    y = mercator_y(lat) * (2 ** zoom)
    
    # 每个瓦片的像素数（scale=2）
    tile_size = 256 * 2
    
    # 转换为像素坐标
    pixel_x = (x - center_x) * tile_size + width / 2
    pixel_y = (y - center_y) * tile_size + height / 2
    
    return int(pixel_x), int(pixel_y)

def draw_markers(img, user_location, poi_list, center_lng, center_lat, zoom):
    """在地图上绘制标记"""
    draw = ImageDraw.Draw(img)
    width, height = img.size
    
    # 尝试加载字体
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    except:
        font = ImageFont.load_default()
        small_font = font
    
    # 绘制 POI 标记（简洁无阴影）
    poi_colors = ['#FF1744', '#FF9100', '#FFD600']  # 鲜艳的红、橙、黄
    labels = ['①', '②', '③', '④', '⑤']
    
    for i, poi in enumerate(poi_list):
        poi_lng, poi_lat = map(float, poi['location'].split(','))
        px, py = lng_lat_to_pixel(poi_lng, poi_lat, center_lng, center_lat, zoom, width, height)
        
        # 白色外圈
        draw.ellipse([px-12, py-12, px+12, py+12], fill='#FFFFFF', outline='#000000', width=2)
        
        # 彩色圆
        color = poi_colors[i % len(poi_colors)]
        draw.ellipse([px-10, py-10, px+10, py+10], fill=color)
        
        # 白色内圈
        draw.ellipse([px-6, py-6, px+6, py+6], fill='#FFFFFF')
        
        # 数字
        label = labels[i] if i < len(labels) else str(i+1)
        bbox = draw.textbbox((0, 0), label, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        draw.text((px - text_w/2, py - text_h/2 - 2), label, fill=color, font=font)
    
    # 绘制用户位置（蓝色标记 - 简洁无阴影）
    user_lng, user_lat = map(float, user_location.split(','))
    ux, uy = lng_lat_to_pixel(user_lng, user_lat, center_lng, center_lat, zoom, width, height)
    
    # 白色外圈
    draw.ellipse([ux-14, uy-14, ux+14, uy+14], fill='#FFFFFF', outline='#000000', width=2)
    
    # 蓝色主圈
    draw.ellipse([ux-11, uy-11, ux+11, uy+11], fill='#2979FF')
    
    # 白色内圈
    draw.ellipse([ux-7, uy-7, ux+7, uy+7], fill='#FFFFFF')
    
    # 蓝色星标
    draw.text((ux-8, uy-9), '★', fill='#2979FF', font=font)
    
    return img

def generate_static_map(user_location, poi_list, output_file="/tmp/static_map.png", 
                        width=800, height=600):
    """生成静态地图"""
    
    # 计算最佳中心点和缩放级别
    center, zoom, bounds = calculate_bounds(user_location, poi_list)
    center_lng, center_lat = map(float, center.split(','))
    
    print(f"🗺️  中心点：{center}, Zoom: {zoom}")
    
    # 下载基础地图
    img = download_base_map(center, zoom, width, height)
    if not img:
        return False
    
    # 转换为 RGB 模式（支持彩色绘制）
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # 绘制标记
    img = draw_markers(img, user_location, poi_list, center_lng, center_lat, zoom)
    
    # 保存图片
    img.save(output_file, 'PNG')
    return True

def main():
    parser = argparse.ArgumentParser(description="高德地图静态地图生成器")
    parser.add_argument("--keywords", required=True, help="搜索关键词（如：汉堡）")
    parser.add_argument("--location", required=True, help="用户位置坐标 (lng,lat)")
    parser.add_argument("--count", type=int, default=3, help="显示几个 POI")
    parser.add_argument("--radius", type=int, default=1500, help="搜索半径 (米)")
    parser.add_argument("--output", default="/tmp/static_map.png", help="输出文件路径")
    parser.add_argument("--width", type=int, default=800, help="地图宽度")
    parser.add_argument("--height", type=int, default=600, help="地图高度")
    
    args = parser.parse_args()
    
    print(f"🔍 正在搜索：{args.keywords}")
    
    # 搜索 POI
    pois = search_poi(
        keywords=args.keywords,
        location=args.location,
        radius=args.radius,
        offset=args.count
    )
    
    if not pois:
        print("❌ 未找到结果")
        sys.exit(1)
    
    print(f"✅ 找到 {len(pois)} 个结果")
    
    # 计算距离并排序
    for poi in pois:
        poi['distance'] = calculate_distance(args.location, poi['location'])
    
    # 按距离排序
    pois.sort(key=lambda x: x['distance'])
    
    # 生成静态地图
    print(f"🗺️  正在生成地图...")
    success = generate_static_map(
        user_location=args.location,
        poi_list=pois[:args.count],
        output_file=args.output,
        width=args.width,
        height=args.height
    )
    
    if success:
        print(f"✅ 地图已生成：{args.output}")
        
        # 输出结果
        print("\n📍 位置信息:")
        for i, poi in enumerate(pois[:args.count], 1):
            marker = '🏆' if i == 1 else f'{i}.'
            print(f"{marker} {poi.get('name', '未知')}")
            print(f"   距离：{poi['distance']:.0f}米")
            print(f"   地址：{poi.get('address', '未知')}")
        
        print(f"\n📊 地图文件：{args.output}")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
