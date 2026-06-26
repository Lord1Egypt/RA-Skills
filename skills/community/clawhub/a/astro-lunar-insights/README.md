# 🌙 astro-lunar-insights

Lunar phase analysis and Moon influence on a person using **Swiss Ephemeris** (pyswisseph) + Pillow.

Calculates Moon phases, transit Moon aspects to natal Moon, transit Moon through natal houses, personal solar-lunar phase, lunar day number (tithi), Moon speed, illumination, perigee/apogee, and transit Moon aspects to all natal planets. Bilingual (RU/EN). Renders a 2-wheel chart (Moon phase wheel + natal wheel with transit Moon) with 3-group legend and text analysis panel.

## 🔬 Engine

- **Swiss Ephemeris** (pyswisseph 2.10.3.2) — JPL DE431 ephemerides, ~0.003° precision
- **Pillow 12.x** — chart rendering
- House cusps: **Placidus system**

## ⚠️ Requirements

| Requirement | Details |
|---|---|
| **OS** | Windows (x64) |
| **Python** | 3.14.x |
| **Runtime** | MSVC++ Redistributable 2015–2022 (x64) |
| **Pillow** | `pip install pillow` |

## Usage

```bash
# Text analysis
python scripts/lunar_analysis.py 24.04.1983 07:00 Ижевск --lang ru --name "Алексей"

# Graphical chart
python scripts/draw_lunar.py 24.04.1983 07:00 Ижевск --lang ru --name "Алексей"

# AI-enhanced chart (with AI conclusion)
python scripts/draw_lunar.py 24.04.1983 07:00 Ижевск --lang ru --name "Алексей" --conclusion conclusion.json
```

## CLI Arguments

| Argument | Description |
|---|---|
| `date` | Birth date DD.MM.YYYY |
| `time` | Birth time HH:MM |
| `city` | Birth city |
| `--target-date` | Analysis date (default: today) |
| `--lang` | `ru` or `en` |
| `--name` | Person's name |
| `--json` | JSON output |
| `--output` | Write JSON to file (UTF-8) |
| `--conclusion` | Path to AI conclusion JSON |

## Chart Layout (5760×2880 px)

```
+---------------------------+---------------------------+-------------------+
|  ФАЗА ЛУНЫ                |  НАТАЛЬНОЕ КОЛЕСО         |  TEXT ANALYSIS    |
|  Moon Phase Wheel         |  Natal Chart Wheel        |  PANEL            |
|  (1700px)                 |  (1700px)                 |  (2360px)         |
|                           |                           |                   |
|  - Phase circle           |  - Sign sectors (elements)|  - Moon phase     |
|  - Illumination % center  |  - House cusps (Placidus) |  - Nearest phases |
|  - Phase degree markers   |  - Natal planets          |  - Lunar day      |
|  - Current position       |  - Transit Moon (outer)   |  - Moon aspects   |
|    indicator              |  - ASC/MC lines           |  - Personal phase |
|                           |  - Colored aspect lines   |  - House          |
|                           |                           |  - Moon speed     |
|                           |                           |  - Conclusion     |
+---------------------------+---------------------------+-------------------+

Legend (3 uniform-height groups):
┌───────────────┬───────────────┬───────────────┐
│ ПЛАНЕТЫ       │ АСПЕКТЫ       │ СТИХИИ        │
│ PLANETS       │ ASPECTS       │ ELEMENTS      │
│ ♈ SU Sun     │ □ Conj        │ ■ Огонь       │
│ ♉ MO Moon    │ ✶ Sext       │ ■ Земля       │
│ ♊ ME Mercury │ □ Sqr        │ ■ Воздух      │
│ ...           │ △ Trine       │ ■ Вода        │
│               │ □ Qnc         │               │
│               │ ☍ Opp         │               │
└───────────────┴───────────────┴───────────────┘
```

## What It Calculates

1. **Current Moon Phase** — 8 phases with illumination %, distance, exact dates
2. **Transit Moon → Natal Moon** — Personal lunar cycle (~28 days)
3. **Personal Solar-Lunar Phase** — Personal lunar month (~29.5 days)
4. **Transit Moon Through Natal Houses** — Which life area is emotionally active
5. **Lunar Day (Tithi)** — 30 Vedic lunar days with specific energy
6. **Moon Speed** — Fast/slow emotional processing
7. **Transit Moon Aspects to All Natal Planets** — Complete psychological picture

## AI Conclusion Format

When using `--conclusion`, provide a JSON file with top-level metric keys:

```json
{
  "overall": "General summary for section 9...",
  "moon_phase": { "interpretation": "..." },
  "lunar_day": { "interpretation": "..." },
  "personal_phase": { "interpretation": ["Name", "Details..."] },
  "transit_moon_aspects": { "interpretation": "..." }
}
```

## Links

- **ClawHub**: https://clawhub.ai/dynamicsalex/astro-lunar-insights
- **Related**: [astro-natal-chart](https://github.com/dynamicsAlex/astro-natal-chart)

## License

This is an entertainment/educational tool. Do not make medical or financial decisions based on astrological readings.
