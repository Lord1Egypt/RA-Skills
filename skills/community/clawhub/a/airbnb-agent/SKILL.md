---
name: airbnb-agent
slug: airbnb-agent
version: 1.0.2
description: Search Airbnb listings, filter short-term rentals, and analyze detail pages for parking, basement, and renovation signals.
---

# Airbnb Agent

Search Airbnb via pyairbnb API, filter listings, and inspect detail pages without login or browser automation.

## When to Use

Use for Airbnb rental searches, shortlist comparison, coordinate-based filtering, and listing detail analysis when login-only data is not required.

## Setup

```bash
bash scripts/setup.sh
```

Creates `.venv/` with `pyairbnb` + `curl-cffi`.

## Quick Reference

| Topic | File |
|-------|------|
| Usage, parameters, and limitations | `references/api-fields.md` |
| API fields and common coordinates | `references/api-fields.md` |

## Core Rules

1. Run setup first if `.venv/` is missing.
2. Search by coordinate box; ask for or derive center coordinates before running.
3. Treat detail keyword matches as signals, not verified facts.
4. Pass the same dates and guest count to both search and detail analysis.
5. Save JSON outputs and cite listing URLs when summarizing recommendations.

## Workflow

```bash
.venv/bin/python3 scripts/search.py "Brighton" \
  --check-in 2026-08-27 --check-out 2026-09-04 --guests 3 \
  --bedrooms 2 --max-price 20000 --min-rating 4.8 \
  --center-lat 50.8225 --center-lng -0.1373 --max-distance-km 2.5

.venv/bin/python3 scripts/details.py /tmp/airbnb_candidates.json \
  --top 15 --check-in 2026-08-27 --check-out 2026-09-04 --guests 3
```

Outputs:
- `/tmp/airbnb_candidates.json` from search
- `/tmp/airbnb_results.json` from detail analysis
