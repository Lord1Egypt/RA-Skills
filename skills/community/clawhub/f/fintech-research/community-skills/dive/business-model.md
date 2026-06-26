# Business Model

description: 8-dimension business model scoring for HK-listed companies. Triggers on "business model", "how does it make money", "moat", "VIE risk", "WVR".

## Workflow

### Step 1: Frame
Confirm ticker. Ask: "Any specific competitor or time horizon for moat assessment?" (max 1 question).

### Step 2: Gather data
Run in parallel (max 2 calls):
- `get_ticker_info(ticker=ticker)` — financials, peers, business description
- `get_hkex_disclosures(ticker=ticker, type="annual_report", limit=5)` — latest AR for segment data

### Step 3: Analyze — 8 Dimensions
Score each 1-5 (1=weak, 5=strong):

| Dimension | What to Assess | HK-Specific Twist |
|-----------|---------------|-------------------|
| 1. Revenue Model | Recurring vs one-off | VIE contract structure risk |
| 2. Customer Concentration | Top 5 customer % | Related-party concentration (common in HK) |
| 3. Margin Profile | Gross, EBITDA, net margins | IFRS vs non-GAAP adjustments |
| 4. Moat / Barriers | Switching costs, network effects | Regulatory license moats (HK banking/insurance) |
| 5. Growth Optionality | New markets, products | GBA expansion, HK mainland linkage |
| 6. Capital Intensity | CAPEX/revenue, D&A | Property-heavy HK models |
| 7. Balance Sheet | Net cash, leverage | Offshore debt, USD bond exposure |
| 8. Governance Risk | Related-party transactions | WVR, VIE, HK Code compliance |

Overall score = average of 8 dimensions.

### Step 4: Present
```
| Dimension | Score (1-5) | Evidence | Risk Flag |
|-----------|-------------|----------|-----------|
| Revenue Model | ... | ... | ... |
| ... | ... | ... | ... |
| Overall | ... | ... | ... |
```

Add "HK Structure Alert" section if applicable:
- VIE structure: contract enforceability risk
- WVR: voting control misalignment
- PRC red chip: state influence assessment

## Important Notes
- Token: respect depth setting from style.md; present scorecard first, drill-down on request
- HK-specific: flag VIE/WVR/PRC red-chip structure explicitly; these are non-standard vs US GAAP
- Use disclosed segment revenue from AR; do not estimate segment splits
- Max 2 parallel calls per step
