---
name: ai-stock-watchdog
slug: ai-stock-watchdog
displayName: AI stock watchdog
description: "Daily monitoring for Indian equity holdings (NSE/BSE) using a documented severity rubric. Silent by default — only surfaces Sev-1 events (governance, cash flow, promoter/pledge, surveillance, earnings, flows). Includes quarterly checks, segment view for conglomerates, and guidance tracking."
version: 2.2.0
type: skill
license: MIT-0
author: daveanandraj
homepage: https://github.com/daveanandraj/indian-stock-monitor-clawhub
repository: https://github.com/daveanandraj/indian-stock-monitor-clawhub
category: finance
tags:
  - finance
  - investing
  - india
  - nse
  - bse
  - portfolio
  - alerts
  - earnings
  - monitoring
  - promoter-pledge
  - cash-flow
invocation:
  triggers:
    - "check my stocks"
    - "stock morning brief"
    - "portfolio check"
    - "anything I should know about my holdings"
    - "I bought"
    - "I sold"
    - "add to portfolio"
    - "update my portfolio"
    - "trim"
    - "exit"
    - "set up stock monitor"
    - "scan my holdings"
    - "portfolio health check"
    - "how's my portfolio"
  fileTypes:
    - "image/png"
    - "image/jpeg"
metadata:
  openclaw:
    requires:
      tools:
        - WebSearch
        - Read
        - Write
        - Edit
        - AskUserQuestion
      optional:
        - mcp__scheduled-tasks__create_scheduled_task
      env: []
      binaries: []
    dataFiles:
      - portfolio.json
      - competitors.json
      - severity-rubric.md
      - sources.md
    stateDir: state/
    outputDir: alerts/
compatibility:
  platforms:
    - openclaw
    - claude-code
    - codex
    - copilot
disclaimer: Informational only. NOT investment advice. The author is not a SEBI-registered investment advisor. Stock investments are subject to market risk.
---

# AI stock watchdog v2

> Daily monitoring for NSE/BSE holdings against `severity-rubric.md`. **Silence by default** — notify only when a Sev-1 rule fires or the portfolio-health rules say so. Results depend on available sources and search quality; verify material facts yourself.

## Skill directory convention

All data files live in the **same directory as this SKILL.md file**, referred to as `{SKILL_DIR}`. Resolve it to the actual absolute path at runtime.

Files:
- `{SKILL_DIR}/portfolio.json` — holdings, watchlist, preferences, holding periods
- `{SKILL_DIR}/competitors.json` — sector peers + conglomerate segment mapping
- `{SKILL_DIR}/severity-rubric.md` — Sev-1/2/3 classification rules
- `{SKILL_DIR}/sources.md` — data sources with search query templates
- `{SKILL_DIR}/state/last-run.json` — alerts sent, results calendar, management guidance tracker, suppression log
- `{SKILL_DIR}/alerts/{YYYY-MM-DD}-*.md` — archived alerts
- `{SKILL_DIR}/state/portfolio-backup-{TS}.json` — auto-backups

---

# Routing — pick which workflow to run

| User message contains... | Run |
|---|---|
| portfolio.json `_first_run: true`, OR "set up stock monitor" / "start monitoring" | **Onboarding Workflow** |
| "I bought", "I sold", "add to portfolio", "trim", "exit", "update my portfolio", broker screenshot | **Portfolio Update Workflow** |
| "check my stocks", "morning brief", "scan", "anything I should know", scheduled run | **Daily Monitoring Workflow** |
| "portfolio health check", "how's my portfolio", "concentration risk" | **Portfolio Health Check** (then optionally Daily Monitoring) |
| Ambiguous | Ask the user which they want |

---

# Onboarding Workflow (first run)

portfolio.json starts with `_first_run: true` and empty holdings. Detect on first invocation. NEVER skip — always offer setup.

## Onboard-1 — Greet & explain
Greet warmly. Explain in plain language:
1. It watches your Indian stocks every weekday morning.
2. It ONLY pings you when something genuinely critical happens — promoter selling, governance failures, cash flow deterioration, surveillance moves, big earnings misses.
3. It does deep quarterly analysis: not just headline numbers, but cash flow quality, segment trends, and whether management delivered what they promised.
4. Most days you'll hear nothing — that's the design.

## Onboard-2 — Capture holdings
Use AskUserQuestion (if available) OR ask in chat:

> "How would you like to share your portfolio?"
> 1. **Drop a screenshot** of my broker app (Zerodha, Groww, Upstox, Angel One, etc.)
> 2. **Describe in text** (e.g., "50 shares of XYZ at avg 1500, 10 shares of ABC at 2900")
> 3. **Skip for now**

Follow Update Workflow (Update-2+) for processing.

## Onboard-3 — Capture preferences
Ask:
1. **Investment horizon** → short-term (<3 months) / medium-term (3–12 months) / long-term (1+ year)
2. **Alert sensitivity** → critical only (recommended) / critical + high / daily digest
3. **Delivery** → notify only on critical (recommended) / daily one-liner / live dashboard
4. **Positive signals** → include good news in alerts? (yes / no — default no, silence-first)

Save into `portfolio.json` → `preferences`.

## Onboard-4 — Set up the daily schedule
Offer daily schedule for the Daily Monitoring Workflow every weekday at 8:30 AM IST.

- **If `mcp__scheduled-tasks__create_scheduled_task` is available**: use it with cron `30 8 * * 1-5`. This tool only creates a time-based cron trigger — no shell access.
- **If unavailable**: tell the user to trigger manually ("check my stocks") or set their own reminder.

## Onboard-5 — Baseline scan
Offer: "Want me to do a first-look scan now? I'll check the last 7 days of news, filings, promoter activity, and surveillance status for your holdings."

If yes, run Daily Monitoring Workflow once. If no, confirm setup done.

## Onboard-6 — Mark complete
Set `_first_run: false` in portfolio.json. Save.

---

# Portfolio Update Workflow

The user never edits portfolio.json. They describe changes or drop screenshots.

## Update-1 — Detect intent
- **Buy**: "I bought 50 shares at 1620", "picked up XYZ today"
- **Sell / Trim / Exit**: "sold all my XYZ", "trimmed 20 of ABC", "booked profit on PQR"
- **Bulk update**: screenshot + "update my holdings"
- **Watchlist**: "add XYZ to watchlist"
- **Correction**: "my avg for XYZ is actually 1640"

## Update-2 — Gather information

### Screenshot path
Read image using vision. Extract: ticker/company name, quantity, average buy price, broker.

Common layouts:
- **Zerodha Kite**: Instrument | Qty | Avg. cost | LTP | Cur. val | P&L
- **Groww**: ticker, qty, "Avg. ₹X", "Invested ₹Y"
- **Upstox / Angel One / ICICI Direct / Kotak Neo / other brokers**: similar tabular

**CRUCIAL**: Before computing diff, ASK: *"Is this your complete portfolio, or just additions/changes?"* Default: layer onto existing. Never silently remove based on absence.

If truncated (scroll indicator, "+N more"), ask to scroll and re-upload.

### Text path
Parse natural language:
- Resolve company name → NSE ticker. If ambiguous, ASK. Many Indian company names map to multiple tickers (e.g., a group name may have 5+ listed entities). Always confirm before assuming.
- "all" / "exited" → full sell
- "trimmed 20" → subtract from current
- "I now hold 30" → set, don't add
- Missing price on buy → ASK. Never fabricate.

### Sector & segment inference (when adding a new ticker)
1. Look up `competitors.json` → `ticker_to_sector`. If found, use it.
2. If not found, check `sector_peers`.
3. If still not found, web search "{TICKER} NSE sector industry".
4. For conglomerates (check `conglomerate_segments` key in competitors.json), also note the segment mapping for the ticker if it exists.
5. ADD the mapping to `competitors.json`. Never leave sector blank.

### Record holding start date
When adding a new stock, record `buy_date: "{YYYY-MM-DD}"` in portfolio.json. This is used for:
- STCG vs LTCG awareness (365-day boundary for equity)
- Holding period context in alerts

## Update-3 — Read current portfolio
Read `{SKILL_DIR}/portfolio.json`. Compute proposed new state.

## Update-4 — Show diff & confirm (mandatory)
NEVER write without explicit confirmation:

```
Proposed portfolio update:

  ✱ ADD     {TICKER_A}  qty: 10     avg: ₹2,900   sector: {sector}
  ✏ UPDATE  {TICKER_B}  qty: 50→75  avg: ₹1,620→₹1,607 (weighted)
  ✗ REMOVE  {TICKER_C}  (full exit)

  Concentration check: {TICKER_A} would be 28% of portfolio — within limits.

Summary: +1 new, 1 increased, 1 exit. Net 2 holdings.

Apply? (yes / no / edit)
```

Wait for explicit confirmation.

## Update-5 — Backup, then write
1. Copy current portfolio.json to `{SKILL_DIR}/state/portfolio-backup-{YYYY-MM-DD-HHMMSS}.json`
2. Write new portfolio.json preserving structure
3. Update `competitors.json` → `ticker_to_sector` for new tickers
4. Confirm: "Portfolio updated. {N} holdings, {M} on watchlist. Backup saved."

## Update-6 — Weighted average (adding to existing)
```
new_avg = ((old_qty × old_avg) + (new_qty × new_price)) / (old_qty + new_qty)
```
Show the calculation. If user states explicit avg, use theirs.

## Update-7 — Edge cases
- **Sell to zero**: REMOVE entirely.
- **Sell more than held**: STOP, ask.
- **Sell stock not in portfolio**: STOP, ask.
- **Stock split / bonus**: adjust qty × ratio, avg ÷ ratio. CONFIRM.
- **Renamed/merged tickers**: confirm with user.
- **F&O / MF / ETF**: not supported — tell user.
- **Buy without price**: ASK.

## Update-8 — Post-update offer
- New holding → "Want a quick first-look scan of {TICKER}?"
- New sector → "Added {sector} peers to monitoring."
- Full exit → confirm only. If held >1 year: "Note: this was a long-term holding — gains qualify for LTCG (10% above ₹1.25 lakh)."

---

# Portfolio Health Check

Run this before daily monitoring OR when user asks "how's my portfolio" / "portfolio health check". This catches structural risks the daily scan doesn't.

## Health-1 — Concentration risk
- Any single stock >30% of invested value → FLAG as concentration risk
- Any single sector >40% of invested value → FLAG as sector overweight
- Report: "Your portfolio has {N} holdings across {M} sectors. Largest position: {TICKER} at {X}% of invested value."

## Health-2 — Correlation check
- If 3+ holdings in same sector, note: "You have high {sector} correlation. A sector-wide event would hit {X}% of your portfolio."
- If 2+ holdings in same promoter group (Tata group, Adani group), note the group concentration.

## Health-3 — Liquidity check
- If any held stock has average daily volume <₹5 crore, flag: "Exit may be difficult for {TICKER} — average daily volume is only ₹{X} crore."

## Health-4 — Holding period tracker
- For each stock, compute days held since `buy_date`.
- Flag stocks approaching LTCG boundary (between 300–365 days): "Note: {TICKER} held for {N} days. LTCG threshold in {365-N} days — trimming before would mean STCG (20%)."
- Stocks held >365 days: note "LTCG eligible" in any exit recommendations.

## Health-5 — Unrealized P&L awareness
If current price data is available from scan:
- Flag stocks with >30% unrealized loss held >180 days: "You're sitting on a {X}% unrealized loss on {TICKER} for {N} days. This may be anchoring bias."
- Flag stocks with >50% unrealized gain: "Consider whether {TICKER}'s position size (now {X}% of portfolio due to appreciation) warrants a trim."

---

# Daily Monitoring Workflow

You apply this skill's rubric to Indian equities. Job: **silence by default**. Only surface when a Sev-1 trigger matches `severity-rubric.md` (plus the notify rules below). False positives erode trust faster than missed noise.

## Step 1 — Setup & portfolio health
- Read `{SKILL_DIR}/portfolio.json`. If `_first_run: true` OR holdings empty → route to Onboarding.
- Pull every ticker in `holdings`.
- Look up each ticker's sector and segment mapping in `competitors.json`. Build peer set.
- Read `{SKILL_DIR}/state/last-run.json` for alert history and management guidance tracker.
- Note today's date in IST.
- Run Portfolio Health Check (Health-1 through Health-3 only — skip Health-4/5 in automated mode unless concentration risk found).

## Step 2 — India market calendar check
Before stock-level scanning, check:

### 2a. Is today a market holiday?
If NSE is closed today (Republic Day, Holi, Diwali, etc.), skip the scan. Update state with "market_holiday" and exit.

### 2b. Macro events today/this week
Quick search for:
- RBI MPC decision (if this is an MPC week) → impacts all bank/NBFC holdings
- Union Budget (if Feb 1 window) → impacts everything
- GST Council meeting → impacts FMCG, cement, auto
- F&O monthly expiry (last Thursday) → note elevated volatility context

### 2c. Pre-market global cues
Search: US close (Dow/Nasdaq/S&P), GIFT Nifty, Brent crude, USD/INR, US 10Y yield, India VIX.

Only flag if global shock directly maps to a holding:
- Crude up >5% with oil & gas / refining stocks held → flag (for diversified refiners, note that GRM benefits while petchem margins may compress)
- USD/INR sharp move (>1%) with IT / pharma export stocks → flag tailwind/headwind
- US 10Y yield spike >20bps → FII outflow risk, flag for all holdings

## Step 3 — Per-stock daily scan
For each held ticker, run in parallel:

### 3a. Exchange announcements (last 24h)
Search: `site:nseindia.com "{COMPANY_NAME}" announcement`, `site:bseindia.com "{COMPANY_NAME}"`.
Look for: results dates, board meetings, auditor changes, KMP exits, credit rating actions, pledge disclosures, SAST/PIT filings, corporate governance reports, scheme of arrangement.

### 3b. News scan (last 24h)
- `"{COMPANY_NAME}" news` last 1 day — prefer Moneycontrol / ET / Reuters / Mint / Business Standard
- `"{COMPANY_NAME}" SEBI` last 7 days
- `"{COMPANY_NAME}" ED CBI "income tax" raid` last 30 days (only if NEW)
- `"{COMPANY_NAME}" downgrade` last 7 days
- `"{COMPANY_NAME}" fraud whistleblower "forensic audit"` last 90 days (only if NEW)

### 3c. Promoter & institutional activity

**Promoter holding & pledge (check against latest quarterly shareholding pattern):**
- Search: `"{COMPANY_NAME}" promoter holding` or `"{TICKER}" shareholding pattern`
- Compare with previous quarter stored in state. Flag per severity-rubric.md Section A.
- If near a quarterly filing deadline (21 days post quarter-end), actively look for fresh filing.

**Insider trading disclosures (last 7 days):**
- Search: `"{TICKER}" insider trading SAST PIT disclosure site:nseindia.com`
- Flag KMP sales, especially pre-results.

**Block/bulk deals (last 24h):**
- Search: `"{TICKER}" block deal bulk deal`
- Decode: is the seller a promoter entity, FII, PE fund, or retail? Promoter selling = Sev-1.

**FII/MF holding changes (when quarterly data available):**
- Compare latest quarter vs previous from Trendlyne or Screener.
- FII cut >2pp = Sev-1. MF net selling >0.5% = Sev-2.

### 3d. Surveillance & price action
- GSM/ASM status: search `"{TICKER}" GSM ASM surveillance`. Cache 7 days.
- F&O ban list (if near expiry week): check NSE F&O ban page.
- 52-week low yesterday? Flag if on >2x average volume.
- Volume vs 20-day average — flag if >3x with negative move.

### 3e. Sector & peer activity (per unique sector, last 24h)
For each sector:
- Did any peer announce results, guidance, or material news?
- Did a sector regulator issue anything? (RBI for banks, USFDA for pharma, TRAI for telecom, PNGRB for gas)
- Cross-map peer concerns: 2+ peer Sev-1 in 7 days = industry stress trigger.

### 3f. Upcoming results check
- Has the company announced next results date? Track in `state/last-run.json → results_calendar`.
- If results declared in last 24h → trigger Quarterly Deep-Dive (Step 5).
- If results due within 7 days → note "results watch" (no alert, but heightened sensitivity).

### 3g. Conglomerate segment check (for multi-business companies)
If the ticker is flagged as a conglomerate in `competitors.json → conglomerate_segments`:
- Look up the segment definitions and `key_metrics` for each segment in the data file.
- Search for segment-specific news using those key metrics (e.g., refining margins for O2C segments, subscriber data for telecom segments, store count for retail segments).
- A segment turning loss-making or cross-subsidy pattern = Sev-1.

## Step 4 — Severity classification
Classify each signal against `severity-rubric.md`. Apply context modifiers:
- Peer-relative adjustment (sector-wide fall reduces individual severity)
- Horizon adjustment (short-term → elevate price triggers; long-term → demote price, elevate fundamental)
- Position size adjustment (>25% of portfolio → elevate Sev-2 to Sev-1)
- Market regime adjustment (broad correction → raise price thresholds)

**Suppression rule**: If already alerted on same `signal_id` in last 14 days, suppress.

## Step 5 — Quarterly Deep-Dive (when results are out)

Quarterly deep-dive should cover cash flow quality and segment trends, not only headline PAT and EPS vs consensus.

### 5a. Headline numbers
Pull from BSE/NSE filing, Screener, or Trendlyne:
- Revenue: YoY %, QoQ %
- EBITDA: absolute, margin (bps change QoQ and YoY)
- PAT: YoY %, QoQ %
- EPS vs consensus

### 5b. Cash flow quality check (most underrated — catches manipulation)
Pull cash flow statement (Screener cash flow tab or filing):
- **CFO vs PAT**: compute CFO/PAT ratio. Below 0.5x for 2+ quarters = Sev-1.
- **CFO trend**: is CFO growing in line with PAT? If PAT up 20% but CFO flat = red flag.
- **Free cash flow**: CFO minus capex. Negative FCF for 3+ quarters in a non-capex-cycle company = Sev-2.
- **Working capital changes**: large working capital build draining CFO = Sev-1 if receivables/inventory growing >2x revenue.

### 5c. Balance sheet quality
- **Net debt**: QoQ change. Debt increasing while profits grow = fund-flow mismatch.
- **Debt maturity**: >30% maturing within 12 months with weak CFO = refinancing risk.
- **Interest coverage**: EBITDA/interest expense. Below 1.5x = Sev-1.
- **Contingent liabilities**: compare vs previous year. Sharp jump = potential hidden risk.
- **Related party transactions**: jumped >50% YoY without proportionate revenue = Sev-1.
- **Trade receivables**: absolute growth and days outstanding. Over 90 days = collection risk.
- **Inventory days**: rising faster than revenue = demand slowdown or channel stuffing.

### 5d. Segment-wise analysis (critical for conglomerates)
For companies with multiple reported segments (refer to `conglomerate_segments` in competitors.json for segment definitions):
- Revenue and EBIT per segment vs previous quarter and same quarter last year.
- Any segment turned EBIT-negative? → Sev-1.
- Cross-subsidization pattern: profitable segment margin declining while loss-making segment scales → flag.
- Use `key_metrics` from the conglomerate_segments data to know which numbers to pull for each segment.

### 5e. Vs consensus
Pull consensus from Trendlyne or Moneycontrol:
- Revenue miss >15% = Sev-1. Miss 10–15% = Sev-2.
- PAT miss >25% = Sev-1. Miss 15–25% = Sev-2.
- Margin miss >200 bps = Sev-2. Miss >400 bps = Sev-1.

### 5f. Concall analysis
Locate transcript (Screener Documents tab or company IR):
1. **Guidance tracking**: what did management guide last quarter? Extract specific numbers (revenue growth %, margin target, capex plan, order book target). Compare with actuals. If missed >30% of guided number → management credibility drops. Record in `state/last-run.json → guidance_tracker`.
2. **Forward guidance**: extract new guidance numbers. Store for next quarter comparison.
3. **Tone analysis**: compare language with previous 2 concalls. "Confident/strong" → "cautious/watchful" = Sev-2 (Sev-1 if combined with earnings miss).
4. **Specific red flag phrases**: "challenging environment", "one-off", "non-recurring" (used 2+ quarters = it's recurring), "right-sizing", "restructuring charges", "deferred revenue recognition".
5. **Analyst pushback**: if multiple analysts question the same metric (receivables, related party, cash flow) — that's smart money flagging something.
6. **Duration/access**: significantly shorter concall or fewer questions taken = management avoiding scrutiny.

### 5g. Banking-specific quarterly checks (for bank / NBFC holdings)
- **NIM (Net Interest Margin)**: QoQ bps change. Compression >10 bps = note. >20 bps = Sev-2.
- **CASA ratio**: declining = higher cost of funds ahead.
- **GNPA / NNPA**: absolute and ratio. Any uptick = note. Sharp uptick from a low base = Sev-2.
- **Slippage ratio**: fresh slippages as % of opening standard advances. Rising = Sev-2.
- **Credit cost**: provisions as % of average advances.
- **CD ratio (Credit-Deposit)**: above 80% = aggressive lending. Above 85% = risk flag.
- **PCR (Provision Coverage Ratio)**: declining = less buffer for future shocks.
- If the bank has undergone a recent merger, also track: merged book integration, loan-to-deposit ratio normalization, PSL compliance, and synergy realization.

### 5h. Build verdict
- **One-line verdict**: ACCUMULATE / HOLD / WATCH / EXIT BIAS
- **Why** (3 bullets max)
- **Counter-view** (1 bullet — always include)
- **Action**: specific for this week, based on user's horizon
- **Management credibility**: HIGH / MEDIUM / LOW (based on guidance delivery history)

## Step 6 — Quarterly for peers
Same as Step 5 but summarized: one paragraph per peer (QoQ delta + concall tone). Sector-level read: "Industry trend: {strong / mixed / weak / deteriorating}."

Surface ONLY if it changes the read on a held stock.

## Step 7 — Decide whether to notify
Notify only if:
1. ≥1 Sev-1 trigger on a held stock not flagged in last 14 days, OR
2. ≥2 Sev-1 triggers across peers in same sector within 7 days (industry stress), OR
3. Quarterly deep-dive concluded EXIT BIAS or WATCH, OR
4. Portfolio health found >30% concentration in a stock with any Sev-2+ signal.

Otherwise — update state and exit silently.

EXCEPTION: if `delivery` = `daily_brief`, always post a one-liner: "All clear — no Sev-1 across {N} holdings as of {time}."

## Step 8 — Notification format
Save to `{SKILL_DIR}/alerts/{YYYY-MM-DD}-alert.md` AND surface in chat:

```
🔴 STOCK ALERT — {date}

{TICKER} — {one-line headline}
Severity: Sev-1 | Category: {rubric section} | Sector: {sector}

What happened:
{2-3 lines, factual, with specific numbers}

Why it matters for YOU ({horizon} holder, avg ₹{avg_price}, {N} shares):
- {bullet 1 — direct portfolio impact}
- {bullet 2 — what this historically leads to}

Suggested action: {Hold / Watch closely / Trim / Exit bias}
Confidence: {High / Medium / Low}
Management credibility: {High / Medium / Low} (based on {N} quarters tracked)

Sources:
- [Title](URL)
- [Title](URL)

Counter-view: {one line — what could make this NOT critical}

Portfolio impact: This holding is {X}% of your portfolio. {If concentrated: "Given your concentrated position, consider this signal with extra weight."}
```

If multiple stocks triggered, repeat per ticker. Group by severity.

## Step 9 — State update
Update `{SKILL_DIR}/state/last-run.json`:
- `last_run_date`: today's date
- `alerts_sent`: append any new alerts with signal_id and timestamp
- `results_calendar`: update upcoming/past results dates
- `guidance_tracker`: store management guidance numbers for forward comparison
- `promoter_holding_history`: store latest promoter holding % and pledge % per ticker
- `institutional_holding_history`: FII %, DII %, MF holding % per ticker
- `management_credibility`: running score per company based on guidance vs actual
- `surveillance_check`: last checked date, any active GSM/ASM entries

---

# Hard rules

1. NEVER provide buy/sell as financial advice. Frame as "based on rubric, signal suggests…" Remind: informational only, not SEBI-registered.
2. NEVER hallucinate. If can't verify via a source, say "could not verify — check directly."
3. ALWAYS cite sources at the bottom of any alert with markdown links.
4. NEVER repeat an alert already sent in last 14 days for the same signal_id.
5. Default to silence. Most days have nothing to say.
6. NEVER write portfolio.json without showing diff and getting explicit confirmation.
7. ALWAYS back up portfolio.json before writing.
8. If `_first_run: true` or holdings empty → route to Onboarding.
9. Indian markets only — NSE & BSE. All times in IST.
10. For short-term holders: elevate block deals, volume anomalies, 52W low, F&O ban signals.
11. For long-term holders: elevate cash flow quality, governance, promoter pledge, management credibility signals. Demote single-day price moves.
12. NEVER ignore cash flow quality. A company reporting growing profits with declining/negative operating cash flow is the single most common pattern before Indian accounting frauds.
13. For conglomerates: always do segment-level analysis. Consolidated numbers can hide a dying segment behind a thriving one.
14. Track management guidance and hold them accountable. Two consecutive quarters of missing own guidance = downgrade credibility rating.

# Manual invocation
User can trigger ad-hoc:
- "Check my stocks"
- "Stock morning brief"
- "Run portfolio scan"
- "Portfolio health check"
- "How's my portfolio"
- "Anything I should know about my holdings?"

In ad-hoc mode, run same workflow but if nothing critical, give a one-liner: "All clear — no Sev-1 triggers across {N} holdings as of {time}." rather than total silence.
