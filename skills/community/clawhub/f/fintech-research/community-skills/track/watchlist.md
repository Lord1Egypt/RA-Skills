# Watchlist

description: Track HK-listed tickers with Connect eligibility and AH status. Triggers on "watchlist", "track", "add ticker", "remove ticker", "my list".

## Workflow

### Step 1: Frame
Check user intent:
- "view" → show current watchlist
- "add TICKER" → add to watchlist
- "remove TICKER" → remove from watchlist
- No args → show current watchlist

### Step 2: Gather data
For view/add operations:
- `batch_ticker_info(tickers=watchlist_tickers)` — prices, changes, market cap

For HK-specific enrichment:
- `get_ah_spread(tickers=dual_listed_subset)` — AH discount/premium

### Step 3: Maintain
When adding:
1. Validate ticker format (.HK suffix or recognized HK ticker)
2. Flag Stock Connect Southbound eligibility
3. Flag if A+H dual-listed (shows AH spread column)
4. Add metadata: date added, thesis tag (optional)

When viewing:
- Sort by: user preference (default: market cap desc)
- Show columns: Ticker, Name, Last Price, Chg%, Market Cap, AH Spread, Connect Eligible

### Step 4: Present
```
| # | Ticker | Name | Price | Chg% | Market Cap | AH Spread | Connect | Added |
|---|--------|------|-------|------|------------|-----------|---------|-------|
| 1 | 0700.HK | Tencent | ... | ... | ... | N/A | Yes | 2024-01 |
| 2 | 2318.HK | Ping An | ... | ... | ... | -18% | Yes | 2024-02 |
```

Add summary: total HK$m market cap, avg AH spread (for dual-listed), count of Connect names.

## Important Notes
- Token: respect depth setting from style.md; table first, detail on request
- HK-specific: always flag Stock Connect eligibility and AH dual-list status
- Persist watchlist across sessions (if storage available); otherwise ask user to save
- Max 2 parallel calls per step
