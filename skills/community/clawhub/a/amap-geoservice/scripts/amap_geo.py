#!/usr/bin/env python3
"""
高德开放平台地理信息服务
地理编码、POI搜索、路径规划、距离测量等

依赖：
  pip install requests

环境变量（优先）或配置文件（二选一）：
  export AMAP_API_KEY="your-api-key"
  export AMAP_SECRET_KEY="your-secret-key"  # 如需签名
  
  或创建 config.txt 填入 Key

用法：
  # 地理编码
  python amap_geo.py --action geo --address "北京市朝阳区"
  
  # 逆地理编码
  python amap_geo.py --action regeo --location "116.4074,39.9042"
  
  # POI搜索
  python amap_geo.py --action poi --keywords "餐厅" --city "北京"
  
  # 路径规划
  python amap_geo.py --action direction --from "116.4074,39.9042" --to "116.4274,39.9042"
"""

import os
import sys
import json
import hashlib
import argparse
import requests

# ========== 配置区 ==========
# 高德开放平台 API 基础 URL
API_BASE_URL = "https://restapi.amap.com"

# 配置文件路径（skill 根目录）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
CONFIG_FILE = os.path.join(SKILL_DIR, "config.txt")
# ========== 配置区结束 ==========

# 常用城市 AdCode
CITY_ADCODES = {
    "北京": "110000", "上海": "310000", "广州": "440100", "深圳": "440300",
    "成都": "510100", "武汉": "420100", "杭州": "330100", "南京": "320100",
    "西安": "610100", "重庆": "500000", "天津": "120000", "苏州": "320500",
    "郑州": "410100", "长沙": "430100", "沈阳": "210100", "青岛": "370200",
}


def get_config():
    """获取 API 配置"""
    api_key = os.environ.get("AMAP_API_KEY")
    secret_key = os.environ.get("AMAP_SECRET_KEY", "")
    
    if not api_key and os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    if "=" in line:
                        k, v = line.split("=", 1)
                        k, v = k.strip(), v.strip()
                        if k == "AMAP_API_KEY":
                            api_key = v
                        elif k == "AMAP_SECRET_KEY":
                            secret_key = v
    
    if not api_key:
        print(f"错误：未找到 API Key", file=sys.stderr)
        print(f"请设置环境变量 AMAP_API_KEY 或创建 {CONFIG_FILE}", file=sys.stderr)
        sys.exit(1)
    
    return api_key, secret_key


def generate_signature(api_key, params, secret_key):
    """
    生成高德 API 签名
    签名 = MD5(api_key + sorted_params + secret_key)
    """
    if not secret_key:
        return ""
    
    filtered = {k: v for k, v in params.items() if k != "sign"}
    sorted_keys = sorted(filtered.keys())
    param_str = "".join(k + str(filtered[k]) for k in sorted_keys)
    sign_str = api_key + param_str + secret_key
    
    md5 = hashlib.md5()
    md5.update(sign_str.encode("utf-8"))
    return md5.hexdigest()


def api_request(endpoint, params, need_signature=False):
    """发送 API 请求"""
    api_key, secret_key = get_config()
    
    params["key"] = api_key
    
    if need_signature and secret_key:
        params["sign"] = generate_signature(api_key, params, secret_key)
    
    url = API_BASE_URL + endpoint
    
    try:
        resp = requests.get(url, params=params, timeout=10)
        return resp.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"网络请求失败: {e}"}


def geo_encode(address, city=""):
    """地理编码：地址 → 经纬度"""
    params = {"address": address}
    if city:
        params["city"] = city
    
    data = api_request("/v3/geocode/geo", params)
    
    if "error" in data:
        return data
    
    if data.get("status") != "1":
        return {"error": f"API返回错误: {data.get('info', '未知')}"}
    
    geocodes = data.get("geocodes", [])
    if not geocodes:
        return {"error": "未找到该地址"}
    
    result = []
    for g in geocodes:
        result.append(f"【{g.get('province', '')} {g.get('city', '')} {g.get('district', '')}】")
        result.append(f"地址：{g.get('formatted_address', '')}")
        result.append(f"经度：{g.get('location', '').split(',')[0] if ',' in g.get('location', '') else '?'}")
        result.append(f"纬度：{g.get('location', '').split(',')[1] if ',' in g.get('location', '') else '?'}")
        result.append(f"AdCode：{g.get('adcode', '')}")
    
    return "\n".join(result)


def regeo(location):
    """逆地理编码：经纬度 → 地址"""
    params = {"location": location}
    
    data = api_request("/v3/geocode/regeo", params)
    
    if "error" in data:
        return data
    
    if data.get("status") != "1":
        return {"error": f"API返回错误: {data.get('info', '未知')}"}
    
    regeocode = data.get("regeocode", {})
    address = regeocode.get("formatted_address", "未知")
    
    result = [f"【坐标 {location}】"]
    result.append(f"地址：{address}")
    
    # 附近地址组件
    component = regeocode.get("addressComponent", {})
    if component:
        result.append(f"省/市：{component.get('province', '')}")
        result.append(f"市/区：{component.get('city', '')}")
        result.append(f"区/县：{component.get('district', '')}")
        result.append(f"街道：{component.get('streetNumber', {}).get('street', '')}")
        result.append(f"门牌号：{component.get('streetNumber', {}).get('number', '')}")
    
    return "\n".join(result)


def poi_search(keywords, city="", citycode=""):
    """POI搜索"""
    if citycode:
        params = {"keywords": keywords, "citycode": citycode}
    else:
        params = {"keywords": keywords, "city": city}
    
    data = api_request("/v3/place/text", params)
    
    if "error" in data:
        return data
    
    if data.get("status") != "1":
        return {"error": f"API返回错误: {data.get('info', '未知')}"}
    
    pois = data.get("pois", [])
    if not pois:
        return "未找到相关POI"
    
    count = min(len(pois), 10)  # 最多显示10条
    result = [f"【POI搜索: {keywords}】（共{data.get('count', '?')}条，显示前{count}条）"]
    
    for i, poi in enumerate(pois[:count]):
        result.append(f"\n{i+1}. {poi.get('name', '未知')}")
        result.append(f"   地址：{poi.get('address', '未知')}")
        result.append(f"   类型：{poi.get('type', '未知')}")
        result.append(f"   距离：{poi.get('distance', '?')}米")
        result.append(f"   坐标：{poi.get('location', '未知')}")
    
    return "\n".join(result)


def around_search(location, keywords, radius="1000"):
    """周边搜索"""
    params = {
        "location": location,
        "keywords": keywords,
        "radius": radius,
    }
    
    data = api_request("/v3/place/around", params)
    
    if "error" in data:
        return data
    
    if data.get("status") != "1":
        return {"error": f"API返回错误: {data.get('info', '未知')}"}
    
    pois = data.get("pois", [])
    if not pois:
        return f"周边{radius}米内未找到相关POI"
    
    count = min(len(pois), 10)
    result = [f"【周边搜索: {keywords}】（{radius}米内共{data.get('count', '?')}条，显示前{count}条）"]
    
    for i, poi in enumerate(pois[:count]):
        result.append(f"\n{i+1}. {poi.get('name', '未知')}")
        result.append(f"   地址：{poi.get('address', '未知')}")
        result.append(f"   类型：{poi.get('type', '未知')}")
        result.append(f"   距离：{poi.get('distance', '?')}米")
    
    return "\n".join(result)


def direction_driving(origin, destination):
    """驾车路径规划"""
    params = {
        "origin": origin,
        "destination": destination,
        "extensions": "all",
    }
    
    data = api_request("/v3/direction/driving", params, need_signature=True)
    
    if "error" in data:
        return data
    
    if data.get("status") != "1":
        return {"error": f"API返回错误: {data.get('info', '未知')}"}
    
    route = data.get("route", {})
    paths = route.get("paths", [])
    
    if not paths:
        return "未找到路线"
    
    result = [f"【驾车路线: {origin} → {destination}】"]
    
    for i, path in enumerate(paths[:3]):  # 显示前3条
        result.append(f"\n--- 方案{i+1} ---")
        result.append(f"距离：{path.get('distance', '?')}米（约{int(path.get('distance', 0))//1000}公里）")
        result.append(f"时间：{path.get('duration', '?')}秒（约{int(path.get('duration', 0))//60}分钟）")
        
        # 简单显示路线
        steps = path.get("steps", [])
        if steps:
            result.append("途经道路：")
            for j, step in enumerate(steps[:5]):  # 只显示前5步
                road = step.get("road_name", '未命名道路')
                instruction = step.get("instruction", '')
                if road and road != '未命名道路':
                    result.append(f"  {j+1}. {road}")
                elif instruction:
                    result.append(f"  {j+1}. {instruction[:30]}")
            if len(steps) > 5:
                result.append(f"  ...（共{len(steps)}步）")
    
    return "\n".join(result)


def direction_walking(origin, destination):
    """步行路径规划"""
    params = {
        "origin": origin,
        "destination": destination,
    }
    
    data = api_request("/v3/direction/walking", params)
    
    if "error" in data:
        return data
    
    if data.get("status") != "1":
        return {"error": f"API返回错误: {data.get('info', '未知')}"}
    
    route = data.get("route", {})
    paths = route.get("paths", [])
    
    if not paths:
        return "未找到路线"
    
    path = paths[0]
    result = [f"【步行路线: {origin} → {destination}】"]
    result.append(f"距离：{path.get('distance', '?')}米（约{int(path.get('distance', 0))//1000}公里）")
    result.append(f"时间：{path.get('duration', '?')}秒（约{int(path.get('duration', 0))//60}分钟）")
    
    steps = path.get("steps", [])
    if steps:
        result.append("\n路线：")
        for i, step in enumerate(steps[:8]):
            road = step.get("road_name", '')
            instruction = step.get("instruction", '')
            if road and road != '未命名道路':
                result.append(f"  {i+1}. {road}")
            elif instruction:
                result.append(f"  {i+1}. {instruction[:40]}")
        if len(steps) > 8:
            result.append(f"  ...（共{len(steps)}步）")
    
    return "\n".join(result)


def distance_measure(origin, destination):
    """距离测量"""
    params = {
        "origins": origin,
        "destination": destination,
    }
    
    data = api_request("/v3/distance", params, need_signature=True)
    
    if "error" in data:
        return data
    
    if data.get("status") != "1":
        return {"error": f"API返回错误: {data.get('info', '未知')}"}
    
    results = data.get("results", [])
    if not results:
        return "未找到距离数据"
    
    result = [f"【距离测量】"]
    for r in results:
        result.append(f"起点：{r.get('origin', '?')}")
        result.append(f"终点：{r.get('destination', '?')}")
        result.append(f"直线距离：{r.get('distance', '?')}米（约{int(r.get('distance', 0))//1000}公里）")
        result.append(f"步行距离：{r.get('walking_distance', '?')}米" if r.get('walking_distance') else "")
    
    return "\n".join(result)


def main():
    parser = argparse.ArgumentParser(description="高德地理信息服务")
    parser.add_argument("--action", "-a", 
                        choices=["geo", "regeo", "poi", "around", "direction", "distance", "walking"],
                        required=True, help="操作类型")
    
    # 地理编码参数
    parser.add_argument("--address", help="地址（用于地理编码）")
    parser.add_argument("--city", default="", help="城市名称")
    
    # 逆地理编码参数
    parser.add_argument("--location", help="坐标（用于逆地理编码）")
    
    # POI搜索参数
    parser.add_argument("--keywords", help="关键词")
    parser.add_argument("--citycode", default="", help="城市代码")
    parser.add_argument("--radius", default="1000", help="周边搜索半径（米）")
    
    # 路径规划参数
    parser.add_argument("--from", dest="origin", help="起点坐标")
    parser.add_argument("--to", dest="destination", help="终点坐标")
    
    args = parser.parse_args()
    
    # 执行对应操作
    if args.action == "geo":
        if not args.address:
            print("错误：地理编码需要 --address 参数", file=sys.stderr)
            sys.exit(1)
        result = geo_encode(args.address, args.city)
    
    elif args.action == "regeo":
        if not args.location:
            print("错误：逆地理编码需要 --location 参数", file=sys.stderr)
            sys.exit(1)
        result = regeo(args.location)
    
    elif args.action == "poi":
        if not args.keywords:
            print("错误：POI搜索需要 --keywords 参数", file=sys.stderr)
            sys.exit(1)
        result = poi_search(args.keywords, args.city, args.citycode)
    
    elif args.action == "around":
        if not args.location or not args.keywords:
            print("错误：周边搜索需要 --location 和 --keywords 参数", file=sys.stderr)
            sys.exit(1)
        result = around_search(args.location, args.keywords, args.radius)
    
    elif args.action == "direction":
        if not args.origin or not args.destination:
            print("错误：路径规划需要 --from 和 --to 参数", file=sys.stderr)
            sys.exit(1)
        result = direction_driving(args.origin, args.destination)
    
    elif args.action == "walking":
        if not args.origin or not args.destination:
            print("错误：步行路线需要 --from 和 --to 参数", file=sys.stderr)
            sys.exit(1)
        result = direction_walking(args.origin, args.destination)
    
    elif args.action == "distance":
        if not args.origin or not args.destination:
            print("错误：距离测量需要 --from 和 --to 参数", file=sys.stderr)
            sys.exit(1)
        result = distance_measure(args.origin, args.destination)
    
    else:
        result = "未知操作"
    
    print(result)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python amap_geo.py --action <操作> [参数]", file=sys.stderr)
        print("", file=sys.stderr)
        print("操作类型:", file=sys.stderr)
        print("  geo        - 地理编码（地址→坐标）", file=sys.stderr)
        print("  regeo     - 逆地理编码（坐标→地址）", file=sys.stderr)
        print("  poi       - POI搜索", file=sys.stderr)
        print("  around    - 周边搜索", file=sys.stderr)
        print("  direction - 驾车路线", file=sys.stderr)
        print("  walking   - 步行路线", file=sys.stderr)
        print("  distance  - 距离测量", file=sys.stderr)
        print("", file=sys.stderr)
        print("首次使用请先配置 API Key：", file=sys.stderr)
        print("  export AMAP_API_KEY=\"your-key\"", file=sys.stderr)
        print("  export AMAP_SECRET_KEY=\"your-secret\"  # 如需签名", file=sys.stderr)
        print(f"  或创建 {CONFIG_FILE} 填入 Key", file=sys.stderr)
        sys.exit(1)
    
    main()
