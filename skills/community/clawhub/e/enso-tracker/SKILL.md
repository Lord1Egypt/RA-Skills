---
name: enso-tracker
description: Track global city temperatures and analyze El Niño/La Niña (ENSO) phenomena with Imperial Modernity visualization
---

# ENSO Tracker

Track global city temperatures and analyze El Niño/La Niña (ENSO) phenomena. Generate publication-quality charts using the Imperial Modernity color palette.

## Overview

ENSO Tracker is an OpenClaw skill for:

- Tracking the hottest cities worldwide with real-time temperature data
- Showing current ENSO status (ONI index + phase classification)
- Analyzing correlation between ENSO cycles and extreme heat events
- Generating beautiful charts with the Imperial Modernity design system

Run `enso_tracker.py correlate` to generate an ENSO–India extreme heat correlation chart with gradient lines, danger zones, and key record annotations.

---

## Data Sources

| Source | Purpose | URL |
|--------|---------|-----|
| NOAA Climate Prediction Center | ONI index, ENSO phase classification | https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt |
| OpenWeatherMap API | Real-time global city weather | https://openweathermap.org/api |
| Berkeley Earth | Historical temperature anomaly data | http://berkeleyearth.org/data/ |

### NOAA ONI Index

The Oceanic Niño Index (ONI) is the standard monitoring metric for ENSO, published by NOAA CPC. Data is provided as 3-month running means, organized by meteorological season.

### OpenWeatherMap API

The free tier provides 1,000 calls per day — sufficient for tracking major cities worldwide. Supports current weather, forecasts, and historical data.

### Berkeley Earth

Provides global and regional temperature anomaly records for long-term trend analysis.

---

## API Key Setup

### OpenWeatherMap Configuration

1. **Sign up**: Visit https://openweathermap.org/api and click "Sign Up"
2. **Get your key**: After logging in, go to "API Keys" and copy your key
3. **Create config file**:

```bash
mkdir -p ~/.openclaw/workspace/skills/enso-tracker
cat > ~/.openclaw/workspace/skills/enso-tracker/config.json << 'EOF'
{
  "openweather_api_key": "YOUR_API_KEY_HERE"
}
EOF
```

4. **Replace** `YOUR_API_KEY_HERE` with your actual API key

> The config file is excluded from version control via `.gitignore`.

---

## Commands

### Track Hottest Cities

Fetch real-time temperatures and generate a ranking chart:

```bash
python enso_tracker.py cities --top 20 --output ~/Downloads/hottest_cities.png
```

Options:
- `--top N` — Show top N hottest cities (default: 10)
- `--output` — Output file path (default: `~/Downloads/city_ranking.png`)
- `--lang` — Chart language: `zh` or `en` (default: `zh`)
- `--rate-limit` — API request interval in seconds (default: 1.0)

### Show ENSO Status

Fetch current ONI index and phase classification:

```bash
python enso_tracker.py status
```

Sample output:
```
📊 Current ENSO Status
======================
ONI Index: +1.2°C
Phase: El Niño
Intensity: Moderate
Season: DJF 2023
```

### Correlate ENSO with Extreme Heat

Generate an overlay chart of ENSO cycles and extreme heat records:

```bash
python enso_tracker.py correlate --output ~/Downloads/enso_india_heat.png
```

Chart features:
- Dual Y-axis: ONI index (left) and temperature (right)
- El Niño phases highlighted in red
- La Niña phases highlighted in blue
- Extreme heat event annotations

### Generate Temperature Anomaly Chart

Plot regional or global temperature anomalies over time:

```bash
python enso_tracker.py anomaly --region "India" --output ~/Downloads/india_anomaly.png
```

Options:
- `--region` — Region name (e.g. "India", "Global", "Europe")
- `--start-year` — Start year (default: 1950)
- `--end-year` — End year (default: current year)

### Compare Years

Compare temperature data between two years:

```bash
python enso_tracker.py compare --year1 2023 --year2 2024 --output ~/Downloads/year_comparison.png
```

### ENSO Timeline

Generate a timeline chart of ONI values over a date range:

```bash
python enso_tracker.py timeline --start-year 2015 --output ~/Downloads/enso_timeline.png
```

---

## Color Palette

The Imperial Modernity color system draws from traditional Chinese court aesthetics, fused with modern data visualization principles.

### Core Colors

| Name | Hex | Usage |
|------|-----|-------|
| Heritage Red | `#930013` / `#BD1020` | Primary, El Niño phases, danger zones |
| Imperial Gold | `#D4AF37` | Highlights, annotations, key data points |
| Rice Paper | `#faf9f5` | Chart background |

### Gradient System

- **Temperature gradient line**: YlOrRd colormap, normalized to data range
- **ENSO phases**:
  - El Niño (ONI > +0.5): Red `#BD1020`
  - La Niña (ONI < −0.5): Blue `#2171B5`
  - Neutral: Gray `#6B7280`

### Chart Style

- Background: Rice Paper `#faf9f5`
- No top/right spines
- Grid lines: light gray, semi-transparent
- CJK font support: PingFang HK, Hiragino Sans GB, STHeiti, Arial Unicode MS
- Output resolution: 180 DPI

---

## Usage Examples

### Quick Query

```
User: What are the hottest cities in the world right now?
→ Run: enso_tracker.py cities --top 10
→ "Current global hottest city ranking has been generated..."
```

### ENSO Analysis

```
User: Is it El Niño or La Niña right now?
→ Run: enso_tracker.py status
→ "Currently in El Niño phase, ONI index at +1.2°C..."
```

### Deep Analysis

```
User: Analyze the relationship between ENSO and India heat waves
→ Run: enso_tracker.py correlate
→ "Data shows extreme heat events in India increase by 23% during El Niño years..."
```

---

## File Structure

```
enso-tracker/
├── SKILL.md              # This document
├── enso_tracker.py       # Main entry point with CLI
├── sources.py            # Data source adapters
├── viz.py                # Visualization module
└── config.json           # API key config (gitignored, user-created)
```

---

## Security

- All API keys stored in `config.json` — never hardcoded in source
- Config file excluded from version control via `.gitignore`
- All network calls use HTTPS
- **Berkeley Earth uses HTTP** (legacy academic server) — only read-only temperature data, no sensitive information transmitted
- No personal paths hardcoded — all paths use `~/` or relative paths
- Security audit script: `.security-check.sh`

---

## Dependencies

```bash
pip install pandas matplotlib numpy scipy
```

> Note: The code uses Python standard library `urllib` for HTTP requests — no need to install `requests`.

---

## License

This skill is part of the OpenClaw project. Data sourced from public APIs. For educational and research use.