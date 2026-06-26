# Alt Plays

description: Find better-priced expressions of a thesis. Triggers on "alt-plays", "alternatives", "cheaper way to play", "better value", "AH arbitrage", "spread".

## Workflow

### Step 1: Frame
Identify the thesis or anchor ticker. Examples:
- "I like AI but NVDA is expensive" → find HK-listed AI plays
- "0700.HK is too rich" → find alternative gaming/fintech names
- "AH spread on 601318" → evaluate A vs H discount

### Step 2: Gather data
Run in parallel (max 2 calls):
- `batch_ticker_info(tickers=candidates)` where candidates are theme peers
- `get_ah_spread(tickers=[dual_listed_candidates])` for A+H discount/premium

Then:
- `get_price_history(tickers=candidates, period="6mo")` for relative performance

### Step 3: Analyze
For each alternative candidate:
1. Valuation comparison: PE, PB, EV/EBITDA vs anchor
2. AH spread analysis: discount > 20% flagged as "deep discount"
3. Quality check: ROE, debt/equity, FCF yield
4. Liquidity: average daily turnover (HK$)

Scoring:
- Score = (valuation_discount * 0.4) + (quality_score * 0.35) + (liquidity_score * 0.25)
- Flag "AH arbitrage candidate" if AH discount > 15% and H-share undervalued

### Step 4: Present
```
| Ticker | Theme | PE (TTM) | AH Spread | ROE | Daily Turnover | Score | Note |
|--------|-------|----------|-----------|-----|---------------|-------|------|
| ...    | ...   | ...      | ...       | ... | ...           | ...   | ...  |
```

Add "Top Pick" and "AH Arbitrage Picks" subsections.

## Important Notes
- Token: respect depth setting from style.md; present ranked table first
- HK-specific: AH spread is the primary differentiator — always check for dual-listed names
- Do not recommend illiquid names (turnover < HK$10m/day) without warning
- Max 2 parallel calls per step
