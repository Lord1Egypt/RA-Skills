---
name: astro-natal-chart
version: 4.3.7
description: Natal chart calculation, interpretation, and graphical visualization using Swiss Ephemeris (pyswisseph) + Pillow. 3-column layout: wheel + essential data (1/3) + interpretation panel (2/3). AI conclusion via --conclusion flag. Planets, zodiac signs, aspects, houses, wheel chart rendering with bilingual interpretation (RU/EN). Input: birth date, time, and location. Language --lang ru/en (default en), filename includes person name. Windows-compatible with bundled .pyd binary.
metadata:
  openclaw:
    requires:
      bins:
        - python3
    emoji: "✨"
    homepage: https://github.com/dynamicsAlex/astro-natal-chart
---

# Astrology — Natal Chart

## Engine: Swiss Ephemeris (pyswisseph 2.10.3.2) + Pillow (PIL)

This skill uses **pyswisseph 2.10.3.2** for astrological computation and **Pillow 12.x** for graphical chart rendering.

## ⚠️ Requirements

| Requirement | Details |
|---|---|
| **OS** | Windows (x64) — tested on Windows 10/11 |
| **Python** | **3.14.x** (bundled `.pyd` compiled for CPython 3.14) |
| **Runtime** | **Microsoft Visual C++ Redistributable 2015–2022 (x64)** — required for the bundled native extension |
| **Pillow** | **12.x** — `pip install pillow` (for graphical wheel chart rendering) |

Installation steps:
1. Install [Python 3.14](https://www.python.org/downloads/release/python-3145/)
2. Install [Microsoft Visual C++ Redistributable x64](https://aka.ms/vs/17/release/vc_redist.x64.exe) (`winget install Microsoft.VCRedist.2015+.x64`)
3. Install Pillow: `pip install pillow`

---

## Architecture

All astrological calculations flow through a single source of truth:

```
natal_chart_swe.py --json  →  JSON data  →  draw_wheel.py  →  PNG image
                                  ↕
                          natal_chart_swe.py  →  text output
```

`natal_chart_swe.py` is the **sole calculation engine**. `draw_wheel.py` only renders — it calls `natal_chart_swe.py --json` via subprocess and draws the wheel from that data. This guarantees text and graphical output always match.

---

## Text Output (Swiss Ephemeris)

### Usage

```bash
python scripts/natal_chart_swe.py <date DD.MM.YYYY> <time HH:MM> <city>
python scripts/natal_chart_swe.py 14.12.1991 18:30 Ижевск
```

### JSON Output (for renderers)

```bash
python scripts/natal_chart_swe.py <date> <time> <city> --json
python scripts/natal_chart_swe.py 14.12.1991 18:30 Ижевск --json
```

JSON structure:
```json
{
  "date": "14.12.1991", "time": "18:30", "city": "Ижевск",
  "city_full": "Ижевск, Россия",
  "lat": 56.8519, "lon": 53.2114, "tz": "Europe/Samara",
  "tz_offset": 4, "jd": 2448605.104167,
  "planets": {
    "Sun":     {"lon": 262.097, "speed": 1.017, "retro": false},
    "Moon":    {"lon": 354.459, "speed": 12.461, "retro": false},
    ...
  },
  "houses": [116.94, 130.43, ...],
  "asc": 116.94, "mc": 352.89,
  "planet_houses": {"Sun": 6, "Moon": 10, ...},
  "aspects": [
    {"p1": "Mercury", "p2": "Venus", "type": "semisextile", "orb": 0.5},
    ...
  ]
}
```

---

## Graphical Chart Rendering (Pillow)

The skill includes `scripts/draw_wheel.py` — a full-featured natal chart wheel renderer that produces a composite PNG image.

**Important:** `draw_wheel.py` does NOT perform its own astrological calculations. It calls `natal_chart_swe.py --json` and renders the returned data. This eliminates data discrepancies between text and graphical output.

### Usage

```bash
# English (default)
python scripts/draw_wheel.py

# Russian
python scripts/draw_wheel.py --lang ru

# Arbitrary birth data
python scripts/draw_wheel.py 24.04.1983 06:00 Ижевск --lang ru

# Explicit English
python scripts/draw_wheel.py --lang en
```

### Output

| File | Language |
|---|---|
| `natal_full.png` | English chart (5760×2880) |
| `natal_full_ru.png` | Russian chart (5760×2880) |

### Image Layout (5760×2880 px)

```n+------------------+---------------------------+------------------+
|                  |                           |                  |
|   NATAL WHEEL    |     ESSENTIAL DATA        |  ZODIAC CIRCLE   |
|   (2160×2160)    |     (1440×2880)           |  (2160×2160)     |
|                  |                           |                  |
|  - Sign sectors  |  - Date, time, place      |  - Sign sectors  |
|  - House cusps   |  - Coordinates, timezone  |  - Planet marks  |
|  - Planet marks  |  - ASC / MC positions     |  - ASC/DSC/MC    |
|  - Aspect lines  |                           |  - Same size as  |
|  - ASC/MC lines  |                           |    natal wheel   |
|                  |                           |                  |
|  --- Legends --- |                           |                  |
|  Planet|Element  |                           |                  |
|  |Aspect       |                           |                  |
+------------------+---------------------------+------------------+
```

### Image Layout (5760×2880 px)

```
+------------------+---------------------------------------------+
|                  |                                             |
|   NATAL WHEEL    |          INTERPRETATION PANEL               |
|   (2160×2160)    |            (3600×2880)                      |
|                  |                                             |
|  - "NATAL CHART" |  - Date, time, place, coordinates, tz       |
|    title + name  |  - ASC / MC positions                       |
|  - Sign sectors  |  - Sun/Moon/ASC sign interpretation         |
|  - House cusps   |  - Dominant element, stelliums, retrogrades |
|  - Planet marks  |  - All 12 houses with cusp positions,       |
|  - Aspect lines  |    house meanings, and planets in each      |
|  - ASC/MC lines  |                                             |
|                  |                                             |
|  --- Legends --- |                                             |
|  Planet|Element  |                                             |
|  |Aspect       |                                             |
|  | ClawHub link |                                             |
+------------------+---------------------------------------------+
```
```

### Font Handling

Two bundled fonts in `scripts/`:

| Font | Purpose | Glyphs |
|---|---|---|
| `seguisym.ttf` (2.4 MB) | Zodiac symbols | ♈♉♊♋♌♍♎♏♐♑♒♓ (U+2648–U+2653) + latin |
| `segoeuisl.ttf` (854 KB) | All other text | Cyrillic, latin, digits, punctuation |

The `rtext()` function selects fonts **per character**: zodiac symbols → `seguisym.ttf`, everything else → `segoeuisl.ttf`. This ensures correct rendering of mixed content like "♈ Овен AR".

**Why not a single font?** No standard Windows font contains both zodiac symbols AND cyrillic. `seguisym.ttf` has zodiac but no cyrillic. `segoeui.ttf` has cyrillic but no zodiac. Per-character selection is the solution.

### Pillow Dependencies

`draw_wheel.py` uses these Python modules:

| Module | Purpose | Install |
|---|---|---|
| `PIL` (Pillow) | Image creation, drawing (circle, ellipse, line, pieslice, text) | `pip install pillow` |
| `math` | Trigonometric calculations (cos, sin, radians) | Stdlib |
| `json` | Parse natal_chart_swe.py JSON output | Stdlib |
| `subprocess` | Call natal_chart_swe.py --json | Stdlib |
| `os`, `sys` | File path operations | Stdlib |
| `argparse` | CLI argument parsing (`--lang en/ru`) | Stdlib |

Note: `draw_wheel.py` does NOT import `swisseph` directly. It receives all planetary data from `natal_chart_swe.py --json`.

---

## Standard Text Output Format

```
🌟 NATAL CHART  [Swiss Ephemeris vX.XX]
📅 Date: [date]  ⏰ Time: [time]  📍 Place: [city]
🌍 Coordinates: [lat], [lon]  🕐 Timezone: [tz] (UTC+/-offset)
📊 JD: [julian_day]

⬆️ ASC — [sign] [degrees]′
🜨 MC — [sign] [degrees]′

PLANETS:
☀️ Sun — [sign] [degrees]′ [house] [℞] (speed °/day)
🌙 Moon — [sign] [degrees]′ [house]
...

HOUSES:
I house — [sign] [degrees]′
... (all 12 houses)

MAJOR ASPECTS:
☌ Conjunction: [planet]-[planet] (orb: X.X°)
...

INTERPRETATION:
[detailed interpretation]
```

## Aspect Orbs

| Aspect | Symbol | Orb |
|--------|--------|-----|
| Conjunction | ☌ | ±8° |
| Opposition | ☍ | ±8° |
| Square | □ | ±7° |
| Trine | △ | ±7° |
| Sextile | ✶ | ±5° |
| Semisextile | ⚺ | ±2° |
| Quincunx | ⚹ | ±2° |
| Semisquare | ∠ | ±2° |

## Zodiac Signs — Keywords

- ♈ Aries: initiative, energy, impulsiveness
- ♉ Taurus: stability, sensuality, stubbornness
- ♊ Gemini: sociability, intellect, curiosity
- ♋ Cancer: emotionality, nurturing, intuition
- ♌ Leo: creativity, leadership, pride
- ♍ Virgo: analytical, practical, perfectionist
- ♎ Libra: harmony, diplomacy, partnership
- ♏ Scorpio: depth, transformation, intensity
- ♐ Sagittarius: optimism, philosophy, freedom
- ♑ Capricorn: ambition, discipline, responsibility
- ♒ Aquarius: originality, independence, innovation
- ♓ Pisces: intuition, compassion, dreaminess

## Planets — Meanings

- **Sun** — ego, essence, vitality, father
- **Moon** — emotions, subconscious, mother, instincts
- **Mercury** — thinking, communication, learning
- **Venus** — love, beauty, values, finances
- **Mars** — energy, action, aggression, sexuality
- **Jupiter** — expansion, luck, wisdom, growth
- **Saturn** — limitations, discipline, karma, structure
- **Uranus** — change, rebellion, innovation, suddenness
- **Neptune** — illusion, spirituality, creativity, dissolution
- **Pluto** — transformation, power, death/rebirth

## Houses — Life Areas

1. **I (ASC)** — personality, appearance, self-presentation
2. **II** — money, values, resources
3. **III** — communication, siblings, learning
4. **IV (IC)** — home, family, roots
5. **V** — creativity, children, romance
6. **VI** — health, work, routine
7. **VII (DSC)** — partnership, marriage
8. **VIII** — transformation, shared resources, intimacy
9. **IX** — philosophy, travel, higher education
10. **X (MC)** — career, reputation, goals
11. **XI** — friends, hopes, groups
12. **XII** — solitude, subconscious, karma

## Interpretation Guidelines

When interpreting, consider:
1. **Sun** — core personality
2. **Moon** — emotional nature
3. **Ascendant** — mask, first impression
4. **MC** — career aspirations
5. **Stelliums** (3+ planets in one sign/house)
6. **Retrograde planets** — energy turned inward
7. **Major aspects** — personality dynamics
8. **Dominant elements** (fire, earth, air, water)

## Disclaimer

This is an entertainment/educational tool, not a scientific method. Do not make medical or financial predictions based on astrological readings.

---

## Scripts Reference

| Script | Purpose | Dependencies |
|---|---|---|
| `scripts/natal_chart_swe.py` | **Sole calculation engine.** Text natal chart with `--json` export | swisseph (bundled .pyd), math, os |
| `scripts/draw_wheel.py` | **Renderer only.** Calls `natal_chart_swe.py --json`, draws 5760×2880 chart PNG | subprocess, json, math, os, argparse, Pillow |
| `scripts/seguisym.ttf` | **Zodiac symbol font.** Bundled for correct ♈♉♊... rendering. ~2.4 MB. | — |
| `scripts/segoeuisl.ttf` | **Cyrillic/latin font.** Bundled for cyrillic, digits, latin text. ~854 KB. | — |
| `scripts/swisseph.cp314-win_amd64.pyd.dat` | Bundled Swiss Ephemeris binary (2 MB) | MSVC++ Redist |

### draw_wheel.py — Quick Reference

```bash
# Generate chart with interpretation (English, default Matvey's data)
python scripts/draw_wheel.py

# Generate for any person (Russian)
python scripts/draw_wheel.py 24.04.1983 06:00 Ижевск --lang ru --name "Алексей"

# Generate for any person (English)
python scripts/draw_wheel.py 25.10.1985 21:35 Можга --lang en

# Options:
#   --name "Person Name"  — name shown above the wheel
#   --lang ru|en          — language of interpretation (default: en)
#   --conclusion FILE     — path to text file with AI-generated conclusion
#   --frame FILE          — path to .png.dat image (QR code). Default: bundled frame_small.png.dat

# Output files:
#   natal_full.png     — English version
#   natal_full_ru.png  — Russian version

# AI Conclusion workflow (for OpenClaw agents):
#   Step 1: python scripts/natal_chart_swe.py <date> <time> <city> --json
#   Step 2: AI analyzes JSON and writes conclusion to a file
#   Step 3: python scripts/draw_wheel.py <date> <time> <city> --lang ru --name "Name" --conclusion <file>
```

### natal_chart_swe.py — Quick Reference

```bash
# Text chart
python scripts/natal_chart_swe.py 14.12.1991 18:30 Ижевск

# JSON export (used by draw_wheel.py)
python scripts/natal_chart_swe.py 14.12.1991 18:30 Ижевск --json
```

---

## Changelog

### v4.3.7 (2026-06-24)
- **QR code now renders by default** — --frame now defaults to bundled rame_small.png.dat instead of being optional
- Updated .gitignore to exclude runtime-generated .png files
- SKILL.md: updated --frame documentation

### v4.3.6 (2026-06-11)

### v4.3.6 (2026-06-11)
- **Fixed QR code transparency**: RGBA frame images now preserve alpha channel when pasted onto the chart (was converting to RGB, causing black background behind transparent QR codes)
- SKILL.md version bumped to 4.3.6

### v4.3.5 (2026-06-11)
- **Moved divider line above ClawHub link and QR code**: thin separator now appears before the ClawHub URL and QR code in the info panel
- **Added frame_small.png.dat**: bundled QR code image for embedding in chart output
- SKILL.md version bumped to 4.3.5

### v4.3.4 (2026-06-11)
- **Moved divider line above ClawHub link and QR code**: thin separator now appears before the ClawHub URL and QR code in the info panel
- **Added frame_small.png.dat**: bundled QR code image for embedding in chart output
- SKILL.md version bumped to 4.3.4

### v4.3.3 (2026-06-11)
- **Moved divider line above ClawHub link and QR code**: thin separator now appears before the ClawHub URL and QR code in the info panel, improving visual separation from the aspects block
- **Added frame_small.png.dat**: bundled QR code image for embedding in chart output
- SKILL.md version bumped to 4.3.3

### v4.3.2 (2026-06-02)
- **Moved aspects & configurations to Info panel**: detailed aspect list with descriptions (from interp panel) now appears in the middle Info panel, below planet/house tables
- **Added text labels to aspect legend**: wheel legend now shows Unicode symbol + text abbreviation (☌ Conj, □ Sqr, △ Trine, etc.)
- **Restored AI conclusion block**: "ЗАКЛЮЧЕНИЕ" / "CONCLUSION" block at bottom of Interpretation panel (was accidentally removed during refactoring)
- SKILL.md version bumped to 4.3.2

### v4.3.1 (2026-06-02)
- **Fixed aspect symbol rendering**: aspect symbols (☌, ☍, □, △, ✶, ⚹, ⚺, ∠) were rendering as rectangles because `segoeuisl.ttf` does not contain them — now all aspect symbols use `seguisym.ttf` via extended `is_z()` check
- **Legend aspect symbols**: replaced text abbreviations (cj/sx/sq/tr/qn/op) in the wheel legend with proper Unicode aspect symbols from `seguisym`
- SKILL.md version bumped to 4.3.1

### v4.3.0 (2026-06-02)
- **`--conclusion FILE` flag**: draw_wheel.py accepts a path to a text file with an AI-generated conclusion
  - Conclusion appears at the bottom of the Interpretation panel, after the houses section
  - Decorative gold separator lines frame the conclusion block
  - Title: «CONCLUSION» (EN) / «ЗАКЛЮЧЕНИЕ» (RU)
  - Multi-paragraph text is wrapped to panel width (2400px)
  - Works with any AI-generated summary — not rendered if flag is omitted
- **3-phase workflow for OpenClaw agent**: (1) `natal_chart_swe.py --json` → (2) AI generates conclusion → (3) `draw_wheel.py ... --conclusion file.txt`
- SKILL.md version bumped to 4.3.1

### v4.2.0 (2026-06-02)
- **3-column layout**: right panel split into Info (1/3 = 1200px) and Interpretation (2/3 = 2400px)
  - **Info panel (1/3)**: essential data (date, time, place, coordinates, timezone), ASC/MC, planet table with houses, house cusp table, compact aspect list
  - **Interpretation panel (2/3)**: Sun/Moon/ASC interpretation, dominant element, stelliums, retrograde planets, aspects with descriptions, houses with full planet meanings
- **Text wrapping fixed**: `wrap_text()` now uses per-panel width (1200px for Info, 2400px for Interp) — long descriptions properly wrap instead of being clipped
- **Renamed 'ТОЛКОВАНИЕ' → 'ИНТЕРПРЕТАЦИЯ'** in Russian mode (was already 'INTERPRETATION' in English)
- **Vertical dividers** between all three columns
- SKILL.md version bumped to 4.2.0

### v4.0.0 (2026-06-01)
- **Bilingual interpretation**: all interpretation text available in both Russian and English
  - Default language: English (`--lang en`)
  - Russian: `--lang ru`
  - Separate interpretation data module: `scripts/interp_data.py`
  - Includes `HOUSE_TEXTS_RU/EN`, `PLANET_MEANING_RU/EN`, `SIGN_KEYWORDS_RU/EN`, `ASPECT_MEANING_RU/EN`
- **Extended house descriptions**: each house now has a detailed 3-sentence description covering multiple life areas
- **Aspect interpretation block**: all aspects listed with orb values and brief interpretation
- **Filename includes person name**: output format is now `{Name}_full_natal_{lang}.png` (e.g. `Анна_full_natal_ru.png`, `Anna_full_natal_en.png`)
- **Fixed planet meaning context bug**: planet meanings now correctly reference the planet itself (not the Sun's sign)
- **Separated interpretation data**: `interp_data.py` contains all text constants, `draw_wheel.py` contains rendering logic
- SKILL.md updated with new CLI flags and output file naming

### v3.8.0 (2026-06-01)
- **Fixed element coloring bug**: `Pillow pieslice()` uses a different coordinate system than `cos/sin` — sectors were drawn at mirrored positions, causing wrong element colors (Fire showed as Earth's green, Air as Water's blue, etc.). Replaced `pieslice()` with `draw.polygon()` using explicit `aof(d) = radians(90-d)` coordinate math, which is consistent with planet/symbol positioning.
- **Sector boundaries aligned to zodiac signs**: sectors now start from the beginning of each sign (e.g. 270° for Capricorn), not from the ASC degree. This ensures clean 30° sign sectors regardless of ASC position.
- **Bundled fonts**: `seguisym.ttf` (2.4 MB, zodiac symbols) and `segoeuisl.ttf` (854 KB, cyrillic/latin) are both included in `scripts/` and published with the pack.
- SKILL.md changelog updated.

### v3.7.0 (2026-06-01)
- **Two equal-size wheels**: natal chart with houses (left) and zodiac planet circle (right) — both 2160×2160px
- **Panoramic layout**: 5760×2880 total (2:1), data panel (1440px) between the two wheels
- **Dual-font rendering**: `seguisym.ttf` for zodiac symbols (large, 44pt), `segoeuisl.ttf` for cyrillic/latin/digits — bundled in `scripts/`
- **Per-character font selection**: `rtext()` automatically picks the right font per character — no more tofu
- **Zodiac planet circle**: same planet orbit radius (RP=648) and planet size (r=18) as main wheel
- **Essential data panel**: date, time, place, coordinates, timezone, ASC/MC between the wheels
- **Roman numerals** for house cusps (I–XII)
- **ASC/DSC/MC lines** on zodiac circle
- **Planet, element, aspect legends** below the left wheel
- Bundled fonts: `seguisym.ttf` (zodiac) + `segoeuisl.ttf` (cyrillic/latin) in `scripts/`

### v3.4.0 (2026-06-01)
- **Fixed zodiac symbol rendering**: all font loading now uses a single TrueType font (Segoe UI) with guaranteed Unicode zodiac + Cyrillic support. Symbols like ♈♉♊ render correctly everywhere — wheel, legend, and interpretation text.
- **Unified font system**: replaced separate `get_symbol_font()`/`get_font()` with single cached `font()` function that scans fallback chain and verifies glyph coverage
- **Element legend added**: color-coded legend showing Fire/Earth/Air/Water with colored rectangles
- **Legends fully below wheel**: planet, element, and aspect legends placed at `cy + R_OUTER + 50`, guaranteed zero overlap with the circular chart

### v3.3.0 (2026-06-01)
- **4K resolution**: canvas is now 3840×2160 (was 2840×1800), all elements scaled proportionally
- **Legend moved below wheel**: planet legend, element legend, and aspect legend are now placed entirely below the circular chart area — zero overlap with the wheel
- **Zodiac symbols in all text**: interpretation text uses ♈♉♊... instead of TA/SG/AR/etc. abbreviations
- **Element color legend**: added visual legend showing Fire/Earth/Air/Water color coding used in sign sectors
- Layout: wheel area 2160×2160, text area 1680×2160, legends below wheel in left panel

### v3.2.0 (2026-06-01)
- **Zodiac symbols instead of text abbreviations**: wheel now shows ♈♉♊♋♌♍♎♏♐♑♒♓ instead of AR/TA/GE/etc.
- **2x resolution**: canvas is now 2840×1800 (was 1420×900), all fonts and elements scaled proportionally
- **Planet legend moved to bottom-left**: no longer overlaps the chart wheel; placed below info box
- **Full interpretation fits**: larger text panel (1040px) with bigger fonts ensures all 12 houses + aspects render without truncation
- Added get_symbol_font() helper: uses Segoe UI Symbol for reliable zodiac glyph rendering
- Version bumped: 3.1.0 → 3.2.0

### v3.1.0 (2026-06-01)
- **Unified calculation architecture**: `draw_wheel.py` removed all duplicate astrological calculation code
  - Now calls `natal_chart_swe.py --json` via subprocess for all planetary/house/aspect data
  - Guarantees text and graphical output always match (single source of truth)
- **Added `--json` flag to natal_chart_swe.py**: exports all calculated data (planets, houses, aspects, metadata) as parseable JSON
- **draw_wheel.py now accepts CLI arguments**: `draw_wheel.py [date] [time] [city] [--lang en/ru]`
  - Default: Matvey's chart (14.12.1991 18:30 Ижевск)
  - Custom: any date/time/city combination
- **Generated interpretation**: stelliums, key configurations, house-by-house now auto-detected from JSON data rather than hardcoded
- Updated SKILL.md: architecture diagram, JSON format docs, scripts reference
- Version bumped: 3.0.0 → 3.1.0

### v3.0.0 (2026-06-01)
- **Added graphical chart renderer** (`scripts/draw_wheel.py`) using Pillow (PIL)
  - Composite 3840×2160 PNG (4K): circular wheel (left) + house interpretation (right)
  - 12 sign sectors colored by element (fire/earth/air/water)
  - Planet markers with retrograde(℞) indication
  - House cusp lines with numbered divisions
  - ASC/MC highlighted lines
  - Aspect lines color-coded by type (conj/sqr/trine/sext/opp/quinc)
  - Info box with ASC/MC positions and aspect legend
  - Planet legend panel
  - Full house-by-house textual interpretation on the right panel
- **Localization support** (`--lang en` / `--lang ru`)
  - English (default) and Russian output
  - All labels, headers, and interpretation text localized
- **Added Pillow dependency** (installed via `pip install pillow`)
- **Pillow drawing API documented** in SKILL.md
- **Scripts reference table** added to SKILL.md
- Version bumped: 2.1.0 → 3.0.0
- Description updated to mention graphical visualization

### v2.1.0 (2026-05-28)
- **Fixed `.pyd.dat` loading on Windows** — `importlib.util.spec_from_file_location` does not recognize non-standard extensions; added auto-copy to temporary `.pyd` before loading
- **Added Microsoft Visual C++ Redistributable as explicit requirement** — bundled `.pyd` compiled with MSVC 14.44 requires `vcruntime140.dll` and friends
- **Requires Python 3.14.x** — binary extension compiled for CPython 3.14 ABI
- Added Requirements section to SKILL.md with installation instructions
- Updated metadata: version bumped to 2.1.0, description mentions Windows compatibility
- Tested on Windows 10 (10.0.19045, x64) with Python 3.14.5 and VC++ Redist 14.51.36231.0

### v2.0.0 (2026-05-28)
- **Switched to Swiss Ephemeris** (pyswisseph 2.10.3.2) as the primary calculation engine — replaces simplified analytical formulas
- Replaced hardcoded positions with `swe.calc_ut()` using NASA JPL DE431 ephemerides
- House calculation now uses `swe.houses_ex()` (exact iterative Placidus) instead of analytical approximations
- Added retrograde detection via `FLG_SPEED` flag (velocity sign)
- Bundled `swisseph.cp314-win_amd64.pyd` (2 MB) in `scripts/` — no system-wide pip installation required
- Version detection: `swe.__version__` returns int `20230604` — formatted as `vYY.MM.BLD` string
- Expanded city database to 50+ cities with coordinates and timezone data
- Added proper Julian Day conversion through `swe.julday()`
- Removed legacy scripts: `natal_chart.py`, `placidus_iterative.py`, `placidus_meeus.py` and all debug/fix scripts (11 files)
- SKILL.md rewritten in English with full documentation

### v1.x (earlier)
- Initial release using simplified analytical formulas
- Separate iterative and Meeus-based Placidus implementations
- Planet positions calculated with approximate algorithms (0.5–15° error range)
