#!/usr/bin/env python3
"""高德地图全能版 - 17项地图能力，免Key即用"""

import os
import sys
import json
import urllib.request
import urllib.error

PROXY_URL = "https://1439498936-bl10af74fl.ap-guangzhou.tencentscf.com"
PROXY_TOKEN = os.environ.get("PROXY_TOKEN", "")
TIMEOUT = 30


def _call_proxy(rtype, params, timeout=None):
    """调用高德代理API"""
    body = json.dumps({"type": rtype, "params": params}, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    req = urllib.request.Request(
        PROXY_URL, data=body,
        headers={"Content-Type": "application/json", "X-Proxy-Token": PROXY_TOKEN},
        method="POST",
    )
    _timeout = timeout or TIMEOUT
    try:
        with urllib.request.urlopen(req, timeout=_timeout) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err = ""
        try: err = e.read().decode("utf-8", errors="replace")[:300]
        except: pass
        return {"error": "proxy error " + str(e.code) + ": " + err}
    except Exception as e:
        return {"error": "request error: " + str(e)}


def call_api(api, params):
    """调用高德代理API（兼容旧接口）"""
    return _call_proxy(api, params)


def geocode_address(address, city=""):
    """地理编码，带自动重试"""
    params = {"address": address}
    if city:
        params["city"] = city
    data = _call_proxy("geocode/geo", params)
    geocodes = data.get("geocodes", [])
    if geocodes:
        location = geocodes[0].get("location", "")
        if location:
            return location
    if city and city not in address:
        params2 = {"address": city + address, "city": city}
        data2 = _call_proxy("geocode/geo", params2)
        geocodes2 = data2.get("geocodes", [])
        if geocodes2:
            return geocodes2[0].get("location", "")
    return ""


# ==================== 工具函数 ====================

def tool_geocode(params):
    p = {"address": params["address"]}
    if params.get("city"):
        p["city"] = params["city"]
    return call_api("geocode/geo", p)


def tool_regeocode(params):
    return call_api("geocode/regeo", {"location": params["location"]})


def tool_poi_search(params):
    p = {"keywords": params["keywords"]}
    for k in ["city", "types", "offset", "page"]:
        if params.get(k):
            p[k] = params[k]
    return call_api("place/text", p)


def tool_poi_around(params):
    p = {"location": params["location"], "keywords": params["keywords"]}
    for k in ["radius", "offset", "page"]:
        if params.get(k):
            p[k] = params[k]
    return call_api("place/around", p)


def tool_poi_detail(params):
    return call_api("place/detail", {"id": params["id"]})


def tool_input_tips(params):
    p = {"keywords": params["keywords"], "datatype": params.get("datatype", "all")}
    if params.get("city"):
        p["city"] = params["city"]
    return call_api("assistant/inputtips", p)


def tool_district(params):
    p = {"keywords": params.get("keywords", ""), "subdistrict": params.get("subdistrict", "1")}
    return call_api("config/district", p)


def tool_driving_route(params):
    return call_api("direction/driving", {"origin": params["origin"], "destination": params["destination"]})


def tool_transit_route(params):
    p = {"origin": params["origin"], "destination": params["destination"], "city": params["city"]}
    if params.get("cityd"):
        p["cityd"] = params["cityd"]
    return call_api("direction/transit/integrated", p)


def tool_walking_route(params):
    return call_api("direction/walking", {"origin": params["origin"], "destination": params["destination"]})


def tool_cycling_route(params):
    return call_api("direction/riding", {"origin": params["origin"], "destination": params["destination"]})


def tool_driving_route_by_address(params):
    origin = geocode_address(params["origin_address"], params.get("origin_city", ""))
    if not origin:
        return {"error": "起点地址解析失败: " + params["origin_address"]}
    destination = geocode_address(params["destination_address"], params.get("destination_city", ""))
    if not destination:
        return {"error": "终点地址解析失败: " + params["destination_address"]}
    return call_api("direction/driving", {"origin": origin, "destination": destination})


def tool_transit_route_by_address(params):
    city = params["city"]
    cityd = params.get("cityd", "")
    origin_city = params.get("origin_city", "") or city
    destination_city = params.get("destination_city", "") or cityd or city
    origin = geocode_address(params["origin_address"], origin_city)
    if not origin:
        return {"error": "起点地址解析失败: " + params["origin_address"]}
    destination = geocode_address(params["destination_address"], destination_city)
    if not destination:
        return {"error": "终点地址解析失败: " + params["destination_address"]}
    p = {"origin": origin, "destination": destination, "city": city}
    if cityd:
        p["cityd"] = cityd
    return call_api("direction/transit/integrated", p)


def tool_walking_route_by_address(params):
    origin = geocode_address(params["origin_address"], params.get("origin_city", ""))
    if not origin:
        return {"error": "起点地址解析失败: " + params["origin_address"]}
    destination = geocode_address(params["destination_address"], params.get("destination_city", ""))
    if not destination:
        return {"error": "终点地址解析失败: " + params["destination_address"]}
    return call_api("direction/walking", {"origin": origin, "destination": destination})


def tool_cycling_route_by_address(params):
    origin = geocode_address(params["origin_address"], params.get("origin_city", ""))
    if not origin:
        return {"error": "起点地址解析失败: " + params["origin_address"]}
    destination = geocode_address(params["destination_address"], params.get("destination_city", ""))
    if not destination:
        return {"error": "终点地址解析失败: " + params["destination_address"]}
    return call_api("direction/riding", {"origin": origin, "destination": destination})


def tool_weather(params):
    return call_api("weather/weatherInfo", {"city": params["city"]})


def tool_ip_location(params):
    p = {}
    if params.get("ip"):
        p["ip"] = params["ip"]
    return call_api("ip", p)


# ==================== 工具路由 ====================

TOOLS = {
    "geocode": tool_geocode,
    "regeocode": tool_regeocode,
    "poi_search": tool_poi_search,
    "poi_around": tool_poi_around,
    "poi_detail": tool_poi_detail,
    "input_tips": tool_input_tips,
    "district": tool_district,
    "driving_route": tool_driving_route,
    "transit_route": tool_transit_route,
    "walking_route": tool_walking_route,
    "cycling_route": tool_cycling_route,
    "driving_route_by_address": tool_driving_route_by_address,
    "transit_route_by_address": tool_transit_route_by_address,
    "walking_route_by_address": tool_walking_route_by_address,
    "cycling_route_by_address": tool_cycling_route_by_address,
    "weather": tool_weather,
    "ip_location": tool_ip_location,
}


def main():
    if len(sys.argv) < 3:
        print(json.dumps({"error": "用法: python3 main.py <tool> '<json_params>'"}, ensure_ascii=False))
        sys.exit(1)

    tool_name = sys.argv[1]
    try:
        params = json.loads(sys.argv[2])
    except json.JSONDecodeError as e:
        print(json.dumps({"error": "参数JSON解析失败: " + str(e)}, ensure_ascii=False))
        sys.exit(1)

    if tool_name not in TOOLS:
        print(json.dumps({"error": f"未知工具: {tool_name}，可用工具: {', '.join(TOOLS.keys())}"}, ensure_ascii=False))
        sys.exit(1)

    try:
        result = TOOLS[tool_name](params)
        print(json.dumps(result, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
