# Financial Forensics

description: FCF gap analysis, SBC dilution, IFRS non-GAAP reconciliation. Triggers on "forensics", "FCF gap", "cash vs earnings", "IFRS adjustment", "SBC dilution".

## Workflow

### Step 1: Frame
Confirm ticker and period (default: latest 3 fiscal years). Ask: "Focus on a specific red flag?" (optional, max 1 question).

### Step 2: Gather data
Run in parallel (max 2 calls):
- `get_ticker_info(ticker=ticker)` — key financials, shares outstanding
- `run_sql(query="SELECT * FROM financials WHERE ticker = :ticker ORDER BY fiscal_year DESC LIMIT 3")` — detailed line items

Then if needed:
- `get_hkex_disclosures(ticker=ticker, type="annual_report", limit=2)` — for notes to accounts

### Step 3: Analyze
1. **FCF vs Net Income Gap**
   - Compute CFO - CAPEX vs reported net income for 3 years
   - Flag if gap > 30% persistently
   - Decompose: working capital drag? aggressive capitalization?

2. **SBC Dilution Check**
   - SBC / revenue > 5%? Flag
   - Shares outstanding YoY change > 3%? Dilution alert
   - Options outstanding / diluted shares? Overhang

3. **IFRS Non-GAAP Reconciliation**
   - HK-listed firms often report "adjusted" metrics
   - Compare reported profit to IFRS-compliant profit
   - Common adjustments: SBC, fair value gains, one-offs

4. **Red Flag Checklist**
   - [ ] Receivables growing faster than revenue
   - [ ] Inventory build with no sales growth
   - [ ] Related-party transactions > 10% of revenue
   - [ ] Off-balance-sheet entities mentioned
   - [ ] Audit qualification or emphasis of matter

### Step 4: Present
```
| Metric | FY(t-2) | FY(t-1) | FY(t) | Trend | Flag |
|--------|---------|---------|-------|-------|------|
| Net Income | ... | ... | ... | ... | ... |
| CFO | ... | ... | ... | ... | ... |
| FCF | ... | ... | ... | ... | ... |
| FCF/NI Gap | ... | ... | ... | ... | ... |
| SBC/Revenue | ... | ... | ... | ... | ... |
| Shares Outstanding | ... | ... | ... | ... | ... |
```

Add "Red Flags" callout: any checked items with severity (yellow/orange/red).
Add "IFRS vs Adjusted" table if data available.

## Important Notes
- Token: respect depth setting from style.md; summary table first, detail on request
- HK-specific: IFRS adjustments are common; related-party transactions are a key focus
- Do not fabricate line-item data; if unavailable, note "data not disclosed"
- Max 2 parallel calls per step
