---
name: expected-move-visualizer
description: "Expected move visualizer for stocks and ETFs: turn implied volatility into a self-contained HTML chart showing the modeled 30, 60 and 90 day expected move cone around the current price, skewed by 25-delta put and call demand, with IV rank context and the next earnings date marked inside the cone. Renders offline from a bound data snapshot, no live call at view time. Use for expected move calculator, how much is this stock expected to move, implied volatility chart, options expected move, IV rank, earnings move visualizer, straddle move estimate. Read-only. No trading, no purchases, no write operations, no wallet access."
homepage: https://sentisense.ai
primaryEnv: SENTISENSE_API_KEY
metadata:
  openclaw:
    primaryEnv: SENTISENSE_API_KEY
    envVars:
      - name: SENTISENSE_API_KEY
        required: false
        description: "SentiSense API key, optional to install. Get one free at https://app.sentisense.ai/get-api-key, or with no key follow the No key yet steps in the 0-sentisense-onboarding skill for a temporary free one with no signup. Used only to authenticate read-only data calls; no write or trading scope."
---
# Expected Move Visualizer (SentiSense)

Turn options pricing into a picture. This skill fetches one stock's implied volatility, its last price, its recent daily closes, its next earnings date and how it moved on its last eight reports, all from the read-only SentiSense API, binds them into a reviewed HTML template that ships with the skill, and hands back a single self-contained file: a modeled expected-move cone at 30, 60 and 90 days, tilted by 25-delta put and call demand, with the next report marked inside it and the modeled move set against what this stock has actually done on past earnings.

The artifact renders offline. Everything it needs is inlined at build time, so it opens with no network access, no external stylesheet and no script from anywhere else. That is deliberate: it is a snapshot you can keep, screenshot, attach to a note, or open next week and still have render.

Read-only educational data interface. Every figure it draws is modeled from end-of-day implied volatility, and the output is informational context, never a personalized buy or sell recommendation.

## When to Use

- "How much is $NVDA expected to move?" or "what is the expected move into earnings?"
- "Draw me the implied move for this stock", "show me the volatility cone"
- "Is implied volatility rich or cheap here?", "how does the implied move compare to how it actually moved last time?" (the artifact sets the modeled move against past earnings reactions, or against realized volatility when a ticker has no reported history)
- "What is the options market pricing before the report?"
- Any time a chart communicates better than a paragraph of numbers.

Not this skill: options flow and positioning readings such as put/call percentiles, skew percentiles, open-interest walls and unusually active contracts belong to `unusual-options-activity`. What a company actually reported belongs to `stock-earnings-analysis`. This skill does one job, which is turning implied volatility into a picture.

## What an expected move is, and what it is not

Read this before presenting a number from this skill.

- **It is modeled, not quoted.** The API serves implied volatility, not option premiums. The cone is computed in the template from at-the-money implied volatility and the last price. It is not a straddle price and it must never be described as one. The artifact labels itself "modeled" for this reason; keep that word in your own summary too.
- **The formula, stated plainly.** A one-standard-deviation move over a horizon is `spot * iv * sqrt(days / 365)`. Calendar days, because an option's life is wall-clock time to expiry and the served implied volatilities are annualized on that basis.
- **One standard deviation is a band, not a boundary.** Under the model roughly two thirds of outcomes land inside it. Real distributions have fatter tails, and a stock can and does close outside the band. Never present the edges as targets, support, resistance, or a price prediction.
- **The tilt is an assumption.** The 25-delta call and put implied volatilities are served for the near expiry only, so the template carries that skew shape forward to the 60 and 90 day horizons. The level of volatility changes across the term; the shape is held fixed. Say "modeled" rather than implying the tilt was measured at every horizon.
- **This is end-of-day data.** `asOf` is the latest completed session and the figures describe that completed session. Prices are delayed, not live. The options `asOf` can trail the quote by a session on some tickers, so date the implied volatility by `asOf` rather than dating the price by it. The artifact stamps the options session it describes; do not present it as an intraday read.
- **An earnings date inside the window is why the cone is wide.** When a report falls inside a horizon, the implied volatility for that horizon already carries the event. Point that out rather than treating a wide cone as a signal on its own.

## Prerequisites

- A free `SENTISENSE_API_KEY`. Get one at https://app.sentisense.ai/get-api-key. Send it on every call; anonymous requests do not return the dataset. No key yet? Follow "No key yet" in the `0-sentisense-onboarding` skill: one POST returns a temporary free key the agent can use right away and a link the user opens to keep it.
- Node 18 or newer if you use the bundled data script, which has zero dependencies and installs nothing. Otherwise any HTTP client, including plain `curl`.
- Network access to `https://app.sentisense.ai` at build time only. The finished artifact needs none.
- Read-only scope. Every endpoint here is a GET. Nothing this skill does can place a trade, move money, or modify account state.

## Permissions

- Network: HTTPS to app.sentisense.ai only.
- Credentials: SENTISENSE_API_KEY from the environment.
- Shell: one bundled Node/Python script, run locally.
- Files: writes one HTML file the user names.

| Tier | Quota | Rate |
|------|-------|------|
| Free | 1,000 requests/month | 30 requests/min |
| PRO ($15/mo) | Unlimited | 300 requests/min |

One artifact costs five requests, or six for an ETF: the stock quote endpoint declines a fund ticker and the quote is refetched from the ETF quote endpoint, so the declined call counts too. Two of the calls are tiered on a free key:

- **The options dossier.** A free key gets the full dossier on ten covered calls each calendar month (repeat calls for the same ticker count, and the allowance resets on the first of the month, US Eastern time), then a headline preview with `atmIv` and `ivRank1y` flattened directly under `data`. On that preview the 30 day cone still draws while the 60 and 90 day bands and the skew tilt drop out. Full data on a set of sample companies is free: their dossier comes back in full on a free key, marked `sampleCompany: true`, and never spends one of the ten (read the list from `upgrade.sampleTickers` on an options dossier preview, or see https://sentisense.ai/docs/api/#full-sample-responses-with-a-free-key). The commands below use TSLA, one of them.
- **The earnings calendar.** A free key gets only the first week of the requested window, through the coming Sunday, while the envelope's `totalCount` still counts the whole window. A report further out than that week is missing from the rows, so its date is unknown on a free key, not unscheduled.

The bundled script reads both previews, and the artifact says so on its face: a preview label, and the next report shown as unknown when the free calendar left it out.

## How to Run

**Identify your client.** Send a `User-Agent` naming your agent runtime and this skill, for example `OpenClaw/1.4 (expected-move-visualizer)` or `ClaudeCode/2.1 (expected-move-visualizer)`. Substitute your own runtime and version if neither matches. You can also volunteer what your agent is called by adding an `agent/<your-agent-name>` token inside the same parentheses, as in `OpenClaw/1.4 (expected-move-visualizer; agent/research-desk)`. All of it is optional, and it is what tells us this skill has real integrations behind it, so it gets prioritized and you get notice before it changes. The bundled script already carries the skill slug and honors `SENTISENSE_AGENT_NAME` the same way, so exporting that name is all it takes on the script path: it sends `node/prepare_data (expected-move-visualizer; agent/research-desk)`.

Three steps: gather the data, bind it into the template, hand over the file.

### 1. Gather the data

The bundled script does every call and prints exactly the JSON the template expects:

```bash
export SENTISENSE_API_KEY=...      # or however your host supplies secrets
node scripts/prepare_data.mjs TSLA > /tmp/tsla.json
```

It is a single file with no dependencies, so nothing is installed and there is nothing to audit but the script itself. It exits non-zero with a specific message when the key is missing or rejected, when the symbol is not a ticker, when the ticker has no options coverage, and when the latest session carries no at-the-money implied volatility. A free headline preview is not an error: the script binds its 30 day reading and sets `isPreview: true`.

### 2. Bind it into the template

`scripts/template.html` carries two JSON blocks, each holding exactly one placeholder token, and each token appears exactly once in the file so a plain text replacement is unambiguous:

- `/*__SENTISENSE_DATA__*/` takes the script's JSON output verbatim
- `/*__SENTISENSE_META__*/` takes a small object, `{"title": "Expected move: TSLA", "subtitle": "..."}`; the subtitle is optional

Replace the token text inside each block and leave everything else alone. **Do not rewrite the math, the chart code, or the styling.** They live in the template so that they are written once and reviewed once: an expected-move chart that is re-derived per conversation is a chart that is eventually wrong on someone's screen, and a wrong one is worse than none. Your job is binding, not deriving.

Write the result to a new file, for example `expected_move_TSLA.html`, and give the user that path. An unbound template renders a clear "no data bound" message rather than an empty chart, so a failed bind is visible rather than silent.

### 3. Hand it over

Give the user the file and a two or three sentence read of what it shows: the modeled move at the near horizon, whether implied volatility is rich or cheap against its own year (`ivRank1y`), and whether an earnings date falls inside the window. Present the surrounding surface however your host does it. Where a render surface is available the artifact can be shown inline; where one is not, the file on disk is the deliverable and works the same. Do not make the first render depend on anything the host may not have.

## The data, and how to fetch it yourself

The bundled script is a convenience. Everything it does is five plain GETs, documented here so this skill works with no script, no CLI and no SDK.

All of them take the header `X-SentiSense-API-Key: $SENTISENSE_API_KEY`. The options dossier and the earnings calendar are wrapped in the envelope `{ isPreview, previewReason, data }`, and a calendar preview adds `totalCount`; read `.data`. The quote, the chart and the reactions endpoint return their payload directly.

- **`GET /api/v1/stocks/{ticker}/options/summary`** : the end-of-day options dossier. A full dossier carries what the cone needs in `data.latest` and `data.context`. From `latest`: `atmIv` (at-the-money implied volatility for the near expiry, a fraction, so `0.4051` is 40.51%), `atmIv60` and `atmIv90` (the same reading at roughly 60 and 90 days, which is the term structure), and `iv25c` / `iv25p` (the raw 25-delta call and put implied volatilities, where `skew25d == iv25p - iv25c`). From `context`: `ivRank1y`, where today's `atmIv` sits in its own trailing year on a 0 to 100 scale. **A free headline preview is flat instead** (`isPreview: true`): `atmIv`, `ivRank1y` and `expectedMove1d` sit directly under `data` beside `asOf`, `sentiment`, `pcVol`, `pcVolPctl1y` and `maxPain`, and there is no `latest`, no `context`, no `atmIv60`/`atmIv90` and no 25-delta legs. Read `data.latest ?? data` and `data.context ?? data`, bind the preview's `atmIv` as `iv.atm30`, leave the 60 and 90 day readings and the legs null, and keep `isPreview: true`. A full `latest` also serves ready-made move fields you can use directly for those horizons instead of deriving them: `expectedMove1d`/`expectedMove5d`/`expectedMove20d` are calibrated 90% ranges and `expectedMove1s1d`/`expectedMove1s5d`/`expectedMove1s20d` are the one-sigma convention, all fractions of price over 1, 5 and 20 TRADING sessions (`sqrt(h / 252)`), which is a different clock from this skill's own cone (calendar days, `sqrt(d / 365)`), so read them as their own horizons rather than mixing the two. **`data` is `null` for a ticker outside the covered universe**, which is the most actively optioned US names plus the tracked ETFs; an unknown symbol behaves the same rather than answering 404, so treat a null as "no coverage", never as an error. Percentiles are omitted while a baseline builds.
- **`GET /api/v1/stocks/{ticker}/quote`** : the last price, in `currentPrice`. This is the regular-session price and it is delayed, not live. **Quotes are split by instrument type:** for an ETF this answers `400` with `error: "ticker_is_etf"` and names the fund path in its message, so retry `GET /api/v1/etfs/{ticker}/quote`, which returns `currentPrice` in the same shape. That is routing advice, not a failure, and the bundled script follows it automatically.
- **`GET /api/v1/stocks/{ticker}/earnings/reactions`** : how this company's stock actually moved on its recent reports, newest first, in `reactions`. Each row is `{ reportDate, timing, priorClose, nextClose, movePct }`, where `movePct` is the signed percentage from the close before the report to the next session's close. Up to 12 quarters, no parameters; the panel uses the newest 8, so slice client-side. `timing` is `"AMC"` (after the close) or `"BMO"` (before the open), and **`null` means the session was inferred rather than observed**, so a caller that wants only confirmed timings can drop those rows; `movePct` is still computed either way. A ticker with no reported history, an unknown symbol and a fund that never reports all answer `200` with an empty `reactions` array rather than a 404, so read the array's length rather than treating an empty result as an error. Note this vocabulary differs from the calendar endpoint's `before_open` / `after_close`; do not compare the two fields directly.
- **`GET /api/v1/stocks/chart?ticker={ticker}&timeframe=1Y`** : about 251 daily bars, each with a `close`. This feeds the realized-volatility comparison. Valid timeframe values are `1D, 5D, 1W, 1M, 3M, 6M, 1Y, 5Y, 10Y, MAX`; an unrecognized value returns 400 `invalid_timeframe`, so pass `1Y` exactly.
- **`GET /api/v1/calendar/earnings?ticker={ticker}&from={today}`** : the next scheduled report, the first row of `data.earnings` dated today or later, carrying `earningsDate`, `earningsTime` (`before_open`, `after_close`, `during_market` or `unknown`) and `confirmed`. The default window opens on the Monday of the current US Eastern week, so without `from` a report from earlier this week can come back as the first row: pass `from` as today's US Eastern date (`YYYY-MM-DD`), as the bundled script does, or skip rows dated before today. On PRO the window runs about 60 days forward and an empty list means no report inside it. On a free key the rows cover only the first week of the window while `totalCount` counts all of it: an empty list with a larger `totalCount` means the next report is past the free week and its date is unknown here, never that nothing is scheduled.

```bash
curl -H "X-SentiSense-API-Key: $SENTISENSE_API_KEY" \
  "https://app.sentisense.ai/api/v1/stocks/TSLA/options/summary"
```

The REST recipe in this file is the primary path. A maintained command-line client is available as the separate `sentisense-cli` skill for hosts that prefer one.

A rate-limited call returns `429` with a `Retry-After` header; back off for the indicated seconds.

## The data shape the template expects

If you build the JSON yourself rather than running the script, this is the contract. Everything is optional except `ticker`, `spot` and `iv.atm30`; the template degrades rather than failing when a field is absent.

```json
{
  "ticker": "NVDA",
  "asOf": "2026-08-20",
  "generatedAt": "2026-08-22T05:13:26.229Z",
  "spot": 214.72,
  "iv": {
    "atm30": 0.4051, "atm60": 0.3856, "atm90": 0.4002,
    "call25": 0.3954, "put25": 0.4246, "skew25d": 0.0293, "rank1y": 38.3
  },
  "realizedVolatility": [
    { "sessions": 20, "value": 0.3827 },
    { "sessions": 250, "value": 0.3673 }
  ],
  "realizedSessions": 251,
  "nextEarnings": {
    "date": "2026-08-26", "timing": "after_close", "confirmed": true, "estimatedEps": 2.09
  },
  "nextEarningsStatus": "scheduled",
  "reactions": [
    { "reportDate": "2026-05-20", "timing": "AMC",
      "priorClose": 223.47, "nextClose": 219.51, "movePct": -1.77 }
  ],
  "isPreview": false
}
```

Implied volatilities are annualized fractions. `realizedVolatility` entries are annualized standard deviations of daily closing returns over the stated number of sessions, computed on 252 trading days a year rather than 365 calendar days, because the sample is one return per session. Mixing those two conventions is the usual reason an implied and a realized number end up looking further apart than they are.

On a free headline preview the same contract holds with `iv.atm60`, `iv.atm90`, `iv.call25`, `iv.put25` and `iv.skew25d` set to `null` and `isPreview: true`: the template draws the 30 day band alone, untilted, under a preview label.

Four fields in that example are easy to misread:

- **`realizedSessions`** is how many daily closes the script actually received, which is the sample every `realizedVolatility` entry was computed from. A year of daily bars is about 251 closes, so the longest window you can honestly compute is a little under a full year. It is bookkeeping, not a reading; the artifact labels each bar with its own `sessions` count instead.
- **`nextEarningsStatus`** says what a missing `nextEarnings` means: `scheduled` (the date is bound), `not_scheduled` (the calendar answered for its whole window and holds no upcoming report), `outside_preview` (a free calendar preview left rows out, so the date is unknown and the page says so) or `unavailable` (the calendar call failed). Without it the template reads a null `nextEarnings` as not scheduled, so set it whenever you bind a free calendar slice by hand.
- **`nextEarnings.estimatedEps`** is the consensus estimate for the upcoming report, carried through from the calendar. It is scheduling context and plays no part in the expected-move math. It is `null` when no estimate is published.
- **`reactions` drives which comparison panel the artifact draws.** With rows, the template renders the last eight earnings reactions as signed bars against the modeled move; empty, it falls back to the implied-against-realized panel. That is why a fund or an uncovered ticker still produces a complete artifact. Each row is `{ reportDate, timing, priorClose, nextClose, movePct }`, and a `null` timing renders as a bare date rather than a guess. Take these from the reactions endpoint rather than assembling them by hand: rows you compute yourself would put unverified numbers on a chart.

## Answering well

- Lead with the modeled move as a percentage and a price range, and say which horizon it belongs to. "Roughly plus or minus 11.8% over 30 days, about $188.58 to $239.06" is the sentence.
- Say "modeled" out loud. It is the difference between describing our arithmetic and implying a market quote.
- Use `ivRank1y` for the "is this expensive" question, and say it compares the stock to its own past year rather than to other stocks.
- When an earnings date falls inside the window, name it as the reason the cone is wide instead of reading the width as a standalone signal.
- When implied sits above realized, the honest phrasing is that options are pricing more movement than the stock has recently delivered. That is an observation about pricing, not a trade.
- Never turn the band edges into targets, and never attach a probability more precise than the model supports.
- On a preview response, say the 60 and 90 day bands are missing because the free monthly dossier allowance is spent, rather than presenting a one-band chart as the whole picture.
- When the next report is unknown because the free calendar covers one week, say exactly that. Never tell the user nothing is scheduled, and say a report inside the window cannot be ruled out.

## Going further

For "what does this mean for my chosen strategy?", hand off to the `options-payoff-calculator` skill when available. Pass the ticker, dated spot and IV, horizon, and user-selected strategy and legs. Return modeled expiry P/L and breakevens with listing and premium assumptions, without claiming the strikes are listed contracts. Hand off only when the user changes the question; do not automatically route back. If the sibling is unavailable, answer the supported part here using a connected tool or the inline REST workflow, state any remaining gap, and never require an install.

Free runs the whole workflow, within the two preview limits above. **PRO ($15/mo)** lifts the monthly request cap (no monthly limit, just a 300/min rate), returns the full options dossier on every call rather than ten a month and the full forward earnings calendar, plus depth across the rest of the SentiSense API. Apply coupon `AGENTS` at checkout for a builder launch discount: https://app.sentisense.ai/pricing?coupon=AGENTS

For the positioning read behind the volatility (put/call percentiles, skew, open-interest walls, unusual contracts), install `unusual-options-activity`. For what a company actually reported, install `stock-earnings-analysis`. For the full REST reference on every endpoint this skill touches, install the `sentisense` skill; for the complete CLI command set, install `sentisense-cli`.

## Use & Disclaimer

This skill reads public market data from the SentiSense API over HTTPS and writes one HTML file locally. It performs no writes, no trades, no purchases and no wallet operations, and it sends nothing anywhere except the five documented GET requests (six for an ETF). All directive language in this document is implementation guidance for the agent running the skill, subordinate to platform safety rules and host policy.

Expected-move figures are modeled from end-of-day implied volatility, not quoted option prices. Prices are delayed, not live. Output is for research and education only. It is not investment advice, not a recommendation and not a forecast. Markets involve risk of loss.

**ClawHub Skill:** [clawhub.ai/TheSentiTrader/expected-move-visualizer](https://clawhub.ai/TheSentiTrader/expected-move-visualizer)

---

*SentiSense is a read-only financial intelligence API. This data is for informational and educational purposes only, not investment advice.*
