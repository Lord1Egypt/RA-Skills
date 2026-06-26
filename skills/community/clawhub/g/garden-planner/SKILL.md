---
name: garden-planner
description: "Comprehensive garden planning — track plants, get planting recommendations, watering schedules, and frost alerts. Use when: garden, plant, planting, harvest, frost warning, watering schedule, what should I plant, garden status, garden planner."
---

# Garden Planner Skill

Track what's growing, when to water, what to plant, and when frost threatens.

## Data Location

Default: `~/.openclaw/workspace/garden/garden.json`
All scripts accept `--data-dir PATH` to override.

## Scripts

All scripts are in `skills/garden-planner/scripts/`. Run with `python3`.

---

### Add a Plant

```bash
python3 add_plant.py --name "Cherokee Purple Tomato" --type vegetable
python3 add_plant.py --name "Basil" --type herb --location container-1
python3 add_plant.py --name "Cucumber" --type vegetable --planted-date 2025-05-20 --location bed-B --notes "Spacemaster variety"
```

**Options:**
- `--name` (required) — plant name
- `--type` (required) — `vegetable`, `herb`, `flower`, or `fruit`
- `--planted-date` — YYYY-MM-DD (default: today)
- `--location` — bed/container/row label (default: `unspecified`)
- `--notes` — free text notes
- `--days-to-harvest N` — override auto-lookup from planting calendar

Harvest date is auto-calculated from `references/planting-calendar.md`.

---

### Garden Status

```bash
python3 garden_status.py
python3 garden_status.py --all      # include harvested plants
python3 garden_status.py --json
```

Shows: growth stage (seedling → vegetative → flowering → fruiting → ready), days since planting, expected harvest date, next action. Flags plants ready to harvest.

---

### Weather & Frost Warnings

```bash
python3 weather_check.py --lat 37.54 --lon -77.44
python3 weather_check.py --zip 23220
python3 weather_check.py --json     # reads lat/lon from garden.json config
```

Fetches 7-day forecast from Open-Meteo (free, no API key). Flags:
- ⚠️  Frost warning: low approaching 34°F / 1°C
- ❄️  Frost: low at or below 32°F / 0°C
- 🧊 Hard freeze: low at or below 25°F / -4°C

---

### Planting Guide

```bash
python3 planting_guide.py --zone 7
python3 planting_guide.py --zone 6 --date 2025-04-01
python3 planting_guide.py --zone 7 --type vegetable
python3 planting_guide.py --zone 7 --json
```

Recommends: **plant now**, **start indoors**, **coming soon**, or **too late** — based on zone frost dates and current date. Uses `references/planting-calendar.md` and `references/zones.md`.

---

### Watering Schedules

```bash
python3 watering.py status                              # what needs water today
python3 watering.py list                                # all schedules
python3 watering.py set --target bed-A --days 2 --notes "Deep water"
python3 watering.py log --target bed-A                  # log watered today
python3 watering.py log --target bed-A --date 2025-06-10
```

---

## Garden Config (in garden.json)

Set zone, location name, and coordinates so weather/planting scripts work without extra flags:

```json
{
  "config": {
    "zone": "7",
    "location_name": "Backyard — Richmond, VA",
    "lat": 37.5407,
    "lon": -77.4360
  }
}
```

---

## References

- `references/planting-calendar.md` — 30 vegetables and herbs with days-to-harvest and zone ranges
- `references/zones.md` — USDA hardiness zones with frost date data
- `assets/garden.example.json` — example garden file to copy and customize
