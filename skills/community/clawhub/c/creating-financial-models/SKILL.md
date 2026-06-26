---
name: creating-financial-models
description: Use when user wants to build financial models, DCF analysis, valuation, sensitivity analysis, e-commerce business planning, investment decisions, or project finance assessments.
version: "1.0.0"
---


# Creating Financial Models

This skill provides a comprehensive suite for building financial models, including Discounted Cash Flow (DCF) analysis, sensitivity testing, Monte Carlo simulations, and scenario planning. It is ideal for valuation, investment decisions, e‑commerce business planning, and any situation requiring rigorous financial analysis.

## Overview

- **Core workflow**: Gather inputs → run DCF model → perform sensitivity analysis → optional Monte Carlo simulation → scenario comparison.
- **Outputs**: Excel workbook with full model, valuation summary, charts, and a PDF report.

## Core Workflow

1. **Collect data**
   - Historical financial statements (3‑5 years).
   - Revenue growth assumptions, margin forecasts, capex, working‑capital needs.
   - Discount rate components (risk‑free rate, beta, market premium) to compute WACC.
2. **Run DCF model** (`scripts/dcf_model.py`)
   - Projects free cash flow, computes terminal value, discounts to present value.
   - Generates enterprise and equity valuations.
3. **Sensitivity analysis** (built‑in in the script)
   - Varies key inputs (growth rate, WACC) and produces tornado charts.
4. **Monte Carlo simulation** (optional)
   - Executes thousands of iterations with probabilistic inputs, returns confidence intervals.
5. **Scenario planning**
   - Define best/base/worst cases, assign probabilities, compare outcomes.
6. **Deliver output**
   - `output/model.xlsx` – full model.
   - `output/summary.pdf` – executive summary with charts.

## Usage Examples

- `Create a DCF valuation for Acme Corp using the attached financials.`
- `Run a sensitivity analysis on the WACC and growth rate for the startup model.`
- `Perform a Monte Carlo simulation with 5,000 iterations on the acquisition model.`
- `Generate best, base, and worst case scenarios for the new e‑commerce platform rollout.`

## References

- See `references/methodology.md` for detailed methodology, assumptions, and best‑practice guidelines.

## Scripts

- `scripts/dcf_model.py` – Core DCF engine (Python). Use `python scripts/dcf_model.py <input.json> <output.xlsx>`.

---


---

**Created by [Simon Cai](https://github.com/simoncai519) · More e-commerce skills: [github.com/simoncai519/open-accio-skill](https://github.com/simoncai519/open-accio-skill)**
