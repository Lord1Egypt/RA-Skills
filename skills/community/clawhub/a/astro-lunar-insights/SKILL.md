---
name: astro-lunar-insights
version: 1.3.3
description: Lunar phase analysis and Moon influence on a person using Swiss Ephemeris (pyswisseph). Calculates Moon phases (exact dates), transit Moon aspects to natal Moon (personal lunar cycle), transit Moon through natal houses, personal solar-lunar phase (Moon -> Natal Sun), lunar day number (tithi), Moon speed, illumination, perigee/apogee, and transit Moon aspects to all natal planets. Bilingual (RU/EN). Renders a 2-wheel chart (Moon phase wheel + natal wheel with transit Moon) with 3-group legend, text panel, and QR code for donations. Windows 10/11 compatible. Accuracy ensured by Swiss Ephemeris (JPL DE431 ephemerides, ~0.003° precision). Requires: Python 3.14.x, Pillow 12.x, MSVC++ Redist 2015–2022. Related: astro-daily-transits skill for daily transit forecast, astro-natal-chart skill for natal chart calculation.
metadata:
  openclaw:
    requires:
      bins:
        - python3
    emoji: "🌙"
    homepage: https://github.com/dynamicsAlex/astro-lunar-insights
---

# Astrology — Lunar Phase & Influence Analysis

## Engine: Swiss Ephemeris (pyswisseph 2.10.3.2) + Pillow (PIL)

This skill calculates **lunar phases** and analyzes the **Moon's influence** on a person through multiple astrological lenses. It renders a chart with 2 wheels side-by-side (Moon phase + natal chart with transit Moon), 3-group horizontal legend below wheels, and a text analysis panel on the right.

The chart **always includes a QR code** (for donations) at the bottom of the text panel. By default the bundled rame_small.png.dat is used; users can override with --frame.

### 🔬 Precision

All planetary positions are computed using the **Swiss Ephemeris** library (pyswisseph 2.10.3.2), based on NASA's **JPL DE431 ephemerides**. Planetary position accuracy: ~0.003°. House cusps: **Placidus system** via `swe.houses_ex()`.

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
lunar_analysis.py --json  →  JSON data (all lunar metrics)  →  draw_lunar.py  →  PNG image
         ↕
   lunar_analysis.py  →  text analysis output
```

`lunar_analysis.py` is the **sole calculation engine**. `draw_lunar.py` renders the chart by calling it via subprocess.

---

## What This Skill Calculates

### 1. Current Moon Phase
The Moon's position relative to the Sun (elongation angle):
- **0°** = New Moon (🌑) — conjunction
- **90°** = First Quarter (🌓) — waxing
- **180°** = Full Moon (🌕) — opposition
- **270°** = Last Quarter (🌗) — waning
- Plus 4 intermediate phases (Crescent, Gibbous, etc.)

Also calculates: illumination %, distance from Earth (km), exact dates of nearest phases.

### 2. Transit Moon → Natal Moon (Personal Lunar Cycle)
The most important personal lunar metric. The transit Moon forms aspects to the natal Moon over a ~28-day cycle:

| Aspect | Timing | Meaning |
|---|---|---|
| **Conjunction** | Every ~28 days | Personal New Moon — emotional reset, new cycle begins |
| **Square** | ~7 & 21 days | Crisis point — need for action, tension |
| **Opposition** | ~14 days | Personal Full Moon — emotional climax, awareness |
| **Trine** | ~7 & 21 days | Harmony — intuition flows, good for planning |
| **Sextile** | ~4 & 24 days | Opportunity — gentle support |
| **Quincunx** | ~11 & 17 days | Adjustment — something needs realignment |
| **Semisquare** | ~3.5 & 10.5 days | Minor irritation |
| **Sesquiquadrate** | ~10.5 & 17.5 days | Restlessness — break patterns |
| **Semisextile** | ~2 & 16 days | Subtle influence |

### 3. Personal Solar-Lunar Phase (Transit Moon → Natal Sun)
The Moon's position relative to the natal Sun defines a **personal lunar month** (~29.5 days):

| Phase | Elongation | Meaning |
|---|---|---|
| **Personal New Moon** | 0° | Beginning of personal cycle. Inward energy. Start new projects. |
| **Personal Crescent** | 45° | Emerging. Energy builds. First steps. |
| **Personal First Quarter** | 90° | Action point. Challenges arise. Push through. |
| **Personal Gibbous** | 135° | Refinement. Fine-tune approach. |
| **Personal Full Moon** | 180° | CLIMAX. Maximum awareness. Emotional revelation. |
| **Personal Disseminating** | 225° | Sharing. Teach what you've learned. |
| **Personal Last Quarter** | 270° | Crisis of consciousness. Let go. |
| **Personal Balsamic** | 315° | Rest. Reflection. Prepare for next cycle. |

### 4. Transit Moon Through Natal Houses
Shows which life area is emotionally activated:

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

### 5. Lunar Day (Tithi) — Vedic System
30 lunar days from New Moon to New Moon, each with specific energy:
- **Day 1**: New beginning, planning
- **Day 14**: Peak energy — best for starting anything
- **Day 20**: Eagle day — see the big picture
- **Day 29**: Difficult day, caution
- **Day 30**: Blessing, gratitude, cycle completion

### 6. Moon Speed Analysis
Moon's daily motion affects emotional processing:
- **>14.5°/day**: Very fast — quick events, less depth
- **13.5–14.5°**: Fast — rapid emotional shifts
- **11.5–13.5°**: Normal — balanced processing
- **10–11.5°**: Slow — lingering feelings, deeper impact
- **<10°/day**: Very slow — prolonged emotional intensity

Also tracks approach to perigee (closer = stronger) or apogee (farther = weaker).

### 7. Transit Moon Aspects to All Natal Planets
Complete picture of how the transit Moon interacts with every natal planet — shows which psychological functions are emotionally activated.

---

## Usage

### Text Analysis (CLI)

```bash
# Analysis for today
python scripts/lunar_analysis.py 24.04.1983 07:00 Ижевск --lang ru --name "Алексей"

# Analysis for any specific date
python scripts/lunar_analysis.py 24.04.1983 07:00 Ижевск --target-date 05.06.2026 --lang ru

# English output
python scripts/lunar_analysis.py 24.04.1983 07:00 Ижевск --lang en

# JSON output (for renderers / AI)
python scripts/lunar_analysis.py 24.04.1983 07:00 Ижевск --target-date 05.06.2026 --json
```

### Graphical Chart

```bash
# Chart for today (Russian)
python scripts/draw_lunar.py 24.04.1983 07:00 Ижевск --lang ru --name "Алексей"

# Chart for any specific date
python scripts/draw_lunar.py 24.04.1983 07:00 Ижевск --target-date 05.06.2026 --lang ru --name "Алексей"

# English
python scripts/draw_lunar.py 24.04.1983 07:00 Ижевск --target-date 05.06.2026 --lang en --name "Alexey"
```

### CLI Arguments

| Argument | Description |
|---|---|
| `date` | Birth date DD.MM.YYYY |
| `time` | Birth time HH:MM |
| `city` | Birth city |
| `--target-date` | Target date in DD.MM.YYYY or YYYY-MM-DD format (default: today). Supports any past, present, or future date. **When omitted, uses current system date.** Supported in both `lunar_analysis.py` and `draw_lunar.py`. |
| `--lang` | Language: `ru` or `en` (default: `ru`) |
| `--name` | Person's name for display |
| `--json` | Output JSON instead of text |
| `--output` | Write JSON directly to file (UTF-8, bypasses console encoding) |
| `--conclusion` | Path to JSON file with AI-generated conclusion |

---

## JSON Output Format

```json
{
  "name": "Алексей",
  "birth_date": "24.04.1983",
  "birth_time": "07:00",
  "birth_city": "Ижевск, Россия",
  "target_date": "05.06.2026",
  "moon_phase": {
    "name": "Waning Gibbous",
    "elongation": 236.33,
    "illumination": 77.7,
    "distance_au": 0.002669,
    "distance_km": 399206
  },
  "nearest_phases": {
    "New Moon": {"date": "15.06.2026", "days_diff": 9.6},
    "Full Moon": {"date": "31.05.2026", "days_diff": -5.1}
  },
  "lunar_day": {"number": 20, "meaning_ru": "День орла..."},
  "transit_moon": {"lon": 311.18, "sign": "Capricorn", "speed": 12.14},
  "transit_moon_to_natal_moon": {"aspect": "Sesquiquadrate", "orb": 0.91},
  "personal_phase": {"key": "last_quarter", "name_ru": "Персональная последняя четверть"},
  "transit_moon_house": {"house": 7, "title_ru": "Партнёрство, брак..."},
  "moon_speed": {"speed": 12.14, "description_ru": "Нормальная..."},
  "transit_moon_aspects": [
    {"transit": "Moon", "natal": "Sun", "aspect": "Square", "major": true, "orb": 7.6}
  ],
  "engine": "Swiss Ephemeris v20230604"
}
```

---

## Image Layout (5760×2880 px)

```
+---------------------------+---------------------------+-------------------+
|                           |                           |                   |
|     ФАЗА ЛУНЫ             |     НАТАЛЬНОЕ КОЛЕСО      |   TEXT ANALYSIS   |
|     MOON PHASE WHEEL      |     NATAL CHART WHEEL     |   PANEL           |
|     (3400/2 = 1700 wide)  |     (1700 wide)           |   (2360×2880)     |
|                           |                           |                   |
|  - Phase circle           |  - Sign sectors (elements)|  - Moon phase     |
|  - Illumination % center  |  - House cusps (Placidus) |  - Nearest phases |
|  - Phase degree markers   |  - Natal planets (circles |  - Lunar day      |
|  - Current position       |    with letter codes)     |  - Moon aspects   |
|    indicator (yellow)     |  - Transit Moon (outer    |  - Personal phase |
|                           |    orbit, highlighted)    |  - House          |
|                           |  - ASC/MC lines           |  - Moon speed     |
|                           |  - Aspect lines (colored) |  - All aspects    |
|                           |                           |  - Conclusion     |
|                           |                           |                   |
+---------------------------+---------------------------+-------------------+

Legend (below wheels, 3 uniform-height groups side by side):
┌─────────────────┬─────────────────┬─────────────────┐
│  ПЛАНЕТЫ        │  АСПЕКТЫ        │  СТИХИИ         │
│  (PLANETS)      │  (ASPECTS)      │  (ELEMENTS)     │
│                 │                 │                 │
│  ♈ SU Sun      │  □ Conj          │  ■ Огонь        │
│  ♉ MO Moon     │  ✶ Sext          │  ■ Земля        │
│  ♊ ME Mercury  │  □ Sqr           │  ■ Воздух       │
│  ...            │  △ Trine         │  ■ Вода         │
│                 │  □ Qnc           │                 │
│                 │  ☍ Opp           │                 │
└─────────────────┴─────────────────┴─────────────────┘
```

- Wheels centered vertically in the image (cy=1440)
- Wheels radius: 640px each
- Legend: 3 groups of uniform height below wheels
- Left panel: 3400px (2 wheels × 1700px)
- Right panel: 2360px text interpretation

---

## Font Handling

Two bundled fonts in `scripts/`:

| Font | Purpose | Extension |
|---|---|---|
| `seguisym.ttf.dat` | Zodiac symbols ♈♉♊... + planet symbols ☉☽☿... | `.dat` (ClawHub-compatible) |
| `segoeuisl.ttf.dat` | Cyrillic, latin, digits | `.dat` (ClawHub-compatible) |

Both are auto-copied to `.ttf` at runtime for Pillow compatibility.

---

## Scripts Reference

| Script | Purpose | Dependencies |
|---|---|---|
| `scripts/lunar_analysis.py` | **Sole calculation engine.** All lunar metrics, text + JSON output. | swisseph, math, json |
| `scripts/draw_lunar.py` | **Renderer.** Calls lunar_analysis.py --json, draws 5760×2880 chart. | subprocess, json, math, Pillow |
| `scripts/swisseph.cp314-win_amd64.pyd.dat` | Swiss Ephemeris binary (2 MB) — JPL DE431 ephemerides | MSVC++ Redist |
| `scripts/seguisym.ttf.dat` | Zodiac + planet symbol font | — |
| `scripts/segoeuisl.ttf.dat` | Cyrillic/latin font | — |

---

## AI Conclusion Workflow (for OpenClaw agents)

```
Step 1: python scripts/lunar_analysis.py <date> <time> <city> --json --target-date <date>
Step 2: AI analyzes JSON and writes enhanced conclusion to a JSON file
        (see AI Conclusion JSON Format below)
Step 3: python scripts/draw_lunar.py <date> <time> <city> --lang ru --name "Name" --conclusion <file.json>
```

When `--conclusion` is provided, the AI-generated text is used verbatim in the chart.
Each metric gets its own interpretation section (1–8), and the overall summary
is shown in section 9 (Conclusion). Without `--conclusion`, the script generates
built-in autonomous interpretations.

### AI Conclusion JSON Format

The conclusion file must have metric keys at the **top level** (not nested under `metrics`).
Each metric contains an `interpretation` field (string, dict with `description`, or tuple).
The `overall` field contains the general summary for section 9.

```json
{
  "overall": "General summary text for section 9...",
  "moon_phase": {
    "interpretation": {
      "name": "Waning Gibbous",
      "description": "Full interpretation text for section 1..."
    }
  },
  "nearest_phases": {
    "interpretation": "Interpretation text for section 2..."
  },
  "lunar_day": {
    "interpretation": "Interpretation text for section 3..."
  },
  "transit_moon_to_natal_moon": {
    "interpretation": "Interpretation text for section 4..."
  },
  "personal_phase": {
    "interpretation": ["Phase Name", "Interpretation text for section 5..."]
  },
  "transit_moon_house": {
    "interpretation": "Interpretation text for section 6..."
  },
  "moon_speed": {
    "interpretation": "Interpretation text for section 7..."
  },
  "transit_moon_aspects": {
    "interpretation": "Interpretation text for section 8..."
  }
}
```

**Supported `interpretation` formats:**
- `dict` with `description` key — used by autonomous mode
- `tuple/list` of `[title, text]` — used by autonomous mode for personal_phase
- `string` — plain text interpretation (AI mode)

The renderer (`draw_text_panel`) automatically detects the format and extracts
the text accordingly. AI mode shows full text without truncation; autonomous mode
limits text to keep the chart compact.

## AI Workflow (for OpenClaw agents)

**⚠️ ПРАВИЛО: ВСЕГДА предоставляй расширенную интерпретацию ИИ, когда это возможно.**

Автономная интерпретация (встроенная в скрипт) — это fallback для CLI-использования. Когда скилл вызывается через OpenClaw агент, агент **обязан** проанализировать JSON и сгенерировать расширенную интерпретацию по всем метрикам. Это ключевое отличие качественного прогноза от шаблонного.

```
Step 1: python scripts/lunar_analysis.py <date> <time> <city> --json --target-date <date>
Step 2: AI analyzes JSON and provides extended interpretation for ALL metrics
Step 3: AI writes conclusion JSON file with overall summary
Step 4: python scripts/draw_lunar.py <date> <time> <city> --lang ru --name "Name" --conclusion <file.json>
```

**Без шага 3-4 карта будет содержать только автономную (краткую) интерпретацию.**

The AI should focus on:
- **Personal New/Full Moon** — most significant events
- **Transit Moon house** — which life area is emotionally active
- **Transit Moon → Natal Moon aspect** — emotional cycle phase
- **Moon speed** — depth vs. speed of emotional processing
- **Lunar day meaning** — Vedic tithi guidance
- **Transit Moon aspects to all natal planets** — detailed psychological analysis
- **Overall synthesis** — practical recommendations for the day

---

## Encoding & Console Handling

**Problem:** Windows console (cmd/PowerShell) redirects stdout in cp1251/cp866, breaking UTF-8 output even with `PYTHONIOENCODING=utf-8`.

**Solution:** `lunar_analysis.py` supports `--output file.json` which writes JSON directly to a file via `open(..., encoding='utf-8')`, completely bypassing the console. `draw_lunar.py` uses this internally — it passes `--output /tmp/lunar_analysis_tmp.json` to the subprocess and reads the file directly.

**For CLI users:** Use `--output` when redirecting to files:
```bash
python scripts/lunar_analysis.py 24.04.1983 07:00 Ижевск --lang ru --json --output result.json
```

For text output in terminal, set `PYTHONIOENCODING=utf-8` and `chcp 65001` (cmd) or use PowerShell with `$env:PYTHONIOENCODING='utf-8'`.

---

## Disclaimer

This is an entertainment/educational tool, not a scientific method. Do not make medical or financial decisions based on astrological readings.

---

## Changelog

### v1.3.3 (2026-06-24)
- **QR code is now always rendered by default** — --frame parameter now defaults to bundled rame_small.png.dat instead of being optional. Users no longer need to pass --frame explicitly.
- **Updated description** (frontmatter + intro) to mention QR code for donations as a feature
- **Updated CLI args table** — --frame now documented as having a bundled default

### v1.3.2 (2026-06-07)

### v1.0.1 (2026-06-05)
- **Encoding fix:** Added `--output file.json` flag to `lunar_analysis.py` — writes JSON directly to file in UTF-8, bypassing Windows console cp1251 encoding issues
- **draw_lunar.py** now uses `--output` internally via temp file for subprocess communication
- **Layout redesign:** 2 wheels side-by-side (horizontal), vertically centered (cy=1440)
- **Legend:** 3 uniform-height groups (planets, aspects, elements) arranged horizontally below wheels
- **Planet circles** with 2-letter codes (SU, MO, ME...) matching astro-natal-chart style
- **Colored aspect lines** on natal wheel (red=square, blue=trine, green=sextile, etc.)
- **Text panel** widened to 2360px with smaller fonts for better text fit
- **Output filename** now includes person name: `lunar_{name}_{date}_{lang}.png`
- **Target date** shown in text panel instead of "today"
- **Font/binary setup:** All `.ttf` and `.pyd` files shipped as `.dat` (ClawHub-compatible), auto-copied at runtime
- Removed `__pycache__` and generated `.ttf`/`.pyd` from skill directory
- Updated SKILL.md with encoding guide, new CLI args, and updated layout diagram

### v1.0.0 (2026-06-05)

### v1.2.0 (2026-06-07)
- **Cosmetic: aspect symbols in text panel** — Section 8 (Aspects) now renders graphical aspect symbols (△ □ ✶ ☌ ☍ ⚹ ⚺ ∠) from `seguisym.ttf` instead of text names (Trine, Square, etc.), matching the legend style
- **Symbol color coding**: aspect glyphs are rendered in their astrological colors (green △, red □, blue ✶, etc.) via `_get_word_color` + `ASP_SYMBOL_COLORS` map
- **`draw_lunar.py` now supports `--target-date` flag** — previously only `lunar_analysis.py` supported target dates via positional arg; now both scripts accept `--target-date`
- **Subprocess propagation**: `draw_lunar.py` passes `--target-date` through to `lunar_analysis.py` subprocess call
- **`lunar_analysis.py` `--target-date` as explicit flag** — previously only supported as 4th positional argument; now also parsed as `--target-date` flag for consistency
- **Dual date format support**: both `DD.MM.YYYY` and `YYYY-MM-DD` formats accepted for `--target-date`
- **AI Conclusion rule added**: SKILL.md now explicitly states that agents MUST always provide extended AI interpretation when possible; autonomous interpretation is a CLI fallback only
- **Updated AI workflow**: 4-step process (analyze → interpret → write conclusion → render chart) documented with explicit warning about missing conclusion = short output only

### v1.1.0 (2026-06-06)
- **Cosmetic overhaul of text panel:** Font sizes now match astro-natal-chart (FS=19, FM=22, FL=26, LH=22)
- **Text wrapping improved:** Line width reduced to half (`max_w = w // 2 - 20`) for 2x faster line breaks
- **Section headers raised:** Title labels above both wheels moved up (80px from wheel edge) for better visual balance
- **Colored planet names in text:** Planet names in interpretation text are now rendered in their astrological colors (e.g., Марс in red, Венера in green, Уран in cyan)
- **Colored aspect type names:** Aspect type names (Square, Trine, Sextile, Quincunx, etc.) in text are colored to match the legend
- **Section 9 (Conclusion) always visible:** Now displays for both AI mode (`overall` text) and autonomous mode (`summary.cycle_energy` + `summary.intensity`)
- **Fixed aspect list rendering:** Transit Moon aspects in section 8 now show readable text instead of raw dict representation
- **Fixed `interp_text()` robustness:** Now handles all conclusion data formats — string, list, dict with `description`, dict with `interpretation` key, tuple
- **Fixed nested function scope:** Replaced `nonlocal y` pattern with mutable list `_y = [y]` to avoid UnboundLocalError in nested drawing functions
- **Backup files preserved:** `draw_lunar.py.bak` and `draw_lunar.py.bak2` kept for rollback

### v1.0.2 (2026-06-06)
- **AI conclusion rendering restructured:** AI interpretations are now distributed across
  metric sections (1–8) instead of being piled into section 9 (Conclusion)
- **New AI conclusion JSON format:** Metric keys at top level (`moon_phase`, `lunar_day`, etc.),
  each with `interpretation` field; `overall` field for section 9 summary only
- **Helper functions `interp_text()` and `show_interp()`** in `draw_text_panel`:
  unified extraction of interpretation text from dict, tuple, or string formats
- **AI mode:** full text displayed without truncation in sections 1–8; section 9 shows only `overall`
- **Autonomous mode:** preserved with text limits for compact layout
- **Section 8 (Aspects):** added AI interpretation of transit Moon aspects after the aspect list
- **Conclusion JSON format documented** in SKILL.md with examples for all supported formats
- Updated SKILL.md with AI Conclusion JSON Format specification

### v1.0.1 (2026-06-05)
- Initial release
- Moon phase calculation (8 phases) with Swiss Ephemeris
- Exact phase date prediction (New Moon, First Quarter, Full Moon, Last Quarter)
- Transit Moon → Natal Moon aspects (personal lunar cycle)
- Personal solar-lunar phase (Moon → Natal Sun)
- Transit Moon through natal houses (Placidus)
- Lunar day (tithi) with 30-day Vedic meanings
- Moon speed analysis (fast/slow emotional processing)
- Illumination percentage and Earth distance
- Perigee/Apogee tracking
- Transit Moon aspects to all natal planets
- Bilingual text output (RU/EN)
- JSON export for AI integration
- 2-wheel side-by-side chart layout (5760×2880 px)
- Horizontal 3-group legend below wheels (planets, aspects, elements — uniform height)
- Text analysis panel with target date and person name
- Output filename includes person name and date: `lunar_{name}_{date}_{lang}.png`
- Bundled fonts and swisseph as .dat files (ClawHub-compatible, auto-copied at runtime)
- Vertical wheel centers at image middle (cy=1440), legend fits below
