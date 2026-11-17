#!/usr/bin/env python3
"""ClawWeather Pro — trading weather (unique feature: killzone-relevant).

PRIVACY: city/hub names are sent over the network to wttr.in (a third-party
service). They can reveal location interests or trading hubs. No API key
involved for the free path.
"""
import sys
import json
import urllib.request

HUBS = {
    "london": ("London", 51.5, -0.12),
    "newyork": ("New York", 40.7, -74.0),
    "tokyo": ("Tokyo", 35.7, 139.7),
    "sydney": ("Sydney", -33.9, 151.2),
    "frankfurt": ("Frankfurt", 50.1, 8.7),
}


def get_open_meteo(lat: float, lon: float) -> dict:
    url = (f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
           "&current_weather=true&daily=weathercode,temperature_2m_max,temperature_2m_min&timezone=auto")
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            return json.load(r)
    except Exception as e:
        return {"error": str(e)}


def trading_weather(hubs=None):
    hubs = hubs or ["london", "newyork"]
    out = ["🌦️ Trading-vejr (finans-hubber)", ""]
    for h in hubs:
        name, lat, lon = HUBS.get(h, (h, None, None))
        if lat is None:
            out.append(f"⚠️ Ukendt hub: {h} (mulige: {', '.join(HUBS)})")
            continue
        d = get_open_meteo(lat, lon)
        if "error" in d:
            out.append(f"  {name}: ⚠️ {d['error']}")
            continue
        cur = d.get("current_weather", {})
        codes = {0: "☀️ Klart", 1: "🌤️ Let skyet", 2: "⛅ Skyet", 3: "☁️ Overskyet",
                 45: "🌫️ Tåge", 51: "🌦️ Støvregn", 61: "🌧️ Regn", 71: "🌨️ Sne",
                 80: "🌧️ Byger", 95: "⛈️ Torden"}
        wc = cur.get("weathercode", 0)
        out.append(f"  {name}: {codes.get(wc, wc)} {cur.get('temperature', '?')}°C, vind {cur.get('windspeed', '?')} km/t")
    out.append("")
    out.append("💡 Tip: Ekstremt vejr i London/NY kan give øget volatilitet i åbnings-sessionerne.")
    return "\n".join(out)


if __name__ == "__main__":
    hubs = None
    if "--hubs" in sys.argv:
        hubs = sys.argv[sys.argv.index("--hubs") + 1].split(",")
    print(trading_weather(hubs))
