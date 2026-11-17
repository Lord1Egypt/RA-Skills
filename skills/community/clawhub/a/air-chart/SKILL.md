---
name: air-chart
description: Query global air-quality data (OpenAQ monitoring network) and render high-resolution trend charts via x-cmd Draw (URL-as-Data). Use when the user asks to "check/compare air quality in a city, PM2.5/PM10/ozone trends, or generate an air-quality chart". Supports single-city trends, multi-city comparison (up to 4 cities), multi-parameter charts, and multi-station snapshots; automatically prefers active government reference-grade stations, overlays WHO guideline lines, and aligns timestamps to station local time.
---

# air-chart — Air Quality Chart Generation Skill

## What it does

End-to-end pipeline from a natural-language query to a chart (rendered by x-cmd Draw, URL-as-Data):
city resolution → OpenAQ station selection → data cleaning → a `x-cmd.com/draw` URL that both renders the chart and carries the data. The local side stays pure `bash`/`jq`/`awk`/`curl` — no renderer to install or maintain; the URL is shareable, embeddable, and editable (change a value, the chart updates).
Zero heavy dependencies; no Python/Node required.

## When to use

Invoke this skill when the user asks things like:

- "Show me Beijing's PM2.5 over the past week"
- "Compare Tokyo and Seoul air quality for the last 7 days"
- "Delhi PM10 daily averages over 30 days vs the WHO limit"
- "Hourly ozone in Singapore for the past 48 hours"
- "Generate an air-quality chart"

## How to call

```bash
scripts/air_chart.sh --city <city> [--city <city2> ...] [--param <pollutant>] [--period <range>] [options]
```

### Options

| Option | Description | Values |
| --- | --- | --- |
| `--city, -c` | City name (built-in gazetteer of ~250 world cities, case-insensitive, Chinese names supported) or raw `"lat,lon"`. Repeatable, up to 4 | e.g. `Beijing`, `New Delhi`, `中山`, `39.9,116.4` |
| `--param, -p` | Pollutant, default `pm25`. Multiple allowed for a single city; only one for multi-city | `pm25` `pm10` `o3` `no2` `so2` `co` |
| `--period, -t` | Time range, default `7d`. `24h/48h` aggregate hourly; `7d/14d/30d` daily | `24h` `48h` `7d` `14d` `30d` |
| `--snapshot` | Snapshot mode: horizontal bar chart of current values across the city's active stations (top 6) | flag |
| `--theme` | Color theme | `light` (default) / `dark` |
| `--style` | x-cmd Draw palette | `opendata` (default), `evil`, `evil-glow`, `shadcn`, ... |
| `--lang` | Output language | `en` `zh` `es` `hi` `ja` `ko` `fr` (default: auto-detect from system locale) |
| `--out, -o` | Download chart as `.svg` or `.png` | default: print the x-cmd Draw URL only |
| `--demo` | Demo mode with built-in sample data; no API key needed | flag |

### Mode auto-selection

- 1 city × 1 parameter → single-city trend line chart
- Multiple cities × 1 parameter → multi-city comparison line chart (high-contrast palette)
- 1 city × multiple parameters → multi-parameter line chart
- `--snapshot` → multi-station horizontal bar chart

## Prerequisites

An OpenAQ API key (free, ~1 minute):

1. Register or log in: `https://explore.openaq.org/register` (existing account: `https://explore.openaq.org/login`)
2. Open your account page `https://explore.openaq.org/account` — your API key is shown near the bottom; copy it.
3. Configure it (either one):

- Ephemeral/CI: `export OPENAQ_API_KEY="..."`
- Persistent: `echo 'OPENAQ_API_KEY=...' > ~/.config/air-chart/config` (`~/.air-chart.env` also recognized)

Without a key the script exits with code 3 and prints this guidance — never an unhandled error. `--demo` mode needs no key.

## Output guide (for agents)

The script prints `[air-chart] Chart saved: <path>` plus a data summary (station name,
reference-grade flag, n/min/max/avg, units). The agent should:

1. Show the user the x-cmd Draw chart URL by default (embeddable as an image in Markdown); if --out was given, also give the local file path.
2. Present the summary as text, noting the units are **physical concentration** (e.g. µg/m³), not AQI.
3. Charts overlay the WHO 24-hour guideline by default (see `data/parameters.tsv`: PM2.5=15, PM10=45, O3=100, NO2=25, SO2=40 µg/m³, CO=4 mg/m³) — green when compliant, red when exceeded. If a station reports non-default units (e.g. ppm), the line is auto-suppressed to avoid dimensional confusion.

## Errors & degradation

| Case | Exit code | Behavior |
| --- | --- | --- |
| Missing API key | 3 | Prints registration link and setup commands |
| Network/API/auth failure, rate-limit retries exhausted | 4 | Clear message with HTTP status |
| City not in gazetteer | 2 | Prints close candidates; suggests passing coordinates |
| No active station / no valid data | 5 | Explains why; suggests another city/parameter/period |
| No active station within 24h | — | Automatically retries with a 72h window |

- In multi-city mode, if one city fails the rest still render; tell the user which city failed and why.
- Responses are cached (`~/.cache/air-chart/`, 20 min for hourly / 2 h for daily data), so repeat queries return in well under a second.

## Implementation notes (for maintainers)

- `scripts/geo_resolve.sh`: city → coordinates/timezone (`data/top_cities.tsv`), raw-coordinate fallback.
- `scripts/openaq_client.sh`: API v3 wrapper (X-API-Key auth, User-Agent, md5 cache, 429 exponential backoff, liveness filter, sensor match by fixed parameter ID, reference-grade first).
- `data/parameters.tsv`: static parameter dictionary (slug / fixed ID / name / unit / WHO 24h guideline / physical cap / per-parameter color) — no redundant `/parameters` round-trips.
- `scripts/data_transform.awk`: negative/extreme-spike filtering, gap detection (breaks the line, never zero-fills), min/max/avg stats.
- `scripts/render_draw.sh`: x-cmd Draw URL builder (URL-as-Data: type=line/hbar + labels + series; WHO guideline injected as a constant series; optional .svg/.png export).

## Visual spec (aligned with openaq-explorer)

- Per-parameter palette: PM2.5 `#E65100`, PM10 `#6A1B9A`, O3 `#0277BD`, NO2 `#00838F` (lighter variants in dark theme).
- Multi-city colorblind-friendly palette: `#2563EB` / `#DC2626` / `#059669` / `#D97706`.
- WHO guideline line: `dasharray="4,4"`, safety green `#10B981` when all data complies, alert red `#EF4444` otherwise; label includes value and unit (e.g. `WHO 24h: 15 µg/m³`).
