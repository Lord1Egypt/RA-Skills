<div align="center">

# Air-chart

**One sentence. Your AI draws you a professional air-quality chart.**

English | [简体中文](README.zh.md) | [Español](README.es.md) | [हिन्दी](README.hi.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md)

![Claude Code](https://img.shields.io/badge/Claude%20Code-native-blue)
![Cursor](https://img.shields.io/badge/Cursor-native-blue)
![Codex CLI](https://img.shields.io/badge/Codex%20CLI-compatible-blue)
![ClawHub](https://img.shields.io/badge/ClawHub-publishable-green)
![skills.sh](https://img.shields.io/badge/skills.sh-installable-green)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

## What does this skill do?

Say one sentence in your AI chat — it **finds the station, fetches the data, and hands back a chart link** for you, powered by [x-cmd Draw](https://x-cmd.com/draw) — data and chart in one URL:

> 💬 "Show me Beijing's PM2.5 trend over the past week"
> 💬 "Compare Tokyo vs Seoul air quality for the last 7 days"
> 💬 "Delhi PM10 over 30 days, against the WHO guideline"
> 💬 "Hourly ozone in Singapore for the past 48 hours"
> 💬 "Which monitoring station in Beijing is worst right now?"

Behind the scenes, a fully automated pipeline: resolve the city → pick a **genuinely active** station from **OpenAQ** (reference-grade government monitoring data from 100+ countries) → clean outliers and gaps → render a professional chart.

**Why you'll want it:**

- **The chart is a URL — the URL is the data** — by default you get a `x-cmd.com/draw` link that both renders the chart and carries every value in it. Share it, drop it into Markdown as an image, or edit a number in the URL and the chart updates. Need a file? `--out chart.svg` (or `.png`) downloads it.
- **Rendering by x-cmd Draw** — your local pipeline stays pure `bash`/`jq`/`awk`/`curl`; the chart engine is [x-cmd Draw](https://x-cmd.com/draw), so you inherit a growing library of chart types (line, bar, area, pie, radar, gauge, sankey, Gantt, mind maps and more), light/dark themes, multi-language rendering, an online editor and zero renderer code to maintain. Nothing to install, nothing to keep up to date.
- **Trustworthy by design** — prefers government reference-grade stations; charts label physical concentration (µg/m³) and overlay the **WHO 24-hour guideline** as a reference series, so the limit travels with the data instead of being an afterthought. Not a vanity AQI number — data you can put in a report.
- **Global coverage, forgiving input** — built-in coordinates for 250+ cities; fuzzy names (`delhi`, `tOKyo`, `中山`) just work, and raw `lat,lon` is accepted too.
- **Real-world data, not a toy** — drops silent "zombie" stations and sensor-fault spikes; missing hours are dropped from the axis, never zero-filled.

## Showcase

Every chart below is a **real OpenAQ measurement** rendered live from its data-carrying URL — no image files are stored in this repo. Click any chart to open it in the x-cmd Draw editor and tweak the values.

| Multi-city PM2.5, last 7 days (Tokyo · Seoul · London) | New Delhi PM2.5 / PM10, last 14 days |
| --- | --- |
| ![Multi-city PM2.5 comparison][sc1] | ![New Delhi multi-parameter][sc3] |

| London ozone (O3), last 48 hours | New Delhi PM10 snapshot by station (live) |
| --- | --- |
| ![London O3 48h][sc2] | ![New Delhi station snapshot][sc4] |

| Dark theme: multi-city PM2.5 | New Delhi PM2.5, last 30 days |
| --- | --- |
| ![Dark multi-city][sc5] | ![New Delhi 30d][sc6] |

[sc1]: https://x-cmd.com/draw?type=line&title=PM2.5%20comparison%20%C2%B7%20last%207d%20%C2%B7%20multi-city%20%C2%B7%20same%20parameter&unit=%C2%B5g%2Fm%C2%B3&labels=11-06,11-07,11-08,11-09,11-10,11-11,11-12,11-13&series=Tokyo%20PM2.5:5.14,2.73,2.95,5,5.5,6.45,10.4,12.7&series=Seoul%20PM2.5:9.46,7.96,9.58,10.3,16.2,22.8,28.8,28.3&series=London%20PM2.5:37.3,58.3,82.4,49.4,23.9,15.8,10.8,13.7&series=WHO%2024h:15,15,15,15,15,15,15,15&w=960&h=500&t=opendata
[sc2]: https://x-cmd.com/draw?type=line&title=London%20O3%20trend%20%C2%B7%20last%2048h%20%C2%B7%20local%20time%20%28Europe%2FLondon%29&unit=%C2%B5g%2Fm%C2%B3&labels=11-11%2021%3A00,11-11%2022%3A00,11-12%2000%3A00,11-12%2001%3A00,11-12%2002%3A00,11-12%2003%3A00,11-12%2004%3A00,11-12%2005%3A00,11-12%2006%3A00,11-13%2000%3A00,11-13%2001%3A00,11-13%2002%3A00,11-13%2003%3A00,11-13%2004%3A00,11-13%2005%3A00,11-13%2006%3A00,11-13%2007%3A00&series=London%20O3:48.8,44.6,51.1,52.7,51.2,42.7,43.1,41,31.4,42.7,44.9,46.5,48.3,39.6,17.1,15.4,17&series=WHO%2024h:100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100&w=960&h=500&t=opendata
[sc3]: https://x-cmd.com/draw?type=line&title=New%20Delhi%20PM2.5%20%2F%20PM10%20trend%20%C2%B7%20last%2014d%20%C2%B7%20multi-parameter&unit=%C2%B5g%2Fm%C2%B3&labels=10-30,10-31,11-01,11-02,11-03,11-04,11-05,11-06,11-07,11-08,11-09,11-10,11-11,11-12,11-13&series=New%20Delhi%20PM2.5:44.7,110,205,217,241,265,305,306,339,302,222,163,147,232,172&series=New%20Delhi%20PM10:56.7,156,283,320,345,396,427,409,438,328,162,198,196,286,222&series=WHO%2024h:15,15,15,15,15,15,15,15,15,15,15,15,15,15,15&w=960&h=500&t=opendata
[sc4]: https://x-cmd.com/draw?type=hbar&title=New%20Delhi%20PM10%20snapshot%20by%20station%20%C2%B7%202026-11-14%2009%3A19%20IST%20%C2%B7%2025km%20radius&unit=%C2%B5g%2Fm%C2%B3&labels=Alipur,Anand%20Vihar,Ashok%20Vihar,Aya%20Nagar,Bawana,Burari%20Crossing&values=372.0,320.0,335.0,367.0,367.0,472.0&num=all&w=960&h=480&t=evil-glow
[sc5]: https://x-cmd.com/draw?type=line&title=PM2.5%20comparison%20%C2%B7%20last%207d%20%C2%B7%20multi-city%20%C2%B7%20same%20parameter&unit=%C2%B5g%2Fm%C2%B3&labels=11-06,11-07,11-08,11-09,11-10,11-11,11-12,11-13&series=Tokyo%20PM2.5:5.14,2.73,2.95,5,5.5,6.45,10.4,12.7&series=Seoul%20PM2.5:9.46,7.96,9.58,10.3,16.2,22.8,28.8,28.3&series=London%20PM2.5:37.3,58.3,82.4,49.4,23.9,15.8,10.8,13.7&series=WHO%2024h:15,15,15,15,15,15,15,15&w=960&h=500&scheme=dark&t=opendata
[sc6]: https://x-cmd.com/draw?type=line&title=New%20Delhi%20PM2.5%20trend%20%C2%B7%20last%2030d%20%C2%B7%20local%20time%20%28Asia%2FKolkata%29&unit=%C2%B5g%2Fm%C2%B3&labels=10-14,10-15,10-16,10-17,10-18,10-19,10-20,10-21,10-22,10-23,10-27,10-28,10-29,10-30,10-31,11-01,11-02,11-03,11-04,11-05,11-06,11-07,11-08,11-09,11-10,11-11,11-12,11-13&series=New%20Delhi%20PM2.5:104,73.6,65.7,94,127,94,125,142,136,142,138,131,95,44.7,110,205,217,241,265,305,306,339,302,222,163,147,232,172&series=WHO%2024h:15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15&w=960&h=500&t=opendata

## Features

- **Zero heavy dependencies** — pure `bash` / `jq` / `awk` / `curl`; the SVG renderer is written in awk.
- **Global coverage** — built-in coordinates for 200+ major cities worldwide, or pass `lat,lon` directly.
- **Smart station selection** — 25 km radius search → drop "zombie" stations silent for 24h (72h fallback) → prefer government reference-grade monitors.
- **Professional visuals** — physical concentration units (µg/m³) prominently labeled, WHO 24-hour guideline line overlaid by default (green when compliant, red when exceeded), light/dark themes.
- **Engineered for real use** — local cache (20 min for hourly / 2 h for daily data), exponential backoff on HTTP 429, gap-aware rendering (missing slots break the line — never filled with 0), UTC → station-local-time alignment.

## Quick start

### 1. Get an API key (free, ~1 minute)

1. Register or log in at [OpenAQ Explorer](https://explore.openaq.org/register) (existing account: [log in](https://explore.openaq.org/login)).
2. Open your [account page](https://explore.openaq.org/account) — your API key is shown near the bottom; copy it.
3. Configure it — pick one:

```bash
export OPENAQ_API_KEY="your_key"                             # ephemeral / CI
echo 'OPENAQ_API_KEY=your_key' > ~/.config/air-chart/config  # persistent
```

No system keychain required — a free, public-service credential stays in a plain
config file. Without a key, `--demo` mode still renders everything with sample data.

### 2. Run

```bash
# Single city, 7-day PM2.5 trend
./scripts/air_chart.sh --city Beijing --param pm25 --period 7d

# Multi-city comparison (up to 4 cities)
./scripts/air_chart.sh --city Tokyo --city Seoul --param pm25 --period 7d

# Multi-parameter single city (PM2.5 + PM10)
./scripts/air_chart.sh --city Beijing --param pm25 --param pm10 --period 30d

# 48-hour hourly curve (day/night pattern)
./scripts/air_chart.sh --city Singapore --param o3 --period 48h

# Multi-station real-time snapshot (bar chart)
./scripts/air_chart.sh --city Delhi --param pm10 --snapshot

# Dark theme, custom output
./scripts/air_chart.sh --city London --param no2 --period 14d --theme dark -o london.svg
```

### 3. Install as an AI agent skill

```bash
git clone https://github.com/qiakai/air-chart.git ~/.claude/skills/air-chart
# or: npx skills add qiakai/air-chart
```

Then just ask your agent: *"Compare PM2.5 in Tokyo and Seoul over the past 7 days."*

`SKILL.md` is written in English for the broadest agent/registry compatibility; a Chinese version is kept at `SKILL.zh.md`.

## CLI reference

| Flag | Description | Values |
| --- | --- | --- |
| `--city, -c` | City name (repeatable, ≤4) or coordinates `"lat,lon"` | `Beijing`, `New Delhi`, `39.9,116.4` |
| `--param, -p` | Pollutant (default `pm25`) | `pm25` `pm10` `o3` `no2` `so2` `co` |
| `--period, -t` | Time range (default `7d`) | `24h` `48h` (hourly) · `7d` `14d` `30d` (daily) |
| `--snapshot` | Multi-station real-time snapshot bar chart | flag |
| `--theme` | Color theme | `light` / `dark` |
| `--lang` | Output language (charts + messages) | `en` `zh` `es` `hi` `ja` `ko` `fr` (default: auto-detect from system locale) |
| `--out, -o` | Download chart as `.svg` or `.png` | default: print the x-cmd Draw URL only |
| `--demo` | Demo mode, no API key needed | flag |

## Architecture

```text
[city / pollutant / time range]
   │
   ▼
geo_resolve.sh      city name → coordinates + timezone (built-in gazetteer / raw lat,lon)
   │
   ▼
openaq_client.sh    OpenAQ API v3: auth, User-Agent, md5 cache,
                    429 exponential backoff, liveness filter (24h/72h),
                    sensor match by fixed parameter ID, reference-grade first
   │
   ▼
data_transform.awk  cleaning (negatives / physically impossible spikes),
                    gap detection (breaks, never zero-filled), stats, local-time labels
   │
   ▼
render_draw.sh      x-cmd Draw URL builder (URL-as-Data; optional .svg/.png download)
```

`data/parameters.tsv` is a static parameter dictionary aligned with the openaq-api
fixed pollutant IDs: slug / param_id / name / unit / WHO 24h guideline / physical
cap / per-parameter color — no redundant `/parameters` round-trips. Visuals follow
openaq-explorer conventions: per-parameter palette (PM2.5 `#E65100`, PM10 `#6A1B9A`,
O3 `#0277BD`, NO2 `#00838F`), a colorblind-friendly multi-city palette, and a WHO
guideline line in safety green `#10B981` / alert red `#EF4444`. If a station reports
units that differ from the dictionary default (e.g. ppm), the Y-axis uses the actual
units and the WHO line is suppressed to avoid dimensional confusion.

## Exit codes

| Code | Meaning |
| --- | --- |
| 3 | No API key configured (prints setup guidance) |
| 4 | Network / API error / rate-limit retries exhausted |
| 5 | No active station or no valid data |
| 2 | City name unresolvable (prints close candidates) |

## License

MIT
