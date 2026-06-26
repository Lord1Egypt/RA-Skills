# Themes

description: Cross-market theme discovery across HK, US, and A-share markets. Triggers on "themes", "market themes", "what's working", "cross-market themes".

## Workflow

### Step 1: Frame
Ask the user (max 1 question):
- "Which market lens? [HK-only / A+H / Global with HK tilt]"
- Or infer from tickers mentioned (e.g., 0700.HK implies HK tilt).

### Step 2: Gather data
Run in parallel (max 2 calls):
- `batch_ticker_info(tickers=["^HSI", "^HSCE", "^HSCC", "000300.SS", "SPX"])` — index level data
- `get_price_history(tickers=["^HSI", "^HSCE", "2800.HK", "000300.SS", "SPY"], period="3mo")` — momentum

Then fetch sector rotation data:
- `batch_ticker_info(tickers=sector_tickers)` for HK sector ETFs (2801.HK financials, 2802.HK utilities, 2803.HK telecom, 2806.HK property, 2810.HK commodity)

### Step 3: Analyze
Bottom-up clustering (not GICS-based):
1. Identify 3-5 themes currently rewarded by the market
2. Flag A+H cross-market linkage themes (e.g., dual-listed momentum)
3. Note Southbound Connect concentration themes
4. Rank by: price momentum (1m, 3m), volume confirmation, breadth

### Step 4: Present
```
| Theme | HK Tickers | A-Share Ticker | Momentum (1m/3m) | Breadth | Connect Flow |
|-------|-----------|----------------|------------------|---------|-------------|
| ...   | ...       | ...            | ...              | ...     | ...         |
```

Add a "Narrative" section: 2-3 sentences on what the market is pricing.
Add an "AH Linkage Watch" subsection: themes where A-share and H-share moves are diverging (>5% gap).

## Important Notes
- Token: respect depth setting from style.md; present summary table first, details on request
- HK-specific: always check Southbound Connect flow as confirming signal for HK themes
- Do not fabricate Connect data; if unavailable, note as "Connect data: N/A"
- Max 2 parallel calls per step
