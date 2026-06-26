# Reporting Quality

description: IFRS metric drift, accounting policy changes, ESG disclosure quality. Triggers on "reporting quality", "accounting", "IFRS drift", "ESG disclosure", "metric change".

## Workflow

### Step 1: Frame
Confirm ticker. Ask: "Focus on accounting quality, ESG disclosure, or both?" (max 1 question).

### Step 2: Gather data
Run in parallel (max 2 calls):
- `get_hkex_disclosures(ticker=ticker, type="annual_report", limit=3)` — for accounting policy notes
- `get_ticker_info(ticker=ticker)` — for financial trend data

Then:
- `get_hkex_disclosures(ticker=ticker, type="ESG_report", limit=3)` — ESG disclosures

### Step 3: Analyze
1. **Metric Drift Check**
   - Has the company changed KPI definitions year-to-year?
   - Are "adjusted" metrics becoming more favorable vs IFRS?
   - Segment reporting: has segment definition changed?

2. **IFRS Policy Changes**
   - New IFRS standards adopted (HKFRS 9, 15, 16 impacts)
   - Revenue recognition policy changes
   - Lease capitalization impact post-HKFRS 16

3. **ESG Disclosure Quality**
   - GRI / TCFD / HKEX ESG Guide compliance
   - Quantitative targets vs qualitative narrative
   - Board diversity disclosure
   - Climate risk assessment

4. **Scoring Matrix**
   - Transparency (1-5): consistency, comparability
   - Governance (1-5): board independence, audit committee
   - ESG Maturity (1-5): targets, metrics, third-party assurance

### Step 4: Present
```
| Check | FY(t-2) | FY(t-1) | FY(t) | Drift? | Severity |
|-------|---------|---------|-------|--------|----------|
| KPI definition | ... | ... | ... | ... | ... |
| Adj vs IFRS gap | ... | ... | ... | ... | ... |
| Segment changes | ... | ... | ... | ... | ... |
| IFRS adoption | ... | ... | ... | ... | ... |
```

Add "ESG Disclosure Score" section:
```
| Dimension | Score (1-5) | Evidence |
|-----------|-------------|----------|
| Transparency | ... | ... |
| Governance | ... | ... |
| ESG Maturity | ... | ... |
```

## Important Notes
- Token: respect depth setting from style.md; drift table first, detail on request
- HK-specific: HKEX ESG Reporting Guide compliance is mandatory for main board since 2016
- Flag any un-explained metric change as yellow flag
- Do not speculate on accounting quality without disclosure evidence
- Max 2 parallel calls per step
