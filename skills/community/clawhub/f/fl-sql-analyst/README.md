# SQL Analyst — Ask Your Database Anything in Plain English

**"What were our top 10 customers by revenue last quarter?" — answered in seconds, no SQL required.**

Turn questions into queries. Turn data into decisions.

---

## The Problem

Your data is locked inside a database. Getting answers means writing SQL, which means either:
1. You know SQL and spend 10 minutes writing/debugging a query for a simple question
2. You don't know SQL and wait 2 days for the data team to get back to you
3. You export to a spreadsheet and spend an hour with pivot tables

None of these should exist in 2026.

## The Solution

SQL Analyst translates your questions into SQL, runs them, and presents clear results with insights. Works with SQLite, PostgreSQL, and MySQL. Drop in a CSV for instant analysis.

- **"What were our top 10 customers by revenue last quarter?"** — query generated, executed, results formatted
- **"Import sales.csv and show me trends by region"** — CSV imported to SQLite, analysis ready
- **"Compare this month vs last month"** — side-by-side comparison with percentage changes
- **"Save this as 'weekly-metrics'"** — saved, reusable with one command
- **"Explain the query"** — full breakdown of what the SQL does and why

### Key Features

| Feature | Free | Pro ($19/mo) |
|---------|------|-------------|
| Natural language to SQL | 10 queries/day | Unlimited |
| SQLite support | Yes | Yes |
| PostgreSQL/MySQL | -- | Yes |
| Result formatting | Yes | Yes |
| Query explanation | Yes | Yes |
| CSV import to SQLite | -- | Yes |
| Saved query shortcuts | -- | Yes |
| Text-based visualizations | -- | Yes |
| Export results to CSV | -- | Yes |
| Schema auto-discovery | Yes | Yes |

### What It Looks Like

```
> "Top 5 products by units sold this month"

SELECT p.name, SUM(o.quantity) AS units, SUM(o.total) AS revenue
FROM orders o JOIN products p ON o.product_id = p.id
WHERE o.created_at >= '2026-03-01'
GROUP BY p.id, p.name
ORDER BY units DESC LIMIT 5;

 #  Product          Units Sold    Revenue
 1  Widget Pro       1,247         $37,410.00
 2  Gadget Max       892           $44,600.00
 3  Basic Plan       756           $7,560.00
 4  Pro Upgrade      543           $27,150.00
 5  Enterprise Add   234           $46,800.00

Insight: Gadget Max has fewer units but highest revenue ($50/unit avg).
Enterprise Add has the highest unit value at $200/unit.
```

### Why SQL Analyst?

- **No SQL knowledge needed.** Ask in English, get answers. (But you'll learn SQL along the way — every query is shown and explained.)
- **Multi-database.** SQLite for quick analysis, PostgreSQL and MySQL for production data. Same natural language interface.
- **CSV to insights in 30 seconds.** Drop a CSV, get a queryable table. No import wizards, no column mapping dialogs.
- **Save and reuse.** Named query shortcuts for reports you run weekly. "Run weekly-metrics" and done.
- **Safe by default.** Read-only queries only. Destructive operations require explicit confirmation.
- **Local and private.** Your data stays on your machine. No cloud analytics platform harvesting your business data.

### Who It's For

- Founders who need quick answers from their database
- Product managers who are tired of waiting for the data team
- Developers who want to explore data without writing SQL from scratch
- Analysts who want to prototype queries faster
- Anyone with a CSV they need to make sense of

---

## Getting Started

1. Install the skill in OpenClaw
2. Point it at your database (or drop in a CSV)
3. Ask a question in plain English
4. Get answers.

## Supported Databases

- **SQLite** — built-in, zero config, perfect for CSV analysis
- **PostgreSQL** — connect with standard connection string
- **MySQL** — connect with standard connection string

## Tags

`sql` `analytics` `data` `database` `queries` `sqlite` `postgresql` `mysql` `csv` `reporting` `bi`

---

*Built by [@felipe_bmottaa](https://threads.net/@felipe_bmottaa) — because your data should answer questions, not create them.*
