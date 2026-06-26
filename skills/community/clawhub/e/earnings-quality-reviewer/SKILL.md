---
name: earnings-quality-reviewer
description: Reviews earnings quality before valuation when structured financial statements are available; optional notes improve confidence. Requires supplied data only and performs no direct data fetching.
compatibility: Requires structured financial statements and optional notes; no direct data fetching.
---

# Earnings Quality Reviewer

## Purpose

Assess whether reported earnings are reliable enough to support valuation conviction.

## Scope

- Income statement.
- Balance sheet.
- Cash flow statement.
- Profitability, liquidity, leverage, and efficiency ratios.
- Financial statement notes.
- One-offs and non-recurring items.
- Related-party notes.
- Debt maturity notes.

## Non-goals

- No data fetching.
- No fabrication of missing notes.
- No absolute buy/sell instructions.

## Input contract

Provide structured financials and optional notes:

- Income statement line items, including revenue, gross profit, operating profit, finance cost, tax, net income, and non-recurring items when available.
- Balance sheet line items, including cash, receivables, inventory, current assets, debt, payables, current liabilities, equity, and total assets.
- Cash flow line items, including cash flow from operations, capital expenditure, free cash flow, financing cash flows, and material working-capital movements.
- Ratios or enough raw fields to compute ratios.
- Optional notes covering accounting policy changes, related-party transactions, debt maturities, contingencies, and management adjustments.

## Data quality gate

Before reviewing earnings quality, assess:

- Statement freshness: whether statement dates are current enough for the valuation date.
- Missing lines: whether key income statement, balance sheet, or cash flow lines are absent.
- Cash-flow completeness: whether operating cash flow, capital expenditure, and free cash flow are available or can be derived.
- Notes availability: whether notes are supplied for accounting policies, one-offs, related parties, contingencies, and debt maturities.

If the data gate fails, still provide a review when possible, but lower confidence and list the gaps in the handoff bundle.

## Review checklist

- Cash conversion: compare net income with operating cash flow and free cash flow across the available period.
- Accrual risk: identify large earnings-without-cash patterns, margin expansion without cash support, capitalization concerns, or abnormal non-cash items.
- Working capital pressure: review receivables, inventory, payables, current ratio trends, and cash conversion cycle signals when available.
- Leverage/refinancing risk: assess debt load, short-term maturities, interest burden, covenant or liquidity pressure, and refinancing dependence.
- One-off adjustments: separate recurring earnings power from asset sales, impairments, restructuring charges, tax effects, FX effects, and other non-recurring items.
- Governance/accounting red flags: flag related-party transactions, accounting policy changes, auditor concerns, restatements, unusually aggressive assumptions, and unexplained note gaps.

## Required output format

Use exactly these sections:

1. `Input Quality`
2. `Earnings Quality Score`
3. `Cash Conversion and Accruals`
4. `Balance Sheet and Working Capital`
5. `One-Offs and Accounting Red Flags`
6. `Valuation Confidence Impact`
7. `Handoff Bundle`

## Shared confidence rubric

- `High`: fresh statements, complete income statement, balance sheet, and cash flow data, notes available, consistent cash conversion, limited accrual concerns, and no material unresolved red flags.
- `Medium`: usable statements and cash-flow data, but notes are incomplete, one major line group is limited, or there are moderate unresolved earnings-quality concerns.
- `Low`: stale statements, missing cash-flow data, missing notes, major unexplained accruals, significant working-capital stress, refinancing risk, or material accounting/governance red flags.

## Guardrails

- Separate facts, assumptions, and inference.
- Do not fabricate missing line items, notes, explanations, or management intent.
- Cap confidence at `Medium` when relevant notes are missing.
- Treat red flags as valuation-risk inputs, not trading commands.
- Use cautious language when the evidence is incomplete or mixed.

## Handoff bundle

Include these exact markers:

- `ticker`
- `as_of_date`
- `earnings_quality_tier`
- `cash_conversion`
- `accrual_risk`
- `working_capital_pressure`
- `leverage_refinancing_risk`
- `one_off_adjustments`
- `red_flags`
- `valuation_confidence_impact`
- `data_gaps`

## Trigger examples

- "Review earnings quality before I run valuation."
- "Check whether these reported profits are cash-backed."
- "Assess accrual risk and working-capital pressure from these statements."
- "Prepare an earnings-quality handoff for the valuation model."
