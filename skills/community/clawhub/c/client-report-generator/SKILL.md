---
name: client-report-generator
description: Generate professional client-facing reports from raw data, metrics, and KPIs. Supports analytics summaries, project status reports, monthly/weekly performance reviews, and campaign results. Use when asked to create a client report, generate a performance report, summarize metrics for a client, build a weekly/monthly report, create a project status update, format analytics data into a report, or produce a deliverable report from raw data. Triggers on "client report", "performance report", "weekly report", "monthly report", "status report", "generate report from data", "metrics report", "campaign report", "analytics summary".
---

# Client Report Generator

Generate polished, client-ready reports from raw data. Feed it CSV, JSON, analytics exports, or plain text metrics — get back a professional report formatted for delivery.

## Workflow

### 1. Ingest Data

Determine input type and extract data:

- **CSV/TSV file** → Read and parse into structured data
- **JSON file/API response** → Parse and extract key metrics
- **Pasted text/numbers** → Parse inline data
- **URL (dashboard/analytics)** → Use `web_fetch` to extract visible data
- **Multiple sources** → Combine into unified dataset

Run `scripts/parse_data.py` to normalize any structured input:

```bash
python3 scripts/parse_data.py <input-file> [--format csv|json|auto]
```

Output: normalized JSON with detected metrics, dimensions, and time ranges.

### 2. Analyze & Summarize

Before generating the report, analyze the data:

1. **Key metrics** — Identify top-line numbers (revenue, growth, conversions, etc.)
2. **Trends** — Period-over-period changes (up/down/flat + percentage)
3. **Highlights** — Best-performing items, records, milestones
4. **Concerns** — Underperforming areas, declining trends, anomalies
5. **Context** — Infer reporting period, industry, and audience from data

### 3. Select Report Template

Choose based on user request or data type. See `references/report-templates.md` for detailed templates.

| Template | Best For |
|----------|----------|
| **Performance Review** | Monthly/weekly KPI summaries |
| **Campaign Report** | Marketing campaign results |
| **Project Status** | Development/project progress updates |
| **Analytics Summary** | Website/app analytics overview |
| **Custom** | User-specified structure |

### 4. Generate Report

Structure every report with:

```
# [Report Title]
**Period:** [date range]  |  **Prepared for:** [client name]  |  **Date:** [today]

## Executive Summary
[2-3 sentences: what happened, key takeaway, recommendation]

## Key Metrics
| Metric | Current | Previous | Change |
|--------|---------|----------|--------|
| ...    | ...     | ...      | +X%    |

## [Detailed Sections — template-specific]

## Highlights & Wins
- ...

## Areas for Improvement
- ...

## Recommendations & Next Steps
1. ...
```

### 5. Format Output

**Default output:** Markdown (clean, portable, renders in most tools)

**Other formats on request:**
- **HTML** → Run `scripts/report_to_html.py` for styled HTML with inline CSS
- **Plain text** → Stripped formatting for email body
- **Structured data** → JSON summary of all metrics and analysis

```bash
python3 scripts/report_to_html.py <report.md> [--template default|minimal|branded]
```

## Customization Options

Users can specify:
- **Client name** — appears in header and throughout
- **Reporting period** — "last week", "March 2026", "Q1 2026"
- **Tone** — professional (default), friendly, executive-brief
- **Sections** — include/exclude specific sections
- **Branding** — company name, colors (for HTML output)
- **Comparison** — vs previous period, vs target/goal, vs benchmark
- **Charts** — include ASCII/text charts for key metrics (when data supports it)
- **Language** — generate in specified language

## Data Handling

- Automatically detect metric types (currency, percentages, counts, rates)
- Format numbers appropriately (commas, decimal places, currency symbols)
- Calculate period-over-period changes when historical data is available
- Flag statistical anomalies or significant changes (>20% swings)
- Round appropriately for audience (executives get rounded numbers, analysts get precision)

## Tips

- For executive audiences: lead with the bottom line, keep it to 1 page equivalent
- For marketing reports: emphasize ROI and conversion metrics
- For project status: focus on timeline, blockers, and deliverables
- When data is incomplete: note gaps clearly, don't fabricate numbers
- Include "So what?" after every metric — explain why the number matters
