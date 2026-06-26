# Management

description: Capital allocation, WVR governance, HK Corporate Governance Code compliance. Triggers on "management", "CEO", "capital allocation", "governance", "WVR", "board".

## Workflow

### Step 1: Frame
Confirm ticker. Ask: "Focus on capital allocation, governance structure, or both?" (max 1 question).

### Step 2: Gather data
Run in parallel (max 2 calls):
- `get_ticker_info(ticker=ticker)` — management info, board composition
- `get_hkex_disclosures(ticker=ticker, type="annual_report", limit=2)` — CG report, remuneration policy

Then:
- `get_hkex_disclosures(ticker=ticker, type="announcements", limit=10)` — recent board changes, transactions

### Step 3: Analyze
1. **Capital Allocation Scorecard**
   | Use of Cash | Score (1-5) | Evidence |
   |-------------|-------------|----------|
   | Dividends | ... | payout ratio, consistency |
   | Buybacks | ... | historical track record |
   | M&A | ... | ROIC of deals |
   | CAPEX | ... | growth vs maintenance |
   | Debt paydown | ... | leverage trend |

2. **Governance Assessment**
   - Board independence: INED ratio (HK code: minimum 1/3)
   - Chair/CEO separation (HK code: should be separate)
   - WVR structure: voting power disparity, sunset clause
   - Related-party transaction controls
   - Audit committee independence

3. **HK Corporate Governance Code Compliance**
   - Compliance level: C (comply) or E (explain)
   - Check key provisions:
     - A.2.1: Chair/CEO separation
     - A.4.1: INED term limits
     - A.5.1: remuneration committee
     - D.3.1: risk management committee

4. **Management Track Record**
   - CEO tenure and prior performance
   - Key person risk (founder-dependent?)
   - Succession planning disclosed?

### Step 4: Present
```
| Dimension | Score (1-5) | Evidence | HK Code Ref |
|-----------|-------------|----------|-------------|
| Capital Allocation | ... | ... | ... |
| Board Independence | ... | ... | A.4.1 |
| Chair/CEO Split | ... | ... | A.2.1 |
| WVR Risk | ... | ... | ... |
| Related-Party Controls | ... | ... | ... |
| Succession Planning | ... | ... | ... |
```

Add "Red Flag" section: any governance gaps with severity.

## Important Notes
- Token: respect depth setting from style.md; scorecard first, detail on request
- HK-specific: WVR and VIE structures are governance-critical; always assess
- HK Code compliance: note "comply or explain" deviations
- Do not assess management quality without disclosed evidence
- Max 2 parallel calls per step
