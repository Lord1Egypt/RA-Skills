---
name: corporate-credit-memo
version: 1.0.0
description: >
  Generates institutional-grade corporate credit application memoranda (Credit Memos) in English
  from uploaded annual reports, financial statements, or user-provided financial data.
  Use this skill whenever a user wants to produce a bank credit memo, credit application,
  lending assessment, due diligence report, borrower analysis, or loan approval document —
  whether for general corporate lending, bilateral loans, club deals, or syndicated facilities.
  Also triggers for requests like "analyse this company for a loan", "write up a credit paper",
  "prepare a credit committee memo", "assess this borrower", or "draft a credit application
  for [company name]". Designed for banking professionals including credit analysts, relationship
  managers, risk officers, and CROs. Applies UK/international banking standards with awareness
  of PRA supervisory expectations.
homepage: https://github.com/henrijoe20/corporate-credit-memo
tags:
  - finance
  - banking
  - credit
  - due-diligence
  - risk
metadata:
  clawdbot:
    emoji: "🏦"
    requires:
      env: []
    files: ["references/*", "assets/*"]
# Security manifest:
# Environment variables accessed: none
# External endpoints called: web search only (read-only)
# Local files read: references/credit-memo-structure.md, references/financial-ratios.md,
#                   references/risk-framework.md, assets/disclaimer.md
# Local files written: output .docx only
# No shell execution, no API keys required
---

# Corporate Credit Memo Skill

Produces full institutional-grade Credit Application Memoranda (20–30+ pages) from uploaded
financial documents and user-provided deal parameters. Output follows the 8-section structure
used by major international banks, with all financial ratios calculated and flagged where data
is insufficient.

---

## Step 1 — Intake & Clarification

When triggered, immediately check what the user has provided. Do NOT ask multiple questions
at once. Follow this sequence:

### 1a. Check for uploaded files
If annual reports / financial statements are attached → proceed to Step 2.
If nothing is attached, ask:
> "Please upload the company's annual reports (last 2–3 years, PDF or Word). If you don't
> have them, paste the key financials and I'll work with those."

### 1b. Collect deal parameters (ask once, in a single message)
Once files are confirmed, ask the user to confirm or provide:

```
1. Borrower legal name
2. Facility type & amount (e.g. GBP 50m term loan / USD 120m revolving credit)
3. Tenor (e.g. 3 years, 5 years)
4. Purpose of loan (working capital / capex / refinancing / acquisition)
5. Security / guarantee structure (if known)
6. Repayment profile (bullet / amortising / quarterly)
7. Pricing (if known — e.g. SONIA + 250bps)
8. Lending bank / branch name
9. Any internal policy or industry classification to reference?
   (If unsure, leave blank — I will note it as [TO BE CONFIRMED])
```

Tell the user:
> "Items marked [TO BE CONFIRMED] will be flagged in the report for your team to complete —
> including RAROC, internal limits, and any policy-specific thresholds."

---

## Step 2 — Document Extraction

Read all uploaded files carefully. Extract and organise:

**From financial statements (P&L, Balance Sheet, Cash Flow):**
- 3 years of annual data + latest interim period if available
- All line items needed for ratio calculation (see `references/financial-ratios.md`)
- Auditor name and opinion type (unqualified / qualified / emphasis of matter)
- Reporting currency and any FX translation notes

**From the annual report narrative:**
- Business description, segment breakdown, revenue mix
- Key customers and suppliers (concentration risk)
- Management team and ownership structure
- Geographic footprint
- Material litigation, contingent liabilities, off-balance-sheet items
- ESG disclosures if present

**Flag clearly** any data that is:
- Missing → label `[DATA NOT AVAILABLE — please provide]`
- Restated vs prior year → note the restatement
- Unaudited → label `[UNAUDITED]`

---

## Step 3 — Research (Web Search)

Use web search to supplement document data for:
- Industry overview: market size, growth rate, cycle positioning
- Regulatory / policy environment relevant to the borrower's sector
- Competitive landscape: 2–3 named peers with approximate market share
- Recent news on the company (last 12 months): M&A, rating actions, management changes
- Macroeconomic context relevant to the jurisdiction and sector

Do NOT fabricate specific figures. If web search returns insufficient data, note:
> "[Industry data limited — recommend analyst review / Bloomberg supplement]"

---

## Step 4 — Calculate Financial Ratios

Read `references/financial-ratios.md` for all formulas and flag logic.

Calculate every ratio for each available year. Apply the following flag rules:
- ✅ Calculated successfully → show figure
- ⚠️ Calculated but at borderline threshold → show figure + note
- 🔲 Data insufficient → show `[N/A — data required]`
- 📋 Requires internal input → show `[TO BE CONFIRMED — internal policy]`

RAROC and internal capital allocation are always `[TO BE CONFIRMED]`.
DSCR denominator must match the proposed repayment schedule — confirm with user if unclear.

---

## Step 5 — Draft the Credit Memo

Read `references/credit-memo-structure.md` for the full 8-section structure and
content requirements for each section.

### Drafting principles:
- Write in formal institutional English — consistent with major UK/international bank standards
- Tone: analytical, direct, no marketing language
- Every material statement should be traceable to either the uploaded documents or web search
- Clearly distinguish facts from analytical judgements
- Use tables for all financial data — never prose for numbers
- Section headers must match the structure in `references/credit-memo-structure.md` exactly
- Flag all `[TO BE CONFIRMED]` items inline — do not omit them or leave blank
- Do not invent internal policy figures (hurdle rates, limits, RWA) — always flag these

### Risk section (Section 6):
Read `references/risk-framework.md` before drafting.
Assign a risk rating (Low / Medium / High) for each risk category with a one-line rationale.
This section reflects the analytical approach expected of a senior risk function,
consistent with PRA supervisory expectations for credit risk governance.

### Disclaimer:
Append the standard disclaimer from `assets/disclaimer.md` at the end of every report.

---

## Step 6 — Output as Word Document (.docx)

Generate the final report as a formatted .docx file using the docx skill conventions:
- Font: Arial throughout
- Colour scheme: dark navy headers (#1F4E79), mid-blue subheadings (#2E75B6)
- All financial tables: dark navy header row, alternating white/light-blue rows
- Info tables (deal terms, company details): two-column label/value format
- Risk rating boxes: colour-coded text (green=Low, amber=Medium, red=High)
- Page header: "Credit Application Memorandum | Confidential — Internal Use Only"
- Page footer: document date + page number
- Cover page: borrower name, facility type, amount, date, classification label

Present the .docx file to the user when complete.
Also offer a brief verbal summary of the key credit highlights and top 3 risks.

---

## Quality Checklist (run before presenting output)

Before finalising, verify:
- [ ] All 3 years of financials extracted and populated in tables
- [ ] Every ratio in `references/financial-ratios.md` either calculated or flagged
- [ ] No internal policy figures invented (RAROC, RWA, limits)
- [ ] Risk section has a rating for each of the 7 categories
- [ ] All [TO BE CONFIRMED] items visible and not hidden
- [ ] Disclaimer appended
- [ ] Document is .docx format, not markdown

---

## Handling Edge Cases

**Listed company:** Extract financials from uploaded annual report. Use web search for
stock performance context and peer comparison. Note exchange and ticker.

**Unlisted / private company:** Flag absence of public ratings. Rely on audited accounts.
Note that valuation of pledged equity (if any) requires independent appraisal.

**Holding company borrower / SPV:** Distinguish between holdco and opco financials.
Analyse guarantor separately. Note structural subordination risk.

**Insufficient financials (only 1 year available):** Complete what is possible.
Note that trend analysis is limited and recommend additional data before credit approval.

**Chinese-language source documents:** Extract data from tables regardless of language.
For narrative sections, translate key disclosures as needed. Note source language.

**M&A / acquisition finance:** Produce pro-forma combined financials. Separate target
and acquirer analysis. Reference `references/credit-memo-structure.md` Section 1 addendum
for transaction analysis structure.
