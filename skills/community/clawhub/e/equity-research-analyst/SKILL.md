---
name: equity-research-analyst
description: Use when the user asks for institutional-style equity research on a public company, ETF, or TradingView-resolvable ticker, including initiation reports, earnings updates or previews, catalyst calendars, morning notes, sector or peer overviews, thesis reviews, model refreshes, and stock screening or idea generation.
---

# Equity Research Analyst

Produce institutional-grade equity research deliverables covering nine distinct workflows. Each workflow has its own dedicated reference file in `references/workflows/`; this SKILL.md is the dispatcher and the hub for cross-workflow conventions.

## Loading Strategy

Keep context tight and load only the files needed for the active task.

1. Match the request to exactly one workflow in `references/workflows/`.
2. Read only that workflow file first.
3. Open deep-dive references only when the active workflow points to them.
4. Read `references/tradingviewapi.md` before opening anything in `references/tradingviewapi-docs/`.
5. Treat `references/tradingviewapi-docs/` as a lookup bundle: search by endpoint name or JSON field, then open the smallest relevant file instead of loading an entire large example file.

### `tradingviewapi` lookup guide

- Start with `references/tradingviewapi.md` for task-to-endpoint mapping.
- Use `references/tradingviewapi-docs/README.md` for file selection inside the bundled API docs.
- Use `references/tradingviewapi-docs/openapi.json` as the source of truth for exact parameters, defaults, and allowed enum values.
- Use `references/tradingviewapi-docs/examples/` mainly for concrete URL patterns and response shapes, not for deciding which asset-class parameter should be used.
- If an example and the OpenAPI spec disagree, trust `openapi.json` for parameters and trust executed examples only for payload shape after the request has been validated against the spec.
- Search patterns that usually find the right example quickly:
  - `GET /api/market-data/{symbol}`
  - `GET /api/calendar/earnings`
  - `GET /api/search/market/{query}`
  - `earnings_release_next_date`
  - `analyst-recommendations`

## When to invoke which workflow

Match the user request to one of the nine workflows below and read the corresponding reference file from `references/workflows/`. If the request is ambiguous, ask the user to confirm before committing.

| Workflow | Trigger phrases | Reference |
|---|---|---|
| **Initiating coverage** | "initiation report", "first-time coverage", "new coverage on X", "write a full report on X" | `references/workflows/initiating-coverage.md` |
| **Earnings analysis** | "earnings update", "Q1/Q2/Q3/Q4 results for X", "post-earnings report", "beat/miss analysis" | `references/workflows/earnings-analysis.md` |
| **Earnings preview** | "earnings preview", "what to watch in X's earnings", "pre-earnings note" | `references/workflows/earnings-preview.md` |
| **Catalyst calendar** | "catalyst calendar", "upcoming events", "earnings calendar", "event tracker" | `references/workflows/catalyst-calendar.md` |
| **Morning note** | "morning note", "daily brief", "pre-market note", "morning wrap" | `references/workflows/morning-note.md` |
| **Sector overview** | "sector report", "industry overview", "peer comp", "sector deep-dive" | `references/workflows/sector-overview.md` |
| **Thesis tracker** | "thesis tracker", "investment thesis review", "revisit thesis on X", "thesis check" | `references/workflows/thesis-tracker.md` |
| **Model update** | "update the model", "model maintenance", "refresh estimates", "re-forecast" | `references/workflows/model-update.md` |
| **Idea generation** | "screen for X", "find me stocks that", "idea generation", "investment ideas" | `references/workflows/idea-generation.md` |

### Single-workflow discipline (especially for `initiating-coverage`)

The initiation-report workflow has five sequential tasks (Company Research → Financial Modeling → Valuation → Charts → Assembly). Execute **one task per user request**, verify prerequisites before the next task, and never auto-chain. Details in `references/workflows/initiating-coverage.md`.

## Primary data source: `tradingviewapi`

Before Web Search, pull structured numeric data (financials, TTM ratios, analyst consensus, calendars, prices, technicals, news) from the bundled `tradingviewapi` (TradingView proxy). **One call to `/api/market-data/{symbol}` covers ~70% of the numeric content of a typical research report.**

- Full endpoint map, curl examples, and JSON-path-to-report-field mapping: `references/tradingviewapi.md`
- OpenAPI spec and example responses: `references/tradingviewapi-docs/`

**Authentication**: users must provide their own `RAPIDAPI_KEY` env var (RapidAPI hosted).

**Use Web Search ONLY for narrative content**: MD&A text, forward guidance wording, earnings call transcripts, segment breakdowns, risk factors, management bios, industry research, FDA/regulatory decisions. Pull raw SEC 10-K/10-Q only when direct quotation or audit is required.

## Global conventions

### Data freshness
- Training data is outdated. Before writing, verify today's date and confirm that the latest fetched data is current (next earnings date, last reported quarter).
- If `data.current.fiscal_period_current` is >90 days old, flag as "last reported" and Web Search for newer disclosures.
- Treat `data.current.fiscal_period_current` as a structured provider label, not the final narrative quarter label. If company IR / SEC naming differs (for example provider `2025-Q4` vs company-reported `Fiscal 2026 Q4`), use the latest primary-source wording in the written report and cite that source explicitly.

### Ticker resolution
- Always use `EXCHANGE:TICKER` format (e.g., `NASDAQ:AAPL`, `NYSE:JPM`).
- If the user supplies only a company name, resolve it via `/api/search/market/{query}?filter=stock` before proceeding.
- Use the resolved symbol from `/api/search/market/{query}` as the canonical identifier for the workflow. Do not rely on `data.company.ticker` or `data.company.exchange` from `/api/market-data/{symbol}` as the canonical listing identifier, because those fields may be null or may reflect a quote venue rather than the primary exchange.

### Citation standard
Every numeric fact in a deliverable must cite its source:

```
Source: Structured data via tradingviewapi (TradingView); fetched [YYYY-MM-DD]
        Endpoint: /api/market-data/NASDAQ:AAPL
        Fiscal period: 2026-Q1
```

SEC filings keep separate EDGAR hyperlinks. When consensus data comes from the API, cite the `analyst-recommendations` endpoint explicitly instead of a generic terminal label.

### Output formatting
- Default font for Word deliverables: **Times New Roman**.
- Do **not** add emojis to research reports unless the user explicitly requests them.
- Follow the page/structure templates in `assets/initiating-coverage/report-template.md` for initiation reports.
- Use `references/initiating-coverage/quality-checklist.md` for final initiation-report QA.
- Other workflows use the template embedded in their own reference file.

### No shortcuts
- Deliver exactly the outputs specified in each workflow reference. Do **not** create extra "completion summaries", "executive summaries", or "quick reference guides".
- Do not fabricate data. Missing field → "N/A". Missing consensus → state "consensus not available".

## Fallback strategy
1. `tradingviewapi` unavailable → fall back to Web Search + SEC EDGAR per the workflow reference.
2. Ticker unresolved → ask the user for `EXCHANGE:TICKER`.
3. Ambiguous workflow → ask the user which deliverable they want.

## Directory layout

```
equity-research-analyst/
├── SKILL.md                              # This file
├── references/
│   ├── tradingviewapi.md                   # Endpoint map + report-field mapping
│   ├── tradingviewapi-docs/                # Bundled API spec + examples (snapshot)
│   │   ├── README.md
│   │   ├── openapi.json
│   │   └── examples/ (12 .md files)
│   ├── workflows/                        # One dispatch target per workflow
│   │   ├── initiating-coverage.md
│   │   ├── earnings-analysis.md
│   │   ├── earnings-preview.md
│   │   ├── catalyst-calendar.md
│   │   ├── morning-note.md
│   │   ├── sector-overview.md
│   │   ├── thesis-tracker.md
│   │   ├── model-update.md
│   │   └── idea-generation.md
│   ├── earnings-analysis/                # Deep-dive references for earnings workflow
│   │   ├── workflow.md
│   │   ├── report-structure.md
│   │   └── best-practices.md
│   └── initiating-coverage/              # Deep-dive references for initiation tasks 1-5
│       ├── task1-company-research.md
│       ├── task2-financial-modeling.md
│       ├── task3-valuation.md
│       ├── task4-chart-generation.md
│       ├── task5-report-assembly.md
│       ├── quality-checklist.md
│       └── valuation-methodologies.md
├── assets/
│   └── initiating-coverage/              # Templates used in output
│       └── report-template.md
```
