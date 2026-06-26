---
name: clicky-analytics
description: Fetch website analytics from Clicky (clicky.com) via their REST API. Use when the user asks about website traffic, visitors, pageviews, top pages, bounce rate, search rankings, traffic sources, countries, or any Clicky analytics data. Also use for scheduled analytics reports or comparing traffic across date ranges.
metadata: {"openclaw":{"emoji":"📊","primaryEnv":"CLICKY_SITEKEY","requires":{"bins":["curl"],"env":["CLICKY_SITE_ID","CLICKY_SITEKEY"]}}}
---

# Clicky Analytics

Fetch analytics from the Clicky API. Supports multiple sites via environment variables.

## Setup

Store site credentials as environment variables. Use the naming convention `CLICKY_<NAME>_SITE_ID` and `CLICKY_<NAME>_SITEKEY`:

```bash
# In ~/.openclaw/.env or your shell profile
CLICKY_ENVELOPEBUDGET_SITE_ID=101427673
CLICKY_ENVELOPEBUDGET_SITEKEY=c287a01cc00f70cb
CLICKY_ZAPYETI_SITE_ID=99999999
CLICKY_ZAPYETI_SITEKEY=abc123def456
```

For a single default site, use:
```bash
CLICKY_SITE_ID=101427673
CLICKY_SITEKEY=c287a01cc00f70cb
```

## Usage

```bash
# Named site (reads CLICKY_<NAME>_SITE_ID and CLICKY_<NAME>_SITEKEY env vars)
scripts/clicky.sh envelopebudget visitors,actions-pageviews

# Default site (reads CLICKY_SITE_ID and CLICKY_SITEKEY env vars)
scripts/clicky.sh default visitors,actions-pageviews

# With options
scripts/clicky.sh envelopebudget pages --date last-7-days --limit 20
scripts/clicky.sh envelopebudget visitors --date 2026-03-01,2026-03-13 --daily
```

### Options
- `--date DATE` — today, yesterday, last-7-days, last-30-days, YYYY-MM-DD, or range YYYY-MM-DD,YYYY-MM-DD
- `--limit N` — max results (default 50, max 1000)
- `--daily` — break results down by day
- `--page N` — paginate through results

### Combine types in one request
Use commas: `visitors,visitors-unique,actions-pageviews,bounce-rate,time-average-pretty`

## Common Reports

| Report | Types |
|--------|-------|
| Overview | `visitors,visitors-unique,actions-pageviews,bounce-rate,time-average-pretty` |
| Content | `pages,pages-entrance,pages-exit` |
| Traffic | `traffic-sources,links-domains,searches,countries` |
| SEO | `searches,searches-rankings,searches-keywords` |

## API Reference

See `references/api-types.md` for all available data types, date formats, and limits.
