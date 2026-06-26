# Earnings Preview

description: Build pre-earnings analysis with estimate models, scenario frameworks, and key metrics to watch. Use before a company reports quarterly earnings to prepare positioning notes, set up bull/bear scenarios, and identify what will move the stock. Triggers on "earnings preview", "what to watch for [company] earnings", "pre-earnings", "earnings setup", or "preview Q[X] for [company]".

## Structured Data Source

Use `tradingviewapi` for the numeric setup before Web Search:

- `GET /api/market-data/{symbol}` — next earnings date/time, current-period ratios, TTM history arrays, next-quarter EPS forecast
- `GET /api/market-data/{symbol}/analyst-recommendations` — price-target range and current buy/hold/sell distribution
- `GET /api/quote/{symbol}?session=regular&fields=all` — current price, pre/post-market session, daily move, volume
- `GET /api/price/{symbol}?timeframe=D&range=252` — 1-year price context for the trading setup
- `GET /api/ta/{symbol}` and `/api/ta/{symbol}/indicators` — technical context for the setup section

Web Search is still required for whisper numbers, management's exact prior guidance wording, segment-specific consensus not present in the API, and options-implied move.

## Execution Notes

- Resolve the company to `EXCHANGE:TICKER` with `/api/search/market/{query}?filter=stock` first, and treat that resolved symbol as canonical for the workflow.
- Use `GET /api/quote/{symbol}?session=regular&fields=all` for the quote baseline. In the payload, quote fields are nested under `data.data` and session status is typically `data.data.current_session`.
- Treat `data.current.fiscal_period_current` as a provider label, not the final written quarter name. If it conflicts with the latest IR / SEC wording, use the primary-source quarter label in the preview note.

## Workflow

### Step 1: Gather Context

- Identify the company and reporting quarter
- Resolve the ticker to `EXCHANGE:TICKER` if needed via `/api/search/market/{query}?filter=stock`
- Pull structured consensus and baseline data via `tradingviewapi` (`/api/market-data/{symbol}` and `/analyst-recommendations`)
- Find the earnings date and time (pre-market vs. after-hours) from `indicators.earnings_release_next_date` and `earnings_release_next_time`
- Use `/api/quote/{symbol}?session=regular&fields=all`, `/api/price/{symbol}`, and `/api/ta/{symbol}` for the trading setup baseline
- Review the company's prior quarter earnings call and letter only for guidance wording or narrative commentary that is not in the API

### Step 2: Key Metrics Framework

Build a "what to watch" framework specific to the company:

**Financial Metrics:**
- Revenue vs. consensus (total and by segment)
- EPS vs. consensus
- Margins (gross, operating, net) — expanding or contracting?
- Free cash flow
- Forward guidance vs. consensus

**Operational Metrics** (sector-specific):
- Tech/SaaS: ARR, net retention, RPO, customer count
- Retail: Same-store sales, traffic, basket size
- Industrials: Backlog, book-to-bill, price vs. volume
- Financials: NIM, credit quality, loan growth, fee income
- Healthcare: Scripts, patient volumes, pipeline updates

### Step 3: Scenario Analysis

Build 3 scenarios with stock price implications:

| Scenario | Revenue | EPS | Key Driver | Stock Reaction |
|----------|---------|-----|------------|----------------|
| Bull | | | | |
| Base | | | | |
| Bear | | | | |

For each scenario:
- What would need to happen operationally
- What management commentary would signal this
- Historical context — how has the stock moved on similar prints?

### Step 4: Catalyst Checklist

Identify the 3-5 things that will determine the stock's reaction:

1. [Metric] vs. [consensus/whisper number] — why it matters
2. [Guidance item] — what the buy-side expects to hear
3. [Narrative shift] — any strategic changes, M&A, restructuring

### Step 5: Output

One-page earnings preview with:
- Company, quarter, earnings date
- Consensus estimates table
- Key metrics to watch (ranked by importance)
- Bull/base/bear scenario table
- Catalyst checklist
- Trading setup: recent stock performance from `tradingviewapi`; implied move from options via external source if needed

## Important Notes

- Consensus estimates change — always note the source and date of estimates
- "Whisper numbers" from buy-side surveys are often more relevant than published consensus
- Historical earnings reactions help calibrate expectations (search for "[company] earnings reaction history")
- Options-implied move tells you what the market expects — compare to your scenarios, but source it externally because `tradingviewapi` does not provide options-implied move
