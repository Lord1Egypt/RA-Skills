---
name: data-pipeline-agent
version: 1.0.0
description: >
  ETL pipeline builder for business data — API extraction, data cleaning,
  transformation, and warehouse loading. Use when you need to move data
  between systems, automate data collection from APIs or CSVs, clean and
  normalize messy datasets, load into databases or warehouses, or schedule
  recurring data syncs. NOT for: real-time streaming (use dedicated streaming
  tools), BI dashboards (use Tableau/Power BI/Looker), raw SQL query writing
  (use direct DB tooling), or one-off manual data exports.
tags:
  - etl
  - data
  - pipeline
  - automation
  - finance
  - api
  - analytics
author: PrecisionLedger
---

# Data Pipeline Agent

Build, run, and monitor ETL (Extract → Transform → Load) pipelines for business data. Specializes in financial data flows, API integrations, and warehouse loading patterns for accounting and operations teams.

## When to Use

- Extracting data from APIs (QBO, Stripe, Salesforce, bank feeds, etc.)
- Cleaning and normalizing messy spreadsheets or CSV exports
- Merging data from multiple sources into one canonical dataset
- Loading transformed data into databases, data warehouses, or Google Sheets
- Scheduling recurring data syncs (daily GL pulls, weekly AR aging refresh, etc.)
- Auditing data quality — detecting nulls, duplicates, type mismatches

## When NOT to Use

- **Real-time streaming** — use Kafka, Kinesis, or Pub/Sub for sub-second latency
- **Interactive dashboards** — this agent outputs data; visualization belongs in BI tools
- **Raw SQL query optimization** — use DBA tooling for query plans and indexes
- **One-off manual exports** — if it happens once, just download the CSV
- **Transactional writes to client systems** — read-only extraction only unless Irfan approves write access

---

## Pipeline Patterns

### Pattern 1: API Extract → Clean → CSV

```python
# Extract from REST API, clean, output CSV
import requests, pandas as pd, json
from datetime import datetime, timedelta

def extract(api_url, headers, params=None):
    """Pull paginated JSON from any REST endpoint."""
    results = []
    while api_url:
        r = requests.get(api_url, headers=headers, params=params)
        r.raise_for_status()
        data = r.json()
        results.extend(data.get("data", data if isinstance(data, list) else [data]))
        api_url = data.get("next_page_url")  # pagination
        params = None  # only pass params on first call
    return results

def clean(records, rename_map=None, drop_nulls_on=None, date_cols=None):
    """Normalize, rename, parse dates, drop nulls."""
    df = pd.DataFrame(records)
    if rename_map:
        df = df.rename(columns=rename_map)
    if date_cols:
        for col in date_cols:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    if drop_nulls_on:
        df = df.dropna(subset=drop_nulls_on)
    df = df.drop_duplicates()
    return df

def load_csv(df, output_path):
    df.to_csv(output_path, index=False)
    print(f"✅ Saved {len(df)} rows → {output_path}")

# Example: QBO Invoice Extract
HEADERS = {"Authorization": "Bearer <TOKEN>", "Accept": "application/json"}
records = extract("https://quickbooks.api.intuit.com/v3/company/<REALM>/query?query=SELECT * FROM Invoice", HEADERS)
df = clean(records, rename_map={"TxnDate": "invoice_date", "TotalAmt": "amount"}, date_cols=["invoice_date"])
load_csv(df, f"data/invoices_{datetime.today().date()}.csv")
```

### Pattern 2: Multi-Source Merge

```python
import pandas as pd

def merge_gl_with_bank(gl_path, bank_path, match_on="amount", date_tolerance_days=3):
    """
    Match GL entries to bank transactions.
    Flags unmatched rows for manual review.
    """
    gl = pd.read_csv(gl_path, parse_dates=["date"])
    bank = pd.read_csv(bank_path, parse_dates=["date"])

    # Merge on amount + date proximity
    merged = pd.merge_asof(
        gl.sort_values("date"),
        bank.sort_values("date"),
        on="date",
        by=match_on,
        tolerance=pd.Timedelta(days=date_tolerance_days),
        direction="nearest",
        suffixes=("_gl", "_bank")
    )

    unmatched_gl = gl[~gl.index.isin(merged.dropna(subset=["date_bank"]).index)]
    unmatched_bank = bank[~bank.index.isin(merged.dropna(subset=["date_gl"]).index)]

    print(f"✅ Matched: {len(merged.dropna())} | ⚠️ Unmatched GL: {len(unmatched_gl)} | Bank: {len(unmatched_bank)}")
    return merged, unmatched_gl, unmatched_bank
```

### Pattern 3: Data Quality Audit

```python
import pandas as pd

def audit_dataset(df, required_cols=None, expected_types=None):
    """
    Run data quality checks. Returns a report dict.
    """
    report = {
        "row_count": len(df),
        "duplicate_rows": int(df.duplicated().sum()),
        "null_summary": df.isnull().sum().to_dict(),
        "issues": []
    }

    if required_cols:
        missing = [c for c in required_cols if c not in df.columns]
        if missing:
            report["issues"].append(f"Missing required columns: {missing}")

    if expected_types:
        for col, dtype in expected_types.items():
            if col in df.columns and not pd.api.types.is_dtype_equal(df[col].dtype, dtype):
                report["issues"].append(f"{col}: expected {dtype}, got {df[col].dtype}")

    # Flag columns with >20% nulls
    for col, nulls in report["null_summary"].items():
        pct = nulls / len(df) * 100
        if pct > 20:
            report["issues"].append(f"{col}: {pct:.1f}% null — review required")

    return report

# Usage
df = pd.read_csv("data/ar_aging.csv")
report = audit_dataset(
    df,
    required_cols=["customer_id", "invoice_date", "amount", "due_date"],
    expected_types={"amount": "float64", "customer_id": "object"}
)
print(report)
```

### Pattern 4: Scheduled Cron Pipeline

```bash
#!/bin/bash
# daily-gl-sync.sh — run via cron or OpenClaw cron tool
# Extracts GL, cleans, loads to SQLite, notifies on error

set -euo pipefail
LOG="logs/gl-sync-$(date +%Y-%m-%d).log"
mkdir -p logs data

echo "[$(date)] Starting GL sync..." | tee -a "$LOG"

python3 pipelines/gl_extract.py >> "$LOG" 2>&1 && \
python3 pipelines/gl_clean.py >> "$LOG" 2>&1 && \
python3 pipelines/gl_load.py >> "$LOG" 2>&1 && \
echo "[$(date)] ✅ GL sync complete" | tee -a "$LOG" || \
echo "[$(date)] ❌ GL sync FAILED — check $LOG" | tee -a "$LOG"
```

### Pattern 5: Load to SQLite / PostgreSQL

```python
import pandas as pd
import sqlite3

def load_to_sqlite(df, db_path, table_name, if_exists="replace"):
    """
    Load DataFrame to SQLite. Use if_exists='append' for incremental loads.
    """
    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists=if_exists, index=False)
    conn.close()
    print(f"✅ Loaded {len(df)} rows → {db_path}::{table_name}")

# PostgreSQL version (requires psycopg2 + sqlalchemy)
from sqlalchemy import create_engine

def load_to_postgres(df, conn_str, table_name, schema="public", if_exists="replace"):
    engine = create_engine(conn_str)
    df.to_sql(table_name, engine, schema=schema, if_exists=if_exists, index=False)
    print(f"✅ Loaded {len(df)} rows → {schema}.{table_name}")
```

---

## Common Business Pipelines

### AR Aging Refresh Pipeline

```
1. Extract: QBO Invoices API → raw JSON
2. Transform: Calculate days_outstanding, aging_bucket (0-30, 31-60, 61-90, 90+)
3. Enrich: Join with customer contact data
4. Load: Google Sheets "AR Aging" tab + SQLite archive
5. Alert: Flag invoices >60 days for follow-up queue
```

### Bank Feed Reconciliation Pipeline

```
1. Extract: Bank API (Plaid/CSV export) + QBO GL
2. Transform: Normalize dates, amounts, memo fields
3. Match: Fuzzy join on amount + date (±3 days tolerance)
4. Flag: Unmatched transactions → manual review CSV
5. Load: Reconciliation log → SQLite + email summary
```

### Payroll → GL Mapping Pipeline

```
1. Extract: Payroll system CSV export (Gusto, ADP, etc.)
2. Transform: Map payroll codes → GL account numbers
3. Validate: Totals match payroll register
4. Load: Journal entry template → QBO batch import format
5. Archive: Raw + transformed files in dated folder
```

---

## Pipeline Design Checklist

Before building any pipeline:

- [ ] **Idempotency** — Can the pipeline re-run without duplicating data?
- [ ] **Error handling** — What happens if the API is down? Partial load?
- [ ] **Logging** — Is every step logged with timestamps?
- [ ] **Data quality** — Are nulls, duplicates, and type mismatches caught?
- [ ] **Reversibility** — Can the load be rolled back if something goes wrong?
- [ ] **Rate limits** — Does the source API have call limits? Add retry logic.
- [ ] **Secrets** — Are API keys in env vars, not hardcoded?
- [ ] **Schedule** — How often does this run? Who monitors it?

---

## Data Cleaning Quick Reference

| Problem | Solution |
|---|---|
| Mixed date formats | `pd.to_datetime(col, infer_datetime_format=True)` |
| Currency strings ("$1,234.56") | `col.str.replace(r'[$,]', '', regex=True).astype(float)` |
| Duplicate rows | `df.drop_duplicates(subset=['id'])` |
| Null amounts | `df['amount'].fillna(0)` or `df.dropna(subset=['amount'])` |
| Inconsistent casing | `df['name'].str.strip().str.title()` |
| Leading/trailing spaces | `df.apply(lambda x: x.str.strip() if x.dtype == 'object' else x)` |
| Outlier detection | `df[df['amount'].between(df['amount'].quantile(.01), df['amount'].quantile(.99))]` |

---

## Scheduling with OpenClaw Cron

```
# Daily GL sync at 6 AM CST
Schedule: cron "0 6 * * *" tz=America/Chicago
Payload: agentTurn — "Run the daily GL sync pipeline in ~/workspace/pipelines/"
Delivery: announce to Telegram on completion or failure
```

---

## Dependencies

Install Python data stack:

```bash
pip install pandas requests sqlalchemy psycopg2-binary openpyxl xlrd
# For Google Sheets
pip install gspread gspread-dataframe google-auth
# For Plaid bank feeds
pip install plaid-python
```

---

## File Organization

```
workspace/
  pipelines/
    gl_extract.py
    gl_clean.py
    gl_load.py
    ar_aging.py
    bank_reconcile.py
  data/
    raw/          ← API responses, CSV imports (never edited)
    processed/    ← cleaned, transformed data
    archive/      ← date-stamped historical snapshots
  logs/
    pipeline-YYYY-MM-DD.log
  scripts/
    run-daily-pipelines.sh
```

---

## Safety Rules

1. **Extract is always read-only.** Never write to source systems during extraction.
2. **Archive raw data** before any transformation — keep the original.
3. **Validate row counts** before and after each transformation step.
4. **Test on sample data** (10-100 rows) before running full pipeline.
5. **Client system writes require Irfan approval** — QBO, bank APIs, payroll systems are extract-only by default.
6. **Never hardcode credentials** — use environment variables or 1Password CLI.
