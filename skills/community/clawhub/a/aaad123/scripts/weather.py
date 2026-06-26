#!/usr/bin/env python3
"""Current weather via wttr.in (no API key needed)."""

import argparse, json, sys, urllib.request, urllib.parse


def get_weather(city):
    """Fetch current weather from wttr.in."""
    encoded = urllib.parse.quote(city)
    url = f"https://wttr.in/{encoded}?format=j1"
    
    req = urllib.request.Request(url, headers={"User-Agent": "curl/7.68.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read())
    
    current = data.get("current_condition", [{}])[0]
    area = data.get("nearest_area", [{}])[0]
    
    # Extract data
    temp_c = int(current.get("temp_C", 0))
    feels_c = int(current.get("FeelsLikeC", 0))
    humidity = int(current.get("humidity", 0))
    wind_kmph = int(current.get("windspeedKmph", 0))
    wind_dir = current.get("winddir16Point", "")
    visibility = current.get("visibility", "N/A")
    uv_index = current.get("uvIndex", "N/A")
    pressure = current.get("pressure", "N/A")
    cloud_cover = current.get("cloudcover", "N/A")
    precip = current.get("precipMM", "0")
    desc = current.get("weatherDesc", [{}])[0].get("value", "N/A")
    
    city_name = area.get("areaName", [{}])[0].get("value", city)
    country = area.get("country", [{}])[0].get("value", "")
    region = area.get("region", [{}])[0].get("value", "")
    
    # Weather emoji
    emoji = _weather_emoji(desc, temp_c)
    
    return {
        "city": city_name,
        "country": country,
        "region": region,
        "description": desc,
        "emoji": emoji,
        "temperature": temp_c,
        "feels_like": feels_c,
        "humidity": humidity,
        "wind_speed": wind_kmph,
        "wind_direction": wind_dir,
        "visibility": visibility,
        "uv_index": uv_index,
        "pressure": pressure,
        "cloud_cover": cloud_cover,
        "precipitation": precip,
        "comfort": _comfort_level(temp_c, humidity, wind_kmph),
    }


def _weather_emoji(desc, temp):
    desc_l = desc.lower()
    if "sun" in desc_l or "clear" in desc_l: return "☀️"
    if "cloud" in desc_l and "part" in desc_l: return "⛅"
    if "cloud" in desc_l or "overcast" in desc_l: return "☁️"
    if "rain" in desc_l and "heavy" in desc_l: return "🌧️"
    if "rain" in desc_l or "drizzle" in desc_l: return "🌦️"
    if "snow" in desc_l: return "❄️"
    if "thunder" in desc_l: return "⛈️"
    if "fog" in desc_l or "mist" in desc_l: return "🌫️"
    if temp > 35: return "🥵"
    if temp < 0: return "🥶"
    return "🌤️"


def _comfort_level(temp, humidity, wind):
    """Calculate comfort level."""
    if 18 <= temp <= 26 and humidity < 70:
        return {"level": "舒适", "icon": "😊", "score": 5}
    elif 15 <= temp <= 30 and humidity < 80:
        return {"level": "较舒适", "icon": "🙂", "score": 4}
    elif 10 <= temp <= 35:
        return {"level": "一般", "icon": "😐", "score": 3}
    elif 0 <= temp <= 40:
        return {"level": "不舒适", "icon": "😣", "score": 2}
    else:
        return {"level": "极端", "icon": "⚠️", "score": 1}


def format_output(data):
    lines = [
        f"{data['emoji']} {data['city']}, {data['country']} — {data['description']}",
        "",
        f"🌡️ 温度：{data['temperature']}°C",
        f"🤗 体感：{data['feels_like']}°C",
        f"💧 湿度：{data['humidity']}%",
        f"💨 风速：{data['wind_speed']} km/h {data['wind_direction']}",
        f"👁️ 能见度：{data['visibility']} km",
        f"☀️ UV指数：{data['uv_index']}",
        f"🌡️ 气压：{data['pressure']} hPa",
        f"☁️ 云量：{data['cloud_cover']}%",
        f"🌧️ 降水：{data['precipitation']} mm",
        "",
        f"{data['comfort']['icon']} 舒适度：{data['comfort']['level']} ({data['comfort']['score']}/5)",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--city", required=True, help="City name")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    data = get_weather(a.city)
    print(json.dumps(data, indent=2, ensure_ascii=False) if a.json else format_output(data))
