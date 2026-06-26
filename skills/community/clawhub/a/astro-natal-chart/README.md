# ✨ Astro Natal Chart

An [OpenClaw](https://github.com/openclaw/openclaw) skill — natal chart calculation, interpretation, and graphical visualization using **Swiss Ephemeris** and **Pillow**.

Generates a full-featured 5760×2880 px PNG chart (3 columns): natal wheel + essential data + detailed interpretation. Supports Russian and English languages.

## Features

- **Precise calculation** via Swiss Ephemeris (pyswisseph 2.10.3.2) — NASA JPL DE431 ephemerides
- **10 planets**: Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto
- **12 houses** in Placidus system (exact iterative calculation)
- **8 aspect types**: conjunction, opposition, trine, square, sextile, quincunx, semisextile, semisquare
- **Retrograde detection** via planet velocity sign
- **Bilingual interpretation**: Russian (`--lang ru`) and English (`--lang en`)
- **3-column layout**: wheel (2160px) + data (1200px) + interpretation (2400px)
- **50+ cities** with coordinates and timezones in the built-in database

## Layout

```
+------------------+------------------+---------------------------+
|                  |                  |                           |
|    NATAL         |    ESSENTIAL     |    INTERPRETATION         |
|    WHEEL         |    DATA          |   (2400px = 2/3)          |
|   (2160px)       |   (1200px = 1/3) |                           |
|                  |                  |   - Sun/Moon/Ascendant    |
|  - Sign sectors  |   - Date, time,  |   - Dominant element      |
|  - House cusps   |     place        |   - Stelliums             |
|  - Planet marks  |   - Coordinates  |   - Retrograde planets    |
|  - Aspect lines  |   - ASC / MC     |   - Aspects with          |
|  - ASC / MC      |   - Planet table |     descriptions          |
|                  |   - House table  |   - 12 houses with        |
|  --- Legends --- |   - Aspects      |     meanings & planets    |
|  Planets|Elements|                  |                           |
|  Aspects         |                  |                           |
+------------------+------------------+---------------------------+
```

## Requirements

| Requirement | Details |
|---|---|
| **OS** | Windows (x64) — tested on Windows 10/11 |
| **Python** | **3.14.x** (bundled `.pyd` compiled for CPython 3.14) |
| **Runtime** | **Microsoft Visual C++ Redistributable 2015–2022 (x64)** |
| **Pillow** | **12.x** — `pip install pillow` |

Installation steps:
1. Install [Python 3.14](https://www.python.org/downloads/release/python-3145/)
2. Install [VC++ Redist x64](https://aka.ms/vs/17/release/vc_redist.x64.exe)
3. Install Pillow: `pip install pillow`

## Architecture

```
natal_chart_swe.py --json  →  JSON data  →  draw_wheel.py  →  PNG image
                                  ↕
                          natal_chart_swe.py  →  text output
```

`natal_chart_swe.py` is the **sole calculation engine**. `draw_wheel.py` only renders — it calls `natal_chart_swe.py --json` via subprocess and draws the wheel from that data. This guarantees text and graphical output always match.

## Installation

### Via ClawHub (recommended)

```bash
openclaw skills install "clawhub:astro-natal-chart"
```

### From repository

```bash
git clone https://github.com/dynamicsAlex/astro-natal-chart.git
cd astro-natal-chart
pip install pillow
```

## Usage

### Text calculation

```bash
# Basic usage
python scripts/natal_chart_swe.py <date DD.MM.YYYY> <time HH:MM> <city>
python scripts/natal_chart_swe.py 24.04.1983 06:00 Ижевск

# JSON export (for renderers)
python scripts/natal_chart_swe.py 24.04.1983 06:00 Ижевск --json
```

### Graphical chart (PNG 5760×2880)

```bash
# Default (English)
python scripts/draw_wheel.py

# Russian language
python scripts/draw_wheel.py --lang ru

# Custom birth data
python scripts/draw_wheel.py 24.04.1983 06:00 Ижевск --lang ru --name "Alexey"
python scripts/draw_wheel.py 25.10.1985 21:35 Можга --lang en --name "Natalya"
```

**Options:**
- `--name "Name"` — name displayed above the wheel
- `--lang ru|en` — interpretation language (default: `en`)
- `--conclusion FILE` — path to text file with AI-generated conclusion (optional)

**Output files:**
- `{Name}_full_natal_en.png` — English version
- `{Name}_full_natal_ru.png` — Russian version

### AI Conclusion workflow

The `--conclusion` flag enables a 3-phase workflow for AI-assisted chart analysis:

```bash
# Step 1: Get chart data as JSON
python scripts/natal_chart_swe.py 25.10.1985 21:35 Можга --json

# Step 2: AI analyzes JSON and writes conclusion to a file
# (agent writes analysis to /tmp/conclusion.txt)

# Step 3: Render chart with AI conclusion embedded
python scripts/draw_wheel.py 25.10.1985 21:35 Можга --lang ru --name "Natalya" --conclusion /tmp/conclusion.txt
```

The conclusion appears at the bottom of the Interpretation panel, after the houses section, framed by decorative gold separator lines. Title: «CONCLUSION» (EN) / «ЗАКЛЮЧЕНИЕ» (RU). Multi-paragraph text is auto-wrapped to panel width (2400px).

Without `--conclusion` the chart renders normally (no AI summary block).

### JSON structure

```json
{
  "date": "24.04.1983", "time": "06:00", "city": "Ижевск",
  "city_full": "Ижевск, Россия",
  "lat": 56.8519, "lon": 53.2114, "tz": "Europe/Samara",
  "tz_offset": 4, "jd": 2447273.75,
  "planets": {
    "Sun":     {"lon": 38.333, "speed": 0.985, "retro": false},
    "Moon":    {"lon": 143.317, "speed": 12.19, "retro": false}
  },
  "houses": [5.83, 37.47, 69.12, ...],
  "asc": 5.83, "mc": 341.25,
  "planet_houses": {"Sun": 12, "Moon": 6, ...},
  "aspects": [
    {"p1": "Mercury", "p2": "Venus", "type": "semisextile", "orb": 0.5}
  ]
}
```

## Text output format

```
🌟 NATAL CHART  [Swiss Ephemeris v20.23]
📅 Date: 24.04.1983  ⏰ Time: 06:00  📍 Place: Ижевск, Россия
🌍 56.8519°N, 53.2114°E  🕐 Europe/Samara (UTC+4)
📊 JD: 2447273.75

⬆️ ASC — Gemini 1°50′
🜨 MC  — Capricorn 24°45′

PLANETS:
☀️ Sun     — Taurus 3°20′  [12 house]  (+0.985°/d)
🌙 Moon    — Virgo 22°19′   [6 house]   (+12.19°/d)
...

HOUSES:
I house — Gemini 1°50′
...
XII house — Pisces 19°46′

MAJOR ASPECTS:
☌ Conjunction: Mercury-Venus (orb: 0.5°)
...

INTERPRETATION:
[detailed interpretation]
```

## Aspects and orbs

| Aspect | Symbol | Orb |
|---|---|---|
| Conjunction | ☌ | ±8° |
| Opposition | ☍ | ±8° |
| Square | □ | ±7° |
| Trine | △ | ±7° |
| Sextile | ✶ | ±5° |
| Semisextile | ⚺ | ±2° |
| Quincunx | ⚹ | ±2° |
| Semisquare | ∠ | ±2° |

## Font rendering

Two bundled fonts in `scripts/`:

| Font | Purpose | Glyphs |
|---|---|---|
| `seguisym.ttf` (2.4 MB) | Zodiac symbols + aspect symbols | ♈♉♊♋♌♍♎♏♐♑♒♓ (U+2648–U+2653) + ☌☍□△✶⚹⚺∠ |
| `segoeuisl.ttf` (854 KB) | All other text | Cyrillic, latin, digits |

The `rtext()` function selects fonts **per character**: zodiac and aspect symbols → `seguisym.ttf`, everything else → `segoeuisl.ttf`. No tofu, no missing glyphs.

## Scripts

| Script | Purpose | Dependencies |
|---|---|---|
| `scripts/natal_chart_swe.py` | **Sole calculation engine.** Text natal chart with `--json` export | swisseph (bundled .pyd), math, os |
| `scripts/draw_wheel.py` | **Renderer only.** Calls `natal_chart_swe.py --json`, draws 5760×2880 chart PNG. Supports `--conclusion FILE` for AI-generated summary | subprocess, json, math, os, argparse, Pillow |
| `scripts/interp_data.py` | Interpretation data (RU/EN): houses, planets, signs, aspects | — |
| `scripts/seguisym.ttf` | Zodiac symbol font (~2.4 MB) | — |
| `scripts/segoeuisl.ttf` | Cyrillic/latin font (~854 KB) | — |
| `scripts/swisseph.cp314-win_amd64.pyd.dat` | Bundled Swiss Ephemeris binary (2 MB) | MSVC++ Redist |

## Interpretation guidelines

1. **Sun** — core personality
2. **Moon** — emotional nature
3. **Ascendant** — mask, first impression
4. **MC** — career aspirations
5. **Stelliums** (3+ planets in one sign/house)
6. **Retrograde planets** — energy turned inward
7. **Major aspects** — personality dynamics
8. **Dominant elements** (fire, earth, air, water)

## Changelog

### v4.3.1 (2026-06-02)
- **Fixed aspect symbol rendering**: aspect symbols (☌, ☍, □, △, ✶, ⚹, ⚺, ∠) were rendering as rectangles because `segoeuisl.ttf` does not contain them — now all aspect symbols use `seguisym.ttf`
- **Legend aspect symbols**: replaced text abbreviations (cj/sx/sq/tr/qn/op) in the wheel legend with proper Unicode aspect symbols

### v4.3.0 (2026-06-02)
- **`--conclusion FILE` flag**: AI-generated conclusion can be embedded in the chart
- 3-phase workflow: JSON → AI analysis → rendered chart with conclusion
- Conclusion appears at the bottom of the Interpretation panel with gold separator lines

### v4.2.0 (2026-06-02)
- **3-column layout**: right panel split into Essential Data (1/3 = 1200px) and Interpretation (2/3 = 2400px)
- **Fixed text wrapping**: `wrap_text()` now uses per-panel width (1200px for Data, 2400px for Interp) — descriptions wrap properly instead of being clipped
- **Renamed «ТОЛКОВАНИЕ» → «ИНТЕРПРЕТАЦИЯ»** in Russian mode
- Vertical dividers between all three columns

### v4.0.0 (2026-06-01)
- **Bilingual interpretation**: Russian and English languages
- Extended house descriptions (3 sentences per house)
- Aspect interpretation block
- Person's name in output filename
- Fixed planet meaning context bug
- Separated interpretation data (`interp_data.py`) from rendering logic

### v3.x (2026-06-01)
- Fixed element coloring for sign sectors
- Two equal-size wheels, panoramic 5760×2880 layout
- Bundled fonts (zodiac + Cyrillic)
- Zodiac symbols instead of text abbreviations
- Legends below wheel — no overlap

### v2.x (2026-05-28)
- Switched to Swiss Ephemeris (pyswisseph 2.10.3.2)
- Placidus system (exact iterative)
- Retrograde detection via `FLG_SPEED`
- 50+ city database
- Windows compatibility with bundled `.pyd`

## Disclaimer

This is an entertainment/educational tool, not a scientific method. Do not make medical or financial decisions based on astrological readings.

## Author

- GitHub: [@dynamicsAlex](https://github.com/dynamicsAlex)
- ClawHub: [astro-natal-chart](https://clawhub.ai/dynamicsalex/astro-natal-chart)

## License

MIT
