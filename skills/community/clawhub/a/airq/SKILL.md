---
name: airq
description: Check air quality, AQI, PM2.5, PM10, pollution levels for any city from the terminal using airq CLI. Installs, configures, and runs air quality queries. Use when the user asks about air quality, pollution, AQI scores, or wants to monitor air in their city.
---

# airq — CLI Air Quality Checker

Check air quality for any city from the terminal. Merges model data (Open-Meteo) with real citizen science sensors (Sensor.Community). No API keys needed.

## Installation

First check if `airq` is already installed:

```bash
airq --version
```

If not installed, detect the user's platform:

### macOS (Homebrew)
```bash
brew tap fortunto2/tap && brew install airq
```

### Linux (prebuilt binary)
```bash
curl -LO https://github.com/fortunto2/airq/releases/latest/download/airq-linux-x86_64.tar.gz
tar xzf airq-linux-x86_64.tar.gz
sudo mv airq /usr/local/bin/
```

### Any platform (Rust/cargo)
```bash
cargo install airq
```

## Configuration (recommended)

If the user mostly checks the same city, set up a config — then just type `airq` without flags:

```bash
airq init --city <city-name>
```

This creates `~/.config/airq/config.toml`. Can also add a favorites list to check multiple cities at once:

```toml
default_city = "berlin"
cities = ["berlin", "tokyo", "istanbul", "new york"]
```

```bash
airq       # checks berlin (default)
airq --all # checks all 4 cities, ranked by pollution
```

## Commands

### Current air quality
```bash
airq                              # uses default city from config
airq --city tokyo                 # specific city
airq --lat 55.75 --lon 37.62     # by coordinates
```

Output shows PM2.5, PM10, CO, NO2, O3, SO2, UV index with color-coded AQI.

### History (sparkline trend)
```bash
airq history --city berlin --days 7
```
Shows daily AQI with sparkline bars for the past N days.

### Rank cities by pollution
```bash
airq top --country germany            # top 5 cities
airq top --country turkey --count 10  # top 10
```
Any country in the world — 10,000+ cities built-in. Use `--list` to see all countries.

### Compare data sources
```bash
airq compare --city berlin                     # model vs area sensors
airq compare --city berlin --sensor-id 72203   # model vs specific sensor
```
Side-by-side table showing Open-Meteo model vs Sensor.Community readings.

### Find nearby sensors
```bash
airq nearby --city paris --radius 10
```
Lists Sensor.Community sensor IDs within the given radius (km).

### Single data source
```bash
airq --city berlin --provider open-meteo           # model only
airq --city berlin --provider sensor-community --sensor-id 72203  # sensor only
```

### Pollution front detection
```bash
airq front --city hamburg --radius 150 --days 3
airq front --city gazipasa --radius 150 --days 3
```
Detects pollution fronts moving between cities using:
- Z-score spike detection on hourly PM2.5 differences
- Cross-correlation with time-lag between city/sensor pairs
- Haversine distance + bearing for speed and direction
- Dual-source: Open-Meteo model + Sensor.Community archive data
- Sensor clustering (~5km zones) with geo-named labels

Shows nearby cities, wind, spikes, fronts with speed/direction, and ETA warnings.

### Pollution source attribution (blame)
```bash
airq blame --city hamburg --radius 20 --days 7
```
Identifies which factories, power plants, or highways contribute to pollution using CPF (Conditional Probability Function). Sources auto-discovered from OpenStreetMap via Overpass API. Custom sources can be added in config `[[sources]]`.

### HTML/PDF report with map, heatmap, and source attribution
```bash
airq report --city hamburg --radius 150 --pdf
airq report --city delhi --radius 200 --days 3 --pdf
```
Generates self-contained HTML report with:
- Leaflet.js map with CartoDB tiles
- PM2.5 heatmap overlay (leaflet.heat)
- Individual sensors colored by air quality level
- Front arrows (green=strong, yellow=medium, orange=weak correlation)
- Pollution source markers on map (⚡ power plants, 🏭 factories, 🛣 highways)
- Source Attribution (CPF) table
- Key Insights, Spikes table, Fronts table, Methodology, AQI reference
- `--pdf` exports via Chrome headless or wkhtmltopdf

Data cached in `~/.cache/airq/` (sensor CSV + Overpass responses).

### JSON output
All commands support `--json` for scripting and piping:
```bash
airq --city tokyo --json
airq history --city berlin --days 7 --json
airq top --country usa --json
```

## AQI scale

| AQI     | Status                         | Action                        |
|---------|--------------------------------|-------------------------------|
| 0-50    | Good                           | No restrictions               |
| 51-100  | Moderate                       | Sensitive people limit outdoor |
| 101-150 | Unhealthy for Sensitive Groups | Reduce prolonged outdoor      |
| 151-200 | Unhealthy                      | Everyone limit outdoor        |
| 201-300 | Very Unhealthy                 | Avoid outdoor activity        |
| 301-500 | Hazardous                      | Stay indoors                  |

## How it works

By default airq fetches both sources concurrently and averages PM2.5/PM10:
- **Open-Meteo** — atmospheric model (~11km grid, global coverage)
- **Sensor.Community** — median of real sensors within 5km (filters outliers)

If no sensors are nearby, falls back to model only.
