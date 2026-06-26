---
name: economic-calendar-pro
description: "Run a local script to fetch economic calendar events for a date range. Defaults to 7 days inclusive from the query day. Uses TradingEconomics when TRADING_ECONOMICS_API_KEY is present and falls back to Yahoo Finance otherwise."
homepage: https://docs.tradingeconomics.com/economic_calendar/snapshot/
metadata: {"clawdbot":{"emoji":"🗓️","requires":{"bins":["uv"]}}}
---

# Skill: Economic Calendar

## When to use
- The user wants the economic calendar for today, this week, or a custom date range.
- The user asks for upcoming macro events, scheduled releases, or high/medium/low impact events.
- The user wants a forward-looking list of calendar items before trading.

## When NOT to use
- The user wants broad market news and sentiment only -> use `market-news-brief`
- The user wants a stock price or company-specific quote -> use `stock-price-checker-pro`
- The user wants company fundamentals -> use `stock-fundamentals`

## Authentication

- Preferred: set `TRADING_ECONOMICS_API_KEY` to your TradingEconomics credential string
- Supported value format: `client:secret`
- Optional: copy `.env.example` to `.env` at the repo root and fill in `TRADING_ECONOMICS_API_KEY`
- Fallback: if no API key is present, the script uses Yahoo Finance's economic calendar endpoint
- Important: Yahoo fallback can omit importance and market-expectation fields, and country values are returned as short codes like `US`, `EU`, or `JP`

## Commands

### Get the default calendar window

```bash
uv run /root/.openclaw/workspace/skills/economic-calendar-pro/src/main.py
```

Defaults to 7 days inclusive from the query day.

### Get a custom calendar window

```bash
uv run /root/.openclaw/workspace/skills/economic-calendar-pro/src/main.py <START_DATE> <END_DATE>
```

Dates must use `YYYY-MM-DD`.

### Examples

```bash
# Default window: query day plus the next 6 days
uv run /root/.openclaw/workspace/skills/economic-calendar-pro/src/main.py

# Start from a specific day and use 7 days inclusive
uv run /root/.openclaw/workspace/skills/economic-calendar-pro/src/main.py 2026-03-10

# Explicit date range
uv run /root/.openclaw/workspace/skills/economic-calendar-pro/src/main.py 2026-03-10 2026-03-24
```

## Scheduling

Use this flow when the user wants to **schedule** a recurring daily economic calendar briefing (e.g. "send me the economic calendar every day at 11 AM CET").
For one-time ad-hoc queries, use the **Commands** section above.

### Scheduling flow

#### Step 1 — Resolve time and timezone

Ask the user two things. Apply defaults if they do not specify.

| Question | Default | Options |
|----------|---------|---------|
| At what time? | **10 AM CET** (Europe/Paris) | Any time in any timezone |
| Which days? | **Weekdays** (Mon–Fri) | Any combination of days |

**Examples of user input and how to parse it:**

- *"every day at 8 AM New York time"* → hour=8, minute=0, tz=America/New_York, cron=`cron:0 8 * * *`
- *"weekdays at 9 AM London"* → hour=9, minute=0, tz=Europe/London, cron=`cron:0 9 * * 1-5`
- *"just use defaults"* → hour=10, minute=0, tz=Europe/Paris, cron=`cron:0 10 * * 1-5`
- *(no time given)* → apply defaults, confirm with user

**Always confirm before proceeding.** Summarise:

> Got it! Here's what I'll set up:
> 🗓️ **Economic Calendar briefing**
> ⏰ **Time:** 10:00 AM CET (Europe/Paris)
> 📅 **Days:** Weekdays (Mon–Fri)
> 📱 **Delivered to:** This chat
>
> Shall I go ahead?

#### Step 2 — Create the daily cron via remind-me

```bash
uv run /root/.openclaw/workspace/skills/remind-me/src/main.py create \
  "Economic Calendar - Weekdays <HH:MM>" \
  "Run: uv run /root/.openclaw/workspace/skills/economic-calendar-pro/src/main.py\nSend the formatted economic calendar briefing to this chat." \
  "cron:<MINUTE> <HOUR> * * <DAYS>" \
  "<channel>" \
  "<chatId>" \
  "tz:<IANA timezone>"
```

> ⚠️ **Critical**: Channel, chatId, and timezone resolution follow the same rules as `remind-me` (see its SKILL.md). Auto-detect from session context. Never ask the user for these.

#### Step 3 — Confirm completion

After the cron is created, report back:

> ✅ Done! Your economic calendar briefing is set up:
> 🗓️ **Briefing:** Daily economic calendar
> ⏰ **Time:** 10:00 AM CET (Europe/Paris)
> 📅 **Days:** Weekdays (Mon–Fri)
> 📱 **Delivered to:** This chat
> 🔍 **Manage:** Use `remind-me list` to view or `remind-me cancel` to stop

## Output

The command returns:
- Requested date range
- Auth source used (`TradingEconomics API` or `Yahoo Finance fallback`)
- Total event count and covered day count
- Events grouped by day
- For each event: UTC time, country, event name, and available actual / forecast / previous values

## Notes

- The script reads `TRADING_ECONOMICS_API_KEY` from the environment first.
- If no env var is set, it also checks a repo-root `.env` file before falling back to Yahoo Finance.
- Yahoo fallback is better than guest TradingEconomics for current/future windows, but it does not expose the same richness of metadata.
- Do NOT use web search for this workflow - use the script so the output is date-filtered and formatted consistently.
- For recurring daily briefings, use the **Scheduling** flow above (creates a cron via `remind-me`).
