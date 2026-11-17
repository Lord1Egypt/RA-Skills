#!/usr/bin/env python3
"""ClawWeather Pro — multi-city comparison (unique feature).

PRIVACY: each city name you pass is sent over the network to wttr.in
(a third-party service). City names can reveal location interests or
travel plans. No API key involved — free path only.
"""
import sys
import json
import urllib.parse
import urllib.request


def get_weather(city: str) -> dict:
    url = f"https://wttr.in/{urllib.parse.quote(city)}?format=j1"
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            return json.load(r)
    except Exception as e:
        return {"error": str(e)}


def compare(cities, days=3):
    out = [f"# Vejr-sammenligning: {', '.join(cities)}", ""]
    out.append(f"| By | Nu | {days}-dages max/min | Vind |")
    out.append("|---|---|---|---|")
    for city in cities:
        d = get_weather(city)
        if "error" in d:
            out.append(f"| {city} | ⚠️ {d['error']} | | |")
            continue
        cur = d.get("current_condition", [{}])[0]
        temp = cur.get("temp_C", "?")
        desc = cur.get("weatherDesc", [{}])[0].get("value", "?")
        wind = cur.get("windspeedKmph", "?")
        forecast = d.get("weather", [])
        if forecast:
            mx = max(int(x.get("maxtempC", 0)) for x in forecast[:days])
            mn = min(int(x.get("mintempC", 0)) for x in forecast[:days])
            out.append(f"| **{city}** | {desc} {temp}°C | {mn}°C / {mx}°C | {wind} km/t |")
        else:
            out.append(f"| **{city}** | {desc} {temp}°C | — | {wind} km/t |")
    return "\n".join(out)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    days = 3
    if "--days" in sys.argv:
        days = int(sys.argv[sys.argv.index("--days") + 1])
    if len(args) < 1:
        sys.exit("BRUG: python3 compare.py \"København\" \"Hargeisa\" [--days 3]")
    print(compare(args, days))
