---
name: ClawWeather Pro
slug: clawweather-pro
version: 1.0.1
description: "Weather and forecasts via free services (wttr.in + Open-Meteo). Multi-city comparison and 7-day planning. Free tools send the city name to wttr.in (third party). Ingen API-nøgle."
metadata: {"clawbot": {"requires": {"bins": ["curl", "python3"]}, "permissions": {"network": ["https://wttr.in", "https://api.open-meteo.com"], "notes": "Free tools send the city name to wttr.in (third party). Ingen API-nøgle, ingen betalte kald."}}}
---

# ClawWeather Pro

Weather skill based on the free services (wttr.in + Open-Meteo), **enhanced with unique features**:

## 🆕 Unique features (not found in the original)

### Feature 1: Multi-city comparison
Compare the weather in several cities side by side — perfect for travel planning
(Hargeisa, Copenhagen, Dubai in one call):

```bash
python3 scripts/compare.py "Copenhagen" "Hargeisa" "Dubai" --days 3
```

### Feature 2: Trading weather (killzone-relevant)
Shows weather + sunrise/sunset to plan London/NY sessions — and whether there is
extreme weather that could affect markets (hurricanes, storms in financial hubs):

```bash
python3 scripts/trading_weather.py --hubs london,newyork
```

### Feature 3: 7-day planning extraction
Gives a clean, structured week plan: "Best day to travel", "Wettest day", "Coldest morning":

```bash
python3 scripts/week_plan.py "Copenhagen" --days 7
```

---

## Basics (inherited)

### wttr.in (primary)
```bash
curl -s "wttr.in/London?format=3"
# London: ⛅️ +8°C

curl -s "wttr.in/London?format=%l:+%c+%t+%h+%w"
curl -s "wttr.in/London?T"     # full forecast
```

Format codes: `%c` condition · `%t` temp · `%h` humidity · `%w` wind · `%l` location · `%m` moon

Tips:
- URL-encode spaces: `wttr.in/New+York`
- Airport codes: `wttr.in/JFK`
- Units: `?m` (metric) `?u` (USCS)
- Today only: `?1` · Now only: `?0`
- PNG: `curl -s "wttr.in/Berlin.png" -o /tmp/weather.png`

### Open-Meteo (fallback, JSON)
```bash
curl -s "https://api.open-meteo.com/v1/forecast?latitude=51.5&longitude=-0.12&current_weather=true"
```
Docs: https://open-meteo.com/en/docs

## 🔒 Privacy note
- The free tools send your **city name** to `wttr.in` (and optionally Open-Meteo) over the network — city names can reveal location interests/travel plans. No API key is involved for the free path.

Get live weather in the financial hubs (London, New York, Tokyo, Frankfurt) — extreme weather can move markets:

```bash

# 2) Trading weather (PAID call — costs per call)
```

- ⚠️ Paid call — each run charges your key. The free weather tools above remain free.

## Feedback
- Helpful? → `clawhub star clawweather-pro`
---
