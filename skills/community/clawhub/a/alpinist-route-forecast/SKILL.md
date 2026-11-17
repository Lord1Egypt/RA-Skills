---
name: "alpinist-route-forecast"
description: "Route-aware weather forecasts for alpine climbs. Terrain-adjusted timing, multi-day camp-to-summit itineraries, three-source verification, descent conditions, and pace calibration that learns your speed over time."
---

# Alpinist Route Forecast

Route-aware weather forecasts for alpine climbs — terrain-adjusted, camp-to-summit, multi-source verified.

## When to Use

- "What's the weather for Rainier DC on Saturday?"
- "I'm climbing Baker Coleman-Deming next Tuesday"
- "Forecast for Forbidden West Ridge this weekend"
- "Is Stuart Cascadian Couloir good this week?"
- "Here's my GPX for tomorrow's climb" *(user attaches file)*
- "I'm climbing something with 6,000 ft gain over 7 miles, summit coords 46.85, -121.76"
- "Which day is better — Saturday or Sunday?"
- "We started at 2 AM and summited at 7:30" *(post-trip calibration)*

## Requirements

- **Python 3** (standard library only — no pip installs)
- **Internet access** for weather APIs
- Script: `mountain_weather.py` (included in this skill)
- Peak database: `peak_routes.json` (included in this skill)
- Alpinist profile: `alpinist_profile.json` (auto-created on first calibration)

### Weather Sources (all free, no API keys)

| Source | Coverage | Range | Used for |
|--------|----------|-------|----------|
| Open-Meteo | Global | 16 days | Primary hourly forecast at each waypoint |
| NOAA/NWS | US only | 7 days | Summit verification (automatic) |
| Mountain-Forecast.com | Named peaks worldwide | 7 days | Optional named-peak verification |

## Privacy & Data Disclosure

- **Open-Meteo**: Route coordinates (lat/lng from GPX or peak database) are sent as query parameters. No account, no personal data beyond coordinates.
- **NOAA/NWS**: Summit coordinates are sent to api.weather.gov. A generic User-Agent header is included (required by NOAA). No personal data.
- **Mountain-Forecast.com**: A single HTTP request fetches the public forecast page for a named peak. No coordinates or personal data are sent.
- **Alpinist profile** (`scripts/data/alpinist_profile.json`): Stored locally only. Contains trip pace data (times and route names). Never transmitted externally.
- **Peak database**: Contains only publicly available geographic data (coordinates, elevations, route descriptions).

## Forecast Confidence

| Days Ahead | Confidence | Sources Available |
|-----------|-----------|-------------------|
| 1–3 days | 🟢 HIGH | Open-Meteo + NOAA + Mountain-Forecast |
| 4–7 days | 🟡 MODERATE | Open-Meteo + NOAA + Mountain-Forecast |
| 8–16 days | 🟠 LOW | Open-Meteo only |
| 17+ days | ❌ Unavailable | No reliable forecast data |

**Always tell the user the confidence level.** For LOW confidence forecasts, recommend checking again closer to the date.

## Input Modes

### 1. Named Route (no files needed)

```bash
python3 scripts/mountain_weather.py --route rainier-dc --date 2026-07-28
python3 scripts/mountain_weather.py --route baker-np --date 2026-08-01 --pace elite
python3 scripts/mountain_weather.py --list-routes
```

Available routes (32 peaks — PNW + California 14ers):

**Pacific Northwest (16):**
- `rainier-dc` — Disappointment Cleaver (2 days)
- `rainier-emmons` — Emmons Glacier (2 days)
- `baker-cd` — Coleman-Deming (2 days)
- `baker-np` — North Ridge (3 days)
- `shuksan-fisher` — Fisher Chimneys (2 days)
- `shuksan-sc` — Sulphide Glacier (2 days)
- `forbidden-wr` — West Ridge (2 days)
- `stuart-nc` — North Ridge (3 days)
- `stuart-cc` — Cascadian Couloir (2 days)
- `adams-south` — South Spur (2 days)
- `hood-south` — South Side/Pearly Gates (1 day)
- `glacier-peak-dc` — Sitkum Glacier (3 days)
- `eldorado` — Eldorado Glacier (2 days)
- `sahale` — Quien Sabe Glacier (2 days)
- `olympus-blue` — Blue Glacier (3 days)
- `st-helens-monitor` — Monitor Ridge (1 day)

**California 14ers (16):**
- `whitney-mt` — Mount Whitney Trail (1 day)
- `williamson-west` — West Side Route (2 days)
- `white-mountain` — Road/Trail (1 day)
- `north-palisade-unotch` — U-Notch Couloir (2 days)
- `starlight-peak` — Milk Bottle Route (2 days)
- `shasta-avalanche` — Avalanche Gulch (2 days)
- `sill-north` — North Couloir / L-Shaped (2 days)
- `mount-russell` — East Ridge (2 days)
- `polemonium-peak` — V-Notch Couloir (2 days)
- `split-mountain` — North Slope (1 day)
- `mount-langley` — New Army Pass (1 day)
- `mount-tyndall` — North Rib (2 days)
- `mount-muir` — South Face (1 day)
- `middle-palisade` — Southeast Slope (2 days)
- `thunderbolt-peak` — Southwest Chute (2 days)
- `winchell-east` — East Couloir (2 days)

### 2. GPX File

```bash
python3 scripts/mountain_weather.py --gpx route.gpx --date 2026-07-28
python3 scripts/mountain_weather.py --gpx route.gpx --date 2026-07-28 --peak "forbidden peak"
```

Works with any GPX file (Garmin, AllTrails, CalTopo, Gaia). The script:
- Detects the summit (highest elevation point)
- Uses ascent portion only (handles out-and-back routes)
- Auto-classifies terrain from slope angle

### 3. Simple Elevation Profile (no file, no route name)

```bash
python3 scripts/mountain_weather.py --trailhead-ft 5400 --summit-ft 14411 --distance-mi 9 \
  --summit-lat 46.8529 --summit-lng -121.7604 --date 2026-07-28
```

For when the user just knows trailhead/summit elevation, distance, and approximate summit coordinates.

## Pace Profiles

| Profile | Vertical Up | Vertical Down | Flat Hiking |
|---------|------------|---------------|-------------|
| `elite` | 1,475 ft/hr | 2,300 ft/hr | 3.4 mph |
| `moderate` | 1,000 ft/hr | 1,640 ft/hr | 2.5 mph |
| `amateur` | 650 ft/hr | 1,310 ft/hr | 1.9 mph |

Default: `moderate`. Use `--pace elite|moderate|amateur`.

### Terrain Adjustments

The script auto-classifies terrain from GPX slope or route database tags:

| Terrain | Slope | Pace Effect | Examples |
|---------|-------|-------------|----------|
| Trail/approach | < 30° | Full speed | Forest trail, meadow |
| Steep snow/scree/glacier | 30–45° | 75% speed | Glacier, snowfield, scree |
| Technical/scramble | > 45° | 45% speed | Exposed ridge, rock scramble, roped |

## Multi-Day Routes

Multi-day routes automatically:
1. Print the itinerary (approach days + summit day)
2. Shift the forecast to **summit day**
3. Forecast only the **camp → summit → camp** portion

The `--date` is the **start date** (Day 1 = approach). Summit day is calculated automatically.

Example: `--route rainier-dc --date 2026-07-28` with a 2-day route → forecasts summit day July 29 from Camp Muir.

## Post-Trip Calibration

After a climb, the user reports actual start and summit times:

```bash
python3 scripts/mountain_weather.py --gpx route.gpx --date 2026-07-28 \
  --actual-start 02:00 --actual-summit 07:30
```

This:
1. Compares actual time to predicted time
2. Calculates a personal pace factor (e.g., 1.1x = 10% faster than moderate)
3. Saves to `scripts/data/alpinist_profile.json`
4. Future forecasts automatically adjust timing

More trips → more accurate personal predictions.

## Output Includes

### Ascent
- Hourly conditions at each waypoint (temp °F, wind mph + gusts, cloud %, precipitation)
- Recommended start time (optimized for best summit weather window)
- Summit conditions + warnings (high wind, precipitation, low visibility)

### Descent
- Conditions at summit, midpoint, and camp during return
- Warnings for afternoon weather changes (thunderstorms, wind, whiteout)

### Verification
- NOAA/NWS hourly forecast at summit (automatic for US)
- Mountain-Forecast.com summit forecast (when `--peak` is specified or auto-detected from route)

## Key Options

| Flag | Description |
|------|-------------|
| `--route <id>` | Named route from database |
| `--gpx <file>` | GPX file path |
| `--trailhead-ft` / `--summit-ft` / `--distance-mi` | Simple mode |
| `--summit-lat` / `--summit-lng` | Summit coordinates (for simple mode or NOAA) |
| `--date YYYY-MM-DD` | Target date (start date for multi-day) |
| `--pace elite\|moderate\|amateur` | Pace profile |
| `--start-hour N` | Override start hour (0-23) |
| `--peak <name>` | Mountain-forecast.com verification |
| `--json` | JSON output |
| `--list-routes` | Show all named routes |
| `--actual-start HH:MM` | Post-trip calibration |
| `--actual-summit HH:MM` | Post-trip calibration |
| `--mf-verify <peak>` | Standalone mountain-forecast check |

## Agent Behavior

1. **Parse the user's intent**: route name, date, pace, whether they have a GPX
2. **Map natural language to flags**:
   - "Rainier DC" → `--route rainier-dc`
   - "Saturday" → calculate the date
   - "I'm slow" → `--pace amateur`
   - "start at 2 AM" → `--start-hour 2`
3. **Run the script** and present the formatted output
4. **Highlight key decisions**: Is the weather good enough? Should they wait a day? Mention the confidence level.
5. **For comparisons** ("Saturday or Sunday?"): run both dates and compare summit conditions
6. **Post-trip**: when user reports times, run calibration and confirm their pace factor

## Limitations

- Open-Meteo underestimates summit winds by 30-50% and can be ±2-4°C on temperature. Always cross-reference with NOAA and Mountain-Forecast.
- Mountain-Forecast.com is scraped HTML — may break if they change their page layout.
- Route database only covers PNW peaks. Users can add their own GPX for any mountain worldwide.
- Terrain auto-detection from slope works best with dense GPX trackpoints. Sparse GPX (few points) may misclassify.
- NOAA is US-only. International climbs get Open-Meteo + Mountain-Forecast only.
