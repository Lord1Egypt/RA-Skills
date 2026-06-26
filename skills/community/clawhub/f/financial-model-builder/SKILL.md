---
name: financial-model-builder
description: Build revenue models, pricing tools, and forecasting spreadsheets with assumptions, scenarios, and projections. Use when creating financial forecasts, unit economics models, pricing calculators, LBO models, DCF analyses, or any structured financial model as Excel or structured data.
license: MIT
metadata:
  version: "2.0.0"
  domain: finance
  triggers: financial model, revenue model, forecast, DCF, LBO, unit economics, pricing model, sensitivity analysis, scenario analysis, cash flow projection, P&L, IRR, NPV, valuation, SaaS metrics, ARR, MRR, WACC, cohort analysis, LTV/CAC, leveraged buyout, tornado chart, terminal value, MOIC
  role: builder
  scope: implementation
  output-format: xlsx
  related-skills: excel-builder, data-analysis-report, tax-return-preparer
---

# Financial Model Builder

Builds structured financial models including revenue forecasts, pricing tools, DCF valuations, LBO models, scenario analyses, and SaaS cohort metrics.

## When to Use This Skill

- Building 3-statement models (P&L, Balance Sheet, Cash Flow)
- Creating SaaS revenue models (MRR, ARR, churn, LTV/CAC)
- DCF (Discounted Cash Flow) valuation analysis with WACC
- Unit economics and pricing sensitivity analysis
- LBO (Leveraged Buyout) models for investment banking
- Budget vs. actuals tracking spreadsheets
- Break-even analysis and contribution margin models
- Cohort analysis and revenue forecasting

## Core Workflow

1. **Define scope** — Identify model type, time horizon (monthly/quarterly/annual), and key drivers
2. **Build assumptions tab** — All inputs in one clearly labeled sheet; color-code inputs (blue) vs. formulas (black)
3. **Build calculation layers** — Revenue model → cost model → P&L → cash flow → balance sheet
4. **Add scenarios** — Base / bull / bear cases with a scenario toggle (data validation dropdown)
5. **Sensitivity tables** — Two-variable data tables for key metrics (e.g., price × volume → revenue)
6. **Dashboard** — Summary sheet with KPIs, charts, and scenario outputs
7. **Validate** — Balance sheet must balance; cash flow must reconcile; check for circular refs

## Standard Model Structure (Excel Tabs)

| Tab | Contents |
|-----|----------|
| `Assumptions` | All input variables with labels, units, and sources |
| `Revenue` | Revenue build-up by segment/product/channel |
| `OpEx` | COGS, gross margin, operating expenses |
| `P&L` | Income statement (3-5 years monthly or annual) |
| `Cash Flow` | Operating, investing, financing cash flows |
| `Balance Sheet` | Assets, liabilities, equity (if full 3-statement) |
| `DCF` | WACC, FCF projections, terminal value, EV bridge |
| `LBO` | Sources & uses, debt schedule, returns summary |
| `Scenarios` | Scenario toggle and outputs |
| `Sensitivity` | Data tables for key variable combinations |
| `Cohort` | MRR cohort waterfall, NRR, GRR |
| `Dashboard` | Charts, KPI summary, executive view |

## Key Formula Patterns

```excel
# Compound growth
=B5*(1+$B$2)^(COLUMN()-COLUMN($B5))

# LTV/CAC
=B_ARPU / B_ChurnRate / B_CAC

# NPV
=NPV(discount_rate, cash_flows_range)

# IRR
=IRR(cash_flows_range)

# Scenario toggle (named range "scenario")
=IF(scenario="bull", bull_value, IF(scenario="bear", bear_value, base_value))
```

## SaaS Metrics Checklist

- MRR / ARR growth rate
- Net Revenue Retention (NRR)
- Gross Revenue Retention (GRR)
- CAC (by channel)
- LTV and LTV/CAC ratio
- Churn rate (logo and revenue)
- Payback period
- Rule of 40 (growth rate + FCF margin)

## Output

Deliver as `.xlsx` file with all tabs labeled. Include a `README` tab explaining assumptions and how to use the scenario toggle. Flag any assumptions that need client input with `[INPUT NEEDED]` in yellow highlight.

---

## DCF Model (Discounted Cash Flow)

### WACC Calculation

**Formula:** `WACC = (E/V) × Re + (D/V) × Rd × (1 − T)`

| Variable | Meaning | Source |
|----------|---------|--------|
| E | Market value of equity | Market cap or comparable |
| D | Market value of debt | Balance sheet + adjustments |
| V | E + D (total capital) | Calculated |
| Re | Cost of equity (CAPM) | Rf + β × ERP |
| Rd | Cost of debt (pre-tax) | Weighted avg interest rate |
| T | Marginal tax rate | Company / jurisdiction rate |

**CAPM for cost of equity:**
```
Re  = Rf + β × ERP
Rf  = risk-free rate (10-yr Treasury yield)
β   = levered beta (from comparable companies; unlever/relever for target structure)
ERP = equity risk premium (typically 4.5–6.5%)
```

**Excel formulas (Assumptions tab → referenced in DCF tab):**
```excel
# Cost of equity (CAPM)
=Risk_Free_Rate + Beta * Equity_Risk_Premium

# Unlevered beta (strip out current capital structure)
=Levered_Beta / (1 + (1 - Tax_Rate) * (Debt_Value / Equity_Value))

# Relever beta at target capital structure
=Unlevered_Beta * (1 + (1 - Tax_Rate) * Target_D_E_Ratio)

# WACC
=(Equity_Value / (Equity_Value + Debt_Value) * Cost_Of_Equity)
+ (Debt_Value / (Equity_Value + Debt_Value) * Cost_Of_Debt * (1 - Tax_Rate))
```

### Free Cash Flow (FCF) Build

```
EBIT
  × (1 − Tax Rate)          → NOPAT (Net Operating Profit After Tax)
  + D&A                     → add back non-cash charge
  − CapEx                   → capital expenditures
  − Δ Net Working Capital   → increase in NWC = cash outflow
= Unlevered Free Cash Flow
```

**Excel FCF row structure (columns = projection years):**
```excel
EBIT:            =Revenue - COGS - OpEx - DA
NOPAT:           =EBIT * (1 - Tax_Rate)
Add D&A:         =DA_row
Less CapEx:      =-CapEx_row
Less ΔNWC:       =-(NWC_row - OFFSET(NWC_row, 0, -1))
FCF:             =NOPAT + DA - CapEx - ΔNWC
Discount factor: =1 / (1 + WACC) ^ period_number
PV of FCF:       =FCF_row * Discount_factor_row
```

### Terminal Value

Always show both methods and reconcile:

**Gordon Growth Model (GGM):**
```excel
# Terminal FCF (year after last projection year)
=FCF_final_year * (1 + Terminal_Growth_Rate)

# Terminal Value
=Terminal_FCF / (WACC - Terminal_Growth_Rate)

# PV of Terminal Value
=Terminal_Value / (1 + WACC) ^ projection_years
```

**Exit Multiple Method:**
```excel
# Terminal EBITDA × multiple
=EBITDA_final_year * Exit_EBITDA_Multiple

# PV of Terminal Value
=Exit_Multiple_TV / (1 + WACC) ^ projection_years
```

### Enterprise Value → Equity Value Bridge

```excel
# Enterprise Value
=SUM(PV_FCF_range) + PV_Terminal_Value

# Net Debt
=Total_Debt + Preferred_Stock + Minority_Interest - Cash - Marketable_Securities

# Equity Value (intrinsic)
=Enterprise_Value - Net_Debt

# Implied share price
=Equity_Value / Diluted_Shares_Outstanding

# Implied EV/EBITDA sanity check
=Enterprise_Value / LTM_EBITDA
```

**Flag: if TV > 80% of EV, projection period is too short — extend to 5–10 years.**

### Python DCF Model

```python
import numpy as np

def build_dcf(
    revenue: list[float],        # projected revenues per year
    ebit_margins: list[float],   # EBIT margin per year
    da_pct: float,               # D&A as % of revenue
    capex_pct: float,            # CapEx as % of revenue
    nwc_pct: float,              # NWC as % of revenue
    tax_rate: float,
    wacc: float,
    terminal_growth: float,
    exit_multiple: float,        # EBITDA exit multiple
    net_debt: float,
    shares_outstanding: float,
) -> dict:
    years = len(revenue)
    fcf = []
    for i, rev in enumerate(revenue):
        ebit = rev * ebit_margins[i]
        nopat = ebit * (1 - tax_rate)
        da = rev * da_pct
        capex = rev * capex_pct
        prev_rev = revenue[i - 1] if i > 0 else rev
        delta_nwc = (rev - prev_rev) * nwc_pct
        fcf.append(nopat + da - capex - delta_nwc)

    discount_factors = [1 / (1 + wacc) ** (i + 1) for i in range(years)]
    pv_fcfs = [f * d for f, d in zip(fcf, discount_factors)]

    # Terminal value — average of both methods
    tv_ggm = fcf[-1] * (1 + terminal_growth) / (wacc - terminal_growth)
    ebitda_final = revenue[-1] * (ebit_margins[-1] + da_pct)
    tv_exit = ebitda_final * exit_multiple
    tv_avg = (tv_ggm + tv_exit) / 2

    pv_tv = tv_avg / (1 + wacc) ** years
    ev = sum(pv_fcfs) + pv_tv
    equity_value = ev - net_debt
    price_per_share = equity_value / shares_outstanding

    return {
        "fcf": fcf,
        "pv_fcfs": pv_fcfs,
        "tv_ggm": tv_ggm,
        "tv_exit": tv_exit,
        "enterprise_value": round(ev, 2),
        "equity_value": round(equity_value, 2),
        "price_per_share": round(price_per_share, 2),
        "tv_pct_ev": round(pv_tv / ev, 4),  # flag if > 0.80
    }
```

---

## Sensitivity Analysis

### Two-Variable Data Table (Excel)

Test how an output changes when two inputs vary simultaneously.

**Setup:**
```excel
# 1. Place output formula in top-left cell of the table range (e.g., D10 = IRR formula)
# 2. Row inputs across the top (e.g., E10:J10 = WACC values)
# 3. Column inputs down the left (e.g., D11:D16 = revenue growth values)
# 4. Select entire table range D10:J16
# 5. Data → What-If Analysis → Data Table
#    Row input cell:    → WACC assumption cell
#    Column input cell: → revenue growth assumption cell
```

**Standard sensitivity ranges:**
```
WACC:            [WACC-2%, WACC-1%, WACC, WACC+1%, WACC+2%]
Revenue growth:  [g-5%, g-2.5%, g, g+2.5%, g+5%]
Exit multiple:   [6.0x, 7.0x, 8.0x, 9.0x, 10.0x]
Terminal growth: [1.0%, 1.5%, 2.0%, 2.5%, 3.0%]
```

**Conditional formatting for tables:**
```excel
# Green: result above target price/IRR
=$E11 > $B$3

# Red: result below target
=$E11 < $B$3
```

### One-Variable Data Table

```excel
# Column A: input values (e.g., revenue growth rates)
# Cell B1: formula referencing the growth rate assumption (=IRR_formula)
# Select A1:B6 → Data → What-If Analysis → Data Table
# Column input cell: → growth rate assumption cell (leave row input blank)
```

### Tornado Chart (Python)

Rank variables by their impact range (high output − low output) to show what moves the needle most.

```python
import matplotlib.pyplot as plt
import numpy as np

def tornado_chart(
    base_value: float,
    variables: list[str],
    low_outputs: list[float],   # output when variable is at downside
    high_outputs: list[float],  # output when variable is at upside
    title: str = "Sensitivity Tornado",
    output_label: str = "IRR (%)",
) -> plt.Figure:
    # Sort by total swing, ascending (largest impact at top)
    impacts = sorted(
        zip(variables, low_outputs, high_outputs),
        key=lambda x: x[2] - x[1],
    )
    vars_sorted, lows, highs = zip(*impacts)
    y_pos = np.arange(len(vars_sorted))

    fig, ax = plt.subplots(figsize=(10, max(4, len(variables) * 0.65)))
    ax.barh(y_pos, [h - base_value for h in highs], left=base_value,
            color="#2ecc71", alpha=0.85, label="Upside")
    ax.barh(y_pos, [l - base_value for l in lows], left=base_value,
            color="#e74c3c", alpha=0.85, label="Downside")
    ax.axvline(x=base_value, color="black", linewidth=1.5, linestyle="--",
               label=f"Base: {base_value}")
    ax.set_yticks(y_pos)
    ax.set_yticklabels(vars_sorted)
    ax.set_xlabel(output_label)
    ax.set_title(title)
    ax.legend()
    plt.tight_layout()
    return fig

# Usage
fig = tornado_chart(
    base_value=18.5,
    variables=["Revenue Growth", "EBITDA Margin", "Exit Multiple", "WACC", "Leverage"],
    low_outputs=[12.1, 14.3, 15.8, 16.2, 17.0],
    high_outputs=[27.3, 23.1, 22.4, 21.0, 20.1],
    title="LBO IRR Sensitivity",
    output_label="IRR (%)",
)
fig.savefig("tornado.png", dpi=150, bbox_inches="tight")
```

---

## Scenario Modeling

### Named Range Scenario Toggle

```excel
# Step 1: Dropdown in Assumptions tab
#   Cell C2: data validation → list → "Base,Bull,Bear"
#   Define named range: scenario = Assumptions!$C$2

# Step 2: Scenario input table (Assumptions rows 30–40)
#   Variable         | Base | Bull | Bear
#   Revenue Growth   | 15%  | 25%  |  5%
#   Gross Margin     | 65%  | 70%  | 55%
#   Monthly Churn    |  8%  |  5%  | 15%
#   Exit Multiple    | 8.0x | 10.0x| 6.0x

# Step 3: Reference in model using CHOOSE + MATCH
=CHOOSE(MATCH(scenario, {"Base","Bull","Bear"}, 0), base_val, bull_val, bear_val)

# Alternative — INDEX/MATCH for table-driven lookup
=INDEX(scenario_table_range,
       MATCH(variable_row_label, variable_labels, 0),
       MATCH(scenario, {"Base","Bull","Bear"}, 0))
```

### OFFSET-based Switching

```excel
# 0=Base, 1=Bull, 2=Bear offset from base column
=OFFSET(base_input_cell, 0, MATCH(scenario, {"Base","Bull","Bear"}, 0) - 1)
```

### Python Scenario Runner

```python
from dataclasses import dataclass
from typing import Literal
import pandas as pd

@dataclass
class Scenario:
    name: Literal["base", "bull", "bear"]
    revenue_growth: float
    gross_margin: float
    churn_rate: float
    exit_multiple: float
    wacc: float

SCENARIOS: dict[str, Scenario] = {
    "base": Scenario("base", revenue_growth=0.15, gross_margin=0.65,
                     churn_rate=0.08, exit_multiple=8.0, wacc=0.12),
    "bull": Scenario("bull", revenue_growth=0.25, gross_margin=0.70,
                     churn_rate=0.05, exit_multiple=10.0, wacc=0.11),
    "bear": Scenario("bear", revenue_growth=0.05, gross_margin=0.55,
                     churn_rate=0.15, exit_multiple=6.0, wacc=0.14),
}

def run_all_scenarios(model_fn, base_inputs: dict) -> pd.DataFrame:
    results = []
    for name, s in SCENARIOS.items():
        inputs = {
            **base_inputs,
            "revenue_growth": s.revenue_growth,
            "gross_margin": s.gross_margin,
            "churn_rate": s.churn_rate,
            "exit_multiple": s.exit_multiple,
            "wacc": s.wacc,
        }
        output = model_fn(**inputs)
        results.append({"scenario": name, **output})
    return pd.DataFrame(results).set_index("scenario")

# Usage
df = run_all_scenarios(build_dcf, base_inputs={...})
print(df[["enterprise_value", "equity_value", "price_per_share"]])
```

---

## LBO Model (Leveraged Buyout)

### Sources & Uses of Funds

```
SOURCES                            USES
──────────────────────────────     ──────────────────────────────
Senior Secured Debt                Purchase Price (EV)
  Term Loan A          $Xm           = Entry EBITDA × Entry Multiple
  Term Loan B          $Xm         Transaction Fees  (~2% of EV)
Subordinated Debt      $Xm         Financing Fees    (~2% of debt)
Sponsor Equity         $Xm         Cash to Balance Sheet (minimum)
──────────────────────────────     ──────────────────────────────
Total Sources          $Xm         Total Uses                  $Xm
```

**Excel formulas:**
```excel
# Entry EV
=Entry_EBITDA * Entry_Multiple

# Equity check (target: sponsor equity 30–50% of EV)
=Sponsor_Equity / Entry_EV

# Sponsor equity (residual plug)
=Total_Uses - Senior_Debt - Sub_Debt

# Total uses
=Entry_EV + Transaction_Fees + Financing_Fees + Min_Cash_on_BS
```

### Debt Schedule

```excel
# Columns per year: Beginning_Bal | New_Borrow | Mandatory_Amort | Optional_Paydown | Ending_Bal | Interest

# Beginning balance (from prior year ending)
=OFFSET(Ending_Bal_cell, 0, -1)

# Mandatory amortization — Term Loan A (5%/yr example)
=-TLA_Original_Principal * TLA_Amort_Rate

# Optional paydown — excess cash sweep
=-MAX(0, Beginning_Cash + Operating_CF - Min_Cash_Balance - Mandatory_Debt_Service)

# Ending balance
=Beginning_Bal + New_Borrow + Mandatory_Amort + Optional_Paydown

# Interest (average balance method)
=(Beginning_Bal + Ending_Bal) / 2 * Interest_Rate
```

### Returns Analysis

```excel
# Exit Enterprise Value
=Exit_Year_EBITDA * Exit_Multiple

# Equity proceeds to sponsor
=Exit_EV - Remaining_Total_Debt + Exit_Cash - Exit_Transaction_Fees

# MOIC (Multiple on Invested Capital)
=Total_Equity_Proceeds / Sponsor_Equity_Invested

# IRR (XIRR for exact dates)
=XIRR(
  {-Sponsor_Equity, 0, 0, 0, 0, Equity_Proceeds},
  {Entry_Date, Y1_Date, Y2_Date, Y3_Date, Y4_Date, Exit_Date}
)
```

**Benchmark targets:** MOIC ≥ 2.5×, IRR ≥ 20%, hold period 3–7 years, leverage ≤ 6–7× EBITDA.

### Python LBO Model

```python
def build_lbo(
    entry_ebitda: float,
    entry_multiple: float,
    exit_multiple: float,
    ebitda_growth: list[float],     # annual growth rates for each hold year
    debt_tranches: list[dict],      # [{"name":"TLA","amount":100,"rate":0.06,"amort":0.05}]
    tax_rate: float = 0.25,
    min_cash: float = 5.0,
    transaction_fee_pct: float = 0.02,
    financing_fee_pct: float = 0.02,
) -> dict:
    entry_ev = entry_ebitda * entry_multiple
    total_debt = sum(t["amount"] for t in debt_tranches)
    transaction_fees = entry_ev * transaction_fee_pct
    financing_fees = total_debt * financing_fee_pct
    sponsor_equity = entry_ev + transaction_fees + financing_fees + min_cash - total_debt

    ebitda_series = [entry_ebitda]
    for g in ebitda_growth:
        ebitda_series.append(ebitda_series[-1] * (1 + g))

    # Debt paydown (mandatory amortization only for simplicity)
    remaining_debt = total_debt
    for _ in ebitda_growth:
        mandatory = sum(t["amount"] * t.get("amort", 0.01) for t in debt_tranches)
        remaining_debt -= mandatory

    exit_ev = ebitda_series[-1] * exit_multiple
    equity_proceeds = max(0.0, exit_ev - remaining_debt)
    moic = equity_proceeds / sponsor_equity if sponsor_equity > 0 else 0.0
    years = len(ebitda_growth)
    irr_approx = moic ** (1 / years) - 1  # geometric approx; use numpy_financial.irr for exact

    return {
        "entry_ev": round(entry_ev, 2),
        "sponsor_equity": round(sponsor_equity, 2),
        "total_debt": round(total_debt, 2),
        "leverage_ratio": round(total_debt / entry_ebitda, 2),
        "exit_ev": round(exit_ev, 2),
        "equity_proceeds": round(equity_proceeds, 2),
        "moic": round(moic, 2),
        "irr_approx": round(irr_approx, 4),
    }
```

---

## Revenue Forecasting & Cohort Analysis

### MRR Waterfall (SaaS)

```
Beginning MRR
  + New MRR           (new logos × ARPU)
  + Expansion MRR     (upsell/cross-sell to existing customers)
  − Contraction MRR   (downgrades)
  − Churned MRR       (cancellations)
= Ending MRR

ARR = Ending MRR × 12
```

**Excel MRR waterfall formulas:**
```excel
# New MRR
=New_Customers_This_Month * ARPU

# Expansion MRR (from existing base)
=Beginning_MRR * Monthly_Expansion_Rate

# Contraction MRR (downgrade rate)
=-Beginning_MRR * Monthly_Contraction_Rate

# Churned MRR (cancellation rate)
=-Beginning_MRR * Monthly_Churn_Rate

# Ending MRR
=Beginning_MRR + New_MRR + Expansion_MRR + Contraction_MRR + Churned_MRR

# NRR (Net Revenue Retention) — trailing 12 months
=(Ending_MRR_cohort - New_MRR_cohort) / Beginning_MRR_cohort

# GRR (Gross Revenue Retention — excludes expansion, floor at 0%)
=MAX(0, (Beginning_MRR + Contraction_MRR + Churned_MRR) / Beginning_MRR)
```

### Cohort Analysis Pattern

Cohort = all customers acquired in the same period.

```
             Month 0   Month 1   Month 2   Month 3  ...
Cohort Jan     100%      85%       74%       67%
Cohort Feb               100%      82%       71%
Cohort Mar                          100%      84%
```

**Excel cohort grid (diagonal offset pattern):**
```excel
# Retention at month M for cohort starting at column C
=IF(COLUMN() - cohort_start_col > 0,
   Retention_Rate ^ (COLUMN() - cohort_start_col),
   IF(COLUMN() = cohort_start_col, 1, ""))

# Revenue from cohort at month M (with expansion)
=Cohort_starting_MRR
  * Retention_Rate ^ M
  * (1 + Monthly_Expansion_Rate) ^ M
```

### Python Cohort Builder

```python
import numpy as np
import pandas as pd

def build_cohort_model(
    cohort_sizes: list[int],          # customers entering each period
    arpu: float,
    monthly_retention: float,         # e.g., 0.92 = 92% retained per month
    monthly_expansion: float = 0.02,  # expansion revenue per retained customer
    periods: int = 24,
) -> pd.DataFrame:
    """Returns cohort × period revenue matrix."""
    n_cohorts = len(cohort_sizes)
    revenue = np.zeros((n_cohorts, periods))

    for i, size in enumerate(cohort_sizes):
        for m in range(periods - i):
            customers = size * (monthly_retention ** m)
            expansion_mult = (1 + monthly_expansion) ** m
            revenue[i, i + m] = customers * arpu * expansion_mult

    df = pd.DataFrame(
        revenue,
        index=[f"Cohort_{i + 1:02d}" for i in range(n_cohorts)],
        columns=[f"Month_{m + 1:02d}" for m in range(periods)],
    )
    df["Total_Revenue"] = df.sum(axis=1)
    return df

def compute_nrr(cohort_df: pd.DataFrame, window: int = 12) -> float:
    """NRR from cohort matrix — trailing window vs next window."""
    start = cohort_df.iloc[:, :window].sum().sum()
    end = cohort_df.iloc[:, window:window * 2].sum().sum()
    return round(end / start, 4) if start > 0 else 0.0
```

### SaaS Unit Economics

```excel
# LTV (gross margin adjusted)
=(ARPU * Gross_Margin_Pct) / Monthly_Churn_Rate

# LTV/CAC ratio (target: > 3×)
=LTV / CAC

# CAC Payback Period in months (target: < 12 months)
=CAC / (ARPU * Gross_Margin_Pct)

# Magic Number — sales efficiency (target: > 0.75)
=(Current_Qtr_ARR - Prior_Qtr_ARR) / Prior_Qtr_Sales_And_Marketing_Spend

# Rule of 40 (target: ≥ 40%)
=YoY_Revenue_Growth_Pct + FCF_Margin_Pct
```

---

## Excel / Python Interoperability

### Build Excel Model with openpyxl

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.utils import quote_sheetname, absolute_coordinate

# Palette
BLUE_FILL   = PatternFill(start_color="DBEAFE", end_color="DBEAFE", fill_type="solid")  # inputs
YELLOW_FILL = PatternFill(start_color="FEF9C3", end_color="FEF9C3", fill_type="solid")  # flagged
HEADER_FILL = PatternFill(start_color="1E3A5F", end_color="1E3A5F", fill_type="solid")  # headers

def style_input(ws, row: int, col: int) -> None:
    cell = ws.cell(row=row, column=col)
    cell.fill = BLUE_FILL
    cell.font = Font(color="1F497D")

def style_header_row(ws, row: int, cols: int, start_col: int = 1) -> None:
    for c in range(start_col, start_col + cols):
        cell = ws.cell(row=row, column=c)
        cell.fill = HEADER_FILL
        cell.font = Font(bold=True, color="FFFFFF")
        cell.alignment = Alignment(horizontal="center")

def add_named_range(wb: Workbook, name: str, sheet: str, cell: str) -> None:
    ref = f"{quote_sheetname(sheet)}!{absolute_coordinate(cell)}"
    wb.defined_names[name] = DefinedName(name, attr_text=ref)

def write_assumptions(wb: Workbook, assumptions: dict) -> None:
    ws = wb.create_sheet("Assumptions")
    ws.column_dimensions["A"].width = 30
    ws.column_dimensions["B"].width = 18
    ws.column_dimensions["C"].width = 12
    style_header_row(ws, 1, 3)
    for col, h in enumerate(["Parameter", "Value", "Unit"], 1):
        ws.cell(row=1, column=col).value = h
    for row, (key, val) in enumerate(assumptions.items(), 2):
        ws.cell(row=row, column=1).value = key
        ws.cell(row=row, column=2).value = val
        style_input(ws, row, 2)

def build_model_xlsx(data: dict, filepath: str) -> None:
    wb = Workbook()
    wb.remove(wb.active)
    write_assumptions(wb, data["assumptions"])
    add_named_range(wb, "WACC", "Assumptions", "B5")
    add_named_range(wb, "scenario", "Assumptions", "B2")
    add_named_range(wb, "terminal_growth", "Assumptions", "B8")
    wb.save(filepath)
```

### Read Excel into Pandas

```python
import pandas as pd

def load_model_tabs(filepath: str) -> dict[str, pd.DataFrame]:
    xl = pd.ExcelFile(filepath)
    return {sheet: xl.parse(sheet, index_col=0) for sheet in xl.sheet_names}

def extract_assumptions(filepath: str) -> dict:
    df = pd.read_excel(filepath, sheet_name="Assumptions", index_col=0)
    return df.iloc[:, 0].to_dict()
```

---

## Validation & Error Checking

### Balance Sheet Balance Check

```excel
# Total Assets
=SUM(Current_Assets_range) + SUM(Non_Current_Assets_range)

# Total Liabilities + Equity
=SUM(Liabilities_range) + Total_Equity

# Balance check cell (must be ~0)
=Total_Assets - Total_Liabilities_And_Equity

# Conditional format: flag if |BS_Check| > 0.01
=ABS(BS_Check_cell) > 0.01
```

### Cash Flow Reconciliation

```excel
# Calculated ending cash (indirect method)
=Beginning_Cash + Operating_CF + Investing_CF + Financing_CF

# Reconciliation check (must be ~0)
=Calculated_Ending_Cash - Balance_Sheet_Cash_Ending

# Flag
=ABS(CF_Recon_cell) > 0.01
```

### Python Validation Suite

```python
def validate_model(results: dict) -> list[str]:
    """Returns list of error messages. Empty list = model passes."""
    errors = []

    bs = results.get("balance_sheet", {})
    if abs(bs.get("total_assets", 0) - bs.get("total_liabilities_equity", 0)) > 0.01:
        errors.append("Balance sheet does not balance")

    cf = results.get("cash_flow", {})
    if abs(cf.get("ending_cash", 0) - cf.get("calc_ending_cash", 0)) > 0.01:
        errors.append("Cash flow does not reconcile with balance sheet")

    dcf = results.get("dcf", {})
    if dcf.get("tv_pct_ev", 0) > 0.80:
        errors.append(
            f"Terminal value is {dcf['tv_pct_ev']:.0%} of EV — extend projection period"
        )

    lbo = results.get("lbo", {})
    if lbo.get("leverage_ratio", 0) > 7.0:
        errors.append(f"Leverage {lbo['leverage_ratio']:.1f}× exceeds 7.0× — review debt structure")
    if 0 < lbo.get("moic", 0) < 2.0:
        errors.append(f"MOIC {lbo['moic']:.2f}× below 2.0× — deal unlikely to pencil")

    saas = results.get("saas_metrics", {})
    if saas.get("ltv_cac", 0) < 3.0:
        errors.append(f"LTV/CAC {saas['ltv_cac']:.1f}× below 3.0× minimum")

    return errors
```

### Common Model Errors

| Error | Detection | Fix |
|-------|-----------|-----|
| Circular reference | Excel warning on open | Reference prior-period NWC, not current |
| Hard-coded values in formulas | `Ctrl+~` formula audit | Move all inputs to Assumptions tab |
| TV > 80% of EV | `tv_pct_ev` flag | Extend projection to 5–10 years |
| NWC includes non-cash items | Manual review | Exclude D&A, impairments from ΔNWC |
| IRR with multiple sign changes | MIRR check | `=MIRR(flows, reinvest_rate, finance_rate)` |
| LBO leverage > 7× | Leverage check cell | Reduce debt quantum or increase equity |
| BS doesn't balance | Balance check cell | Trace retained earnings / equity roll |
