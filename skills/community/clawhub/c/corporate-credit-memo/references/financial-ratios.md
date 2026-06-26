# Financial Ratios Reference

All ratios to be calculated for each available financial year.
Apply flag rules from SKILL.md Step 4 for every ratio.

Currency unit: match the borrower's reporting currency throughout.
All ratios expressed as stated below (x = multiple, % = percentage, days = integer).

---

## 1. LEVERAGE & SOLVENCY

| Ratio | Formula | Unit | Ideal Direction | Flag if |
|---|---|---|---|---|
| Total Debt / EBITDA | (Short-term debt + Long-term debt) / EBITDA | x | Lower | > 4.0x — flag ⚠️ |
| Net Debt / EBITDA | (Total debt - Cash) / EBITDA | x | Lower | > 3.5x — flag ⚠️ |
| Gearing Ratio | Total Debt / Total Equity | x | Lower | > 2.0x — flag ⚠️ |
| Debt-to-Assets | Total Liabilities / Total Assets | % | Lower | > 70% — flag ⚠️ |
| Equity Ratio | Total Equity / Total Assets | % | Higher | < 25% — flag ⚠️ |

**Calculation notes:**
- Total Debt = short-term borrowings + current portion of long-term debt + long-term debt
- Exclude trade payables and deferred revenue from debt
- Cash = cash and cash equivalents only (exclude restricted cash)
- If EBITDA is negative, mark all EBITDA-based ratios `[N/A — negative EBITDA]`

---

## 2. DEBT SERVICE & COVERAGE

| Ratio | Formula | Unit | Minimum | Flag if |
|---|---|---|---|---|
| Interest Coverage (ICR) | EBIT / Net Interest Expense | x | > 2.0x | < 2.0x — flag ⚠️ |
| EBITDA / Interest | EBITDA / Gross Interest Expense | x | > 3.0x | < 2.5x — flag ⚠️ |
| DSCR | EBITDA / (Interest + Scheduled Principal) | x | > 1.20x | < 1.20x — flag ⚠️ |
| Fixed Charge Cover | EBITDA / (Interest + Rent + Scheduled Principal) | x | > 1.10x | < 1.10x — flag ⚠️ |

**DSCR calculation note:**
> ⚠️ The denominator (annual debt service) must reflect the proposed repayment
> schedule under THIS facility. If the facility repayment schedule is not yet confirmed,
> use total interest expense from the most recent year as a proxy and note:
> "[DSCR denominator is indicative — confirm against final repayment schedule]"
>
> Historical DSCR (using existing debt service) and pro-forma DSCR (including this
> facility) should both be shown where data allows.

---

## 3. LIQUIDITY

| Ratio | Formula | Unit | Minimum | Flag if |
|---|---|---|---|---|
| Current Ratio | Current Assets / Current Liabilities | x | > 1.0x | < 1.0x — flag ⚠️ |
| Quick Ratio | (Current Assets - Inventory) / Current Liabilities | x | > 0.8x | < 0.7x — flag ⚠️ |
| Cash Ratio | Cash & Equivalents / Current Liabilities | x | > 0.2x | < 0.1x — flag ⚠️ |
| Net Working Capital | Current Assets - Current Liabilities | GBP/USD m | Positive | Negative — flag ⚠️ |

---

## 4. PROFITABILITY

| Ratio | Formula | Unit | Direction | Notes |
|---|---|---|---|---|
| Gross Margin | Gross Profit / Revenue | % | Higher | Compare to industry |
| EBITDA Margin | EBITDA / Revenue | % | Higher | Compare to industry |
| EBIT Margin | EBIT / Revenue | % | Higher | |
| Net Profit Margin | Net Profit / Revenue | % | Higher | |
| Return on Equity (ROE) | Net Profit / Average Total Equity | % | Higher | Use average of start/end year equity |
| Return on Assets (ROA) | Net Profit / Average Total Assets | % | Higher | |
| Return on Capital Employed (ROCE) | EBIT / (Total Assets - Current Liabilities) | % | Higher | Preferred for capital-intensive businesses |

---

## 5. OPERATIONAL EFFICIENCY

| Ratio | Formula | Unit | Direction | Notes |
|---|---|---|---|---|
| Days Sales Outstanding (DSO) | (Trade Receivables / Revenue) × 365 | Days | Lower | Rising trend = collection risk ⚠️ |
| Days Inventory Outstanding (DIO) | (Inventory / Cost of Sales) × 365 | Days | Lower | Rising trend = obsolescence risk ⚠️ |
| Days Payable Outstanding (DPO) | (Trade Payables / Cost of Sales) × 365 | Days | Higher = better for borrower | Very high DPO may signal liquidity stress |
| Cash Conversion Cycle (CCC) | DSO + DIO - DPO | Days | Lower | CCC > 90 days = elevated working capital risk |
| Asset Turnover | Revenue / Average Total Assets | x | Higher | Declining = efficiency deterioration |

---

## 6. CASH FLOW QUALITY

| Ratio | Formula | Unit | Direction | Notes |
|---|---|---|---|---|
| Cash Conversion (OCF / Net Profit) | Operating Cash Flow / Net Profit | x | Should be ≥ 0.8x | <0.5x = aggressive accruals / earnings quality risk ⚠️ |
| Capex / Revenue | Capex / Revenue | % | Context-dependent | High for capex-intensive industries |
| Capex / Depreciation | Capex / D&A | x | >1.0x = growth investment | <0.5x = underinvestment risk |
| Free Cash Flow Yield | FCF / Total Debt | % | Higher | Negative FCF — flag ⚠️ |

**FCF = Operating Cash Flow - Capex**

---

## 7. PRO-FORMA RATIOS (POST-FACILITY)

Calculate the following on a pro-forma basis assuming full drawdown of the proposed facility:

| Ratio | Formula | Basis |
|---|---|---|
| Pro-forma Net Debt / EBITDA | (Existing net debt + New facility) / LTM EBITDA | LTM EBITDA |
| Pro-forma Total Debt / EBITDA | (Existing total debt + New facility) / LTM EBITDA | LTM EBITDA |
| Pro-forma DSCR | LTM EBITDA / (Total annual debt service incl. new facility) | Proposed repayment schedule |
| Pro-forma Gearing | (Total debt post-facility) / Equity | Latest balance sheet |

Note: Pro-forma ratios assume no other changes to the balance sheet.
If proceeds are used to refinance existing debt, adjust denominator accordingly.

---

## 8. RATIO PRESENTATION FORMAT

In the credit memo, present ratios in a single summary table (Section 3.4):

| Metric | FY[N-2] | FY[N-1] | FY[N] | LTM | Pro-forma | Benchmark |
|---|---|---|---|---|---|---|
| — Leverage — | | | | | | |
| Net Debt / EBITDA | | | | | | < 3.5x |
| Total Debt / EBITDA | | | | | | < 4.0x |
| Gearing | | | | | | < 2.0x |
| Debt-to-Assets | | | | | | < 70% |
| — Coverage — | | | | | | |
| EBIT / Interest (ICR) | | | | | | > 2.0x |
| EBITDA / Interest | | | | | | > 2.5x |
| DSCR | | | | | 📋 | > 1.20x ⚠️ confirm |
| — Liquidity — | | | | | | |
| Current Ratio | | | | | | > 1.0x |
| Quick Ratio | | | | | | > 0.8x |
| — Profitability — | | | | | | |
| Gross Margin % | | | | | | Industry avg |
| EBITDA Margin % | | | | | | Industry avg |
| Net Margin % | | | | | | |
| ROE % | | | | | | |
| ROA % | | | | | | |
| — Efficiency — | | | | | | |
| DSO (days) | | | | | | |
| DIO (days) | | | | | | |
| DPO (days) | | | | | | |
| CCC (days) | | | | | | < 90 days |
| — Cash Flow — | | | | | | |
| OCF / Net Profit | | | | | | ≥ 0.8x |
| FCF (GBP/USDm) | | | | | | Positive |

Legend: ✅ = satisfactory | ⚠️ = borderline / watch | 🔴 = breach | 🔲 = data unavailable | 📋 = requires internal input
