#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
百度地图附近场所推荐工具 - 安全修复版
使用百度地图 Place API 进行周边POI搜索

修复:
- [SECURITY] 移除 SSL 验证禁用代码
- [SECURITY] 添加输入验证和参数清理
- [SECURITY] 限制搜索半径和结果数量
- [SECURITY] API Key 不输出到日志
"""

import os
import sys
import json
import urllib.parse
import urllib.request
import ssl
import socket

# ============== 安全配置 ==============

# 使用系统默认 SSL 上下文
ssl_context = ssl.create_default_context()

# 请求超时（秒）
GEOCODE_TIMEOUT = 10
SEARCH_TIMEOUT = 15

# 参数限制
MAX_RADIUS = 20000      # 最大搜索半径 20km
MAX_PAGE_SIZE = 20      # 最大返回数量
MAX_ADDRESS_LENGTH = 200  # 地址最大长度

# 场所分类映射
CATEGORY_MAP = {
    '餐饮': 'catering',
    '美食': 'catering',
    '餐厅': 'catering',
    '吃饭': 'catering',
    '娱乐': 'entertainment',
    '休闲': 'entertainment',
    '景点': 'scenic',
    '旅游': 'scenic',
    '景区': 'scenic',
    '酒店': 'hotel',
    '住宿': 'hotel',
    '购物': 'shopping',
    '商场': 'shopping',
    '超市': 'shopping',
    '交通': 'transportation',
    '地铁': 'transportation',
    '公交': 'transportation',
    '生活': 'life_service',
    '服务': 'life_service',
    '医疗': 'medical',
    '医院': 'medical',
    '教育': 'education',
    '学校': 'education',
    '金融': 'finance',
    '银行': 'finance',
}

# 分类标签映射
TAG_MAP = {
    'catering': ['中餐厅', '西餐厅', '咖啡厅', '火锅', '烧烤', '小吃', '快餐', '酒吧'],
    'entertainment': ['KTV', '电影院', '网吧', '游乐场', '体育馆', '健身房', '公园'],
    'scenic': ['公园', '广场', '景区', '博物馆', '展览馆', '寺庙', '古迹'],
    'hotel': ['酒店', '宾馆', '旅馆', '招待所'],
    'shopping': ['商场', '购物中心', '超市', '便利店', '专卖店', '市场'],
    'transportation': ['地铁站', '公交站', '火车站', '机场', '汽车站'],
    'life_service': ['加油站', '停车场', '厕所', '快递', '洗衣', '理发'],
    'medical': ['医院', '诊所', '药店', '急救中心'],
    'education': ['大学', '中学', '小学', '幼儿园', '培训机构', '图书馆'],
    'finance': ['银行', 'ATM', '证券', '保险'],
}

DEFAULT_TAGS = {
    'catering': '美食',
    'entertainment': '休闲娱乐',
    'scenic': '旅游景点',
    'hotel': '酒店宾馆',
    'shopping': '购物',
    'transportation': '交通设施',
    'life_service': '生活服务',
    'medical': '医疗保健',
    'education': '教育培训',
    'finance': '金融银行',
}


def validate_coordinates(lat, lng):
    """验证坐标范围"""
    try:
        lat = float(lat)
        lng = float(lng)
        # 中国境内大致范围
        if not (3 <= lat <= 54 and 73 <= lng <= 136):
            return False, "坐标超出中国境内范围"
        return True, (lat, lng)
    except (ValueError, TypeError):
        return False, "坐标格式错误"


def validate_radius(radius):
    """验证搜索半径"""
    try:
        radius = int(radius)
        if radius < 100:
            return False, "搜索半径不能小于100米"
        if radius > MAX_RADIUS:
            return False, f"搜索半径不能超过{MAX_RADIUS}米"
        return True, radius
    except (ValueError, TypeError):
        return False, "半径格式错误"


def validate_page_size(page_size):
    """验证返回数量"""
    try:
        page_size = int(page_size)
        if page_size < 1:
            return False, "返回数量不能小于1"
        if page_size > MAX_PAGE_SIZE:
            return False, f"返回数量不能超过{MAX_PAGE_SIZE}"
        return True, page_size
    except (ValueError, TypeError):
        return False, "数量格式错误"


def sanitize_address(address):
    """清理地址输入"""
    if not address or not isinstance(address, str):
        return None
    
    # 去除首尾空白
    address = address.strip()
    
    # 限制长度
    if len(address) > MAX_ADDRESS_LENGTH:
        address = address[:MAX_ADDRESS_LENGTH]
    
    # 移除潜在危险字符
    address = address.replace('\n', ' ').replace('\r', ' ')
    address = address.replace('<', '').replace('>', '')
    address = address.replace('"', '').replace("'", '')
    
    return address if address else None


def get_api_key():
    """从环境变量获取API Key（不输出到日志）"""
    api_key = os.environ.get('BAIDU_API_KEY') or os.environ.get('BAIDU_AK')
    if not api_key:
        print("错误: 未设置 BAIDU_API_KEY 环境变量")
        print("请访问 https://lbsyun.baidu.com/ 申请AK")
        return None
    
    # 验证 API Key 格式（基本检查）
    if len(api_key) < 10 or len(api_key) > 100:
        print("警告: API Key 格式可能不正确")
    
    return api_key


def mask_api_key(ak):
    """掩码 API Key 用于日志输出"""
    if not ak or len(ak) < 8:
        return "***"
    return ak[:4] + "*" * (len(ak) - 8) + ak[-4:]


def safe_urlopen(url, timeout=10):
    """安全的 URL 请求"""
    try:
        req = urllib.request.Request(url)
        return urllib.request.urlopen(
            req,
            timeout=timeout,
            context=ssl_context
        )
    except urllib.error.HTTPError as e:
        print(f"HTTP错误: {e.code} {e.reason}")
        return None
    except urllib.error.URLError as e:
        print(f"URL错误: {e.reason}")
        return None
    except socket.timeout:
        print("请求超时")
        return None
    except Exception as e:
        print(f"请求失败: {type(e).__name__}")
        return None


def geocode(address, ak):
    """
    地理编码 - 地址转经纬度
    
    Args:
        address: 地址字符串
        ak: 百度API Key
    
    Returns:
        (lat, lng) 或 None
    """
    # 清理地址
    address = sanitize_address(address)
    if not address:
        print("地址无效")
        return None
    
    url = (
        f"https://api.map.baidu.com/geocoding/v3/?"
        f"address={urllib.parse.quote(address)}"
        f"&output=json&ak={ak}"
    )
    
    response = safe_urlopen(url, timeout=GEOCODE_TIMEOUT)
    if not response:
        return None
    
    try:
        data = json.loads(response.read().decode('utf-8'))
        if data.get('status') == 0:
            location = data['result']['location']
            lat, lng = location['lat'], location['lng']
            # 验证返回的坐标
            is_valid, result = validate_coordinates(lat, lng)
            if is_valid:
                return result
            else:
                print(f"返回坐标无效: {result}")
                return None
        else:
            print(f"地理编码失败: {data.get('message', '未知错误')}")
    except json.JSONDecodeError:
        print("响应解析失败")
    except Exception as e:
        print(f"处理响应失败: {type(e).__name__}")
    
    return None


def reverse_geocode(lat, lng, ak):
    """
    逆地理编码 - 经纬度转地址
    
    Args:
        lat: 纬度
        lng: 经度
        ak: 百度API Key
    
    Returns:
        地址字符串 或 None
    """
    url = (
        f"https://api.map.baidu.com/reverse_geocoding/v3/?"
        f"location={lat},{lng}&output=json&ak={ak}"
    )
    
    response = safe_urlopen(url, timeout=GEOCODE_TIMEOUT)
    if not response:
        return None
    
    try:
        data = json.loads(response.read().decode('utf-8'))
        if data.get('status') == 0:
            return data['result'].get('formatted_address')
    except Exception:
        pass
    
    return None


def search_nearby(location, query=None, radius=1000, page_size=10, ak=None):
    """
    周边POI搜索
    
    Args:
        location: 中心点坐标 (lat,lng) 或地址
        query: 搜索关键词
        radius: 搜索半径（米），100-20000
        page_size: 返回结果数量，1-20
        ak: 百度API Key
    
    Returns:
        list: POI列表 或 None
    """
    if not ak:
        ak = get_api_key()
        if not ak:
            return None
    
    # 验证半径
    is_valid, radius = validate_radius(radius)
    if not is_valid:
        print(f"半径错误: {radius}")
        return None
    
    # 验证数量
    is_valid, page_size = validate_page_size(page_size)
    if not is_valid:
        print(f"数量错误: {page_size}")
        return None
    
    # 解析位置
    if isinstance(location, str) and (',' not in location or len(location.split(',')) != 2):
        # 是地址，需要地理编码
        coord = geocode(location, ak)
        if not coord:
            print(f"无法解析位置: {location}")
            return None
        lat, lng = coord
    elif isinstance(location, str):
        # 是坐标字符串
        parts = location.split(',')
        is_valid, result = validate_coordinates(parts[0], parts[1])
        if not is_valid:
            print(f"坐标错误: {result}")
            return None
        lat, lng = result
    else:
        lat, lng = location
    
    # 构建请求
    base_url = "https://api.map.baidu.com/place/v2/search"
    params = {
        'query': query or '美食',
        'location': f"{lat},{lng}",
        'radius': str(radius),
        'output': 'json',
        'ak': ak,
        'scope': '2',
        'page_size': str(page_size),
        'page_num': '0',
    }
    
    url = f"{base_url}?" + urllib.parse.urlencode(params)
    
    response = safe_urlopen(url, timeout=SEARCH_TIMEOUT)
    if not response:
        return None
    
    try:
        data = json.loads(response.read().decode('utf-8'))
        if data.get('status') == 0:
            return data.get('results', [])
        else:
            print(f"搜索失败: {data.get('message', '未知错误')}")
    except json.JSONDecodeError:
        print("响应解析失败")
    except Exception as e:
        print(f"处理失败: {type(e).__name__}")
    
    return None


def get_category_tag(category):
    """获取分类对应的搜索标签"""
    if not category:
        return None
    
    category_lower = category.lower()
    if category_lower in TAG_MAP:
        return DEFAULT_TAGS.get(category_lower, category)
    
    # 中文匹配
    for cn, en in CATEGORY_MAP.items():
        if cn in category or category in cn:
            return DEFAULT_TAGS.get(en, category)
    
    return category


def format_distance(meters):
    """格式化距离"""
    try:
        meters = int(meters)
        if meters >= 1000:
            return f"{meters/1000:.1f}km"
        return f"{meters}m"
    except (ValueError, TypeError):
        return "未知"


def print_poi_results(results, location_name, category=None):
    """格式化打印POI结果"""
    if not results:
        print(f"未找到{category or ''}相关场所")
        return
    
    category_display = category or "周边场所"
    print(f"\n📍 {location_name} 附近的{category_display}推荐")
    print("=" * 50)
    print(f"找到 {len(results)} 个推荐地点\n")
    
    for i, poi in enumerate(results, 1):
        name = poi.get('name', '未知')
        address = poi.get('address', '地址未知')
        distance = poi.get('distance', 0)
        detail = poi.get('detail_info', {})
        rating = detail.get('overall_rating', '')
        price = detail.get('price', '')
        tag = detail.get('tag', '')
        phone = poi.get('telephone', '')
        
        meta = []
        if rating:
            meta.append(f"⭐{rating}")
        if price:
            meta.append(f"💰{price}元")
        if tag:
            meta.append(f"🏷️{tag}")
        
        print(f"{i}. 🏪 {name}")
        print(f"   📍 {address}")
        if meta:
            print(f"   {' | '.join(meta)}")
        print(f"   📏 距离: {format_distance(distance)}")
        if phone:
            print(f"   📞 {phone}")
        print()


def recommend_nearby(location, category=None, radius=1000, limit=10):
    """
    推荐附近场所
    
    Args:
        location: 位置（地址或坐标）
        category: 类别
        radius: 搜索半径（米）
        limit: 返回数量
    
    Returns:
        list: POI列表 或 None
    """
    ak = get_api_key()
    if not ak:
        return None
    
    # 解析位置
    if isinstance(location, str) and (',' not in location or len(location.split(',')) != 2):
        coord = geocode(location, ak)
        if not coord:
            print(f"无法解析位置: {location}")
            return None
        lat, lng = coord
        location_name = sanitize_address(location) or f"{lat},{lng}"
    elif isinstance(location, str):
        parts = location.split(',')
        is_valid, result = validate_coordinates(parts[0], parts[1])
        if not is_valid:
            print(f"坐标错误: {result}")
            return None
        lat, lng = result
        location_name = reverse_geocode(lat, lng, ak) or f"{lat},{lng}"
    else:
        lat, lng = location
        location_name = reverse_geocode(lat, lng, ak) or f"{lat},{lng}"
    
    # 搜索关键词
    query = None
    if category:
        query = get_category_tag(category)
    
    # 执行搜索
    results = search_nearby((lat, lng), query=query, radius=radius, page_size=limit, ak=ak)
    
    if results:
        print_poi_results(results, location_name, category)
    
    return results


def main():
    if len(sys.argv) < 2:
        print("使用方法: python baidu_nearby.py <位置> [类别] [半径(米)] [数量]")
        print("")
        print("位置: 具体地址或经纬度坐标（如：39.9,116.4）")
        print("类别: 餐饮/美食、娱乐/休闲、景点/旅游、酒店、购物等")
        print("半径: 100-20000 米")
        print("数量: 1-20 个")
        print("")
        print("示例:")
        print("  python baidu_nearby.py '北京市朝阳区三里屯' 餐饮 2000 5")
        print("  python baidu_nearby.py '39.9,116.4' 景点 5000 10")
        sys.exit(1)
    
    location = sys.argv[1]
    category = sys.argv[2] if len(sys.argv) > 2 else None
    
    # 验证参数
    try:
        radius = int(sys.argv[3]) if len(sys.argv) > 3 else 1000
    except ValueError:
        print("错误: 半径必须为整数")
        sys.exit(1)
    
    try:
        limit = int(sys.argv[4]) if len(sys.argv) > 4 else 10
    except ValueError:
        print("错误: 数量必须为整数")
        sys.exit(1)
    
    print(f"🔍 正在搜索: {sanitize_address(location) or location}")
    if category:
        print(f"   类别: {category}")
    print(f"   半径: {radius}米")
    print(f"   数量: {limit}个")
    print("-" * 40)
    
    recommend_nearby(location, category, radius, limit)


if __name__ == '__main__':
    main()
