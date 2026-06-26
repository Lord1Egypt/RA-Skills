---
name: clawflight
description: Find flights with Starlink satellite WiFi. Filters to Starlink-equipped airlines only, ranks by WiFi score/price/jet lag, returns affiliate booking links. Use when searching for flights where you need to work on the plane.
---

# ✈️ ClawFlight Skill

AI-first flight search that finds flights with Starlink internet. Built for business travelers and digital nomads who need to work on long-haul flights.

## What It Does

- 🔍 **Search flights** between any airports
- 🛜 **Filter Starlink** — only shows flights with Starlink-equipped airlines
- ⭐ **Rank by priority** — WiFi quality, price, duration, or jet lag friendliness
- 🔗 **Affiliate links** — direct booking links (Kiwi.com + Skyscanner)
- 📊 **Rate flights** — submit WiFi quality ratings (speed, reliability, ease)
- ⏰ **Post-flight nudge** — save flights, get prompted 6h after landing

## Setup

```bash
# Install dependencies
cd ~/clawd/projects/clawflight/skill
npm install

# Get a FREE Amadeus API key (no credit card required):
# 1. Go to https://developers.amadeus.com/self-service
# 2. Register → Create App → copy Client ID + Secret
# 3. Set environment variables:

export AMADEUS_CLIENT_ID="your_client_id"
export AMADEUS_CLIENT_SECRET="your_client_secret"

# Optional: use production data (requires moving to production in Amadeus portal)
export AMADEUS_ENV=production
```

The WiFi ratings database is maintained by ClawFlight — you only need to provide your own Amadeus key for live flight data. No other API key required.

## Commands

### Find a flight

```
clawflight search --from BKK --to LHR --date 2026-03-14 --priority wifi
```

Options:
- `--from, -f` — Origin IATA code (e.g., BKK, LHR, SFO)
- `--to, -t` — Destination IATA code
- `--date, -d` — Departure date (YYYY-MM-DD)
- `--priority, -p` — Sort by: `wifi` (default), `cheap`, `fast`, `jetlag`
- `--adults, -a` — Number of passengers (default: 1)
- `--json` — Output machine-readable JSON

### List Starlink airlines

```
clawflight airlines
```

Shows all airlines in the database with WiFi scores and fleet coverage.

### Save a flight (for post-flight rating)

```
clawflight save --flight UA123 --arrival 2026-03-15T14:30:00Z
```

Saves flight info. A cron job will nudge you 6 hours after arrival to rate the WiFi.

### Rate a flight

```
clawflight rate --airline UA --speed 5 --reliability 4 --ease 5
```

Submit WiFi quality ratings to build the community database.

## Examples

### "Find me a flight from NYC to London next week with good WiFi"

```bash
clawflight search --from JFK --to LHR --date 2026-03-10 --priority wifi
```

Output:
```
🛫 ClawFlight Results

✈️ #1 — United Airlines (Starlink ⭐ 4.7)
   Mar 10 | 7h05 | $540 | New York → London
   Book: https://www.kiwi.com/deep?affilid=clawflight&booking_token=...

✈️ #2 — Air France (Starlink ⭐ 4.3)
   Mar 10 | 7h25 | $485 | New York → Paris → London
   Book: https://www.kiwi.com/deep?...
```

### "Show me the cheapest option"

```bash
clawflight search --from SFO --to NRT --date 2026-04-01 --priority cheap
```

### "I want to minimize jet lag"

```bash
clawflight search --from LAX --to SYD --date 2026-05-15 --priority jetlag
```

## Airline Database

The skill uses a curated list of Starlink-equipped airlines stored in `data/airlines.json`. Current carriers:

| Airline | Code | Fleet Coverage | WiFi Type |
|---------|------|----------------|-----------|
| United Airlines | UA | 85% | Starlink |
| Hawaiian Airlines | HA | 90% | Starlink |
| JSX | JSX | 100% | Starlink |
| Qatar Airways | QR | 40% | Starlink |
| Air France | AF | 30% | Starlink |
| Delta | DL | 15% | Starlink |
| Alaska Airlines | AS | 35% | Starlink |
| Southwest | WN | 20% | Starlink |

**Note:** Fleet coverage is approximate. Airlines swap aircraft. Not guaranteed on every flight.

## Integration with OpenClaw

This skill can be called from within OpenClaw conversations:

```
User: I need a flight from Bangkok to London next month
Agent (uses clawflight): Let me find Starlink flights for you...
```

## Files

```
skill/
├── package.json       # Dependencies (axios, commander)
├── clawflight.js      # Main CLI script
└── SKILL.md          # This file

data/
├── airlines.json      # Starlink airline database
├── saved-flights.json # User-saved flights
└── ratings.json      # Community WiFi ratings
```

## Getting an API Key

1. Go to https://tequila.kiwi.com
2. Sign up (free tier available)
3. Get your API key
4. Set: `export KIWI_API_KEY="your_key"`

## Affiliate Program

- **Kiwi.com**: 5% commission on bookings
- **Affiliate ID**: `clawflight`
- Links auto-tagged with your ID

## Maintenance

- **Airline data**: Updated weekly (Samantha cron)
- **Community ratings**: User-submitted via `rate` command
- **Database location**: `~/clawd/projects/clawflight/data/`

---

*Built with 🐙 by Samantha & Antoine*
*V1.0 — Feb 2026*
