#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
百度地图路线规划工具 - 安全修复版
使用百度地图 DirectionLite API

修复:
- [SECURITY] 移除 SSL 验证禁用代码
- [SECURITY] 添加输入验证和参数清理
- [SECURITY] 限制请求参数范围
- [SECURITY] API Key 不输出到日志
"""

import os
import sys
import json
import urllib.parse
import urllib.request
import ssl
import socket
import re

# ============== 安全配置 ==============

ssl_context = ssl.create_default_context()

GEOCODE_TIMEOUT = 10
DIRECTION_TIMEOUT = 15

MAX_ADDRESS_LENGTH = 200
VALID_MODES = ['driving', 'riding', 'walking', 'transit']

# 中国境内坐标范围
LAT_RANGE = (3, 54)
LNG_RANGE = (73, 136)


def validate_coordinates(coord_str):
    """
    验证坐标字符串格式 "lat,lng"
    
    Returns:
        (is_valid, result_or_error)
    """
    if not coord_str or not isinstance(coord_str, str):
        return False, "坐标为空"
    
    parts = coord_str.split(',')
    if len(parts) != 2:
        return False, "坐标格式应为 'lat,lng'"
    
    try:
        lat = float(parts[0].strip())
        lng = float(parts[1].strip())
    except ValueError:
        return False, "坐标必须为数字"
    
    if not (LAT_RANGE[0] <= lat <= LAT_RANGE[1]):
        return False, f"纬度超出范围 ({LAT_RANGE[0]}-{LAT_RANGE[1]})"
    
    if not (LNG_RANGE[0] <= lng <= LNG_RANGE[1]):
        return False, f"经度超出范围 ({LNG_RANGE[0]}-{LNG_RANGE[1]})"
    
    return True, f"{lat},{lng}"


def is_address(input_str):
    """判断输入是地址还是坐标"""
    if not input_str:
        return True
    
    # 检查是否为坐标格式
    coord_pattern = r'^-?\d+\.?\d*\s*,\s*-?\d+\.?\d*$'
    if re.match(coord_pattern, input_str.strip()):
        return False
    
    return True


def sanitize_address(address):
    """清理地址输入"""
    if not address or not isinstance(address, str):
        return None
    
    address = address.strip()
    if len(address) > MAX_ADDRESS_LENGTH:
        address = address[:MAX_ADDRESS_LENGTH]
    
    # 移除危险字符
    address = address.replace('\n', ' ').replace('\r', ' ')
    address = address.replace('<', '').replace('>', '')
    address = address.replace('"', '').replace("'", '')
    
    return address if address else None


def validate_mode(mode):
    """验证出行方式"""
    if not mode:
        return True, 'driving'
    
    mode = mode.strip().lower()
    if mode not in VALID_MODES:
        return False, f"不支持的出行方式: {mode}（支持: {', '.join(VALID_MODES)}）"
    
    return True, mode


def get_api_key():
    """从环境变量获取API Key"""
    api_key = os.environ.get('BAIDU_API_KEY') or os.environ.get('BAIDU_AK')
    if not api_key:
        print("错误: 未设置 BAIDU_API_KEY 环境变量")
        print("请访问 https://lbsyun.baidu.com/ 申请AK")
        return None
    
    if len(api_key) < 10 or len(api_key) > 100:
        print("警告: API Key 格式可能不正确")
    
    return api_key


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
        "lat,lng" 字符串 或 None
    """
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
            coord = f"{location['lat']},{location['lng']}"
            # 验证返回的坐标
            is_valid, result = validate_coordinates(coord)
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
        print(f"处理失败: {type(e).__name__}")
    
    return None


def direction_lite(origin, destination, mode='driving', ak=None):
    """
    百度地图路线规划
    
    Args:
        origin: 起点 (地址或经纬度 "lat,lng")
        destination: 终点 (地址或经纬度 "lat,lng")
        mode: 出行方式 - driving|riding|walking|transit
        ak: 百度API Key
    
    Returns:
        dict: 路线规划结果 或 None
    """
    if not ak:
        ak = get_api_key()
        if not ak:
            return None
    
    # 验证出行方式
    is_valid, mode_result = validate_mode(mode)
    if not is_valid:
        print(mode_result)
        return None
    mode = mode_result
    
    # 解析起点
    if is_address(origin):
        origin_coord = geocode(origin, ak)
        if not origin_coord:
            print(f"无法解析起点: {sanitize_address(origin) or origin}")
            return None
    else:
        is_valid, origin_coord = validate_coordinates(origin)
        if not is_valid:
            print(f"起点坐标错误: {origin_coord}")
            return None
    
    # 解析终点
    if is_address(destination):
        dest_coord = geocode(destination, ak)
        if not dest_coord:
            print(f"无法解析终点: {sanitize_address(destination) or destination}")
            return None
    else:
        is_valid, dest_coord = validate_coordinates(destination)
        if not is_valid:
            print(f"终点坐标错误: {dest_coord}")
            return None
    
    # 构建请求
    base_url = "https://api.map.baidu.com/directionlite/v1/"
    endpoint = 'transit' if mode == 'transit' else mode
    
    params = {
        'origin': origin_coord,
        'destination': dest_coord,
        'ak': ak,
        'output': 'json'
    }
    
    if mode == 'driving':
        params['alternatives'] = '1'
    
    url = f"{base_url}{endpoint}?" + urllib.parse.urlencode(params)
    
    response = safe_urlopen(url, timeout=DIRECTION_TIMEOUT)
    if not response:
        return None
    
    try:
        data = json.loads(response.read().decode('utf-8'))
        return data
    except json.JSONDecodeError:
        print("响应解析失败")
        return None
    except Exception as e:
        print(f"处理失败: {type(e).__name__}")
        return None


def format_duration(seconds):
    """格式化时间"""
    try:
        seconds = int(seconds)
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        if hours > 0:
            return f"{hours}小时{minutes}分钟"
        return f"{minutes}分钟"
    except (ValueError, TypeError):
        return "未知"


def format_distance(meters):
    """格式化距离"""
    try:
        meters = int(meters)
        if meters >= 1000:
            return f"{meters/1000:.1f}公里"
        return f"{meters}米"
    except (ValueError, TypeError):
        return "未知"


def print_route(result, mode):
    """打印路线结果"""
    if not result:
        print("未获取到路线信息")
        return
    
    status = result.get('status')
    if status != 0:
        print(f"请求失败，状态码: {status}")
        message = result.get('message', '未知错误')
        print(f"错误信息: {message}")
        return
    
    routes = result.get('result', {}).get('routes', [])
    if not routes:
        print("未找到可用路线")
        return
    
    route = routes[0]
    distance = route.get('distance', 0)
    duration = route.get('duration', 0)
    
    mode_names = {
        'driving': '🚗 驾车',
        'riding': '🚴 骑行',
        'walking': '🚶 步行',
        'transit': '🚌 公交'
    }
    
    print(f"\n{mode_names.get(mode, mode)}路线规划")
    print("=" * 40)
    print(f"总距离: {format_distance(distance)}")
    print(f"预计时间: {format_duration(duration)}")
    print()
    
    steps = route.get('steps', [])
    if steps:
        print("详细路线:")
        print("-" * 40)
        step_num = 1
        for step in steps:
            # 公交路线的 steps 是嵌套列表 [[{}, {}], [{}, {}]]
            # 驾车路线的 steps 是 ["指令", "指令"]
            if isinstance(step, list):
                # 公交路线：每个 step 包含多个子步骤
                for sub_step in step:
                    if isinstance(sub_step, dict):
                        instruction = sub_step.get('instruction', '')
                        step_distance = sub_step.get('distance', 0)
                        step_type = sub_step.get('type', 0)
                        vehicle = sub_step.get('vehicle', {})
                        
                        # 根据类型显示不同图标
                        icon = '🚶'
                        if step_type == 3:  # 公交
                            icon = '🚌'
                            vehicle_name = vehicle.get('name', '')
                            if vehicle_name:
                                instruction = f"乘坐{vehicle_name}: {instruction}"
                        elif step_type == 5:  # 步行
                            icon = '🚶'
                        
                        if instruction:
                            print(f"{step_num}. {icon} {instruction} ({format_distance(step_distance)})")
                            step_num += 1
            elif isinstance(step, dict):
                instruction = step.get('instruction', step.get('step_instruction', ''))
                if instruction:
                    step_distance = step.get('distance', 0)
                    print(f"{step_num}. {instruction} ({format_distance(step_distance)})")
                    step_num += 1
            elif isinstance(step, str):
                print(f"{step_num}. {step}")
                step_num += 1
    
    # 显示备选路线
    if len(routes) > 1:
        print(f"\n📋 共 {len(routes)} 条备选路线")
        for idx, alt_route in enumerate(routes[1:], 2):
            alt_dist = format_distance(alt_route.get('distance', 0))
            alt_dur = format_duration(alt_route.get('duration', 0))
            print(f"  路线{idx}: {alt_dist}, {alt_dur}")


def main():
    if len(sys.argv) < 3:
        print("使用方法: python baidu_direction.py <起点> <终点> [出行方式]")
        print("")
        print("起点/终点: 地址 或 经纬度坐标（如：39.9,116.3）")
        print("出行方式: driving(驾车), riding(骑行), walking(步行), transit(公交)")
        print("  默认: driving")
        print("")
        print("示例:")
        print("  python baidu_direction.py '北京市朝阳区' '北京市海淀区' driving")
        print("  python baidu_direction.py '39.9,116.3' '39.8,116.4' walking")
        print("  python baidu_direction.py '天安门' '故宫' transit")
        sys.exit(1)
    
    origin = sys.argv[1]
    destination = sys.argv[2]
    mode = sys.argv[3] if len(sys.argv) > 3 else 'driving'
    
    # 验证出行方式
    is_valid, mode_result = validate_mode(mode)
    if not is_valid:
        print(mode_result)
        sys.exit(1)
    mode = mode_result
    
    # 清理显示
    origin_display = sanitize_address(origin) if is_address(origin) else origin
    dest_display = sanitize_address(destination) if is_address(destination) else destination
    
    print(f"🗺️ 路线规划: {origin_display} → {dest_display}")
    
    result = direction_lite(origin, destination, mode)
    print_route(result, mode)


if __name__ == '__main__':
    main()
