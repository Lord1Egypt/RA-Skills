# Event Radar

description: HKEX announcement monitor, Connect adjustments, index review, short ratio alerts. Triggers on "event radar", "events", "what's coming", "announcements", "short ratio", "connect adjustment".

## Workflow

### Step 1: Frame
Confirm scope:
- Single ticker radar → focus on that ticker
- Portfolio radar → scan all watchlist tickers
- Market radar → broad HK market events

### Step 2: Gather data
Run in parallel (max 2 calls):
- `get_hkex_disclosures(ticker=ticker_or_index, type="announcements", limit=15)` — recent filings
- `get_news_signals(ticker=ticker_or_index, limit=15)` — news and events

Then:
- `get_hkex_disclosures(ticker=ticker_or_index, type="index_review", limit=5)` — index constituent changes

### Step 3: Classify events
| Category | Event Types | Impact |
|----------|-------------|--------|
| Corporate | Earnings, profit warning, dividend | High |
| Governance | Board change, WVR change, related-party | High |
| Connect | Add/remove from Stock Connect list | Medium-High |
| Index | FTSE/MSCI/Hang Seng review | Medium |
| Regulatory | SFC enforcement, HKEX query | High |
| Short | SFC short position disclosure threshold | Medium |

Short ratio alert:
- SFC mandated disclosure: >0.02% of issued shares short
- Flag if any watchlist name has short ratio >5% (high bearish signal)
- Flag if short ratio increased >2% in past week

### Step 4: Present
```
| Date | Ticker | Event | Category | Impact | Action Required |
|------|--------|-------|----------|--------|-----------------|
| ... | ... | ... | ... | ... | ... |
```

Add "Upcoming Catalysts" section:
```
| Date | Event | Ticker(s) | Impact |
|------|-------|-----------|--------|
| ... | Earnings | ... | High |
| ... | Index review | ... | Medium |
```

Add "Short Alert" subsection if any watchlist name has elevated short interest.

## Important Notes
- Token: respect depth setting from style.md; upcoming events first, past events on request
- HK-specific: SFC short position disclosures are weekly; Connect adjustments are monthly
- Only flag events with disclosed dates; do not speculate on unannounced events
- Max 2 parallel calls per step
