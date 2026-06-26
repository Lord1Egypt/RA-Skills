---
name: Financial Ratio Analysis
slug: financial-ratios
version: 1.0.0
description: >
  Compute and report 25+ financial ratios (profitability, liquidity, leverage,
  efficiency, growth) from QBO data. Produces a 9-tab Excel workbook with
  traffic-light scoring, DuPont decomposition, Altman Z-Score, 6-month trend
  charts, trend-reversal detection, and CDC logging. Integrates with
  the Month-End Close pipeline.
tags:
  - finance
  - accounting
  - ratios
  - qbo
  - excel
negative_boundaries:
  - Bank reconciliation → use bank-reconciliation skill
  - P&L line-item variance analysis → use pl-deep-analysis skill
  - Cash flow forecasting → use cash-flow-forecast skill
  - AR collections aging → use ar-collections skill
  - Budget vs. actual → use budget-vs-actual skill
---

# Financial Ratio Analysis — SKILL.md

---

## When to Use This Skill

Use when a user asks for:
- Financial ratio analysis for a QBO-connected client
- Profitability, liquidity, leverage, or efficiency metrics
- DuPont decomposition or Altman Z-Score analysis
- Month-over-month, QoQ, or YoY ratio comparison
- Ratio benchmarking against industry averages
- Trend analysis across 6 months of ratios
- Trend reversal detection for any financial ratio
- CDC (change data capture) on ratio movements

**NOT for:**
- Bank reconciliation → use `bank-reconciliation`
- P&L variance analysis (line-item drill-down) → use `pl-deep-analysis`
- Cash flow forecasting → use `cash-flow-forecast`
- AR collections aging → use `ar-collections`
- Budget vs. actual → use `budget-vs-actual`

---

## Quick Invocation

```bash
# Standard monthly ratio report
python3 scripts/pipelines/financial-ratios.py --slug sb-paulson --month 2026-03

# Custom output directory
python3 scripts/pipelines/financial-ratios.py --slug <client-slug> --month 2026-03 --out ~/Desktop/reports

# QBO sandbox
python3 scripts/pipelines/financial-ratios.py --slug sb-paulson --month 2026-03 --sandbox
```

Unknown slugs use default thresholds and disable inventory/valuation ratios unless SOP file found.

---

## What It Produces

**Excel workbook** saved to `~/Desktop` (or `--out` path):
`FinancialRatios_{slug}_{YYYY_MM}.xlsx`

| Tab | Contents |
|-----|----------|
| Ratio Summary | All ratios with traffic lights, benchmarks, DuPont & Altman summary |
| Profitability | Gross/Operating/Net margins, ROA, ROE, EBITDA margin + 6-mo trend |
| Liquidity | Current/Quick/Cash ratios, Working capital + 6-mo trend |
| Leverage | D/E, D/A, Interest coverage, Equity multiplier + 6-mo trend |
| Efficiency | Asset/Inventory/Receivable/Payable turnover, DSO, DPO, CCC + 6-mo trend |
| Growth | Revenue (MoM/QoQ/YoY), Expense, Net income growth + 6-mo trend |
| DuPont Analysis | 3-factor + 5-factor ROE decomposition, 6-month component trend |
| Trends | All ratios × 6 months with direction arrows + trend reversal flags |
| CDC Log | Ratio changes vs. prior run with trend reversal detection |

---

## Ratio Categories

### Profitability
| Ratio | Formula |
|-------|---------|
| Gross Margin % | Gross Profit / Revenue × 100 |
| Operating Margin % | EBIT / Revenue × 100 |
| Net Margin % | Net Income / Revenue × 100 |
| EBITDA Margin % | EBITDA / Revenue × 100 |
| ROA | Net Income / Total Assets × 100 |
| ROE | Net Income / Total Equity × 100 |

### Liquidity
| Ratio | Formula |
|-------|---------|
| Current Ratio | Current Assets / Current Liabilities |
| Quick Ratio | (Current Assets − Inventory) / Current Liabilities |
| Cash Ratio | Cash / Current Liabilities |
| Working Capital | Current Assets − Current Liabilities |
| Working Capital Ratio | Working Capital / Total Assets × 100 |

### Leverage
| Ratio | Formula |
|-------|---------|
| Debt-to-Equity | Total Liabilities / Total Equity |
| Debt-to-Assets | Total Liabilities / Total Assets |
| Interest Coverage | EBIT / Interest Expense |
| Equity Multiplier | Total Assets / Total Equity |

### Efficiency
| Ratio | Formula |
|-------|---------|
| Asset Turnover | Revenue / Total Assets |
| Inventory Turnover | COGS / Inventory (annualized) |
| Receivable Turnover | Revenue / Accounts Receivable |
| DSO (Days Sales Outstanding) | AR / (Revenue / Days) |
| Payable Turnover | COGS / Accounts Payable |
| DPO (Days Payable Outstanding) | AP / (COGS / Days) |
| Cash Conversion Cycle | DSO + DIO − DPO |

### Growth
| Ratio | Formula |
|-------|---------|
| Revenue Growth MoM | (Current − Prior) / |Prior| × 100 |
| Revenue Growth QoQ | (Current − 3mo ago) / |3mo ago| × 100 |
| Revenue Growth YoY | (Current − 12mo ago) / |12mo ago| × 100 |
| Expense Growth | (Current Opex − Prior Opex) / |Prior Opex| × 100 |
| Net Income Growth | (Current NI − Prior NI) / |Prior NI| × 100 |

### Valuation (SOP-gated)
| Ratio | Formula |
|-------|---------|
| Revenue Multiple | Enterprise Value / (Revenue × 12) |
| EBITDA Multiple | Enterprise Value / (EBITDA × 12) |

---

## DuPont Analysis

### Three-Factor Model
```
ROE = Net Margin × Asset Turnover × Equity Multiplier
```

### Five-Factor Model
```
ROE = Tax Burden × Interest Burden × EBIT Margin × Asset Turnover × Equity Multiplier
```

Both models computed; trend shown for each component across 6 months.

---

## Altman Z-Score

Bankruptcy risk indicator. Model selected automatically by `entity_type` in SOP config:

| Model | Used For | Zones |
|-------|----------|-------|
| Z' (Revised) | Private/Services (default) | Safe >2.9 \| Grey 1.23-2.9 \| Distress <1.23 |
| Z (Original) | Manufacturing | Safe >2.99 \| Grey 1.81-2.99 \| Distress <1.81 |

**Formula (Z' model):**
`Z' = 0.717×(WC/TA) + 0.847×(RE/TA) + 3.107×(EBIT/TA) + 0.420×(BVE/TL) + 0.998×(Revenue/TA)`

---

## Traffic Light Scoring

Each ratio scores GREEN / YELLOW / RED based on thresholds configured per client SOP.
- GREEN: Within healthy range
- YELLOW: Watch — approaching threshold
- RED: Action required

Thresholds are configured in `CLIENT_CONFIGS` within the script. Override by editing the dict or adding a client SOP file.

---

## Trend Reversal Detection

The pipeline detects when a ratio **reverses direction** over the 6-month window:
- Compares direction of first half vs. second half of history
- Flags `⚡ Trend Reversal — Now Improving` or `⚠ Trend Reversal — Now Declining`
- Flagged prominently in Trends tab and CDC Log

---

## Client SOP Integration

Place a `sop.md` file at `clients/{slug}/sop.md`. The pipeline reads it to detect:

| SOP Signal | Effect |
|-----------|--------|
| "POS collection" / "no accounts receivable" | Disables AR ratios (DSO, receivable turnover) |
| "no inventory" / "service-based" | Disables inventory ratios |
| "manufacturing" / "distribution" | Switches to original Altman Z model |
| `enterprise value: $X` | Enables valuation ratios (revenue/EBITDA multiples) |
| `benchmark: {key} {value}` | Overrides specific benchmark values |

---

## Client Configuration

Add clients to `CLIENT_CONFIGS` in the script with:
- `ratios_enabled` list (which ratios to compute/display)
- `thresholds` dict per ratio: `{"green": (min, max), "yellow": (min, max)}`
- `benchmarks` dict per ratio: Decimal values
- `entity_type`: `"services"` or `"manufacturing"` (for Altman Z model)

---

## QBO Data Pulled

| Report | Purpose |
|--------|---------|
| P&L (current month) | Revenue, COGS, OpEx, Net Income, Interest, D&A |
| Balance Sheet (current month-end) | Assets, Liabilities, Equity, Cash, AR, Inventory, AP |
| Cash Flow (current month) | Operating/Investing/Financing cash flows |
| P&L (prior month) | MoM growth ratios |
| P&L (3 months ago) | QoQ growth ratio |
| P&L (12 months ago) | YoY growth ratio |
| All of the above × 6 months | Historical trend analysis |

**Total QBO calls:** ~17 per run (6-month history + current + prior + QoQ + YoY)

---

## CDC Cache

Cache stored at: `.cache/financial-ratios/{slug}.json`

Tracks:
- All ratio values from prior run
- Detects per-ratio changes (delta + % change)
- Flags trend reversals when 6-month history available
- Compares run-over-run for drift monitoring

---

## Technical Notes

- All financial math: **Python Decimal** (no floating-point errors)
- Division-by-zero: returns `ZERO`, never crashes
- Missing QBO lines: `ZERO` (safe fallback), does not inflate ratios
- Inventory turnover: annualized (× 12 for monthly periods)
- Interest coverage = 999.99 when no interest expense (signals no debt burden)
- Altman Z-Score uses **book value of equity** (not market cap) for private company model
- EBITDA = EBIT + D&A; EBIT = Net Income + Interest + Taxes
- Operating margin uses EBIT as proxy for operating income if QBO doesn't separate it

---

## Files

| File | Description |
|------|-------------|
| `scripts/pipelines/financial-ratios.py` | Main pipeline script |
| `skills/financial-ratios/SKILL.md` | This file |
| `.cache/financial-ratios/{slug}.json` | CDC cache per client |

---

