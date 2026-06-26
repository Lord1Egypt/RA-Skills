#!/usr/bin/env python3
"""
Gaode Map All-in-One Search Script
Usage: python gaode_map.py <command> [options]

Commands:
- ip        : IP location - get user location
- geo       : Geocoding - address to coordinates
- poi       : POI search (keyword, nearby, city)
- route     : Route planning (driving, walking, transit)
- weather   : Weather query
- bus       : Bus/Transit search
- traffic   : Traffic status
- tip       : Input tips (autocomplete)
"""

import argparse
import json
import math
import os
import time
import urllib.error
import urllib.parse
import urllib.request
import sys
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, TypeVar

# Type alias
F = TypeVar('F', bound=Callable[..., Any])


# ============ API Key Helper ============
def get_api_key() -> Optional[str]:
    """获取API Key，优先使用环境变量
    
    Returns:
        API Key 字符串，如果环境变量未设置则返回 None
    """
    env_key = os.getenv("AMAP_API_KEY")
    if env_key:
        return env_key
    return None


# ============ Custom Exception ============
class APIError(Exception):
    """API Error Exception"""
    pass


# ============ Retry Decorator ============
def retry(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0) -> Callable[[F], F]:
    """
    Retry decorator with exponential backoff
    
    Args:
        max_attempts: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        backoff: Multiplier for delay after each retry
    """
    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            attempt_delay = delay
            last_exception: Exception = APIError("Unknown error")
            
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except APIError as e:
                    last_exception = e
                    if attempt < max_attempts:
                        time.sleep(attempt_delay)
                        attempt_delay *= backoff
                    else:
                        raise last_exception
                    
            raise last_exception
        return wrapper  # type: ignore
    return decorator


# ============ Parameter Validation ============
def validate_coords(loc: str) -> bool:
    """
    Validate coordinate format (lon,lat)
    
    Args:
        loc: Coordinate string in format "lon,lat"
        
    Returns:
        True if valid, False otherwise
    """
    try:
        lon, lat = map(float, loc.split(","))
        return -180 <= lon <= 180 and -90 <= lat <= 90
    except (ValueError, AttributeError, TypeError):
        return False


def validate_api_key(key: Optional[str]) -> bool:
    """
    Validate API key format
    
    Args:
        key: API key string
        
    Returns:
        True if valid, False otherwise
    """
    if not key or not isinstance(key, str):
        return False
    return len(key) >= 10


# ============ Common Request Layer ============
@retry(max_attempts=3, delay=1.0, backoff=2.0)
def _request(url: str, timeout: int = 10) -> Dict[str, Any]:
    """
    Common HTTP request method with retry mechanism
    
    Args:
        url: Full URL to request
        timeout: Request timeout in seconds
        
    Returns:
        JSON response as dictionary
        
    Raises:
        APIError: If request fails or API returns error status
    """
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("status") != "1":
                raise APIError(data.get("info", "API error"))
            return data
    except urllib.error.URLError as e:
        raise APIError(f"Network error: {e}")
    except json.JSONDecodeError as e:
        raise APIError(f"JSON decode error: {e}")


# ============ IP Location ============
@retry()
def ip_location(key: str, ip: Optional[str] = None) -> Dict[str, Any]:
    """IP location - Get user's current city"""
    if not validate_api_key(key):
        raise APIError("Invalid API key")
    
    base_url = "https://restapi.amap.com/v3/ip"
    params: Dict[str, Any] = {"key": key, "output": "json"}
    if ip:
        params["ip"] = ip
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    return _request(url)


# ============ Geocoding ============
@retry()
def geocode(key: str, address: str, city: Optional[str] = None) -> Dict[str, Any]:
    """Geocoding - Address to coordinates"""
    if not validate_api_key(key):
        raise APIError("Invalid API key")
    if not address:
        raise APIError("Address is required")
    
    base_url = "https://restapi.amap.com/v3/geocode/geo"
    params: Dict[str, Any] = {"key": key, "address": address, "output": "json"}
    if city:
        params["city"] = city
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    return _request(url)


@retry()
def regeo(key: str, location: str) -> Dict[str, Any]:
    """Reverse geocoding - Coordinates to address"""
    if not validate_api_key(key):
        raise APIError("Invalid API key")
    if not validate_coords(location):
        raise APIError(f"Invalid coordinates format: {location}. Expected format: lon,lat")
    
    base_url = "https://restapi.amap.com/v3/geocode/regeo"
    params: Dict[str, Any] = {"key": key, "location": location, "output": "json"}
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    return _request(url)


# ============ POI Search ============
@retry()
def search_poi(
    key: str,
    keyword: str,
    city: Optional[str] = None,
    citylimit: bool = False,
    page: int = 1,
    offset: int = 20
) -> Dict[str, Any]:
    """Keyword search POI"""
    if not validate_api_key(key):
        raise APIError("Invalid API key")
    if not keyword:
        raise APIError("Keyword is required")
    
    base_url = "https://restapi.amap.com/v3/place/text"
    params: Dict[str, Any] = {
        "key": key,
        "keywords": keyword,
        "offset": offset,
        "page": page,
        "extensions": "all",
        "output": "json"
    }
    if city:
        params["city"] = city
    if citylimit:
        params["citylimit"] = "true"
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    return _request(url)


@retry()
def search_nearby(
    key: str,
    location: str,
    radius: int,
    keyword: str,
    page: int = 1,
    offset: int = 20
) -> Dict[str, Any]:
    """Nearby search POI"""
    if not validate_api_key(key):
        raise APIError("Invalid API key")
    if not validate_coords(location):
        raise APIError(f"Invalid coordinates format: {location}. Expected format: lon,lat")
    if radius <= 0 or radius > 50000:
        raise APIError("Radius must be between 1 and 50000 meters")
    if not keyword:
        raise APIError("Keyword is required")
    
    base_url = "https://restapi.amap.com/v3/place/around"
    params: Dict[str, Any] = {
        "key": key,
        "location": location,
        "radius": radius,
        "keywords": keyword,
        "offset": offset,
        "page": page,
        "extensions": "all",
        "output": "json"
    }
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    return _request(url)


# ============ Route Planning ============
@retry()
def route_driving(
    key: str,
    origin: str,
    destination: str,
    strategy: int = 5
) -> Dict[str, Any]:
    """Driving route planning"""
    if not validate_api_key(key):
        raise APIError("Invalid API key")
    if not validate_coords(origin):
        raise APIError(f"Invalid origin coordinates: {origin}. Expected format: lon,lat")
    if not validate_coords(destination):
        raise APIError(f"Invalid destination coordinates: {destination}. Expected format: lon,lat")
    if strategy < 1 or strategy > 10:
        raise APIError("Strategy must be between 1 and 10")
    
    base_url = "https://restapi.amap.com/v3/direction/driving"
    params: Dict[str, Any] = {
        "key": key,
        "origin": origin,
        "destination": destination,
        "strategy": strategy,
        "output": "json"
    }
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    return _request(url)


@retry()
def route_walking(key: str, origin: str, destination: str) -> Dict[str, Any]:
    """Walking route planning"""
    if not validate_api_key(key):
        raise APIError("Invalid API key")
    if not validate_coords(origin):
        raise APIError(f"Invalid origin coordinates: {origin}. Expected format: lon,lat")
    if not validate_coords(destination):
        raise APIError(f"Invalid destination coordinates: {destination}. Expected format: lon,lat")
    
    base_url = "https://restapi.amap.com/v3/direction/walking"
    params: Dict[str, Any] = {
        "key": key,
        "origin": origin,
        "destination": destination,
        "output": "json"
    }
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    return _request(url)


@retry()
def route_transit(
    key: str,
    origin: str,
    destination: str,
    city: str,
    strategy: int = 0
) -> Dict[str, Any]:
    """Transit/bus route planning"""
    if not validate_api_key(key):
        raise APIError("Invalid API key")
    if not validate_coords(origin):
        raise APIError(f"Invalid origin coordinates: {origin}. Expected format: lon,lat")
    if not validate_coords(destination):
        raise APIError(f"Invalid destination coordinates: {destination}. Expected format: lon,lat")
    if not city:
        raise APIError("City is required for transit mode")
    if strategy < 0 or strategy > 2:
        raise APIError("Strategy must be between 0 and 2")
    
    base_url = "https://restapi.amap.com/v3/direction/transit"
    params: Dict[str, Any] = {
        "key": key,
        "origin": origin,
        "destination": destination,
        "city": city,
        "strategy": strategy,
        "output": "json"
    }
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    return _request(url, timeout=15)


# ============ Weather ============
@retry()
def weather(key: str, city: str, extensions: str = "base") -> Dict[str, Any]:
    """Weather query"""
    if not validate_api_key(key):
        raise APIError("Invalid API key")
    if not city:
        raise APIError("City is required")
    if extensions not in ("base", "all"):
        raise APIError("Extensions must be 'base' or 'all'")
    
    base_url = "https://restapi.amap.com/v3/weather/weatherInfo"
    params: Dict[str, Any] = {
        "key": key,
        "city": city,
        "extensions": extensions,
        "output": "json"
    }
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    return _request(url)


# ============ Traffic ============
@retry()
def traffic(key: str, city: str, road: Optional[str] = None) -> Dict[str, Any]:
    """Traffic status query"""
    if not validate_api_key(key):
        raise APIError("Invalid API key")
    if not city:
        raise APIError("City is required")
    
    base_url = "https://restapi.amap.com/v3/traffic/status/road"
    params: Dict[str, Any] = {"key": key, "city": city, "output": "json"}
    if road:
        params["roadname"] = road
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    return _request(url)


# ============ Input Tips ============
@retry()
def input_tips(key: str, keyword: str, city: Optional[str] = None) -> Dict[str, Any]:
    """Input tips (autocomplete)"""
    if not validate_api_key(key):
        raise APIError("Invalid API key")
    if not keyword:
        raise APIError("Keyword is required")
    
    base_url = "https://restapi.amap.com/v3/assistant/tips"
    params: Dict[str, Any] = {"key": key, "keywords": keyword, "output": "json"}
    if city:
        params["city"] = city
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    return _request(url)


# ============ Distance Calculation ============
def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate distance between two points using Haversine formula
    
    Args:
        lat1: Latitude of first point
        lon1: Longitude of first point
        lat2: Latitude of second point
        lon2: Longitude of second point
        
    Returns:
        Distance in meters
    """
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c


@retry()
def route_distance(key: str, origin: str, destination: str) -> int:
    """
    Get driving distance between two points using route planning API
    
    Args:
        key: API key
        origin: Origin coordinates (lon,lat)
        destination: Destination coordinates (lon,lat)
        
    Returns:
        Distance in meters, or -1 if failed
    """
    if not validate_api_key(key):
        raise APIError("Invalid API key")
    if not validate_coords(origin):
        raise APIError(f"Invalid origin coordinates: {origin}")
    if not validate_coords(destination):
        raise APIError(f"Invalid destination coordinates: {destination}")
    
    base_url = "https://restapi.amap.com/v3/direction/driving"
    params: Dict[str, Any] = {
        "key": key,
        "origin": origin,
        "destination": destination,
        "strategy": 5,  # 距离最短
        "output": "json"
    }
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    
    try:
        data = _request(url)
        paths = data.get("route", {}).get("paths", [])
        if paths:
            return int(paths[0].get("distance", 0))
    except APIError:
        pass
    return -1


# ============ Output Formatters ============
def format_output(data: Dict[str, Any], json_output: bool = False, format_type: str = "default", poi_distances: Optional[List[int]] = None) -> None:
    """Format output data"""
    if data.get("status") != "1":
        msg = f"Error: {data.get('info', 'Unknown error')}"
        if json_output:
            print(json.dumps({"error": msg}, ensure_ascii=False))
        else:
            print(msg)
        return
    
    if json_output:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return
    
    # Text format
    if format_type == "ip":
        print(f"Your location: {data.get('province', 'N/A')} {data.get('city', 'N/A')}")
        print(f"City code: {data.get('adcode', 'N/A')}")
    
    elif format_type == "geo" or format_type == "regeo":
        for gc in data.get("geocodes", [data]):
            print(f"Address: {gc.get('province','')}{gc.get('city','')}{gc.get('district','')}{gc.get('township','')}")
            print(f"Location: {gc.get('location', 'N/A')}")
    
    elif format_type == "poi":
        pois = data.get("pois", [])
        count = data.get("count", len(pois))
        print(f"Found {count} results:\n")
        for i, poi in enumerate(pois[:10], 1):
            name = poi.get('name', 'N/A')
            address = poi.get('address', 'N/A')
            
            # 如果有距离信息，显示距离
            if poi_distances and i - 1 < len(poi_distances):
                dist = poi_distances[i - 1]
                if dist >= 0:
                    print(f"{i}. {name} | 地址：{address} | 距离：{dist}米")
                else:
                    print(f"{i}. {name} | 地址：{address} | 距离：计算失败")
            else:
                print(f"{i}. {name}")
                print(f"   Address: {address}")
                print(f"   Location: {poi.get('location', 'N/A')}")
                if poi.get('tel'):
                    print(f"   Phone: {poi.get('tel')}")
    
    elif format_type == "route":
        route = data.get("route", {})
        paths = route.get("paths", [])
        if paths:
            path = paths[0]
            print(f"Distance: {path.get('distance', 'N/A')} meters")
            print(f"Duration: {path.get('duration', 'N/A')} seconds")
            print(f"Strategy: {route.get('strategy', 'N/A')}")
            steps = path.get("steps", [])
            print(f"Steps ({len(steps)}):")
            for i, step in enumerate(steps[:5], 1):
                print(f"  {i}. {step.get('instruction', 'N/A')[:80]}")
            if len(steps) > 5:
                print(f"  ... and {len(steps)-5} more steps")
    
    elif format_type == "weather":
        lives = data.get("lives", [])
        forecasts = data.get("forecasts", [])
        if lives:
            live = lives[0]
            print(f"City: {live.get('city', 'N/A')}")
            print(f"Weather: {live.get('weather', 'N/A')}")
            print(f"Temperature: {live.get('temperature', 'N/A')}°C")
            print(f"Wind: {live.get('winddirection', 'N/A')} {live.get('windpower', 'N/A')}")
            print(f"Humidity: {live.get('humidity', 'N/A')}%")
        if forecasts:
            forecast = forecasts[0]
            print(f"\nForecast:")
            for fc in forecast.get("casts", []):
                print(f"  {fc.get('date')}: {fc.get('dayWeather')} / {fc.get('nightWeather')}, {fc.get('nightTemp')}°C ~ {fc.get('dayTemp')}°C")
    
    elif format_type == "traffic":
        roads = data.get("roads", [])
        print(f"Found {len(roads)} roads with traffic info:")
        for road in roads[:5]:
            print(f"  - {road.get('name', 'N/A')}: {road.get('status', 'N/A')}")
    
    elif format_type == "tips":
        tips = data.get("tips", [])
        print(f"Found {len(tips)} suggestions:\n")
        for i, tip in enumerate(tips[:10], 1):
            print(f"{i}. {tip.get('name', 'N/A')}")
            print(f"   Address: {tip.get('address', 'N/A')}")
            print(f"   Location: {tip.get('location', 'N/A')}")
            print()
    
    else:
        print(json.dumps(data, ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Gaode Map All-in-One Tool")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # IP
    ip_parser = subparsers.add_parser("ip", help="IP location")
    ip_parser.add_argument("--key", help="Gaode API Key (或设置环境变量 AMAP_API_KEY)")
    ip_parser.add_argument("--ip", help="IP address")
    
    # Geo
    geo_parser = subparsers.add_parser("geo", help="Geocoding - address to coordinates")
    geo_parser.add_argument("--key", help="Gaode API Key (或设置环境变量 AMAP_API_KEY)")
    geo_parser.add_argument("--address", required=True, help="Address")
    geo_parser.add_argument("--city", help="City")
    
    # Regeo
    regeo_parser = subparsers.add_parser("regeo", help="Reverse geocoding - coordinates to address")
    regeo_parser.add_argument("--key", help="Gaode API Key (或设置环境变量 AMAP_API_KEY)")
    regeo_parser.add_argument("--location", required=True, help="Coordinates (lon,lat)")
    
    # POI
    poi_parser = subparsers.add_parser("poi", help="POI search")
    poi_parser.add_argument("--key", help="Gaode API Key (或设置环境变量 AMAP_API_KEY)")
    poi_parser.add_argument("--keyword", required=True, help="Keyword")
    poi_parser.add_argument("--city", help="City")
    poi_parser.add_argument("--citylimit", action="store_true", help="Limit to city")
    poi_parser.add_argument("--location", help="Location (lon,lat) for nearby search or distance calculation")
    poi_parser.add_argument("--radius", type=int, default=5000, help="Radius (meters)")
    poi_parser.add_argument("--page", type=int, default=1, help="Page")
    poi_parser.add_argument("--with-distance", action="store_true", help="Calculate and display distance for each POI (requires --location)")
    
    # Route
    route_parser = subparsers.add_parser("route", help="Route planning")
    route_parser.add_argument("--key", help="Gaode API Key (或设置环境变量 AMAP_API_KEY)")
    route_parser.add_argument("--origin", required=True, help="Origin (lon,lat)")
    route_parser.add_argument("--destination", required=True, help="Destination (lon,lat)")
    route_parser.add_argument("--mode", default="driving", choices=["driving", "walking", "transit"], help="Mode")
    route_parser.add_argument("--city", help="City (for transit)")
    route_parser.add_argument("--strategy", type=int, default=5, help="Strategy")
    
    # Weather
    weather_parser = subparsers.add_parser("weather", help="Weather query")
    weather_parser.add_argument("--key", help="Gaode API Key (或设置环境变量 AMAP_API_KEY)")
    weather_parser.add_argument("--city", required=True, help="City")
    weather_parser.add_argument("--forecast", action="store_true", help="Include forecast")
    
    # Traffic
    traffic_parser = subparsers.add_parser("traffic", help="Traffic status")
    traffic_parser.add_argument("--key", help="Gaode API Key (或设置环境变量 AMAP_API_KEY)")
    traffic_parser.add_argument("--city", required=True, help="City")
    traffic_parser.add_argument("--road", help="Road name")
    
    # Tips
    tips_parser = subparsers.add_parser("tips", help="Input tips (autocomplete)")
    tips_parser.add_argument("--key", help="Gaode API Key (或设置环境变量 AMAP_API_KEY)")
    tips_parser.add_argument("--keyword", required=True, help="Keyword")
    tips_parser.add_argument("--city", help="City")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # API Key 获取逻辑：优先使用环境变量，其次使用命令行参数
    if args.key is None:
        args.key = os.getenv("AMAP_API_KEY")
    
    if args.key is None:
        raise ValueError("请通过环境变量 AMAP_API_KEY 或命令行参数 --key 提供API Key")
    
    json_out = args.json
    
    try:
        if args.command == "ip":
            data = ip_location(args.key, args.ip)
            format_output(data, json_out, "ip")
        
        elif args.command == "geo":
            data = geocode(args.key, args.address, args.city)
            format_output(data, json_out, "geo")
        
        elif args.command == "regeo":
            data = regeo(args.key, args.location)
            format_output(data, json_out, "regeo")
        
        elif args.command == "poi":
            poi_distances = None
            
            if args.location:
                data = search_nearby(args.key, args.location, args.radius, args.keyword, args.page)
            else:
                data = search_poi(args.key, args.keyword, args.city, args.citylimit, args.page)
            
            # 如果启用了 --with-distance 且提供了 location，计算每个POI的距离
            if args.with_distance:
                if not args.location:
                    print("Warning: --with-distance requires --location, ignoring distance calculation")
                    format_output(data, json_out, "poi")
                else:
                    origin = args.location
                    pois = data.get("pois", [])[:10]  # 最多处理前10个
                    poi_distances = []
                    
                    print("Calculating distances...")
                    for poi in pois:
                        poi_loc = poi.get("location", "")
                        if poi_loc:
                            # 调用路径规划API获取驾驶距离
                            dist = route_distance(args.key, origin, poi_loc)
                            poi_distances.append(dist)
                        else:
                            poi_distances.append(-1)
                    
                    format_output(data, json_out, "poi", poi_distances)
                    return
            
            format_output(data, json_out, "poi")
        
        elif args.command == "route":
            if args.mode == "driving":
                data = route_driving(args.key, args.origin, args.destination, args.strategy)
                format_output(data, json_out, "route")
            elif args.mode == "walking":
                data = route_walking(args.key, args.origin, args.destination)
                format_output(data, json_out, "route")
            elif args.mode == "transit":
                if not args.city:
                    print("Error: --city is required for transit mode")
                    return
                data = route_transit(args.key, args.origin, args.destination, args.city, args.strategy)
                format_output(data, json_out, "route")
        
        elif args.command == "weather":
            ext = "all" if args.forecast else "base"
            data = weather(args.key, args.city, ext)
            format_output(data, json_out, "weather")
        
        elif args.command == "traffic":
            data = traffic(args.key, args.city, args.road)
            format_output(data, json_out, "traffic")
        
        elif args.command == "tips":
            data = input_tips(args.key, args.keyword, args.city)
            format_output(data, json_out, "tips")
            
    except APIError as e:
        print(f"API Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
