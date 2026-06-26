---
name: astro-daily-transits
version: 5.1.0
description: Daily astrological transit forecast over natal chart using Swiss Ephemeris (pyswisseph) + Pillow. Calculates transit positions, aspects to natal chart, house activations, and renders a 2-column chart (combined natal+transit wheel + wide forecast panel). Bilingual (RU/EN). Windows 10/11 compatible with bundled .pyd.dat binary. Accuracy ensured by Swiss Ephemeris (JPL DE431 ephemerides, ~0.003° precision). Requires: Python 3.14.x, Pillow 12.x, MSVC++ Redist 2015-2022. Related: astro-natal-chart skill for natal chart calculation.
metadata:
  openclaw:
    requires:
      bins:
        - python3
    emoji: "🌞"
    homepage: https://github.com/dynamicsAlex/astro-daily-transits
---

# Astrology — Daily Transit Forecast

## Engine: Swiss Ephemeris (pyswisseph 2.10.3.2) + Pillow (PIL)

This skill calculates **daily transits** over a natal chart and generates an astrological forecast for **any target date** specified by the user (past, present, or future). It renders a composite 2-column chart showing a combined natal+transit wheel and a wide textual forecast panel.

### 🔬 Precision

All planetary positions are computed using the **Swiss Ephemeris** library (pyswisseph 2.10.3.2), which is based on NASA's **JPL DE431 ephemerides**. This ensures planetary position accuracy of approximately **0.003°** — the same engine used by professional astrologers and astronomy software worldwide. House cusps are calculated using the **Placidus system** with exact iterative methods (`swe.houses_ex()`).

---

## ⚠️ Requirements

| Requirement | Details |
|---|---|
| **OS** | Windows (x64) |
| **Python** | **3.14.x** |
| **Runtime** | **Microsoft Visual C++ Redistributable 2015–2022 (x64)** |
| **Pillow** | **12.x** — `pip install pillow` |
| **Swiss Ephemeris** | Bundled as `swisseph.cp314-win_amd64.pyd.dat` |

---

## Architecture

```
daily_transits.py --json  →  JSON data (natal + transits + aspects + houses)  →  draw_daily.py  →  PNG image
         ↕
   daily_transits.py  →  text forecast output
```

`daily_transits.py` is the **sole calculation engine** powered by Swiss Ephemeris. `draw_daily.py` renders the chart by calling it via subprocess. This guarantees text and graphical output always match.

---

## How Daily Transits Work

### Step 1: Natal Chart → Fixed Foundation
The natal chart is the birth snapshot — positions of planets at the moment of birth. This never changes. Computed once from birth date, time, and location.

### Step 2: Transit Positions → Moving Planets on Target Date
Transit positions are where the planets are on the **user-specified target date** (default: today). The user can request a forecast for any date — yesterday, tomorrow, or years in advance.

### Step 3: Aspects Between Transits and Natal
When a transit planet forms an angle (aspect) with a natal planet, it activates that natal planet's energy. Aspect lines are drawn directly on the wheel:

| Aspect | Symbol | Meaning | Line Style |
|---|---|---|---|
| Conjunction | ☌ | Fusion of energies — powerful, direct impact | Solid |
| Opposition | ☍ | Tension, confrontation, awareness through contrast | Solid |
| Trine | △ | Harmony, flow, luck — energy works naturally | Solid |
| Square | □ | Challenge, friction — crisis that mobilizes | Solid |
| Sextile | ✶ | Opportunity — potential that needs action | Solid |
| Semisextile | ⚺ | Subtle influence, minor adjustments | Solid |
| Semisquare | ∠ | Irritation, minor tension | Solid |
| Quincunx | ⚹ | Adjustment needed, discomfort | Solid |
| Retrograde | ℞ | Transit planet moving backward | **Dashed** |

### Step 4: House Activation (Detailed)
Transit planets falling in specific natal houses show **which life areas** are activated. Each house is displayed with:
- House title and description
- Transit planets in the house (with sign, degrees, retrograde status)
- Interpretation of each transit planet in the context of that house
- Activation context if a natal planet also occupies the same house

| House | Life Area |
|---|---|
| I | Personality, appearance, self |
| II | Money, values, resources |
| III | Communication, siblings, learning |
| IV | Home, family, roots |
| V | Creativity, children, romance |
| VI | Health, work, routine |
| VII | Partnership, marriage |
| VIII | Transformation, shared resources |
| IX | Philosophy, travel, higher education |
| X | Career, reputation, public life |
| XI | Friends, groups, hopes |
| XII | Subconscious, solitude, karma |

### Step 5: AI-Generated Extended Conclusion
An extended forecast summary is generated, including:
- Overall energy assessment (powerful/harmonious/challenging/calm)
- Transit planet context (sign position, meaning)
- Most activated house analysis
- Practical recommendations for the day

When run through OpenClaw, the AI agent can provide an enhanced conclusion via the `--conclusion` flag.

---

## Usage

### Text Forecast (CLI)

```bash
# Forecast for today
python scripts/daily_transits.py 24.04.1983 07:00 Ижевск --lang ru --name "Алексей"

# Forecast for any specific date (past, present, or future)
python scripts/daily_transits.py 24.04.1983 07:00 Ижевск --target-date 04.06.2026 --lang ru

# English output
python scripts/daily_transits.py 24.04.1983 07:00 Ижевск --lang en

# JSON output (for renderers / AI)
python scripts/daily_transits.py 24.04.1983 07:00 Ижевск --json --target-date 04.06.2026
```

### Graphical Chart

```bash
# Chart for today (Russian)
python scripts/draw_daily.py 24.04.1983 07:00 Ижевск --lang ru --name "Алексей"

# Chart for any specific date
python scripts/draw_daily.py 24.04.1983 07:00 Ижевск --target-date 04.06.2026 --lang ru --name "Алексей"

# With AI-generated conclusion from file
python scripts/draw_daily.py 24.04.1983 07:00 Ижевск --target-date 04.06.2026 --lang ru --name "Алексей" --conclusion conclusion.txt

# English
python scripts/draw_daily.py 24.04.1983 07:00 Ижевск --target-date 04.06.2026 --lang en --name "Alexey"
```

### CLI Arguments

| Argument | Description |
|---|---|
| `date` | Birth date DD.MM.YYYY |
| `time` | Birth time HH:MM |
| `city` | Birth city |
| `--target-date` | Forecast date DD.MM.YYYY (default: today). Can be **any date** — past, present, or future. |
| `--lang` | Language: `ru` or `en` (default: `ru`) |
| `--name` | Person's name for display |
| `--json` | Output JSON instead of text |
| `--conclusion` | Path to text file with AI-generated conclusion (for draw_daily.py) |

---

## JSON Output Format

```json
{
  "name": "Алексей",
  "birth_date": "24.04.1983",
  "birth_time": "07:00",
  "birth_city": "Ижевск, Россия",
  "target_date": "04.06.2026",
  "natal": {
    "Sun": {"lon": 33.38, "speed": 0.974, "retro": false},
    "Moon": {"lon": 172.92, "speed": 14.116, "retro": false},
    ...
  },
  "transits": {
    "Sun": {"lon": 103.5, "speed": 0.955, "retro": false},
    ...
  },
  "transit_houses": {"Sun": 12, "Moon": 9, ...},
  "planet_houses": {"Sun": 12, "Moon": 6, ...},
  "houses": [asc_deg, ..., mc_deg],
  "asc": 1.83,
  "mc": 22.92,
  "aspects": [
    {"transit": "Sun", "natal": "Venus", "type": "conjunction", "symbol": "☌", "name": "Соединение", "nature": "powerful", "orb": 1.3}
  ],
  "engine": "Swiss Ephemeris v20230604"
}
```

---

## Image Layout (5760×2880 px)

```
+------------------+---------------------------------------------+
|                  |                                             |
|   COMBINED       |          FORECAST PANEL                     |
|   WHEEL          |          (3600×2880)                        |
|   (2160×2160)    |                                             |
|                  |  - Date header + name                       |
|  - Sign sectors  |  - Key aspects (colored planet names)       |
|  - House cusps   |  - Aspect descriptions (word-wrapped)       |
|  - Natal planets |  - House activations (detailed, like natal  |
|    (pale, inner  |    chart skill):                            |
|    orbit RP=520) |    • House title + description              |
|  - Transit       |    • Transit planet (ME ♉ 12°30') in house  |
|    planets       |    • Interpretation of transit in house      |
|    (bright, outer|    • Natal planet activation context        |
|    orbit RP=720) |  - AI Conclusion (extended forecast)        |
|  - Aspect lines  |                                             |
|    (solid=color, |                                             |
|    dashed=retro) |                                             |
|                  |                                             |
|  --- Legends --- |                                             |
|  Planet|Element  |                                             |
|  |Aspect|Retro   |                                             |
+------------------+---------------------------------------------+
```

---

## Font Handling

Two bundled fonts in `scripts/`:

| Font | Purpose | Extension |
|---|---|---|
| `seguisym.ttf.dat` | Zodiac symbols ♈♉♊... + aspect symbols ☌☍△□... | `.dat` (ClawHub-compatible) |
| `segoeuisl.ttf.dat` | Cyrillic, latin, digits | `.dat` (ClawHub-compatible) |

Both are auto-copied to `.ttf` at runtime for Pillow compatibility. Per-character font selection ensures zodiac and aspect symbols render correctly alongside Cyrillic/Latin text.

---

## Scripts Reference

| Script | Purpose | Dependencies |
|---|---|---|
| `scripts/daily_transits.py` | **Sole calculation engine.** Swiss Ephemeris planetary positions, house cusps (Placidus), aspect detection. Text forecast + JSON export. | swisseph, math, json |
| `scripts/draw_daily.py` | **Renderer.** Calls daily_transits.py --json, draws 5760×2880 chart with combined wheel + forecast panel. | subprocess, json, math, Pillow |
| `scripts/swisseph.cp314-win_amd64.pyd.dat` | Swiss Ephemeris binary (2 MB) — JPL DE431 ephemerides | MSVC++ Redist |
| `scripts/seguisym.ttf.dat` | Zodiac + aspect symbol font (2.4 MB) | — |
| `scripts/segoeuisl.ttf.dat` | Cyrillic/latin font (854 KB) | — |

---

## AI Conclusion Workflow (for OpenClaw agents)

```
Step 1: python scripts/daily_transits.py <date> <time> <city> --json --target-date <date>
Step 2: AI analyzes JSON and writes enhanced conclusion to a file
Step 3: python scripts/draw_daily.py <date> <time> <city> --lang ru --name "Name" --conclusion <file>
```

When `--conclusion` is provided, the AI-generated text is used verbatim. Otherwise, the script generates a built-in conclusion.

---

## Disclaimer

This is an entertainment/educational tool, not a scientific method. Do not make medical or financial decisions based on astrological readings.

---

## Changelog

### v5.1.0 (2026-06-24)
- **QR code now renders by default** — --frame defaults to bundled scripts/frame_small.png.dat. QR code is always embedded in the forecast panel after the ClawHub link.
- **RGBA transparency support** — QR code with transparent background renders correctly (no black box behind it)
- **.png.dat auto-copy** — runtime now copies .png.dat → .png alongside .ttf.dat and .pyd.dat
- **.gitignore** added to exclude runtime-generated .png files
- Updated SKILL.md documentation

### v5.0.0 (2026-06-04)

### v5.0.0 (2026-06-04)
- **Combined single wheel**: natal planets (pale, inner orbit) + transit planets (bright, outer orbit) on one wheel
- **Aspect lines on wheel**: solid lines by aspect type, dashed lines for retrograde transits
- **Wide forecast panel** (3600px): full word-wrapped text with colored planet names
- **House activations**: detailed format matching astro-natal-chart skill (title → description → planets → interpretation)
- **Transit planet interpretation**: each transit planet in house gets contextual meaning
- **Natal planet activation**: shows when transit activates a natal planet in the same house
- **AI conclusion**: extended forecast with practical recommendations
- **--conclusion flag**: supports AI-generated conclusion files from OpenClaw
- **Any target date**: forecast can be computed for any past, present, or future date
- **Precision**: Swiss Ephemeris JPL DE431 ephemerides, ~0.003° accuracy

### v1.0.0 (2026-06-04)
- Initial release
- Daily transit calculation with Swiss Ephemeris
- Aspect detection (8 types) with configurable orbs
- House activation analysis
- Bilingual text forecast (RU/EN)
- 3-column graphical chart (natal + transit + forecast)
- JSON export for AI integration
- Bundled fonts and swisseph as .dat files (ClawHub-compatible)
