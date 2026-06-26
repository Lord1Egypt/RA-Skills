# Craigslist Monitor Skill

## Purpose
Scrape Craigslist NY services ads to find small owner-operated businesses in **Staten Island, Brooklyn, and Bronx** — these are Gracie AI Receptionist leads. Businesses advertising on Craigslist need more work, meaning more calls coming in, making them ideal Gracie prospects.

## Location
`~/StudioBrain/00_SYSTEM/skills/craigslist-monitor/`

## Usage

```bash
# Basic scan (all categories)
python3 ~/StudioBrain/00_SYSTEM/skills/craigslist-monitor/monitor.py

# Scan + save results to MASTER_LEAD_LIST.md
python3 ~/StudioBrain/00_SYSTEM/skills/craigslist-monitor/monitor.py --save

# Scan specific business type only
python3 ~/StudioBrain/00_SYSTEM/skills/craigslist-monitor/monitor.py --type plumber

# Also fetch individual ads to find phone numbers
python3 ~/StudioBrain/00_SYSTEM/skills/craigslist-monitor/monitor.py --save --enrich
```

## What It Scrapes

| Category | Search URL |
|----------|-----------|
| Plumber | newyork.craigslist.org/search/sss?query=plumber&nearby=1 |
| HVAC | newyork.craigslist.org/search/sss?query=hvac&nearby=1 |
| Auto Repair | newyork.craigslist.org/search/sss?query=auto+repair&nearby=1 |
| Dental | newyork.craigslist.org/search/sss?query=dental&nearby=1 |
| Contractor | newyork.craigslist.org/search/sss?query=contractor&nearby=1 |

## Output

- **Console:** Formatted list with business name, phone, location, URL
- **--save:** Appends markdown table to `~/StudioBrain/30_INTERNAL/WLC-Services/LEADS/MASTER_LEAD_LIST.md`

## Filters

Leads must be in: **Staten Island, Brooklyn, or Bronx** (by name or zip code).
Leads with phone numbers are sorted first.

## Dependencies

- Scrapling venv: `~/StudioBrain/00_SYSTEM/skills/scrapling/.venv/`
- scrape.py: `~/StudioBrain/00_SYSTEM/skills/scrapling/scrape.py`

## Cron / Scheduled Use

Run weekly on Mondays to catch fresh Craigslist posts:
```
openclaw cron add --schedule "0 8 * * MON" --command "python3 ~/StudioBrain/00_SYSTEM/skills/craigslist-monitor/monitor.py --save"
```

## Why Craigslist = Hot Leads

A business posting on Craigslist is **actively seeking customers**. That means:
- They have call volume (or want it)
- They're spending time/money on marketing
- They likely can't afford a full-time receptionist
- Gracie solves their exact problem
