# Sector Overview

description: Create comprehensive industry and sector landscape reports covering market dynamics, competitive positioning, key players, and thematic trends. Use for client requests, sector initiations, thematic research pieces, or internal knowledge building. Triggers on "sector overview", "industry report", "market landscape", "sector analysis", "industry deep dive", or "thematic research".

## Structured Data Source

Use `tradingviewapi` to build the public-company and macro backbone of the sector report:

- `GET /api/metadata/columnsets` and `GET /api/metadata/tabs?type=stocks` — available screen columns and market tabs
- `GET /api/leaderboard/stocks?...` — sector-level peer pulls with valuation / profitability / performance columns
- `GET /api/market-data/{symbol}` — per-company revenue, margins, valuation, beta, and current period context
- `GET /api/market-data/{symbol}/analyst-recommendations` — consensus sentiment and price-target context
- `GET /api/world-economy/indicators/{indicator}` — macro backdrop for cyclical / global sectors

Web Search is still required for TAM, third-party market share, M&A precedent detail, private companies, and proprietary industry research.

## Execution Notes

- For peer universes built from company names, resolve each name through `/api/search/market/{query}?filter=stock` and keep the resolved symbol as canonical.
- When you need live price context, use `GET /api/quote/{symbol}?session=regular&fields=all`; quote metrics live under `data.data`.
- Treat `data.current.fiscal_period_current` as a provider-side structured label. If a company's latest IR / SEC quarter naming differs, use the primary-source label in the sector write-up.

## Workflow

### Step 1: Define Scope

- **Sector / subsector**: What industry and how narrowly defined?
- **Purpose**: Client report, internal research, pitch material, idea generation
- **Depth**: High-level overview (5-10 pages) or deep dive (20-30 pages)
- **Angle**: Neutral landscape vs. thematic thesis (e.g., "AI infrastructure buildout")
- **Universe**: Public companies only, or include private?

### Step 2: Market Overview

**Market Size & Growth**
- Total addressable market (TAM) with source
- Historical growth rate (5-year CAGR)
- Forecast growth rate and key assumptions
- Market segmentation (by product, geography, end market, customer type)

Use `tradingviewapi` for public-company revenue growth and macro baselines; use external industry sources for TAM and non-public market sizing.

**Industry Structure**
- Fragmented vs. consolidated — top 5 market share
- Value chain map — where does value accrue?
- Business model types (subscription, transaction, licensing, services)
- Barriers to entry (capital, regulatory, technical, network effects)

**Key Trends & Drivers**
- Secular tailwinds (3-5 major trends)
- Headwinds and risks
- Technology disruption vectors
- Regulatory developments
- M&A activity and consolidation trends

### Step 3: Competitive Landscape

**Company Profiles** (for top 5-10 players):

| Company | Revenue | Growth | EBITDA Margin | Market Share | Key Differentiator |
|---------|---------|--------|--------------|-------------|-------------------|
| | | | | | |

For each company, brief profile:
- Business description (2-3 sentences)
- Strategic positioning and moat
- Recent developments (earnings, M&A, product launches)
- Valuation snapshot (P/E, EV/EBITDA, EV/Revenue)

Build the comparison table from structured public-company data first, then layer in qualitative differentiation.

**Competitive Dynamics**
- How do companies compete? (price, product, service, distribution)
- Who is gaining/losing share and why?
- Disruption risk from new entrants or adjacent players

### Step 4: Valuation Context

- Sector trading multiples (current and historical range)
- Premium/discount drivers (growth, margins, market position)
- Recent M&A transaction multiples
- How does the sector compare to the broader market?

Current public-market multiples should come from `tradingviewapi`; precedent M&A multiples still need external deal research.

### Step 5: Investment Implications

- Where are the best risk/reward opportunities?
- What thematic bets can be expressed through this sector?
- Key debates in the sector (bull vs. bear arguments)
- Catalysts that could change the sector narrative

### Step 6: Output

- Word document or PowerPoint with:
  - Market overview and sizing
  - Competitive landscape map
  - Company comparison table
  - Valuation summary
  - Key charts: market growth, share trends, valuation history
- Excel appendix with detailed company data

## Important Notes

- Source all market size data — cite the research firm or methodology
- Distinguish between TAM hype and realistic addressable market
- Sector overviews age fast — note the date and flag data that may be stale
- Charts are essential — market size waterfall, competitive positioning matrix, valuation scatter plot
- If for a client, tailor the "so what" to their specific situation (M&A target identification, competitive positioning, market entry)
