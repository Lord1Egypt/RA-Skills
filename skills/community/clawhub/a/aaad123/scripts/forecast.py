#!/usr/bin/env python3
"""Multi-day weather forecast via wttr.in."""

import argparse, json, sys, urllib.request, urllib.parse


def get_forecast(city, days=5):
    encoded = urllib.parse.quote(city)
    url = f"https://wttr.in/{encoded}?format=j1"
    
    req = urllib.request.Request(url, headers={"User-Agent": "curl/7.68.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read())
    
    area = data.get("nearest_area", [{}])[0]
    city_name = area.get("areaName", [{}])[0].get("value", city)
    country = area.get("country", [{}])[0].get("value", "")
    
    forecasts = []
    for day in data.get("weather", [])[:days]:
        date = day.get("date", "")
        max_c = int(day.get("maxtempC", 0))
        min_c = int(day.get("mintempC", 0))
        avg_c = (max_c + min_c) // 2
        sun_hours = day.get("sunHour", "N/A")
        uv = day.get("uvIndex", "N/A")
        
        # Hourly details - use noon for description
        hourly = day.get("hourly", [])
        noon = hourly[4] if len(hourly) > 4 else hourly[0] if hourly else {}
        desc = noon.get("weatherDesc", [{}])[0].get("value", "N/A")
        humidity = noon.get("humidity", "N/A")
        wind = noon.get("windspeedKmph", "N/A")
        feels = noon.get("FeelsLikeC", avg_c)
        precip = noon.get("precipMM", "0")
        chance_rain = noon.get("chanceofrain", "0")
        
        forecasts.append({
            "date": date,
            "description": desc,
            "max_temp": max_c,
            "min_temp": min_c,
            "avg_temp": avg_c,
            "feels_like": int(feels),
            "humidity": humidity,
            "wind": wind,
            "precipitation": precip,
            "chance_rain": chance_rain,
            "sun_hours": sun_hours,
            "uv_index": uv,
        })
    
    return {
        "city": city_name,
        "country": country,
        "days": len(forecasts),
        "forecasts": forecasts,
    }


def _day_emoji(desc, max_t):
    d = desc.lower()
    if "sun" in d or "clear" in d: return "☀️"
    if "cloud" in d and "part" in d: return "⛅"
    if "cloud" in d: return "☁️"
    if "rain" in d: return "🌧️"
    if "snow" in d: return "❄️"
    if "thunder" in d: return "⛈️"
    return "🌤️"


def format_output(data):
    lines = [f"📅 {data['city']}, {data['country']} — {data['days']}天预报", ""]
    
    for f in data["forecasts"]:
        emoji = _day_emoji(f["description"], f["max_temp"])
        lines.append(f"{emoji} {f['date']}  {f['description']}")
        lines.append(f"   🌡️ {f['min_temp']}°C ~ {f['max_temp']}°C  体感：{f['feels_like']}°C")
        lines.append(f"   💧 湿度：{f['humidity']}%  🌧️ 降雨概率：{f['chance_rain']}%  降水：{f['precipitation']}mm")
        lines.append(f"   💨 风速：{f['wind']} km/h  ☀️ UV：{f['uv_index']}  日照：{f['sun_hours']}h")
        lines.append("")
    
    return "\n".join(lines)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--city", required=True)
    p.add_argument("--days", type=int, default=5)
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    data = get_forecast(a.city, min(a.days, 7))
    print(json.dumps(data, indent=2, ensure_ascii=False) if a.json else format_output(data))
