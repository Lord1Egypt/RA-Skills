# Supply Chain

description: Map upstream/downstream from a ticker or theme. Triggers on "supply chain", "upstream", "downstream", "mapping", "value chain".

## Workflow

### Step 1: Frame
Confirm the anchor ticker or theme. Examples:
- "0700.HK" → map Tencent ecosystem
- "EV battery" → map HK-listed names in the chain
- "AI chips" → map upstream semiconductor + downstream cloud

### Step 2: Gather data
Run in parallel (max 2 calls):
- `get_ticker_info(ticker=anchor_ticker)` — business description, peers, sector
- `get_hkex_disclosures(ticker=anchor_ticker, type="announcements", limit=20)` — recent filings for supplier/customer mentions

Then peer mapping:
- `batch_ticker_info(tickers=peer_tickers)` — where peer_tickers derived from info response

### Step 3: Analyze
1. Build chain: Raw Materials → Components → Assembly → Distribution → End User
2. For each node, list HK-listed names (if any) with market cap
3. Identify bottlenecks: single-source suppliers, China-dependent nodes
4. Flag HK-specific risks: VIE structure exposure, WVR governance, US sanctions

### Step 4: Present
```
| Chain Node | HK Tickers | A-Share Tickers | TTM Rev (HK$m) | Margin | Risk Flag |
|------------|-----------|-----------------|----------------|--------|-----------|
| Raw Materials | ... | ... | ... | ... | ... |
| Components    | ... | ... | ... | ... | ... |
| Assembly      | ... | ... | ... | ... | ... |
| Distribution  | ... | ... | ... | ... | ... |
| End User      | ... | ... | ... | ... | ... |
```

Add "Key Dependencies" callout: 2-3 critical linkages.
Add "HK Listed Exposure" summary: total market cap and average valuation.

## Important Notes
- Token: respect depth setting from style.md; show chain diagram first
- HK-specific: prioritize HK-listed names in each node; note Stock Connect eligibility
- Use disclosed customer/supplier data from filings only; mark inferred relationships with [inferred]
- Max 2 parallel calls per step
