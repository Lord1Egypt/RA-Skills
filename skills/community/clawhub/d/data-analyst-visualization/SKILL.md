---
name: data-analyst-visualization
description: LLM-powered intelligent data analysis assistant supporting natural language queries, SQL generation, visualization, and multi-turn conversation. Suitable for business analysis, report automation, and data exploration. Supports MySQL, PostgreSQL, Snowflake, and Excel/JSON file reading.
---

# Intelligent Data Analysis Assistant

Talk to your data through natural language. No SQL or technical background required for data query, analysis, and visualization.

## Workflow

```
User question → Parse intent → Generate SQL → Execute query → Analyze results → Visualize → Output conclusions
```

## Core Capabilities

### 1. Natural Language → SQL

Chinese questions auto-converted to SQL:

| User Question | SQL |
|---------------|-----|
| "Sales by region last month?" | `SELECT region, SUM(amount) FROM sales WHERE month='2026-04' GROUP BY region` |
| "Which product has the highest return rate?" | `SELECT product, COUNT(*) FROM orders WHERE status='returned' GROUP BY product ORDER BY 2 DESC LIMIT 1` |
| "Compare user growth vs same period last year" | `SELECT DATE_TRUNC('month', created_at), COUNT(*) FROM users WHERE created_at >= NOW() - INTERVAL '1 year' GROUP BY 1 ORDER BY 1` |

### 2. Data Visualization

Results output in two layers:

- **Layer 1**: Inline Markdown summary (metrics table + ASCII trend + conclusions)
- **Layer 2**: Standalone HTML page (Chart.js interactive charts), see [references/visualization-template.md](references/visualization-template.md)

### 3. Multi-turn Conversation

| Mode | Description |
|------|-------------|
| Refine | "Only show East China" → append filter |
| Switch dimension | "Group by month" → re-aggregate |
| Root cause | "Why did it drop?" → drill down |
| Compare | "vs last quarter?" → time comparison |

### 4. File Data Reading

Supports Excel (.xlsx/.xls), JSON/JSONL, CSV file reading. See [references/data-sources.md](references/data-sources.md).

### 5. Database Connections

MySQL / PostgreSQL / Snowflake / SQLite / BigQuery / Redshift. See [references/data-sources.md](references/data-sources.md).

## Output Format

Inline chat output:

```
📊 Results: {title}
─────────────────────────────
{metrics table}

📈 Trend:
{ASCII trend bars}

📋 Analysis:
1. ...
```

For charts, auto-generate HTML page → write to `{domain}_chart.html` → report path.

## Notes

- SQL limited to read-only SELECT
- Privacy fields auto-masked
- Large datasets prompt for LIMIT
- Vague questions trigger clarifying questions
- Uses mock data when no data source configured
- File reading auto-outputs overview (row count, columns, types, first 5 rows)