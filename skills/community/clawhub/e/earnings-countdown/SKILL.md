---
name: earnings-countdown
description: "Set up a daily earnings countdown reminder for a stock. Resolves company name to ticker, fetches the next earnings date, and creates a daily cron reminder via remind-me that runs stock-price-checker-pro and stock-fundamentals every day starting 1–2 weeks before earnings. Triggers: earnings reminder, earnings countdown, notify me before earnings, remind me about earnings, earnings alert."
homepage: https://finance.yahoo.com
metadata: {"clawdbot":{"emoji":"🔔","requires":{"bins":["uv","openclaw"]}}}
---

# Skill: Earnings Countdown

## When to use
- User wants a daily reminder leading up to a company's next earnings release.
- User says "notify me 1 week before NVIDIA earnings every day at 10 AM".
- User says "set up an earnings countdown for Apple".
- User says "remind me daily before Tesla's financial release".
- User wants to track an upcoming earnings event with daily price + fundamentals updates.

## When NOT to use
- User just wants the current stock price → use `stock-price-checker-pro`
- User just wants fundamentals → use `stock-fundamentals`
- User wants a generic reminder (not earnings-related) → use `remind-me`
- User wants a full research report right now → use `equity-research`
- User wants to check the earnings date without scheduling → use `stock-price-checker-pro`

---

## Overview

This skill orchestrates three sub-skills to create a proactive earnings countdown:

1. **Resolve company name → ticker** (LLM agent maps it, same approach as `stock-price-checker-pro`)
2. **Fetch the next earnings date** via the local Python script
3. **Create a daily cron reminder** via `remind-me` that fires every day at the specified time, running `stock-price-checker-pro` + `stock-fundamentals` and delivering a countdown briefing

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
| Rheinmetall | `RHM.DE` |
| SAP | `SAP.DE` |
| ASML | `ASML.AS` |
| Shell | `SHEL.L` |

If unsure, ask: *"Just to confirm — that's the ticker `<TICKER>`, right?"*

### Step 2 — Collect lead time and notification time

Ask the user two questions. Apply defaults if they do not specify.

| Question | Default | Options |
|----------|---------|---------|
| How many weeks before earnings? | **1 week** (7 days) | 1 or 2 weeks |
| At what time? (with timezone) | **10 AM CET** (Europe/Paris) | Any time in any timezone |

**Examples of user input and how to parse it:**

- *"1 week, 9 AM New York time"* → lead_days=7, hour=9, minute=0, tz=America/New_York
- *"2 weeks, 8 AM London"* → lead_days=14, hour=8, minute=0, tz=Europe/London
- *"just use defaults"* → lead_days=7, hour=10, minute=0, tz=Europe/Paris
- *(no lead time or time given)* → apply defaults, confirm with user

**Always confirm before proceeding.** Summarise:

> Got it! Here's what I'll set up:
> 📊 **Company:** NVIDIA (NVDA)
> 📅 **Lead time:** 1 week before earnings
> ⏰ **Time:** 10:00 AM CET (Europe/Paris)
> 🔔 **Delivery:** Daily countdown briefing to this chat
>
> Shall I go ahead?

### Step 3 — Fetch the next earnings date

```bash
uv run /root/.openclaw/workspace/skills/earnings-countdown/src/main.py <TICKER>
```

The command outputs:
```
Ticker: NVDA
Company: NVIDIA Corporation
Next Earnings Date: 2026-06-15
```

If the output contains `Error:`, report the error to the user and stop.

### Step 4 — Compute the reminder schedule

From the script output, compute:

- **reminder_start_date** = `Next Earnings Date` − `lead_days` (7 or 14)
- **cron_expression** = `cron:<minute> <hour> * * *`  (daily at the specified time in the user's timezone)
  - e.g. 10 AM → `cron:0 10 * * *`
  - e.g. 9:30 AM → `cron:30 9 * * *`

⚠️ If `reminder_start_date` is **today or in the past**, start the daily reminders **today** (the cron will fire at the next occurrence of the specified time). Mention this to the user:
> The earnings date is close — reminders will start today at 10 AM CET.

⚠️ If `reminder_start_date` is **after the earnings date** (earnings are very soon), tell the user:
> The earnings date is less than your chosen lead time away. Daily reminders may not be useful. Do you still want to proceed?

⚠️ If the earnings date is **today**, say:
> Earnings are today! Would you like me to run a full briefing now instead of scheduling a reminder?

### Step 5 — Create the daily cron reminder via remind-me

The cron message must contain clear instructions for the agent that fires it each day. The message tells the agent to:

1. Check if today is on or after the earnings date
2. If so: send a final "Earnings day!" message, run `stock-price-checker-pro` + `stock-fundamentals`, and **cancel this reminder**
3. If not: compute days remaining, run `stock-price-checker-pro` + `stock-fundamentals`, and send a countdown briefing

Use the remind-me `create` command:

```bash
uv run /root/.openclaw/workspace/skills/remind-me/src/main.py create \
  "<TICKER> Earnings Countdown - Daily <HH:MM>" \
  "📊 <TICKER> (<COMPANY>) Earnings Countdown. Next earnings date: <EARNINGS_DATE_ISO>.\n\nIf today is on or after <EARNINGS_DATE_ISO>:\n1. Say '🔔 <COMPANY> (<TICKER>) earnings are TODAY! 🎯'\n2. Run: uv run /root/.openclaw/workspace/skills/stock-price-checker-pro/src/main.py <TICKER>\n3. Run: uv run /root/.openclaw/workspace/skills/stock-fundamentals/src/main.py <TICKER>\n4. Send a comprehensive earnings-day briefing with price, fundamentals, and a quick take.\n5. Cancel this reminder by running: uv run /root/.openclaw/workspace/skills/remind-me/src/main.py cancel name '<TICKER> Earnings Countdown - Daily <HH:MM>'\n\nIf today is before <EARNINGS_DATE_ISO>:\n1. Compute days_remaining = days between today and <EARNINGS_DATE_ISO>\n2. Say '🔔 <COMPANY> (<TICKER>) earnings in {days_remaining} days — briefing below.'\n3. Run: uv run /root/.openclaw/workspace/skills/stock-price-checker-pro/src/main.py <TICKER>\n4. Run: uv run /root/.openclaw/workspace/skills/stock-fundamentals/src/main.py <TICKER>\n5. Send a daily countdown briefing summarizing price, key fundamentals, and recent company news." \
  "cron:<MINUTE> <HOUR> * * *" \
  "<channel>" \
  "<chatId>" \
  "tz:<IANA timezone>"
```

> ⚠️ **Critical**: Channel, chatId, and timezone resolution follow the same rules as `remind-me` (see its SKILL.md). Auto-detect from session context. The timezone passed here (`tz:<IANA>`) must match the one resolved in Step 2.

### Step 6 — Confirm completion

After the cron is created, report back:

> ✅ Done! Your earnings countdown is set up:
> 📊 **<TICKER> (<COMPANY>)**
> 📅 **Earnings date:** <EARNINGS_DATE_ISO>
> ⏰ **Daily briefing at:** <HH:MM> <TIMEZONE_LABEL>
> 🔁 **Starting:** <REMINDER_START_DATE_ISO> (<DAYS_UNTIL_START> days from now)
> 📱 **Delivered to:** This chat

---

## Commands

### Fetch the next earnings date

```bash
uv run /root/.openclaw/workspace/skills/earnings-countdown/src/main.py <TICKER>
```

### Examples

```bash
# US stocks
uv run /root/.openclaw/workspace/skills/earnings-countdown/src/main.py NVDA
uv run /root/.openclaw/workspace/skills/earnings-countdown/src/main.py AAPL
uv run /root/.openclaw/workspace/skills/earnings-countdown/src/main.py TSLA

# European stocks
uv run /root/.openclaw/workspace/skills/earnings-countdown/src/main.py RHM.DE
uv run /root/.openclaw/workspace/skills/earnings-countdown/src/main.py SAP.DE
uv run /root/.openclaw/workspace/skills/earnings-countdown/src/main.py ASML.AS
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

### Example — NVIDIA with 1 week lead time, 10 AM CET (all defaults)

**User:** "Set up an earnings countdown for NVIDIA"

1. **Resolve ticker:** NVIDIA → `NVDA`
2. **Apply defaults:** 1 week, 10 AM CET → lead_days=7, hour=10, minute=0, tz=Europe/Paris
3. **Confirm with user** (include timezone line), user says yes
4. **Run script:**

```bash
uv run /root/.openclaw/workspace/skills/earnings-countdown/src/main.py NVDA
```

Output:
```
Ticker: NVDA
Company: NVIDIA Corporation
Next Earnings Date: 2026-06-15
```

5. **Compute schedule:**
   - earnings_date = 2026-06-15
   - reminder_start = 2026-06-08 (7 days before)
   - cron = `cron:0 10 * * *`
   - days_until_start = compute from today

6. **Create cron:**

```bash
uv run /root/.openclaw/workspace/skills/remind-me/src/main.py create \
  "NVDA Earnings Countdown - Daily 10:00" \
  "📊 NVDA (NVIDIA Corporation) Earnings Countdown. Next earnings date: 2026-06-15.\n\nIf today is on or after 2026-06-15:\n1. Say '🔔 NVIDIA Corporation (NVDA) earnings are TODAY! 🎯'\n2. Run: uv run /root/.openclaw/workspace/skills/stock-price-checker-pro/src/main.py NVDA\n3. Run: uv run /root/.openclaw/workspace/skills/stock-fundamentals/src/main.py NVDA\n4. Send a comprehensive earnings-day briefing with price, fundamentals, and a quick take.\n5. Cancel this reminder by running: uv run /root/.openclaw/workspace/skills/remind-me/src/main.py cancel name 'NVDA Earnings Countdown - Daily 10:00'\n\nIf today is before 2026-06-15:\n1. Compute days_remaining = days between today and 2026-06-15\n2. Say '🔔 NVIDIA Corporation (NVDA) earnings in {days_remaining} days — briefing below.'\n3. Run: uv run /root/.openclaw/workspace/skills/stock-price-checker-pro/src/main.py NVDA\n4. Run: uv run /root/.openclaw/workspace/skills/stock-fundamentals/src/main.py NVDA\n5. Send a daily countdown briefing summarizing price, key fundamentals, and recent company news." \
  "cron:0 10 * * *" \
  "telegram" \
  "<chatId>" \
  "tz:Europe/Paris"
```

7. **Confirm completion.**

---

### Example — Apple with 2 weeks lead time, 9 AM New York time

**User:** "Notify me 2 weeks before Apple earnings every day at 9 AM New York time"

1. **Resolve ticker:** Apple → `AAPL`
2. **Parse:** lead_days=14, hour=9, minute=0, tz=America/New_York
3. **Confirm**, user says yes
4. **Run script:**

```bash
uv run /root/.openclaw/workspace/skills/earnings-countdown/src/main.py AAPL
```

5. **Compute:** cron = `cron:0 9 * * *`, tz=America/New_York
6. **Create cron** (same pattern as above, with AAPL details and America/New_York timezone)
7. **Confirm completion.**

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
- The daily cron message tells the agent to run `stock-price-checker-pro` and `stock-fundamentals` and synthesize a briefing.
- The cron auto-cancels on earnings day after delivering the final briefing.
- If no earnings date is found, the skill reports the error and stops — no cron is created.
- Do NOT use the shell wrapper pattern — call `uv run src/main.py` directly as shown above.
- Do NOT use web search or curl to fetch earnings dates — always use this script.
