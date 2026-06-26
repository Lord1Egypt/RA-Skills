#!/usr/bin/env python3

# 高德地图 API 调用脚本
# 支持搜索、周边、POI、导航、地理编码等功能

import json
import requests
from typing import Dict, Any, Optional
import sys
import os
from datetime import datetime
import fcntl

# 获取脚本所在目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
USAGE_FILE = os.path.join(SKILL_DIR, ".usage.json")

# 高德开放平台 Web 服务 API 配置
AMAP_API_KEY = os.getenv("AMAP_API_KEY", "")  # 从环境变量或配置获取
BASE_URL = "https://restapi.amap.com/v3"


def load_usage() -> Dict[str, Any]:
    """加载使用统计"""
    if os.path.exists(USAGE_FILE):
        try:
            with open(USAGE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return {
        "total": 0,
        "success": 0,
        "failed": 0,
        "daily": {},
        "daily_quota": 5000,
        "last_check": None
    }


def save_usage(usage: Dict[str, Any]):
    """保存使用统计（带文件锁，避免并发问题）"""
    with open(USAGE_FILE, 'w', encoding='utf-8') as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        json.dump(usage, f, indent=2, ensure_ascii=False)
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)


def record_usage(success: bool):
    """记录 API 调用"""
    usage = load_usage()
    today = datetime.now().strftime("%Y-%m-%d")
    
    usage["total"] += 1
    if success:
        usage["success"] += 1
    else:
        usage["failed"] += 1
    
    if today not in usage["daily"]:
        usage["daily"][today] = {"count": 0, "success": 0, "failed": 0}
    
    usage["daily"][today]["count"] += 1
    if success:
        usage["daily"][today]["success"] += 1
    else:
        usage["daily"][today]["failed"] += 1
    
    # 保留最近 30 天的记录
    from datetime import timedelta
    cutoff = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    usage["daily"] = {
        k: v for k, v in usage["daily"].items()
        if k >= cutoff
    }
    
    save_usage(usage)


def show_usage():
    """显示使用统计"""
    usage = load_usage()
    
    remaining_today = usage["daily_quota"] - usage["daily"].get(
        datetime.now().strftime("%Y-%m-%d"), {}
    ).get("count", 0)
    
    print("=" * 50)
    print("高德地图 API")
    print("=" * 50)
    print("📊 真实用量请查看控制台：https://console.amap.com/")
    print()
    print("📝 本地脚本调用统计（仅记录通过本脚本的调用）：")
    print(f"   总调用次数：{usage['total']}")
    print(f"   成功：{usage['success']} | 失败：{usage['failed']}")
    print(f"   配额：{usage['daily_quota']} 次/天（个人开发者）")
    print(f"   本地记录今日调用：{usage['daily'].get(datetime.now().strftime('%Y-%m-%d'), {}).get('count', 0)} 次")
    
    print("\n最近 7 天本地记录:")
    print("-" * 50)
    
    # 显示最近 7 天
    from datetime import timedelta
    for i in range(6, -1, -1):
        date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        if date in usage["daily"]:
            d = usage["daily"][date]
            print(f"{date}: {d['count']} 次 (成功:{d['success']} 失败:{d['failed']})")
        else:
            print(f"{date}: 0 次")
    
    print("=" * 50)


def get_api_key() -> str:
    """获取 API Key"""
    if AMAP_API_KEY:
        return AMAP_API_KEY
    # 尝试从配置文件读取（备选）
    config_path = os.path.expanduser("~/.openclaw/openclaw.json")
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                skill_config = config.get("skills", {}).get("entries", {}).get("amap-map", {})
                api_key = skill_config.get("apiKey", "")
                if api_key:
                    return api_key
        except:
            pass
    return ""


def call_api(endpoint: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    调用高德 API
    
    Args:
        endpoint: API 端点
        params: 请求参数
    
    Returns:
        API 响应的 JSON 数据
    """
    api_key = get_api_key()
    if not api_key:
        record_usage(False)
        return {
            "status": "0",
            "info": "未配置 API Key，请在 openclaw.json 中配置 amap-map 的 apiKey",
            "infocode": "10001"
        }
    
    params["key"] = api_key
    params["output"] = "json"
    
    try:
        response = requests.get(f"{BASE_URL}/{endpoint}", params=params, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        # 根据高德 API 返回状态判断成功与否
        success = result.get("status") == "1" and result.get("infocode") in ["10000", "00000"]
        record_usage(success)
        
        return result
    
    except requests.exceptions.RequestException as e:
        record_usage(False)
        return {
            "status": "0",
            "info": f"API 请求失败：{str(e)}",
            "infocode": "10000"
        }


def text_search(keywords: str, city: str = "", limit: int = 10) -> Dict[str, Any]:
    """
    关键词搜索 POI
    
    Args:
        keywords: 搜索关键词
        city: 城市名称（可选）
        limit: 返回数量（默认 10）
    
    Returns:
        搜索结果
    
    示例:
        >>> text_search("餐厅", "北京", 10)
    """
    params = {
        "keywords": keywords,
        "city": city,
        "limit": limit,
        "offset": 0,
        "page": 1
    }
    return call_api("place/text", params)


def around_search(location: str, keywords: str = "", radius: int = 1000, limit: int = 10) -> Dict[str, Any]:
    """
    周边搜索 POI
    
    Args:
        location: 中心点经纬度（格式："经度，纬度"）
        keywords: 搜索关键词（可选）
        radius: 搜索半径（米，默认 1000）
        limit: 返回数量（默认 10）
    
    Returns:
        搜索结果
    
    示例:
        >>> around_search("116.397428,39.90923", "餐厅", 1000, 10)
    """
    params = {
        "location": location,
        "keywords": keywords,
        "radius": radius,
        "limit": limit,
        "offset": 0,
        "page": 1
    }
    return call_api("place/around", params)


def poi_detail(poi_id: str) -> Dict[str, Any]:
    """
    POI 详情查询
    
    Args:
        poi_id: POI ID
    
    Returns:
        POI 详细信息
    
    示例:
        >>> poi_detail("B000A7BK0E")
    """
    params = {
        "id": poi_id
    }
    return call_api("place/detail", params)


def walking(origin: str, destination: str) -> Dict[str, Any]:
    """
    步行路径规划
    
    Args:
        origin: 起点经纬度（格式："经度，纬度"）
        destination: 终点经纬度（格式："经度，纬度"）
    
    Returns:
        路径规划结果
    
    示例:
        >>> walking("116.397428,39.90923", "116.407428,39.91923")
    """
    params = {
        "origin": origin,
        "destination": destination
    }
    return call_api("direction/walking", params)


def bicycling(origin: str, destination: str) -> Dict[str, Any]:
    """
    骑行路径规划（支持 500km 内）
    
    Args:
        origin: 起点经纬度
        destination: 终点经纬度
    
    Returns:
        路径规划结果
    
    示例:
        >>> bicycling("116.397428,39.90923", "116.407428,39.91923")
    """
    params = {
        "origin": origin,
        "destination": destination
    }
    return call_api("direction/bicycling", params)


def driving(origin: str, destination: str, policy: int = 0) -> Dict[str, Any]:
    """
    驾车路径规划
    
    Args:
        origin: 起点经纬度
        destination: 终点经纬度
        policy: 策略（0-最快捷，1-最短路，2-避免收费，3-避免高速）
    
    Returns:
        路径规划结果
    
    示例:
        >>> driving("116.397428,39.90923", "116.407428,39.91923", 0)
    """
    params = {
        "origin": origin,
        "destination": destination,
        "policy": policy
    }
    return call_api("direction/driving", params)


def geo(address: str, city: str = "") -> Dict[str, Any]:
    """
    地理编码（地址转经纬度）
    
    Args:
        address: 地址
        city: 城市名称（可选）
    
    Returns:
        地理编码结果
    
    示例:
        >>> geo("北京市天安门广场", "北京")
    """
    params = {
        "address": address,
        "city": city
    }
    return call_api("geocode/geo", params)


def regeocode(location: str, radius: int = 1000) -> Dict[str, Any]:
    """
    逆地理编码（经纬度转地址）
    
    Args:
        location: 经纬度（格式："经度，纬度"）
        radius: 搜索半径（米，默认 1000）
    
    Returns:
        逆地理编码结果
    
    示例:
        >>> regeocode("116.397428,39.90923")
    """
    params = {
        "location": location,
        "radius": radius
    }
    return call_api("geocode/regeo", params)


def print_usage():
    """打印使用说明"""
    usage = """
高德地图 API 调用脚本

用法：python3 amap.py <功能> <参数>

功能列表:
  text_search <关键词> [城市] [数量]     关键词搜索 POI
  around_search <经纬度> [关键词] [半径] [数量]  周边搜索
  poi_detail <POI_ID>                   POI 详情查询
  walking <起点经纬度> <终点经纬度>       步行导航
  bicycling <起点经纬度> <终点经纬度>     骑行导航
  driving <起点经纬度> <终点经纬度> [策略] 驾车导航
  geo <地址> [城市]                     地址转经纬度
  regeocode <经纬度> [半径]             经纬度转地址
  --usage, -u                           查看使用统计

示例:
  python3 amap.py text_search "餐厅" "北京" 10
  python3 amap.py around_search "116.397428,39.90923" "咖啡" 500
  python3 amap.py walking "116.397428,39.90923" "116.407428,39.91923"
  python3 amap.py geo "北京市天安门广场" "北京"
  python3 amap.py --usage
"""
    print(usage)


def main():
    """命令行接口"""
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
    
    # 检查是否是查询使用统计
    if sys.argv[1] in ["--usage", "-u", "usage"]:
        show_usage()
        return
    
    func_name = sys.argv[1]
    
    # 功能映射
    functions = {
        "text_search": lambda: text_search(*sys.argv[2:4], int(sys.argv[4]) if len(sys.argv) > 4 else 10),
        "around_search": lambda: around_search(
            sys.argv[2],
            sys.argv[3] if len(sys.argv) > 3 else "",
            int(sys.argv[4]) if len(sys.argv) > 4 else 1000,
            int(sys.argv[5]) if len(sys.argv) > 5 else 10
        ),
        "poi_detail": lambda: poi_detail(sys.argv[2]),
        "walking": lambda: walking(sys.argv[2], sys.argv[3]),
        "bicycling": lambda: bicycling(sys.argv[2], sys.argv[3]),
        "driving": lambda: driving(sys.argv[2], sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else 0),
        "geo": lambda: geo(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else ""),
        "regeocode": lambda: regeocode(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 1000)
    }
    
    if func_name not in functions:
        print(f"错误：未知功能 '{func_name}'", file=sys.stderr)
        print_usage()
        sys.exit(1)
    
    # 检查参数数量
    min_args = {
        "text_search": 2,
        "around_search": 1,
        "poi_detail": 1,
        "walking": 2,
        "bicycling": 2,
        "driving": 2,
        "geo": 1,
        "regeocode": 1
    }
    
    provided_args = len(sys.argv) - 2
    if provided_args < min_args[func_name]:
        print(f"错误：{func_name} 至少需要 {min_args[func_name]} 个参数", file=sys.stderr)
        sys.exit(1)
    
    try:
        result = functions[func_name]()
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        if result.get("status") == "0":
            sys.exit(1)
    except Exception as e:
        print(json.dumps({
            "status": "0",
            "info": f"执行错误：{str(e)}"
        }, indent=2, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
