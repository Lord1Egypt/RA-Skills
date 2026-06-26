---
name: astro-synastry
version: 1.1.0
description: Synastry (astrology compatibility) calculation and interpretation — relationship analysis based on two natal charts. Cross-aspects, house overlays, compatibility scores. Requires the astro-natal-chart skill.
metadata:
  openclaw:
    requires:
      bins:
        - python3
      skills:
        - astro-natal-chart
    emoji: "💫"
    homepage: https://github.com/openclaw/openclaw
---

# Astrology — Synastry (Compatibility)

## Dependencies

**This skill requires `astro-natal-chart`** — use it to calculate or load natal charts for both partners before running synastry analysis.

## Input Parameters

For synastry calculation, data for both partners is needed:
1. **Partner 1:** birth date, birth time, birth place
2. **Partner 2:** birth date, birth time, birth place

If natal chart data is already available in memory (USER.md, cached chart files) — use it directly.

## Calculation Algorithm

1. Calculate (or load from files) natal charts for both partners — use the `astro-natal-chart` skill (`scripts/natal_chart_swe.py`)
2. Calculate cross-aspects between Partner 1 and Partner 2 planets — `scripts/synastry.py`
3. Determine house overlays (Partner 1 planets in Partner 2 houses)
4. Generate interpretation by life areas

## Execution

```bash
# Step 1: Calculate natal charts (via astro-natal-chart skill)
python ../astro-natal-chart/scripts/natal_chart_swe.py DD.MM.YYYY HH:MM City1
python ../astro-natal-chart/scripts/natal_chart_swe.py DD.MM.YYYY HH:MM City2

# Step 2: Calculate synastry
python scripts/synastry.py --chart1 chart1.json --chart2 chart2.json
```

Or run the agent workflow: calculate both natal charts first, then feed them into synastry.py.

## Output Format

```
💕 SYNASTRY — Compatibility Report
👤 [Name 1]: [birth date], [birth place]
👤 [Name 2]: [birth date], [birth place]

═══════════════════════════════════════
📊 OVERALL COMPATIBILITY SCORE: [X]/100
═══════════════════════════════════════

🔥 PASSION & PHYSICAL ATTRACTION
   Score: [X]/10
   [Mars-Venus, Mars-Mars, Venus-Venus, Pluto aspects]

💞 EMOTIONAL COMPATIBILITY
   Score: [X]/10
   [Moon-Moon, Moon-Sun, Venus-Moon aspects]

🗣️ COMMUNICATION & INTELLECT
   Score: [X]/10
   [Mercury-Mercury, Mercury-Sun, Mercury-Moon aspects]

🎯 SHARED GOALS & VALUES
   Score: [X]/10
   [Jupiter-Jupiter, Sun-Sun, MC-MC aspects]

🏠 FAMILY & DOMESTIC LIFE
   Score: [X]/10
   [4th house, Moon, Venus aspects]

⚡ CONFLICT POINTS
   [description of tense aspects: squares, oppositions]

✨ STRENGTHS OF THE PAIR
   [description of harmonious aspects: trines, sextiles, conjunctions]

🔑 KEY SYNASTRY ASPECTS:
   [table of all cross-aspects]

📋 RECOMMENDATIONS:
   [practical advice for low-score areas]
```

## Synastry Aspect Orbs

For synastry, orbs are slightly tighter than in natal charts:

| Aspect | Symbol | Orb |
|--------|--------|-----|
| Conjunction | ☌ | ±7° |
| Opposition | ☍ | ±7° |
| Square | □ | ±6° |
| Trine | △ | ±6° |
| Sextile | ✶ | ±4° |
| Semisextile | ⚺ | ±1.5° |
| Quincunx | ⚹ | ±1.5° |
| Semisquare | ∠ | ±1.5° |

## Key Synastry Aspects

### Most important (high weight):
- **Sun — Sun** — core personality compatibility
- **Moon — Moon** — emotional compatibility
- **Sun — Moon** (cross) — deep connection, "recognition"
- **Venus — Mars** (cross) — sexual chemistry, attraction
- **ASC — ASC** — first impression of each other
- **Saturn — Sun/Moon** — stability/seriousness of the relationship

### Important (medium weight):
- **Venus — Venus** — love language
- **Mars — Mars** — energy and conflicts
- **Mercury — Mercury** — communication
- **Jupiter — Sun/Moon** — support and growth
- **Pluto — Sun/Moon** — transformative connection

### Additional:
- **Uranus — Venus** — unexpectedness in love
- **Neptune — Venus** — romance, idealization
- **MC — MC** — shared life directions

## House Overlays

When Partner 1 planets fall into Partner 2 houses:
- **I house** — Partner 1 amplifies Partner 2's personality
- **II house** — influence on finances and values
- **V house** — romance, children, creativity
- **VII house** — partnership, marriage (very important!)
- **VIII house** — transformation, intimacy, shared resources
- **X house** — influence on career and status

## Scoring

Compatibility score formula (0-100):
- Each **trine/sextile** between personal planets: +3-5 points
- Each **conjunction** between personal planets: +2-4 points
- Each **square**: -2-3 points
- Each **opposition**: -1-2 points (can be positive — complementarity)
- **Sun-Moon cross-aspect**: +5-8 points (powerful bond)
- **Venus-Mars cross-aspect**: +5-7 points (sexual chemistry)
- **Saturn harmonious** to Sun/Moon: +4-6 points (stability)
- **Pluto tense**: -3-5 points (control, manipulation risk)

## Interpretation Guidelines

- Synastry is a self-discovery tool, not a verdict
- Tense aspects don't mean "incompatibility" — they indicate growth zones
- Absence of aspects between planets is also informative — a "neutral" zone
- Never make categorical conclusions like "you are not right for each other"
- Always frame challenging aspects as opportunities for growth
- Consider the whole chart — a few hard aspects can be outweighed by many harmonious ones

## Disclaimer

This is an entertainment/educational tool, not a scientific method. Do not make life decisions solely based on astrological readings.

---

## Changelog

### v1.1.0 (2026-05-28)
- **Translated to English** — full SKILL.md rewrite from Russian to English
- **Added dependency** — declared `astro-natal-chart` as a required skill
- **Updated metadata** — version bumped to 1.1.0, description notes English language and dependency
- **Added disclaimer** — educational/entertainment use note
- **Expanded interpretation guidelines** — best practices for responsible readings
- **Added changelog section**

### v1.0.0 (earlier)
- Initial release in Russian
- Synastry calculation and interpretation workflow
- Aspect scoring system
- House overlay analysis
