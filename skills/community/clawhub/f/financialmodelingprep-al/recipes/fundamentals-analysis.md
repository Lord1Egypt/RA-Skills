# Recipe: Fundamentals Analysis

## Goal
Produce a multi-year fundamentals analysis (revenue, profitability, margins, returns, leverage) with every figure cited to its period and filing — grounded only in FMP data.

## When to use
The user asks "analyze <company>'s fundamentals", "how have its margins/revenue trended", "is it growing", or wants statement-driven analysis.

## Inputs
- Company name or ticker.
- Number of years/quarters (default: 3–5 annual periods).
- `FMP_API_KEY` in the environment.

## Steps
1. **Resolve & confirm** the symbol (search → profile). Note `reportedCurrency`.
2. **Pull income statement:** `/income-statement?symbol=<TICKER>&period=annual&limit=5`. Read `revenue`, `grossProfit`, `operatingIncome`, `netIncome`, `eps`, plus `date`, `period`, `filingDate`, `reportedCurrency` per row.
3. **Pull ratios:** `/ratios?symbol=<TICKER>&period=annual&limit=5` for `grossProfitMargin`, `netProfitMargin`, `returnOnEquity`, `debtEquityRatio`, `currentRatio`. **Prefer these over hand-computing.**
4. **(Optional) cash flow / balance sheet** for `freeCashFlow`, `totalDebt`, `cashAndCashEquivalents` if leverage/cash matter.
5. **Trend, don't fabricate:** describe the direction across the cited periods. If you compute a growth rate, show the two cited endpoints and label it "derived".
6. **Match periods:** keep all figures annual (or all quarterly). Never mix without labels. If TTM is requested, build it from the last 4 quarters and label it.

## Output
A period-by-period table or list, each figure with currency and period, followed by a short grounded narrative (e.g. "revenue rose from FY2021 to FY2024; net margin expanded from X% to Y%"), then source + disclaimer.

## Example
> **MSFT — annual income statement (USD; FMP `/income-statement`)**
> | Period | Revenue | Net income | Net margin | filingDate |
> |--------|---------|-----------|-----------|-----------|
> | FY2022 | 198.3B | 72.7B | 36.7% | 2022-07-28 |
> | FY2023 | 211.9B | 72.4B | 34.1% | 2023-07-27 |
> | FY2024 | 245.1B | 88.1B | 35.9% | 2024-07-30 |
>
> Margins from FMP `/ratios` (annual). Revenue grew across FY2022→FY2024 (derived from cited revenue figures). Data as-of latest filings; newer periods may exist. *Informational only, not investment advice.*

(Illustrative format only — report live API values.)

## Edge cases
- **Restated/missing periods** → some rows may be `null`; mark "not reported".
- **Fiscal year ≠ calendar year** → cite `period`/`fiscalYear` exactly; don't relabel.
- **Currency** → if non-USD, keep `reportedCurrency`; don't convert silently.
- **Limit exceeds plan history** → fewer rows returned; report what you got.

## Production notes
- 2–3 calls (income + ratios, optionally cash flow). Cache statements in-session.
- Prefer the API's `/ratios` margins over recomputing to avoid arithmetic disputes; if you do recompute, show inputs.
- Keep the analysis descriptive, not prescriptive — no buy/sell language.
