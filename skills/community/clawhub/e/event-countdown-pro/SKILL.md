---
name: event-countdown-pro
description: "Set up a daily countdown reminder for a stock's next price-moving corporate event — earnings releases, AGMs, product launches, investor days, dividend dates, FDA decisions, or any event likely to impact the stock price. Resolves company name to ticker, discovers the next significant event from yfinance and web search, and creates a daily cron reminder via remind-me that runs stock-price-checker-pro and stock-fundamentals every day starting 1–2 weeks before the event. Triggers: earnings reminder, earnings countdown, AGM reminder, AGM countdown, event countdown, corporate event reminder, product launch countdown, investor day reminder, notify me before earnings, remind me about earnings, earnings alert."
homepage: https://finance.yahoo.com
metadata: {"clawdbot":{"emoji":"🔔","requires":{"bins":["uv","openclaw"]}}}
---

# Skill: Event Countdown

## When to use
- User wants a daily reminder leading up to a company's next price-moving event.
- User says "set up a countdown for NVIDIA".
- User says "notify me 1 week before Apple's next event every day at 10 AM".
- User says "remind me daily before Tesla's financial release".
- User says "set up an AGM countdown for Shell".
- User says "notify me before Microsoft's product launch".
- User wants to track an upcoming corporate event with daily price + fundamentals updates.

## When NOT to use
- User just wants the current stock price → use `stock-price-checker-pro`
- User just wants fundamentals → use `stock-fundamentals`
- User wants a generic reminder (not event-related) → use `remind-me`
- User wants a full research report right now → use `equity-research`
- User wants to check the earnings date without scheduling → use `stock-price-checker-pro`

---

## Overview

This skill discovers the **next price-moving corporate event** for a stock and creates a daily countdown to it. It scans two data sources in priority order:

| Priority | Source | Data | Examples |
|----------|--------|------|----------|
| 1 | yfinance (Python script) | Earnings dates, dividend dates | `2026-07-30` (AAPL earnings) |
| 2 | Web search (agent) | AGMs, product launches, investor days, FDA decisions, splits, M&A votes — any event likely to move the stock price | `2026-06-10` (NVIDIA GTC) |

Once the event is found and confirmed, a daily cron fires at the specified time, running `stock-price-checker-pro` + `stock-fundamentals` every day leading up to the event.

---

## Conversation Flow

### Step 1 — Resolve the company name to a ticker

Map the user's company name to its ticker symbol. Use the same approach as `stock-price-checker-pro`: the LLM agent resolves common company names to their Yahoo Finance tickers.

| Company | Ticker |
|---------|--------|
| NVIDIA | `NVDA` |
| Apple | `AAPL` |
| Tesla | `TSLA` |
| Microsoft | `MSFT` |
| Amazon | `AMZN` |
| Google / Alphabet | `GOOGL` |
| Meta / Facebook | `META` |
| Pfizer | `PFE` |
| Rheinmetall | `RHM.DE` |
| SAP | `SAP.DE` |
| ASML | `ASML.AS` |
| Shell | `SHEL.L` |

If unsure, ask: *"Just to confirm — that's the ticker `<TICKER>`, right?"*

### Step 2 — Collect lead time and notification time

Ask the user two questions. Apply defaults if they do not specify.

| Question | Default | Options |
|----------|---------|---------|
| How many weeks before the event? | **1 week** (7 days) | 1 or 2 weeks |
| At what time? (with timezone) | **10 AM CET** (Europe/Paris) | Any time in any timezone |

**Examples of user input and how to parse it:**

- *"1 week, 9 AM New York time"* → lead_days=7, hour=9, minute=0, tz=America/New_York
- *"2 weeks, 8 AM London"* → lead_days=14, hour=8, minute=0, tz=Europe/London
- *"just use defaults"* → lead_days=7, hour=10, minute=0, tz=Europe/Paris
- *(no lead time or time given)* → apply defaults, confirm with user

### Step 3 — Discover the next price-moving event

Scan sources in priority order. Stop as soon as a confirmed event is found.

#### 3a — Check yfinance (earnings + dividends)

Run the local script to get the next earnings date:

```bash
uv run /root/.openclaw/workspace/skills/event-countdown-pro/src/main.py <TICKER>
```

The command outputs:
```
Ticker: NVDA
Company: NVIDIA Corporation
Next Earnings Date: 2026-06-15
```

If the output is valid (no `Error:`), present it to the user:

> I found the next event for <COMPANY> (<TICKER>):
> 📊 **Earnings Release** — <EARNINGS_DATE> (source: Yahoo Finance)
>
> Earnings releases are the most common price-moving events. Use this?

**If user says yes** → set `event_type = "Earnings Release"`, `event_date = <EARNINGS_DATE>`, proceed to Step 4.

**If user says no** (or user specifically mentioned a different event type in their request), proceed to 3b.

Also check for upcoming dividend dates from the script output or from a quick `yf.Ticker` call. If a dividend ex-date is coming up sooner than earnings:

> I also noticed an upcoming **Ex-Dividend Date** on <DIVIDEND_DATE>. Would you prefer to track that instead?

If the script returns an error (no earnings date found), proceed directly to 3b.

#### 3b — Web search for other events

Search the web broadly for the company's upcoming events that could move the stock price. Use queries like:

- `"<COMPANY_NAME> upcoming events <CURRENT_YEAR>"`
- `"<COMPANY_NAME> investor day <CURRENT_YEAR>"`
- `"<COMPANY_NAME> product launch event <CURRENT_YEAR>"`
- `"<COMPANY_NAME> AGM annual general meeting <CURRENT_YEAR>"`
- `"<COMPANY_NAME> FDA decision date <CURRENT_YEAR>"` (for pharma/biotech stocks)
- `"<COMPANY_NAME> shareholder vote <CURRENT_YEAR>"`

Look for events in the near future. Event types to watch for:

| Event Type | What it is | Price impact |
|---|---|---|
| **Earnings Release** | Quarterly financial results | **High** — the #1 price mover |
| **Product Launch / Keynote** | New product announcement (e.g. Apple WWDC, NVIDIA GTC, Tesla AI Day) | **High** — can swing 5-10% |
| **Investor Day** | Management presents strategy and long-term outlook to investors | **Medium-High** — often moves on guidance updates |
| **AGM** (Annual General Meeting) | Yearly shareholder gathering where leadership presents results and shareholders vote on key proposals | **Medium** — can move if major votes or surprises |
| **FDA / Regulatory Decision** | Drug approval, regulatory ruling (pharma, biotech, energy) | **Very High** — binary events, can swing 20%+ |
| **Ex-Dividend Date** | Cutoff date to receive the next dividend payment | **Low-Medium** — routine but relevant for income investors |
| **Stock Split** | Share split (e.g. 10-for-1) | **Medium** — often runs up into the split date |
| **M&A Vote / Ruling** | Shareholder vote or regulatory approval on a merger | **Very High** — can swing 15-30% |
| **Analyst Day** | Company hosts analysts for deep dives | **Medium** — similar to investor day |

Pick the **most impactful, soonest** event. Present it to the user:

> I found the next price-moving event for <COMPANY> (<TICKER>):
> 🗓 **<EVENT_TYPE>** — <EVENT_DATE> (source: <SOURCE_URL>)
>
> Is this the event you want to track? If not, I can search for others.

If multiple events are close together, list them and let the user pick:

> I found multiple upcoming events for <COMPANY> (<TICKER>):
> 1. 📊 **Earnings Release** — <DATE1> (source: Yahoo Finance)
> 2. 🎤 **Investor Day** — <DATE2> (source: <URL>)
> 3. 🏛 **AGM** — <DATE3> (source: <URL>)
>
> Which one should I set up the countdown for?

If the user confirms, set `event_type` and `event_date`.

If no event can be found at all, tell the user:

> I couldn't find any upcoming price-moving events for <COMPANY>. Would you like to provide a date and event type manually? (Format: YYYY-MM-DD, Event Type)

If the user provides a manual date, confirm and proceed.

### Step 4 — Compute the reminder schedule

- **reminder_start_date** = `event_date` − `lead_days` (7 or 14)
- **cron_expression** = `cron:<minute> <hour> * * *`  (daily at the specified time in the user's timezone)
  - e.g. 10 AM → `cron:0 10 * * *`
  - e.g. 9:30 AM → `cron:30 9 * * *`

⚠️ If `reminder_start_date` is **today or in the past**, start the daily reminders **today** (the cron will fire at the next occurrence of the specified time). Mention this to the user:
> The event date is close — reminders will start today at 10 AM CET.

⚠️ If `reminder_start_date` is **after the event date** (the event is very soon), tell the user:
> The event date is less than your chosen lead time away. Daily reminders may not be useful. Do you still want to proceed?

⚠️ If the event date is **today**, say:
> The event is today! Would you like me to run a full briefing now instead of scheduling a reminder?

### Step 5 — Create the daily cron reminder via remind-me

The cron message must contain clear instructions for the agent that fires it each day. The template uses the discovered `<EVENT_TYPE>` (e.g. "Earnings Release", "AGM", "Product Launch", "Investor Day") and the confirmed `<EVENT_DATE>`.

The message tells the agent to:

1. Check if today is on or after the event date
2. If so: send a final event-day message, run `stock-price-checker-pro` + `stock-fundamentals`, and **cancel this reminder**
3. If not: compute days remaining, run `stock-price-checker-pro` + `stock-fundamentals`, and send a countdown briefing

#### Cron template (all event types)

```bash
uv run /root/.openclaw/workspace/skills/remind-me/src/main.py create \
  "<TICKER> <SHORT_EVENT_TYPE> Countdown - Daily <HH:MM>" \
  "📊 <TICKER> (<COMPANY>) <EVENT_TYPE> Countdown. Event date: <EVENT_DATE_ISO>.\n\nIf today is on or after <EVENT_DATE_ISO>:\n1. Say '🔔 <COMPANY> (<TICKER>) — <EVENT_TYPE> is TODAY! 🎯'\n2. Run: uv run /root/.openclaw/workspace/skills/stock-price-checker-pro/src/main.py <TICKER>\n3. Run: uv run /root/.openclaw/workspace/skills/stock-fundamentals/src/main.py <TICKER>\n4. Send a comprehensive event-day briefing with price, fundamentals, and a quick take.\n5. Cancel this reminder by running: uv run /root/.openclaw/workspace/skills/remind-me/src/main.py cancel name '<TICKER> <SHORT_EVENT_TYPE> Countdown - Daily <HH:MM>'\n\nIf today is before <EVENT_DATE_ISO>:\n1. Compute days_remaining = days between today and <EVENT_DATE_ISO>\n2. Say '🔔 <COMPANY> (<TICKER>) — <EVENT_TYPE> in {days_remaining} days. Briefing below.'\n3. Run: uv run /root/.openclaw/workspace/skills/stock-price-checker-pro/src/main.py <TICKER>\n4. Run: uv run /root/.openclaw/workspace/skills/stock-fundamentals/src/main.py <TICKER>\n5. Send a daily countdown briefing summarizing price, key fundamentals, and recent company news." \
  "cron:<MINUTE> <HOUR> * * *" \
  "<channel>" \
  "<chatId>" \
  "tz:<IANA timezone>"
```

**Template variables:**

| Variable | Description | Example |
|----------|-------------|---------|
| `<TICKER>` | Stock ticker | `NVDA` |
| `<COMPANY>` | Full company name | `NVIDIA Corporation` |
| `<EVENT_TYPE>` | Human-readable event type | `Earnings Release`, `Product Launch`, `AGM` |
| `<SHORT_EVENT_TYPE>` | Short label for cron name | `Earnings`, `Product-Launch`, `AGM` |
| `<EVENT_DATE_ISO>` | Event date in YYYY-MM-DD | `2026-06-15` |
| `<MINUTE> <HOUR>` | Time from Step 2 | `0 10` for 10:00 AM |
| `<HH:MM>` | Formatted time for cron name | `10:00` |

> ⚠️ **Critical**: Channel, chatId, and timezone resolution follow the same rules as `remind-me` (see its SKILL.md). Auto-detect from session context. The timezone passed here (`tz:<IANA>`) must match the one resolved in Step 2.

### Step 6 — Confirm completion

After the cron is created, report back:

> ✅ Done! Your event countdown is set up:
> 📊 **<TICKER> (<COMPANY>)**
> 🗓 **<EVENT_TYPE>:** <EVENT_DATE_ISO>
> ⏰ **Daily briefing at:** <HH:MM> <TIMEZONE_LABEL>
> 🔁 **Starting:** <REMINDER_START_DATE_ISO> (<DAYS_UNTIL_START> days from now)
> 📱 **Delivered to:** This chat

---

## Commands

### Fetch the next earnings date (yfinance)

```bash
uv run /root/.openclaw/workspace/skills/event-countdown-pro/src/main.py <TICKER>
```

### Examples

```bash
# US stocks
uv run /root/.openclaw/workspace/skills/event-countdown-pro/src/main.py NVDA
uv run /root/.openclaw/workspace/skills/event-countdown-pro/src/main.py AAPL
uv run /root/.openclaw/workspace/skills/event-countdown-pro/src/main.py TSLA

# European stocks
uv run /root/.openclaw/workspace/skills/event-countdown-pro/src/main.py RHM.DE
uv run /root/.openclaw/workspace/skills/event-countdown-pro/src/main.py SAP.DE
uv run /root/.openclaw/workspace/skills/event-countdown-pro/src/main.py ASML.AS
```

## Output

The script returns three lines:
```
Ticker: <SYMBOL>
Company: <COMPANY_NAME>
Next Earnings Date: <YYYY-MM-DD>
```

Or an error:
```
Error: <message>
```

---

## Full Walkthrough

### Example 1 — Earnings (NVIDIA, all defaults)

**User:** "Set up a countdown for NVIDIA"

1. **Resolve ticker:** NVIDIA → `NVDA`
2. **Apply defaults:** 1 week, 10 AM CET → lead_days=7, hour=10, minute=0, tz=Europe/Paris
3. **Discover event:** Run script → earnings on 2026-06-15. Present to user, user confirms.
4. **Compute:** event_date=2026-06-15, reminder_start=2026-06-08, cron=`cron:0 10 * * *`

5. **Create cron:**

```bash
uv run /root/.openclaw/workspace/skills/remind-me/src/main.py create \
  "NVDA Earnings Countdown - Daily 10:00" \
  "📊 NVDA (NVIDIA Corporation) Earnings Release Countdown. Event date: 2026-06-15.\n\nIf today is on or after 2026-06-15:\n1. Say '🔔 NVIDIA Corporation (NVDA) — Earnings Release is TODAY! 🎯'\n2. Run: uv run /root/.openclaw/workspace/skills/stock-price-checker-pro/src/main.py NVDA\n3. Run: uv run /root/.openclaw/workspace/skills/stock-fundamentals/src/main.py NVDA\n4. Send a comprehensive event-day briefing with price, fundamentals, and a quick take.\n5. Cancel this reminder by running: uv run /root/.openclaw/workspace/skills/remind-me/src/main.py cancel name 'NVDA Earnings Countdown - Daily 10:00'\n\nIf today is before 2026-06-15:\n1. Compute days_remaining = days between today and 2026-06-15\n2. Say '🔔 NVIDIA Corporation (NVDA) — Earnings Release in {days_remaining} days. Briefing below.'\n3. Run: uv run /root/.openclaw/workspace/skills/stock-price-checker-pro/src/main.py NVDA\n4. Run: uv run /root/.openclaw/workspace/skills/stock-fundamentals/src/main.py NVDA\n5. Send a daily countdown briefing summarizing price, key fundamentals, and recent company news." \
  "cron:0 10 * * *" \
  "telegram" \
  "<chatId>" \
  "tz:Europe/Paris"
```

6. **Confirm.**

---

### Example 2 — Product Launch (Apple WWDC, 1 week, 9 AM New York)

**User:** "Set up a countdown for Apple's next event, 1 week before, 9 AM New York"

1. **Resolve ticker:** Apple → `AAPL`
2. **Parse:** lead_days=7, hour=9, minute=0, tz=America/New_York
3. **Discover event:**
   - Run script → earnings on 2026-07-30 (still 2 months away)
   - User said "next event" not "earnings", so search web for other events
   - Web search finds Apple WWDC 2026 keynote on 2026-06-09
   - Present: "I found Apple WWDC 2026 Keynote on 2026-06-09" → user confirms

4. **Compute:** event_date=2026-06-09, reminder_start=2026-06-02, cron=`cron:0 9 * * *`

5. **Create cron:**

```bash
uv run /root/.openclaw/workspace/skills/remind-me/src/main.py create \
  "AAPL Product-Launch Countdown - Daily 09:00" \
  "📊 AAPL (Apple Inc.) Product Launch Countdown. Event date: 2026-06-09.\n\nIf today is on or after 2026-06-09:\n1. Say '🔔 Apple Inc. (AAPL) — Product Launch is TODAY! 🎯'\n2. Run: uv run /root/.openclaw/workspace/skills/stock-price-checker-pro/src/main.py AAPL\n3. Run: uv run /root/.openclaw/workspace/skills/stock-fundamentals/src/main.py AAPL\n4. Send a comprehensive event-day briefing with price, fundamentals, and a quick take.\n5. Cancel this reminder by running: uv run /root/.openclaw/workspace/skills/remind-me/src/main.py cancel name 'AAPL Product-Launch Countdown - Daily 09:00'\n\nIf today is before 2026-06-09:\n1. Compute days_remaining = days between today and 2026-06-09\n2. Say '🔔 Apple Inc. (AAPL) — Product Launch in {days_remaining} days. Briefing below.'\n3. Run: uv run /root/.openclaw/workspace/skills/stock-price-checker-pro/src/main.py AAPL\n4. Run: uv run /root/.openclaw/workspace/skills/stock-fundamentals/src/main.py AAPL\n5. Send a daily countdown briefing summarizing price, key fundamentals, and recent company news." \
  "cron:0 9 * * *" \
  "telegram" \
  "<chatId>" \
  "tz:America/New_York"
```

6. **Confirm.**

---

### Example 3 — AGM (Shell, 2 weeks, 9 AM London)

**User:** "Set up an AGM countdown for Shell, 2 weeks before, 9 AM London"

1. **Resolve ticker:** Shell → `SHEL.L`
2. **Parse:** lead_days=14, hour=9, minute=0, tz=Europe/London
3. **Discover event:** User explicitly said AGM → skip yfinance, go straight to web search. Find Shell AGM on 2026-05-20. Confirm with user.
4. **Compute:** event_date=2026-05-20, reminder_start=2026-05-06, cron=`cron:0 9 * * *`

5. **Create cron:**

```bash
uv run /root/.openclaw/workspace/skills/remind-me/src/main.py create \
  "SHEL.L AGM Countdown - Daily 09:00" \
  "📊 SHEL.L (Shell plc) AGM Countdown. Event date: 2026-05-20.\n\nIf today is on or after 2026-05-20:\n1. Say '🔔 Shell plc (SHEL.L) — AGM is TODAY! 🎯'\n2. Run: uv run /root/.openclaw/workspace/skills/stock-price-checker-pro/src/main.py SHEL.L\n3. Run: uv run /root/.openclaw/workspace/skills/stock-fundamentals/src/main.py SHEL.L\n4. Send a comprehensive event-day briefing with price, fundamentals, and a quick take.\n5. Cancel this reminder by running: uv run /root/.openclaw/workspace/skills/remind-me/src/main.py cancel name 'SHEL.L AGM Countdown - Daily 09:00'\n\nIf today is before 2026-05-20:\n1. Compute days_remaining = days between today and 2026-05-20\n2. Say '🔔 Shell plc (SHEL.L) — AGM in {days_remaining} days. Briefing below.'\n3. Run: uv run /root/.openclaw/workspace/skills/stock-price-checker-pro/src/main.py SHEL.L\n4. Run: uv run /root/.openclaw/workspace/skills/stock-fundamentals/src/main.py SHEL.L\n5. Send a daily countdown briefing summarizing price, key fundamentals, and recent company news." \
  "cron:0 9 * * *" \
  "telegram" \
  "<chatId>" \
  "tz:Europe/London"
```

6. **Confirm.**

---

### Example 4 — Regulatory Decision (Pfizer FDA date)

**User:** "Set up a countdown for Pfizer's next FDA decision"

1. **Resolve ticker:** Pfizer → `PFE`
2. **Apply defaults:** 1 week, 10 AM CET
3. **Discover event:** User said FDA → skip yfinance, search web for "Pfizer FDA decision date 2026". Find PDUFA date on 2026-07-15. Confirm.
4. **Compute:** event_date=2026-07-15, reminder_start=2026-07-08, cron=`cron:0 10 * * *`

5. **Create cron** using event_type="FDA Decision" and event_date="2026-07-15".
6. **Confirm.**

---

## Ticker Format Reference

| Market        | Format       | Example              |
|---------------|--------------|----------------------|
| US stocks     | Plain        | `AAPL`, `NVDA`       |
| German stocks | `.DE` suffix | `RHM.DE`, `SAP.DE`   |
| UK stocks     | `.L` suffix  | `SHEL.L`, `BP.L`     |
| Dutch stocks  | `.AS` suffix | `ASML.AS`            |
| Japanese      | `.T` suffix  | `7203.T`             |
| Korean        | `.KS` suffix | `005930.KS`          |

---

## Notes

- `uv run` reads the inline `# /// script` dependency block in `main.py` and auto-installs `yfinance` in an isolated environment — no pip install or venv setup needed.
- Company name → ticker resolution is done by the LLM agent, following the same pattern as `stock-price-checker-pro`.
- Channel, chatId, and timezone are always auto-detected from session context — never ask the user for these.
- Timezone resolution follows `remind-me`'s 3-tier system (message → USER.md → ask user).
- The daily cron message tells the agent to run `stock-price-checker-pro` and `stock-fundamentals` and synthesize a briefing — this applies to all event types.
- The cron auto-cancels on the event day after delivering the final briefing.
- For earnings dates: always use the Python script (yfinance). Do NOT use web search or curl.
- For all other event types: the agent discovers the date via web search. Always confirm the date and source with the user before creating the cron.
- If no event date can be found after exhausting both sources, tell the user and offer manual date entry.
- Do NOT use the shell wrapper pattern — call `uv run src/main.py` directly as shown above.
- Handles ALL price-moving corporate events — earnings, AGMs, product launches, investor days, FDA decisions, dividend dates, stock splits, M&A votes, and analyst days.
