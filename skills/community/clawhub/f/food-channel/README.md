# Food Channel Skill

An OpenClaw skill for tracking food intake via barcode lookups, photo estimates, and daily summaries.

## Features

- **Barcode lookup** — scan a barcode, get nutrition data from Open Food Facts, log it
- **Photo estimate** — send a photo, get AI-estimated nutrition, log it
- **Daily summary** — aggregated macros + micronutrients with configurable limits
- **Post-log checks** — warns when over calorie/sodium/sugar limits

## Setup

Set required env vars (see SKILL.md for full list):
- `FOOD_CHANNEL_ID` — your food tracking channel ID
- `FOOD_PROFILE_PATH` — path to profile JSON with daily limits (optional)

## Data

Logs to `$WORKSPACE/data/food_log.csv` (one row per entry).

## License

MIT-0
