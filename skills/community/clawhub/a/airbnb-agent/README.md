# Airbnb Agent Skill

OpenClaw agent skill for searching Airbnb listings. Search by location, date, and guest count, then filter by price, rating, bedrooms, and keyword match for parking, basement, and renovation details.

## Features

- 🔍 **Search Airbnb** by coordinate box with custom radius
- 📊 **Filter results**: bedrooms, price, rating, distance from center
- 🅿️ **Keyword analysis**: detect parking availability, basement/semi-basement status, and renovation info
- 📋 **Structured output**: JSON results with URLs, prices, ratings, and keyword matches
- 💰 **Multi-currency support**: CNY, USD, EUR, etc.
- 🌍 **Multi-language**: Chinese, English, and more

## Installation

### ClawHub

```bash
clawhub install airbnb-agent
```

### Manual

```bash
git clone https://github.com/Suidge/airbnb-agent.git
cd airbnb-agent
bash scripts/setup.sh
```

## Usage

### Step 1: Search + Filter

```bash
.venv/bin/python3 scripts/search.py "Brighton" \
  --check-in 2026-08-27 --check-out 2026-09-04 \
  --guests 3 --currency CNY \
  --bedrooms 2 --max-price 20000 --min-rating 4.8 \
  --center-lat 50.8225 --center-lng -0.1373 \
  --max-distance-km 2.5
```

Outputs filtered candidates to `/tmp/airbnb_candidates.json` (sorted by distance).

### Step 2: Detail Analysis (optional)

```bash
.venv/bin/python3 scripts/details.py /tmp/airbnb_candidates.json \
  --top 15 --check-in 2026-08-27 --check-out 2026-09-04
```

Fetches each listing's detail page and searches for:
- 🅿️ **Parking**: free parking, driveway, garage, 停车位
- ⚠️ **Basement**: basement, semi-basement, garden level, 地下室
- 🔨 **Renovation**: newly renovated, refurbished, brand new, 新装修

Output to `/tmp/airbnb_results.json`.

Keyword matches are signals only. Verify important amenities against the listing page or host before booking.

## Key Parameters

| Param | Default | Description |
|-------|---------|-------------|
| `--bedrooms` | 0 | Min bedrooms (0 = no filter) |
| `--max-price` | 0 | Max total price (0 = no filter) |
| `--min-rating` | 0 | Min rating 0-5 (0 = no filter) |
| `--max-distance-km` | 5 | Search radius |
| `--center-lat/lng` | 50.8225/-0.1373 | Brighton College |
| `--currency` | CNY | Price currency |
| `--language` | zh | Result language |

Common city coordinates available in `references/api-fields.md`.

## Skill Structure

```
airbnb-agent/
├── SKILL.md              # Agent-facing instructions & metadata
├── scripts/
│   ├── search.py         # Search + filter script
│   ├── details.py        # Detail page analysis script
│   └── setup.sh          # One-time venv setup
├── references/
│   └── api-fields.md     # API field reference + city coordinates
└── .gitignore
```

## Limitations

- Searches by coordinate box, not place name (provide center lat/lng)
- Detail scraping uses HTML — subject to Airbnb layout changes
- No login/cookie support (can't see personalized prices)
- `curl-cffi` impersonation may break with Chrome updates

## License

MIT

## Author

Created by Neo Shi (@Suidge) with OpenClaw.
