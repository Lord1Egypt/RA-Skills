---
name: bazi
description: Professional BaZi (八字) chart calculator and analysis tool. Calculate Four Pillars of Destiny from birth date, time, and location. Features precise solar term calculation (ephem astronomy), true solar time correction, hidden stems, ten gods, five elements analysis, major luck periods, and clash/combine/harm relationships. Use when user asks about BaZi, Chinese astrology, Four Pillars, birth chart, 八字排盘, 命理, 四柱, 排八字, or fortune telling based on Chinese metaphysics.
---

# 八字排盘 (BaZi Chart Calculator)

Professional Four Pillars of Destiny calculator with astronomical precision.

## Setup

```bash
cd <skill_dir>
python3 -m venv venv && source venv/bin/activate
pip install -r scripts/requirements.txt
```

Only dependency: `ephem` (astronomy library for solar term calculation).

## Usage

```bash
# Text output (default)
python scripts/bazi.py --date 1990-08-18 --time 06:00 --city 上海 --gender male

# JSON output
python scripts/bazi.py --date 1990-08-18 --time 06:00 --city 上海 --gender male --format json

# With coordinates instead of city
python scripts/bazi.py --date 1990-08-18 --time 06:00 --lat 31.23 --lon 121.47 --gender male

# Disable true solar time correction
python scripts/bazi.py --date 1990-08-18 --time 06:00 --city 上海 --gender male --no-solar-correction

# Include annual luck (流年) for specific year
python scripts/bazi.py --date 1990-08-18 --time 06:00 --city 上海 --gender male --year 2026
```

## What It Calculates

| Feature | Description |
|---------|-------------|
| Four Pillars | Year, Month, Day, Hour stems and branches |
| Solar Terms | Precise astronomical calculation for month pillar boundaries |
| True Solar Time | Longitude + equation of time correction (critical for western China) |
| Hidden Stems | 本气/中气/余气 for each branch |
| Ten Gods | All stem relationships relative to Day Master |
| Five Elements | Weighted distribution (hidden stems: 60%/30%/10%) + Day Master strength |
| Major Luck | Forward/reverse periods based on gender + year stem polarity |
| Relationships | 六合, 三合, 六冲, 三刑, 六害, 天干五合, 天干冲 |

## Built-in Cities

50+ Chinese cities with latitude/longitude. Pass `--city 城市名` directly.

## Agent Integration

When a user provides birth info in conversation, extract date/time/city/gender and run the CLI. Format the text output as a message. For deeper analysis questions, use JSON output and interpret the data.

## Module Structure

```
bazi/
├── scripts/bazi.py          # CLI entry point
├── lib/
│   ├── pillars.py           # Four pillar calculation
│   ├── solar_terms.py       # Solar term astronomy (ephem)
│   ├── true_solar_time.py   # True solar time correction
│   ├── hidden_stems.py      # Hidden stems table
│   ├── ten_gods.py          # Ten gods derivation
│   ├── five_elements.py     # Five elements analysis
│   ├── major_luck.py        # Major luck periods
│   ├── relationships.py     # Clash/combine/harm
│   ├── cities.py            # City coordinate lookup
│   └── constants.py         # Stems, branches, mappings
└── data/cities.json         # City database
```
