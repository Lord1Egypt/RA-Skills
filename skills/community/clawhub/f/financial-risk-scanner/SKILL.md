---
name: financial-risk-scanner
description: Scan and analyze potential financial fraud risks in listed company financial statements. Use when users ask to analyze a company's financial health, detect accounting anomalies, or identify red flags in financial reports. Supports 21 risk indicators including cash-debt paradox, receivables anomalies, inventory issues, cash flow-profit divergence, audit concerns, and governance risks. Input: single company stock code (e.g., 000001.SZ). Output: comprehensive risk report with severity ratings and cross-validation recommendations.
metadata:
  openclaw:
    emoji: "🔍"
  homepage: "https://clawhub.ai/skills/financial-risk-scanner"
  author: "laigen"
  license: "MIT"
env:
  TUSHARE_TOKEN:
    required: true
    description: "Tushare Pro API Token for Chinese A-share market data. Required to fetch financial statements, balance sheets, and market data. Register at: https://tushare.pro/register"
    sensitive: true
    scope: financial-data
dependencies:
  - python: ">=3.8"
  - packages: "tushare>=1.2.0, pandas>=1.3.0"
---

# Financial Risk Scanner

Scan listed company financial statements for potential fraud signals and accounting anomalies using Tushare data APIs.

## Quick Start

```bash
python3 scripts/analyze_company.py <ts_code>
```

Example:
```bash
python3 scripts/analyze_company.py 000001.SZ
```

## Workflow

1. **Fetch Financial Data**: Retrieve 10+ years of annual financial statements (balance sheet, income statement, cash flow statement) via Tushare
2. **Calculate Risk Metrics**: Compute 21 risk indicators with historical trend analysis
3. **Cross-validate**: Check company announcements for supporting evidence when anomalies detected
4. **Generate Report**: Produce structured risk assessment with severity ratings and recommendations

## Risk Indicators

| Category | Indicator | Detection Criteria |
|----------|-----------|-------------------|
| **Asset Reality** | Cash-Debt Paradox | Cash > 15% assets + Interest-bearing debt > 30% assets |
| | Receivables Anomaly | Receivables growth >> Revenue growth |
| | Inventory Anomaly | Inventory growth >> COGS growth |
| | Prepayments Surge | Prepayments > 5% assets without business rationale |
| | Other Receivables High | Other receivables > 5% net assets |
| | Construction Suspended | Construction long uncompleted or excessive |
| **Profit Quality** | Cash-Profit Divergence | High profit + Negative operating cash flow (3+ years) |
| | Gross Margin Anomaly | GM far above peers or rising persistently |
| | Sales Expense Anomaly | Sales expense ratio far below peers |
| | Abnormal Non-recurring | Non-recurring items > 30% of profit |
| | Asset Impairment Bath | One-time large impairment charges |
| **Related Party** | Related Transaction High | Related purchase/sales > 30% |
| | Related Fund Flows | Related party in other receivables/payables high |
| | Related Guarantees | External guarantees > 50% net assets |
| **Capital Structure** | Goodwill High | Goodwill > 30% net assets |
| | Debt Ratio High | Debt ratio > 70% and rising |
| | Short-term Liquidity | Short-term debt / Cash > 3x |
| | Dual Debt High | Long + Short debt high with cash strain |
| **Audit & Governance** | Auditor Changes | Consecutive auditor changes |
| | Non-standard Opinion | Audit opinion with emphasis or reservation |
| | Executive Departures | CFO/Board secretary frequent changes |

## Key Metrics Formulas

```
Cash-Debt Paradox Ratio = (Cash / Total Assets) × (Interest Debt / Total Assets)
Cash-Profit Ratio = Operating Cash Flow / Net Profit (threshold: < 0.5 for 3+ years)
Receivables Growth Ratio = Receivables Growth Rate / Revenue Growth Rate
Inventory Turnover Ratio = COGS / Average Inventory
Gross Margin = (Revenue - COGS) / Revenue
Debt Ratio = Total Liabilities / Total Assets
Liquidity Pressure = Short-term Borrowing / Cash Balance
```

## References

For detailed detection logic and thresholds, see [references/risk_indicators.md](references/risk_indicators.md).

## Cross-Validation Sources

When anomalies are detected, cross-validate with:
- Company announcements (via Tushare announcement API)
- Audit reports in annual reports
- Regulatory filings and enforcement notices
- News and media coverage

## Output Format

Reports are saved to `~/.openclaw/workspace/memory/financial-risk/<company_name>_<date>.md`

Report sections:
1. **Company Overview**: Basic info, industry, listing date
2. **Risk Summary**: Total risks, severity distribution, top concerns
3. **Detailed Analysis**: Each indicator with historical trend charts
4. **Cross-validation**: Supporting evidence from announcements
5. **Recommendations**: Priority actions and monitoring points

## Severity Levels

| Level | Symbol | Criteria |
|-------|--------|----------|
| **Critical** | 🔴 | Multiple indicators triggered, strong fraud signals |
| **High** | 🟠 | Single strong indicator or 3+ moderate signals |
| **Moderate** | 🟡 | Anomaly detected but needs verification |
| **Low** | 🟢 | Minor concern, monitor periodically |

## Environment Variables

| Variable | Required | Description |
|----------|:--------:|-------------|
| `TUSHARE_TOKEN` | ✅ Yes | Tushare Pro API Token for Chinese A-share market data |

**How to obtain TUSHARE_TOKEN:**
1. Register at https://tushare.pro/register
2. Get your token from the user center
3. Set environment variable:
   ```bash
   export TUSHARE_TOKEN="your_token_here"
   ```

## Python Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `tushare` | >=1.2.0 | A-share market data API |
| `pandas` | >=1.3.0 | Data manipulation and analysis |

Install dependencies:
```bash
pip install tushare pandas
```

## Notes

- Annual data preferred for stability; quarterly available for recent trends
- Industry comparison essential for margin and expense analysis
- Historical context matters: 10+ years for trend significance

## Limitations

| Limitation | Description |
|------------|-------------|
| **API Token Required** | Requires a Tushare Pro API token to fetch data |
| **Market Scope** | Only supports Chinese A-share market listed companies |
| **Historical Data** | Limited to last 10 years of financial data |
| **Related Party Data** | Transaction data with related parties requires manual verification from annual report notes |
| **Industry Comparison** | Some industry metrics may not have sufficient peer data for comparison |

## Data Sources

| Source | Type | Description |
|--------|------|-------------|
| **Tushare Pro API** | Primary | Chinese A-share financial data, market data, and announcements |

## Provenance

| Field | Value |
|-------|-------|
| **Author** | laigen |
| **License** | MIT |
| **Homepage** | https://clawhub.ai/skills/financial-risk-scanner |
| **Registry** | ClawHub |