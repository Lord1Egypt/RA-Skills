#!/usr/bin/env python3
"""高德地图全能版 v2.0 - 22项地图能力全覆盖，零配置即装即用
新增：距离测量、静态地图、坐标转换、唤端导航、唤端打车"""

import sys
import json
import os
import urllib.request
import urllib.error
import urllib.parse

PROXY_URL = os.environ.get("GAODE_PROXY_URL", "https://1439498936-bl10af74fl.ap-guangzhou.tencentscf.com")
PROXY_TOKEN = os.environ.get("GAODE_PROXY_TOKEN", "tp_8k2mX9vQ4z")


def _post(type_name, params):
    """调用高德代理"""
    body = json.dumps({"type": type_name, "params": params}, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    req = urllib.request.Request(PROXY_URL, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("X-Proxy-Token", PROXY_TOKEN)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("code") == 0:
                return data.get("data", {})
            return data
    except urllib.error.HTTPError as e:
        err = ""
        try:
            err = e.read().decode("utf-8")[:300]
        except:
            pass
        return {"error": "HTTP " + str(e.code) + ": " + err}
    except Exception as e:
        return {"error": str(e)}


def _geocode(address, city=""):
    """辅助：地址转坐标"""
    result = _post("geocode", {"address": address, "city": city})
    geocodes = result.get("geocodes", [])
    if geocodes:
        loc = geocodes[0].get("location", "")
        if loc:
            return loc
    if city and city not in address:
        result2 = _post("geocode", {"address": city + address, "city": city})
        geocodes2 = result2.get("geocodes", [])
        if geocodes2:
            return geocodes2[0].get("location", "")
    return ""


# ==================== 22个工具函数 ====================

# --- 地理编码 ---
def tool_geocode(params):
    """地理编码：地址转经纬度"""
    p = {"address": params["address"]}
    if params.get("city"):
        p["city"] = params["city"]
    return _post("geocode", p)


def tool_regeocode(params):
    """逆地理编码：经纬度转地址"""
    p = {"location": params["location"]}
    if params.get("extensions"):
        p["extensions"] = params["extensions"]
    return _post("regeocode", p)


# --- POI搜索 ---
def tool_poi_search(params):
    """关键词搜索POI"""
    p = {"keywords": params["keywords"]}
    for k in ["city", "types", "offset", "page", "citylimit"]:
        if params.get(k) is not None:
            p[k] = params[k]
    return _post("poi_search", p)


def tool_poi_around(params):
    """周边搜索POI"""
    p = {"location": params["location"], "keywords": params["keywords"]}
    for k in ["radius", "offset", "page", "types"]:
        if params.get(k) is not None:
            p[k] = params[k]
    return _post("poi_around", p)


def tool_poi_detail(params):
    """POI详情查询"""
    return _post("poi_detail", {"id": params["id"]})


def tool_input_tips(params):
    """输入提示自动补全"""
    p = {"keywords": params["keywords"], "datatype": params.get("datatype", "all")}
    if params.get("city"):
        p["city"] = params["city"]
    return _post("input_tips", p)


# --- 行政区划 ---
def tool_district(params):
    """行政区划查询"""
    p = {"keywords": params.get("keywords", ""), "subdistrict": params.get("subdistrict", "1")}
    return _post("district", p)


# --- 路线规划（坐标版）---
def tool_driving_route(params):
    """驾车路线规划（坐标版）"""
    p = {"origin": params["origin"], "destination": params["destination"]}
    if params.get("strategy"):
        p["strategy"] = params["strategy"]
    if params.get("waypoints"):
        p["waypoints"] = params["waypoints"]
    return _post("driving_route", p)


def tool_transit_route(params):
    """公交路线规划（坐标版）"""
    p = {"origin": params["origin"], "destination": params["destination"], "city": params["city"]}
    if params.get("cityd"):
        p["cityd"] = params["cityd"]
    return _post("transit_route", p)


def tool_walking_route(params):
    """步行路线规划（坐标版）"""
    return _post("walking_route", {"origin": params["origin"], "destination": params["destination"]})


def tool_cycling_route(params):
    """骑行路线规划（坐标版）"""
    return _post("cycling_route", {"origin": params["origin"], "destination": params["destination"]})


# --- 路线规划（地址版）---
def tool_driving_route_by_address(params):
    """驾车路线规划（地址版，自动转坐标）"""
    origin = _geocode(params["origin_address"], params.get("origin_city", ""))
    if not origin:
        return {"error": "起点地址解析失败: " + params["origin_address"]}
    dest = _geocode(params["destination_address"], params.get("destination_city", ""))
    if not dest:
        return {"error": "终点地址解析失败: " + params["destination_address"]}
    return _post("driving_route", {"origin": origin, "destination": dest})


def tool_transit_route_by_address(params):
    """公交路线规划（地址版）"""
    city = params["city"]
    cityd = params.get("cityd", "")
    origin = _geocode(params["origin_address"], params.get("origin_city", "") or city)
    if not origin:
        return {"error": "起点地址解析失败: " + params["origin_address"]}
    dest = _geocode(params["destination_address"], params.get("destination_city", "") or cityd or city)
    if not dest:
        return {"error": "终点地址解析失败: " + params["destination_address"]}
    p = {"origin": origin, "destination": dest, "city": city}
    if cityd:
        p["cityd"] = cityd
    return _post("transit_route", p)


def tool_walking_route_by_address(params):
    """步行路线规划（地址版）"""
    origin = _geocode(params["origin_address"], params.get("origin_city", ""))
    if not origin:
        return {"error": "起点地址解析失败: " + params["origin_address"]}
    dest = _geocode(params["destination_address"], params.get("destination_city", ""))
    if not dest:
        return {"error": "终点地址解析失败: " + params["destination_address"]}
    return _post("walking_route", {"origin": origin, "destination": dest})


def tool_cycling_route_by_address(params):
    """骑行路线规划（地址版）"""
    origin = _geocode(params["origin_address"], params.get("origin_city", ""))
    if not origin:
        return {"error": "起点地址解析失败: " + params["origin_address"]}
    dest = _geocode(params["destination_address"], params.get("destination_city", ""))
    if not dest:
        return {"error": "终点地址解析失败: " + params["destination_address"]}
    return _post("cycling_route", {"origin": origin, "destination": dest})


# --- 天气与定位 ---
def tool_weather(params):
    """城市天气查询"""
    p = {"city": params["city"]}
    if params.get("extensions"):
        p["extensions"] = params["extensions"]
    return _post("weather", p)


def tool_ip_location(params):
    """IP定位"""
    p = {}
    if params.get("ip"):
        p["ip"] = params["ip"]
    return _post("ip_location", p)


# --- v2.0新增工具 ---

def tool_distance(params):
    """距离测量：支持驾车/步行/直线距离"""
    p = {"origins": params["origins"], "destination": params["destination"]}
    if params.get("type") is not None:
        p["type"] = str(params["type"])
    return _post("distance", p)


def tool_staticmap(params):
    """静态地图：生成地图图片URL"""
    p = {}
    for k in ["location", "zoom", "size", "scale", "markers", "labels", "paths", "traffic"]:
        if params.get(k) is not None:
            p[k] = params[k]
    return _post("staticmap", p)


def tool_coordinate_convert(params):
    """坐标转换：GPS/百度/MapBar → 高德坐标"""
    p = {"coords": params["coords"], "coordsys": params["coordsys"]}
    return _post("coordinate_convert", p)


def tool_schema_navi(params):
    """唤端导航：生成高德地图APP导航跳转URI"""
    p = {"lon": params.get("lon", ""), "lat": params.get("lat", "")}
    if params.get("name"):
        p["name"] = params["name"]
    if params.get("dev"):
        p["dev"] = params["dev"]
    return _post("schema_navi", p)


def tool_schema_take_taxi(params):
    """唤端打车：生成高德地图APP打车跳转URI"""
    p = {}
    for k in ["slon", "slat", "sname", "dlon", "dlat", "dname"]:
        if params.get(k):
            p[k] = params[k]
    return _post("schema_take_taxi", p)


# ==================== 工具路由 ====================

TOOLS = {
    # 地理编码
    "geocode": tool_geocode,
    "regeocode": tool_regeocode,
    # POI搜索
    "poi_search": tool_poi_search,
    "poi_around": tool_poi_around,
    "poi_detail": tool_poi_detail,
    "input_tips": tool_input_tips,
    # 行政区划
    "district": tool_district,
    # 路线规划（坐标版）
    "driving_route": tool_driving_route,
    "transit_route": tool_transit_route,
    "walking_route": tool_walking_route,
    "cycling_route": tool_cycling_route,
    # 路线规划（地址版）
    "driving_route_by_address": tool_driving_route_by_address,
    "transit_route_by_address": tool_transit_route_by_address,
    "walking_route_by_address": tool_walking_route_by_address,
    "cycling_route_by_address": tool_cycling_route_by_address,
    # 天气与定位
    "weather": tool_weather,
    "ip_location": tool_ip_location,
    # v2.0新增
    "distance": tool_distance,
    "staticmap": tool_staticmap,
    "coordinate_convert": tool_coordinate_convert,
    "schema_navi": tool_schema_navi,
    "schema_take_taxi": tool_schema_take_taxi,
}


def main():
    if len(sys.argv) < 3:
        print(json.dumps({"error": "用法: python3 main.py <tool> '<json_params>'", "available_tools": list(TOOLS.keys())}, ensure_ascii=False))
        sys.exit(1)

    tool_name = sys.argv[1]
    try:
        params = json.loads(sys.argv[2])
    except json.JSONDecodeError as e:
        print(json.dumps({"error": "参数JSON解析失败: " + str(e)}, ensure_ascii=False))
        sys.exit(1)

    if tool_name not in TOOLS:
        print(json.dumps({"error": "未知工具: " + tool_name, "available_tools": list(TOOLS.keys())}, ensure_ascii=False))
        sys.exit(1)

    try:
        result = TOOLS[tool_name](params)
        print(json.dumps(result, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
