# 🏦 Corporate Credit Memo

**Generate institutional-grade Credit Application Memoranda from annual reports — in minutes.**

Built by a bank CRO with PRA Senior Management Function (SMF4) certification.
Designed for credit analysts, relationship managers, risk officers, and CROs at banks
and financial institutions.

---

## What it does

Upload a company's annual report (PDF or Word) and provide basic deal parameters.
The skill produces a full **20–30 page Credit Application Memorandum** in English,
formatted as a `.docx` file ready for credit committee review.

The output follows the 8-section structure used by major international banks:

| Section | Content |
|---|---|
| 1. Request & Background | Facility overview, relationship summary, industry policy compliance |
| 2. Borrower Overview | Company profile, ownership, management, business segments, competitive position |
| 3. Financial Analysis | 3-year P&L / B/S / Cash Flow tables + 28 financial ratios, all calculated |
| 4. Industry & Macro | Market dynamics, regulatory environment, cycle positioning |
| 5. Facility Structure | Sources & uses, term sheet summary, security structure, covenants |
| 6. Risk Analysis | 7-category risk assessment (Credit, Market, Operational, Legal, Collateral, Group, ESG) |
| 7. Post-Lending Monitoring | Reporting covenants, early warning indicators, account monitoring |
| 8. Recommendation | Summary assessment, approval recommendation, conditions precedent |

Plus appendices: financial projections, stress testing, DD checklist.

---

## What you need to provide

**Required:**
- Annual report(s) — PDF or Word, last 2–3 years
- Facility type and amount (e.g. GBP 50m term loan)
- Loan tenor and purpose
- Repayment structure

**Optional (skill will flag as [TO BE CONFIRMED] if not provided):**
- Security / guarantee details
- Pricing (e.g. SONIA + 250bps)
- Internal policy thresholds
- Lending bank / branch name

---

## What it will never fabricate

The skill is designed with strict discipline on items that require internal bank input:

- ❌ **RAROC** — always marked `[TO BE CONFIRMED — internal model]`
- ❌ **Risk-Weighted Assets (RWA)** — always marked `[TO BE CONFIRMED]`
- ❌ **Internal credit policy thresholds** — flagged if not provided
- ❌ **PD / LGD parameters** — always flagged for credit risk team
- ❌ **Internal credit ratings** — never assigned without user input

All `[TO BE CONFIRMED]` items are visible inline in the document — nothing is hidden or omitted.

---

## Financial ratios calculated (28 total)

**Leverage & Solvency:** Net Debt/EBITDA, Total Debt/EBITDA, Gearing, Debt-to-Assets, Equity Ratio

**Coverage:** ICR (EBIT/Interest), EBITDA/Interest, DSCR, Fixed Charge Cover

**Liquidity:** Current Ratio, Quick Ratio, Cash Ratio, Net Working Capital

**Profitability:** Gross Margin, EBITDA Margin, EBIT Margin, Net Margin, ROE, ROA, ROCE

**Efficiency:** DSO, DIO, DPO, Cash Conversion Cycle, Asset Turnover

**Cash Flow Quality:** OCF/Net Profit, Capex/Revenue, Capex/Depreciation, FCF Yield

**Pro-forma:** Net Debt/EBITDA post-facility, DSCR post-facility

All ratios include flag logic: ✅ healthy / ⚠️ borderline / 🔴 breach / 🔲 data unavailable.

---

## Handles these borrower types

- ✅ Listed companies (A-share, H-share, LSE, NYSE)
- ✅ Unlisted / private companies
- ✅ Holding companies and SPV borrowers
- ✅ Chinese-language source documents (data extracted regardless of language)
- ✅ M&A / acquisition finance (with transaction analysis section)
- ✅ Single year of accounts available (with appropriate caveats)

---

## Output format

- `.docx` Word document, formatted for credit committee presentation
- Navy/blue colour scheme with professional table formatting
- Cover page with deal summary box
- Page headers and footers
- Standard disclaimer appended to every report

---

## Disclaimer

Every report includes a hardcoded disclaimer clarifying:
- This is an internal credit review tool, not a regulatory opinion
- RAROC and internal capital figures must be completed by the bank's risk team
- SMF holders remain personally responsible for all regulated decisions
- Data accuracy depends on uploaded source documents

---

## Skill structure

```
corporate-credit-memo/
├── SKILL.md                          ← Main skill (triggers + workflow)
├── README.md                         ← This file
├── references/
│   ├── credit-memo-structure.md     ← Full 8-section report structure
│   ├── financial-ratios.md          ← 28 ratio formulas + flag logic
│   └── risk-framework.md            ← 7-category risk assessment framework
└── assets/
    └── disclaimer.md                ← Standard disclaimer (appended to all reports)
```

---

## Install

```bash
clawhub install corporate-credit-memo
```

Or search "credit memo" on [clawhub.ai](https://clawhub.ai).

---

## Feedback & improvements

Issues and suggestions welcome via GitHub Issues.
If you use this in production and have improvements to the structure or ratio logic,
pull requests are appreciated.

---

*Built with institutional banking standards in mind. Not a substitute for professional
credit judgement or regulatory compliance review.*
