#!/usr/bin/env python3
"""
tpf-generate.py - AI-powered trip generation for travel-page-framework.

Usage:
    tpf generate "杭州3天2晚，西湖+灵隐寺，住湖滨，预算2000"
    tpf generate --from-file prompt.txt --output trip-data.json
    tpf generate "长沙7天地铁全覆盖+湘潭株洲岳阳" --with-metro --with-images

Features:
    - Natural language to structured JSON
    - Auto-fetch metro data for supported cities
    - Auto-search Wikimedia images for attractions
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

# Framework paths
SCRIPT_DIR = Path(__file__).parent.resolve()
FRAMEWORK_DIR = SCRIPT_DIR.parent / "page-generator"
METRO_SCRIPT = FRAMEWORK_DIR.parent / "skills" / "china-travel-planner" / "scripts" / "fetch_subway_data.py"
IMAGE_SCRIPT = FRAMEWORK_DIR / "scripts" / "wikimedia_image_search.py"

def error(msg):
    print(f"[tpf-generate] ❌ {msg}", file=sys.stderr)
    sys.exit(1)

def info(msg):
    print(f"[tpf-generate] ℹ️  {msg}")

def success(msg):
    print(f"[tpf-generate] ✅ {msg}")

def parse_prompt(prompt):
    """Extract key info from natural language prompt."""
    info(f"Parsing: {prompt}")
    
    result = {
        "city": None,
        "days": None,
        "nights": None,
        "attractions": [],
        "hotel_area": None,
        "budget": None,
        "side_trips": []
    }
    
    # Extract city (first 2-4 Chinese chars or English city name)
    city_match = re.search(r'^([\u4e00-\u9fa5]{2,4}|[A-Za-z\s]+)', prompt)
    if city_match:
        result["city"] = city_match.group(1).strip()
    
    # Extract days/nights
    days_match = re.search(r'(\d+)\s*天', prompt)
    if days_match:
        result["days"] = int(days_match.group(1))
    
    nights_match = re.search(r'(\d+)\s*晚', prompt)
    if nights_match:
        result["nights"] = int(nights_match.group(1))
    
    # Extract budget
    budget_match = re.search(r'预算\s*(\d+)', prompt)
    if budget_match:
        result["budget"] = int(budget_match.group(1))
    
    # Extract attractions (between + signs or after commas)
    # Pattern: 西湖+灵隐寺 or 西湖、灵隐寺
    attractions_part = re.search(r'[，,]([^，,]+?)(?:[,，]|$)', prompt)
    if attractions_part:
        attr_text = attractions_part.group(1)
        # Split by + or 、
        attractions = re.split(r'[+/、]', attr_text)
        result["attractions"] = [a.strip() for a in attractions if a.strip()]
    
    # Extract hotel area
    hotel_match = re.search(r'住\s*([^，,]+)', prompt)
    if hotel_match:
        result["hotel_area"] = hotel_match.group(1).strip()
    
    # Extract side trips (周边城市)
    side_match = re.search(r'[+/]([^+/]+?)(?:[,，]|$)', prompt)
    if side_match and ('+' in prompt or '、' in prompt):
        # Check if looks like side trip (different city)
        pass  # Simplified for now
    
    return result

def fetch_metro_data(city):
    """Fetch metro data if city is supported."""
    if not METRO_SCRIPT.exists():
        return None
    
    info(f"Fetching metro data for {city}...")
    try:
        result = subprocess.run(
            ["python3", str(METRO_SCRIPT), city, "--pretty"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
    except Exception as e:
        info(f"Metro data fetch failed: {e}")
    return None

def search_images(query, limit=3):
    """Search Wikimedia Commons for images."""
    if not IMAGE_SCRIPT.exists():
        return None
    
    try:
        result = subprocess.run(
            ["python3", str(IMAGE_SCRIPT), query, "--limit", str(limit)],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            if isinstance(data, list) and len(data) > 0:
                return data[0].get("thumbUrl") or data[0].get("url")
    except Exception as e:
        info(f"Image search failed: {e}")
    return None

def generate_trip_data(parsed, options):
    """Generate complete trip-data.json structure."""
    
    city = parsed.get("city", "目的地")
    days = parsed.get("days", 3)
    nights = parsed.get("nights", days - 1) if parsed.get("nights") else days - 1
    
    # Generate dates (starting from next month 1st for example)
    from datetime import datetime, timedelta
    start_date = datetime.now().replace(day=1) + timedelta(days=32)
    start_date = start_date.replace(day=1)
    
    date_range = f"{start_date.strftime('%Y/%m/%d')} - {(start_date + timedelta(days=days-1)).strftime('%Y/%m/%d')}"
    
    # Build day-by-day itinerary
    days_data = []
    for i in range(days):
        day_date = start_date + timedelta(days=i)
        day_num = i + 1
        
        day_data = {
            "day": f"Day {day_num}",
            "date": day_date.strftime("%m/%d"),
            "theme": f"{city}探索日" if i < days - 1 else "返程日",
            "city": city,
            "hotel": f"{city}酒店" if i < days - 1 else None,
            "metroLines": [],
            "segments": {
                "morning": ["早餐后出发"],
                "afternoon": ["游览主要景点"],
                "evening": ["晚餐及休息"] if i < days - 1 else []
            },
            "note": "根据实际行程调整"
        }
        days_data.append(day_data)
    
    # Build attractions with auto-images if requested
    attractions_data = []
    for attr in parsed.get("attractions", []):
        image_url = None
        if options.get("with_images"):
            image_url = search_images(f"{attr} {city}", limit=1)
        
        attractions_data.append({
            "name": attr,
            "city": city,
            "type": "景点",
            "image": image_url or "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?auto=format&fit=crop&w=1200&q=80",
            "description": f"{city}著名景点",
            "bestFor": ["观光", "拍照"]
        })
    
    # Metro coverage
    metro_data = None
    if options.get("with_metro"):
        metro_data = fetch_metro_data(city)
    
    metro_lines = []
    if metro_data and "lines" in metro_data:
        for line in metro_data["lines"][:5]:  # Max 5 lines
            metro_lines.append({
                "name": line.get("name", "未知线路"),
                "day": f"Day {min(len(metro_lines)+1, days)}",
                "status": "planned"
            })
    
    # Build final structure
    trip_data = {
        "meta": {
            "title": f"{city} {days}天{nights}晚旅行计划",
            "subtitle": f"{date_range}｜探索{city}",
            "description": f"{city} {days}天行程规划，包含主要景点和交通安排。"
        },
        "hero": {
            "title": f"{city} {days}天{nights}晚旅行计划",
            "subtitle": f"探索{city}的精彩旅程",
            "dateRange": date_range,
            "tags": [city, f"{days}天{nights}晚"] + parsed.get("attractions", [])[:2],
            "summary": f"这是一份{city} {days}天的旅行计划，涵盖主要景点和实用建议。",
            "heroImage": ""
        },
        "stats": [
            {"label": "出发", "value": f"出发地 → {city}"},
            {"label": "返程", "value": f"Day {days} 下午"},
            {"label": "时长", "value": f"{days} 天"},
            {"label": "酒店", "value": parsed.get("hotel_area") or "待定"},
            {"label": "预算", "value": f"约 ¥{parsed.get('budget', '?')}/人" if parsed.get('budget') else "待定"}
        ],
        "hotels": [
            {
                "phase": "全程",
                "name": parsed.get("hotel_area") or f"{city}推荐酒店",
                "dateRange": date_range,
                "station": "市中心",
                "status": "推荐",
                "price": "待定",
                "distanceToMetro": "地铁方便",
                "image": "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=1200&q=80",
                "highlights": ["位置便利", "交通方便"]
            }
        ],
        "metroCoverage": {
            "goal": "覆盖主要地铁线路，方便出行",
            "lines": metro_lines if metro_lines else []
        },
        "days": days_data,
        "sideTrips": [],
        "attractions": attractions_data if attractions_data else [
            {
                "name": f"{city}主要景点",
                "city": city,
                "type": "城市地标",
                "image": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?auto=format&fit=crop&w=1200&q=80",
                "description": f"{city}代表性景点",
                "bestFor": ["观光", "初访"]
            }
        ],
        "tips": [
            f"提前预订{city}酒店，节假日价格会上涨。",
            "关注天气预报，准备合适的衣物。",
            "下载当地地铁APP，方便查询线路。"
        ]
    }
    
    return trip_data

def main():
    parser = argparse.ArgumentParser(
        prog="tpf-generate",
        description="Generate trip data from natural language"
    )
    parser.add_argument("prompt", nargs="?", help="Natural language description of the trip")
    parser.add_argument("--from-file", "-f", help="Read prompt from file")
    parser.add_argument("--output", "-o", default="trip-data.json", help="Output file")
    parser.add_argument("--with-metro", action="store_true", help="Auto-fetch metro data")
    parser.add_argument("--with-images", action="store_true", help="Auto-search images")
    parser.add_argument("--pretty", action="store_true", help="Pretty print JSON")
    
    args = parser.parse_args()
    
    # Get prompt
    if args.from_file:
        with open(args.from_file, "r", encoding="utf-8") as f:
            prompt = f.read().strip()
    elif args.prompt:
        prompt = args.prompt
    else:
        parser.print_help()
        sys.exit(1)
    
    # Parse and generate
    parsed = parse_prompt(prompt)
    info(f"Parsed: {json.dumps(parsed, ensure_ascii=False)}")
    
    options = {
        "with_metro": args.with_metro,
        "with_images": args.with_images
    }
    
    trip_data = generate_trip_data(parsed, options)
    
    # Output
    indent = 2 if args.pretty else None
    output = json.dumps(trip_data, ensure_ascii=False, indent=indent)
    
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(output + "\n")
    
    success(f"Generated: {args.output}")
    info(f"City: {trip_data['meta']['title']}")
    info(f"Days: {len(trip_data['days'])}")
    info(f"Attractions: {len(trip_data['attractions'])}")

if __name__ == "__main__":
    main()
