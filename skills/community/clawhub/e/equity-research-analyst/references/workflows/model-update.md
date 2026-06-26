# Model Update

description: Update financial models with new data — quarterly earnings, management guidance, macro changes, or revised assumptions. Adjusts estimates, recalculates valuation, and flags material changes. Use after earnings, guidance updates, or when assumptions need refreshing. Triggers on "update model", "plug earnings", "refresh estimates", "update numbers for [company]", "new guidance", or "revise estimates".

## Structured Data Source

Use `tradingviewapi` first for the numeric refresh:

- `GET /api/market-data/{symbol}` — one-shot pull for current-period ratios, TTM history, next earnings date, and current quarter metadata
- `GET /api/market-data/{symbol}/financials-quarterly` — reported quarterly three-statement actuals
- `GET /api/market-data/{symbol}/analyst-recommendations` — Street recommendation mix and price-target consensus
- `GET /api/market-data/{symbol}/enterprise-value` — EV bridge and EV-based valuation context
- `GET /api/quote/{symbol}?session=regular&fields=all` — current price, market cap, and pre/post-market reaction

Web Search is still needed for exact guidance wording, transcript commentary, segment commentary, restructuring details, and any one-time items that require narrative interpretation.

## Execution Notes

- Resolve the company to `EXCHANGE:TICKER` with `/api/search/market/{query}?filter=stock` first, and keep that resolved symbol as canonical throughout the model update.
- Use `GET /api/quote/{symbol}?session=regular&fields=all` for current price context. Quote fields are nested under `data.data`, not flat at the top level.
- Treat `data.current.fiscal_period_current` as a provider label. If it differs from the company's own quarter naming in the latest release or filing, use the primary-source label in the model commentary and keep the API label only as structured-data context.

## Workflow

### Step 1: Identify What Changed

Determine the update trigger:
- **Earnings release**: New quarterly actuals to plug in
- **Guidance change**: Company updated forward outlook
- **Estimate revision**: Analyst changing assumptions based on new data
- **Macro update**: Interest rates, FX, commodity prices changed
- **Event-driven**: M&A, restructuring, new product, management change

Then pull the structured refresh pack before changing the model: `/api/market-data/{symbol}`, `/financials-quarterly`, `/analyst-recommendations`, `/enterprise-value`, and `/quote/{symbol}?session=regular&fields=all`.

### Step 2: Plug New Data

#### After Earnings
Update the model with reported actuals:

| Line Item | Prior Estimate | Actual | Delta | Notes |
|-----------|---------------|--------|-------|-------|
| Revenue | | | | |
| Gross Margin | | | | |
| Operating Expenses | | | | |
| EBITDA | | | | |
| EPS | | | | |
| [Key metric 1] | | | | |
| [Key metric 2] | | | | |

**Segment Detail** (if applicable):
- Update each segment's revenue and margin
- Note any segment mix shifts

**Balance Sheet / Cash Flow Updates**:
- Cash and debt balances
- Share count (buybacks, dilution)
- Capex actual vs. estimate
- Working capital changes

Use the structured payload as the starting point for these updates, then audit the quarter's earnings release / filing for one-offs and management adjustments.

### Step 3: Revise Forward Estimates

Based on the new data, adjust forward estimates:

| | Old FY Est | New FY Est | Change | Old Next FY | New Next FY | Change |
|---|-----------|-----------|--------|------------|------------|--------|
| Revenue | | | | | | |
| EBITDA | | | | | | |
| EPS | | | | | | |

**Key Assumption Changes:**
- What assumptions are you changing and why?
- Revenue growth rate: old → new (reason)
- Margin assumption: old → new (reason)
- Any new items (restructuring charges, one-time gains, etc.)

### Step 4: Valuation Impact

Recalculate valuation with updated estimates:

| Valuation Method | Prior | Updated | Change |
|-----------------|-------|---------|--------|
| DCF fair value | | | |
| P/E (NTM EPS × target multiple) | | | |
| EV/EBITDA (NTM EBITDA × target multiple) | | | |
| **Price Target** | | | |

Use `/api/quote/{symbol}?session=regular&fields=all` for current share price / market cap and `/enterprise-value` plus `/analyst-recommendations` for market context around the revised target.

### Step 5: Summary & Action

**Estimate Change Summary:**
- One paragraph: what changed, why, and what it means for the stock
- Is this a thesis-changing event or noise?

**Rating / Price Target:**
- Maintain or change rating?
- New price target (if changed) with methodology
- Upside/downside to current price

### Step 6: Output

- Updated Excel model (if user provides the existing model)
- Estimate change summary (markdown or Word)
- Updated price target derivation

## Important Notes

- Always reconcile your estimates to the company's reported figures before projecting forward
- Note any non-recurring items and whether your estimates are GAAP or adjusted
- Track your estimate revision history — it shows your analytical progression
- If the quarter was noisy, separate signal from noise in your estimate changes
- Check consensus after updating — how do your revised estimates compare to the Street and the API's current analyst recommendation / price-target snapshot?
- Share count matters — dilution from stock comp, converts, or buybacks can materially affect EPS
