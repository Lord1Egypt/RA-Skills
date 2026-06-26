---
name: ashare-fund-intel
description: Produce scheduled A-share and fund intelligence reports with bullish and bearish signals, source-backed analysis, and position-adjustment suggestions. Use when user asks for China market/fund daily briefs, timed reminders, or risk-based portfolio adjustment input.
---

# A-Share Fund Intel

## Overview

This skill creates robust A-share and fund monitoring reports at fixed times:
- Pre-open briefing (before 09:00)
- Post-close review (after 15:00)
- NAV/earnings confirmation report (after 21:00)

## Inputs To Confirm

When first used, confirm these and persist in session memory:
- Risk preference: conservative / balanced / aggressive
- Position style: index funds / sector funds / mixed / stock-heavy
- Watchlist: indices, sectors, funds, and key holdings
- Delivery format: concise / detailed

If user did not provide a watchlist, use default broad market + mainstream fund buckets from `references/sources.md`.
If user already provided holdings, read `references/portfolio-current.md` and treat it as highest-priority personalization input.

## Data Collection Rules

1. Use source-backed content only.
2. Prefer official and primary sources first, then mainstream media, then blogger views.
3. If `web_search` is unavailable, continue via `browser` + `web_fetch`; do not stop.
4. If a source is blocked/paywalled, state it explicitly and switch to an alternate source.
5. For each major claim, attach at least one URL.

## Source Priority

Read `references/sources.md` and follow this order:
1. Regulators/exchanges/official disclosures
2. Financial reports and company announcements
3. Authoritative finance media
4. Well-known finance bloggers/opinion leaders (sentiment reference only)

## Three Report Modes

Read `references/report-template.md` and render by mode:

1. `PRE_OPEN` (before 09:00)
- Overnight macro and policy signals
- Futures/ADR/major index context
- Today's A-share and fund key catalysts
- Suggested opening risk posture and position tilt

2. `POST_CLOSE` (after 15:00)
- Market breadth, turnover, northbound flow, sector rotation
- Fund-relevant winners/losers and style shift
- Bullish vs bearish factors from today's tape and news
- Next-session position-adjustment playbook

3. `NIGHT_CONFIRM` (after 21:00)
- Fund NAV/profit confirmation and attribution
- Earnings/announcements impact scan
- Policy/news digest after close
- Risk check and next-day tentative allocation range

For all three modes, include a personalized holdings section:
- Per-fund impact scan (event -> affected fund -> direction)
- Per-fund action tag: `increase` / `hold` / `reduce`
- Simple suggested allocation change range (percentage points)

## Output Constraints

- Use the template structure and keep section titles stable.
- Include:
  - `Bullish factors` (>=3)
  - `Bearish factors` (>=3)
  - `Position suggestion` with explicit range (e.g., equity 55-65%)
  - `Top risks for next window` (>=3)
  - `Personalized holdings actions` for each held fund
- Separate facts from opinions clearly.
- End with:
  - `This is not investment advice.`

## Trigger Phrases

This skill should activate when user asks for:
- A-share/China market daily monitoring
- Fund briefing or NAV confirmation report
- Bullish/bearish signal summary for position adjustment
- Timed finance reports (morning close night)
