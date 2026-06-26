#!/usr/bin/env python3
"""
Gaode Map POI Search Script
Usage: python poi_search.py <command> [options]
"""

import argparse
import json
import math
import urllib.parse
import urllib.request
import sys


def ip_location(key, ip=None):
    """IP location - Get user's current city"""
    base_url = "https://restapi.amap.com/v3/ip"
    
    params = {
        "key": key,
        "output": "json"
    }
    
    if ip:
        params["ip"] = ip
    
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            return data
    except Exception as e:
        return {"status": "0", "info": str(e)}


def search_poi(key, keyword, city=None, location=None, radius=5000, page=1, offset=20):
    """Keyword search POI"""
    base_url = "https://restapi.amap.com/v3/place/text"
    
    params = {
        "key": key,
        "keywords": keyword,
        "offset": offset,
        "page": page,
        "extensions": "all",
        "output": "json"
    }
    
    if city:
        params["city"] = city
    
    if location:
        params["citylimit"] = "true"
    
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            return data
    except Exception as e:
        return {"status": "0", "info": str(e)}


def search_nearby(key, location, radius, keyword, page=1, offset=20):
    """Nearby search POI"""
    base_url = "https://restapi.amap.com/v3/place/around"
    
    params = {
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
    
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            return data
    except Exception as e:
        return {"status": "0", "info": str(e)}


def geocode(key, address, city=None):
    """Geocoding - Address to coordinates"""
    base_url = "https://restapi.amap.com/v3/geocode/geo"
    
    params = {
        "key": key,
        "address": address,
        "output": "json"
    }
    
    if city:
        params["city"] = city
    
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            return data
    except Exception as e:
        return {"status": "0", "info": str(e)}


def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points (in meters)"""
    R = 6371000  # Earth radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi/2) * math.sin(delta_phi/2) + \
        math.cos(phi1) * math.cos(phi2) * \
        math.sin(delta_lambda/2) * math.sin(delta_lambda/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return R * c


def format_ip_results(data, json_output=False):
    """Format IP location results"""
    if data.get("status") != "1":
        msg = f"Query failed: {data.get('info', 'Unknown error')}"
        if json_output:
            return {"error": msg}
        print(msg)
        return None
    
    province = data.get("province", "Unknown")
    city = data.get("city", "Unknown")
    adcode = data.get("adcode", "")
    
    result = {"province": province, "city": city, "adcode": adcode}
    
    if json_output:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Your location: {province} {city}")
        print(f"City code: {adcode}")
        print()
    
    return result


def format_poi_results(data, user_location=None, json_output=False):
    """Format POI search results"""
    if data.get("status") != "1":
        msg = f"Search failed: {data.get('info', 'Unknown error')}"
        if json_output:
            print(json.dumps({"error": msg}, ensure_ascii=False))
        else:
            print(msg)
        return
    
    pois = data.get("pois", [])
    if not pois:
        msg = "No results found"
        if json_output:
            print(json.dumps({"results": [], "count": 0}, ensure_ascii=False))
        else:
            print(msg)
        return
    
    count = data.get("count", len(pois))
    
    results = []
    for poi in pois[:10]:
        name = poi.get("name", "")
        address = poi.get("address", "")
        location = poi.get("location", "")
        telephone = poi.get("tel", "")
        province = poi.get("province", "")
        city = poi.get("city", "")
        district = poi.get("district", "")
        
        # Calculate distance (for keyword search, need manual calculation)
        distance = poi.get("distance", None)
        if not distance and user_location and location:
            try:
                user_lat, user_lon = map(float, user_location.split(","))
                poi_lat, poi_lon = map(float, location.split(","))
                dist = calculate_distance(user_lat, user_lon, poi_lat, poi_lon)
                distance = int(dist)
            except:
                pass
        
        # Format distance
        distance_str = ""
        if distance:
            try:
                d = int(distance)
                if d >= 1000:
                    distance_str = f"{d/1000:.1f}km"
                else:
                    distance_str = f"{d}m"
            except:
                distance_str = str(distance)
        
        item = {
            "name": name,
            "address": f"{province}{city}{district}{address}" if address else f"{province}{city}{district}",
            "location": location,
            "telephone": telephone
        }
        if distance_str:
            item["distance"] = distance_str
        
        results.append(item)
    
    output = {"results": results, "count": count}
    
    if json_output:
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(f"Found {count} results:\n")
        for i, item in enumerate(results, 1):
            print(f"{i}. {item['name']}")
            print(f"   Address: {item['address']}")
            if item.get("distance"):
                print(f"   Distance: {item['distance']}")
            if item["telephone"]:
                print(f"   Phone: {item['telephone']}")
            print()


def format_geocode_results(data, json_output=False):
    """Format geocoding results"""
    if data.get("status") != "1":
        msg = f"Query failed: {data.get('info', 'Unknown error')}"
        if json_output:
            print(json.dumps({"error": msg}, ensure_ascii=False))
        else:
            print(msg)
        return
    
    geocodes = data.get("geocodes", [])
    if not geocodes:
        msg = "No coordinates found for this address"
        if json_output:
            print(json.dumps({"error": msg}, ensure_ascii=False))
        else:
            print(msg)
        return
    
    results = []
    for gc in geocodes:
        results.append({
            "address": f"{gc.get('province', '')}{gc.get('city', '')}{gc.get('district', '')}{gc.get('township', '')}",
            "location": gc.get("location", ""),
            "level": gc.get("level", "")
        })
    
    if json_output:
        print(json.dumps({"results": results}, ensure_ascii=False, indent=2))
    else:
        for item in results:
            print(f"Address: {item['address']}")
            print(f"Coordinates: {item['location']}")
            print(f"Level: {item['level']}")
            print()


def main():
    parser = argparse.ArgumentParser(description="Gaode Map POI Search Tool")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    subparsers = parser.add_subparsers(dest="command", help="Subcommands")
    
    # ip subcommand
    ip_parser = subparsers.add_parser("ip", help="IP location - Get current location")
    ip_parser.add_argument("--key", required=True, help="Gaode API Key")
    ip_parser.add_argument("--ip", help="Specify IP, auto-detect if not provided")
    
    # poi subcommand
    poi_parser = subparsers.add_parser("poi", help="Keyword search POI")
    poi_parser.add_argument("--key", required=True, help="Gaode API Key")
    poi_parser.add_argument("--keyword", required=True, help="Search keyword")
    poi_parser.add_argument("--city", help="City name")
    poi_parser.add_argument("--location", help="Coordinates (lat,lon) for distance calculation")
    poi_parser.add_argument("--radius", type=int, default=5000, help="Search radius (meters)")
    poi_parser.add_argument("--page", type=int, default=1, help="Page number")
    poi_parser.add_argument("--offset", type=int, default=20, help="Results per page")
    
    # geo subcommand
    geo_parser = subparsers.add_parser("geo", help="Geocoding - Address to coordinates")
    geo_parser.add_argument("--key", required=True, help="Gaode API Key")
    geo_parser.add_argument("--address", required=True, help="Address")
    geo_parser.add_argument("--city", help="City name")
    
    args = parser.parse_args()
    
    # Common parameter
    json_output = args.json
    
    if args.command == "ip":
        data = ip_location(args.key, args.ip)
        format_ip_results(data, json_output)
        
    elif args.command == "poi":
        if args.location:
            # Nearby search
            data = search_nearby(args.key, args.location, args.radius, args.keyword, args.page, args.offset)
        else:
            # Keyword search
            data = search_poi(args.key, args.keyword, args.city, args.location, args.radius, args.page, args.offset)
        format_poi_results(data, args.location, json_output)
        
    elif args.command == "geo":
        data = geocode(args.key, args.address, args.city)
        format_geocode_results(data, json_output)
        
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
