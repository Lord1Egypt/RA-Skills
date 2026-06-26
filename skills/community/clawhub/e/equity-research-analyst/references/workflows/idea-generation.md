# Idea Generation

description: Systematic stock screening and investment idea sourcing. Combines quantitative screens, thematic research, and pattern recognition to surface new long and short ideas. Use when looking for new ideas, running screens, or conducting thematic sweeps. Triggers on "idea generation", "stock screen", "find ideas", "what looks interesting", "screen for", "new ideas", or "pitch me something".

## Structured Data Source

Use `tradingviewapi` to source and rank candidates before doing deeper fundamental work:

- `GET /api/leaderboard/stocks` — screen starting universe by gainers / losers / high dividend / 52-week highs / volatility
- `GET /api/metadata/tabs?type=stocks` and `GET /api/metadata/columnsets` — discover available leaderboard slices
- `GET /api/market-data/{symbol}` — validate revenue growth, margins, ROIC, leverage, and valuation
- `GET /api/quote/{symbol}?session=regular&fields=all` and `GET /api/ta/{symbol}` — trading context and momentum confirmation
- `GET /api/ideas/hot` and `GET /api/ideas/list/{symbol}` — crowd positioning and community idea flow
- `GET /api/calendar/ipo?from=&to=` — recent / upcoming IPO names for special-situation work

Web Search is still required for insider buying, short interest, lockup terms, activist filings, and other event-driven / ownership data not present in the API.

## Execution Notes

- When screening by company name, resolve each candidate to `EXCHANGE:TICKER` with `/api/search/market/{query}?filter=stock` before validation.
- Use the resolved symbol as canonical. Do not depend on `data.company.ticker` or `data.company.exchange` from `/api/market-data/{symbol}` to recover the primary listing.
- For trade context, prefer `GET /api/quote/{symbol}?session=regular&fields=all`; quote metrics are nested under `data.data`.

## Workflow

### Step 1: Define Search Criteria

Ask the user for parameters:
- **Direction**: Long ideas, short ideas, or both
- **Market cap**: Large, mid, small, micro
- **Sector**: Specific sector or cross-sector
- **Style**: Value, growth, quality, special situation, event-driven
- **Geography**: US, international, global
- **Theme**: Any specific thematic angle (AI, reshoring, aging demographics, etc.)

### Step 2: Quantitative Screens

Start with `leaderboard` / `metadata` to pull a candidate list, then validate each shortlisted symbol with `/api/market-data/{symbol}`, `/api/quote/{symbol}?session=regular&fields=all`, and `/api/ta/{symbol}`.

Run screens based on the style:

**Value Screen**
- P/E below sector median
- EV/EBITDA below historical average
- Free cash flow yield >5%
- Price/book below 1.5x
- Insider buying in last 90 days
- Dividend yield above market average

**Growth Screen**
- Revenue growth >15% YoY
- Earnings growth >20% YoY
- Revenue acceleration (growth rate increasing)
- Expanding margins
- High return on invested capital (>15%)
- Strong net retention (>110% for SaaS)

**Quality Screen**
- Consistent revenue growth (5+ years)
- Stable or expanding margins
- ROE >15%
- Low debt/equity
- High free cash flow conversion
- Insider ownership >5%

**Short Screen**
- Declining revenue or decelerating growth
- Margin compression
- Rising receivables / inventory vs. sales
- Insider selling
- Valuation premium to peers without justification
- High short interest with deteriorating fundamentals
- Accounting red flags (auditor changes, restatements)

**Special Situation Screen**
- Recent IPOs / SPACs with lockup expirations
- Spin-offs in last 12 months
- Companies emerging from restructuring
- Activist involvement
- Management changes at underperforming companies

Use `tradingviewapi` to source recent IPO names and public-market context, then supplement with external event / filing work.

### Step 3: Thematic Sweep

For thematic ideas, research the theme and identify beneficiaries:

1. Define the thesis (e.g., "AI infrastructure spending accelerates through 2026")
2. Map the value chain — who benefits directly vs. indirectly?
3. Identify pure-play vs. diversified exposure
4. Assess which names are already "priced in" vs. under-appreciated
5. Look for second-order beneficiaries that the market hasn't connected to the theme

### Step 4: Idea Presentation

For each idea that passes the screen, present:

**[Company Name] — [Long/Short] — [One-Line Thesis]**

| Metric | Value | vs. Peers |
|--------|-------|-----------|
| Market cap | | |
| EV/EBITDA (NTM) | | |
| P/E (NTM) | | |
| Revenue growth | | |
| EBITDA margin | | |
| FCF yield | | |

**Thesis (3-5 bullets):**
- Why this is mispriced
- What the market is missing
- Catalyst to realize value

**Key Risks:**
- What would make this wrong

**Suggested Next Steps:**
- Build full model? Deep-dive diligence? Expert call?

### Step 5: Output

- Shortlist of 5-10 ideas with one-page summaries
- Screening criteria and methodology documented
- Comparison table across all ideas
- Prioritized list: which ideas to research first

## Important Notes

- Screens surface candidates, not conclusions — every screen output needs fundamental work
- The best ideas often come from intersections (e.g., quality company at value price due to temporary headwind)
- Avoid crowded trades — check ownership data, short interest, and how many analysts cover the name
- Contrarian ideas need a catalyst — being early without a catalyst is the same as being wrong
- Track idea hit rates over time — which screens and approaches produce the best ideas?
- Short ideas need higher conviction — timing is harder and risk is asymmetric
