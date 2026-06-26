```markdown
---
name: full-link-data-analysis
description: Full-Link Data Analysis Engine: From business Agenda to analytical report with complete seven-layer architecture. Built-in 15 analysis methods, supports data-aware routing ( Agenda semantics + data structure + problem type three dimensions), built-in quality assurance, outputs Feishu doc format analytical reports.
---

# Full-Link Data Analysis

## Overview

The seven-layer architecture automatically transforms business Agenda into structured analytical reports:

```
L1 Persona Understanding → L2 Data Scope Acquisition → L3 Analysis Data Scoping → L4 Problem Decomposition → L5 Method Selection → L6 Execution & Computation → L7 Result Output
```

The Agent writes Python analysis code as needed, no pre-packaged code library required. Each layer acts as a quality gate for the next.

## Trigger Scenarios

- User requests data/business metric analysis
- User wants to understand causes/trends/patterns in data
- User needs a data analysis report
- User mentions "analyze", "attribute", "predict", "cluster", "trend", "data report"
- User presents business Agenda requiring data-driven insights.

## Core Principles

- **Code on Demand**: Use `pandas`/`numpy`/`scipy`/`sklearn`/`statsmodels` to write analysis scripts tailored to the actual data.
- **Data-Aware Routing**: Method selection综合考虑 Agenda semantics, data structure, and problem type.
- **Quality Gate**: Every conclusion output must include confidence annotation and cross-validation description.

## Seven-Layer Process

### L1 — Persona Understanding

Identify the questioner's role, decision-making scenario, and success criteria.

Key Questions:
- **Role**: Executive, analyst, product manager, operations personnel?
- **Decision Scenario**: Strategic planning, operational review, special investigation?
- **Success Criteria**: What metrics/goals define "good"?
- **Data Literacy**: How technical should the report be?

**Output**: Structured persona summary (role, decision scenario, success criteria).

### L2 — Data Scope Acquisition

Discover and validate available data sources.

Steps:
1. Ask user for provided data (files, databases, APIs)
2. Upon receiving files, check schema, sample data, inspect types and missing values
3. Identify relevant fields/tables
4. Confirm data timeliness (update frequency)

**Output**: Data inventory (source, schema, quality notes).

### L3 — Analysis Data Scoping

Narrow down from "all available data" to "data relevant to the Agenda".

Steps:
1. Map business problem keywords to required data dimensions
2. Filter only necessary fields/records
3. Define time window, aggregation granularity, filter conditions
4. Identify potential confounding factors

**Output**: Data scope specification (dimensions, time window, filters, aggregation granularity).

### L4 — Problem Decomposition

Break down the business problem into analyzable sub-problems.

Framework Selection:
- **MECE** (Mutually Exclusive, Collectively Exhaustive): Revenue = Transaction Value × Customer Flow
- **Drill-down**: Decompose by region → channel → product layer by layer
- **Before/After**: Pre-change vs. post-change
- **Cohort**: Group by time/attributes, compare trajectories
- **Funnel**: Step-by-step conversion analysis
- **Hypothesis Tree**: Structured hypothesis testing

**Output**: Problem tree (decomposition structure with clear hypothesis statements).

### L5 — Method Selection

Select analysis method based on data-aware routing. See `references/routing.md`.

Three-Dimensional Routing:
1. ** Agenda Semantics**: Growth, churn, conversion, risk, attribution...
2. **Data Structure**: Time series, cross-sectional, panel, hierarchical...
3. **Problem Type**: Descriptive, diagnostic, predictive, prescriptive

See `references/methods.md` (details on 15 methods).

**Output**: Method plan (primary method + alternative cross-validation method).

### L6 — Execution & Computation

Execute analysis using Python. Process:

1. **Environment Check**: `pip list` to confirm `pandas`, `numpy` availability; install missing packages
2. **Data Loading**: Load data according to L3 scope specification
3. **Data Cleaning**: Handle missing values, outliers, type conversions
4. **Analysis Execution**: Write and execute Python script for selected method(s)
5. **Cross-Validation**: Run comparison using alternative method (see `references/quality.md`)
6. **Result Interpretation**: Extract key figures, statistics, effect sizes

Coding Standards:
- Use `pandas` for data manipulation, `scipy.stats` for statistical tests, `statsmodels`/`sklearn` for modeling
- Print results with clear labels; script output directly constitutes report content
- Handle edge cases (empty data, all-null columns, single-category variables)
- Output structured text rather than raw numbers

### L7 — Result Output

Output analytical report in Feishu document format. See `references/feishu-report.md`.

Report Structure:
1. **Analysis Overview** — Executive summary (1 paragraph)
2. **Key Findings** — Data-backed key insights
3. **Analysis Process** — Methods, data scope, key assumptions
4. **Detailed Results** — Chart descriptions, statistical results, effect sizes
5. **Conclusions & Recommendations** — Actionable recommendations with confidence annotations
6. **Appendix** — Method details, caveats, data quality notes

## Quick Reference

| Layer | Action | Reference |
|-------|--------|-----------|
| L1 Persona | Identify role and decision context | Built-in question set |
| L2 Data | Discover and validate data sources | Built-in check process |
| L3 Scope | Narrow to relevant data | Built-in mapping logic |
| L4 Decompose | Break down into sub-problems | Built-in frameworks |
| L5 Method | Select analysis method | `references/methods.md` + `references/routing.md` |
| L6 Execute | Write Python analysis | Built-in coding standards |
| L7 Output | Generate report | `references/feishu-report.md` + `references/quality.md` |

## Checklist

- [ ] L1: Confirm persona before accessing data
- [ ] L2: Always check schema and sample before analysis
- [ ] L3: Clearly state data scope (time, filters, dimensions)
- [ ] L4: Must decompose first, do not jump directly to methods
- [ ] L5: Consult routing table and document method selection rationale
- [ ] L6: Run at least one cross-validation
- [ ] L7: Each conclusion must include confidence annotation
```