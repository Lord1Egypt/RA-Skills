#!/usr/bin/env python3
"""ClawWeather Pro — 7-day planning extraction (unique feature).

PRIVACY: the city name is sent over the network to wttr.in (a third-party
service). City names can reveal travel plans or location interests.
"""
import sys
import json
import urllib.parse
import urllib.request


def week_plan(city: str, days: int = 7) -> str:
    url = f"https://wttr.in/{urllib.parse.quote(city)}?format=j1"
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            d = json.load(r)
    except Exception as e:
        return f"FEJL: {e}"

    weather = d.get("weather", [])[:days]
    if not weather:
        return f"Ingen data for {city}"

    out = [f"🗓️ Ugeplan: {city} ({days} dage)", ""]
    rows = []
    for w in weather:
        date = w["date"]
        mx, mn = int(w["maxtempC"]), int(w["mintempC"])
        rain = sum(int(h.get("chanceofrain", 0)) for h in w["hourly"]) // len(w["hourly"])
        desc = w["hourly"][len(w["hourly"]) // 2]["weatherDesc"][0]["value"]
        rows.append((date, desc, mn, mx, rain))

    out.append("| Dato | Vejr | Min/Max | Regn-chance |")
    out.append("|---|---|---|---|")
    for date, desc, mn, mx, rain in rows:
        out.append(f"| {date} | {desc} | {mn}°/{mx}° | {rain}% |")

    # Anbefalinger
    if rows:
        driest = min(rows, key=lambda r: r[4])
        warmest = max(rows, key=lambda r: r[3])
        out.append("")
        out.append("## Anbefalinger")
        out.append(f"- 🌞 **Varmeste dag:** {warmest[0]} ({warmest[3]}°)")
        out.append(f"- ☀️ **Tørreste dag (bedst at rejse):** {driest[0]} ({driest[4]}% regn-chance)")
    return "\n".join(out)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("BRUG: python3 week_plan.py \"By\" [--days 7]")
    city = sys.argv[1]
    days = 7
    if "--days" in sys.argv:
        days = int(sys.argv[sys.argv.index("--days") + 1])
    print(week_plan(city, days))
