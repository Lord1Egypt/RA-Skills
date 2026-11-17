# Engineering Hardening: Migration Ledger, Data Quality, Incremental Import, Permissions & Security

> This file is the engineering-grade hardening layer of file-to-database-skill. Build and runtime modes follow the flows described elsewhere; this file adds the four stages of the data-engineering workflow that are essential even in personal scenarios.

## 1. Migration Ledger

Prevents migrations from being executed twice or out of order.

**Mechanism**:
- `migrations/.applied.json` records every executed migration: `{"001_init": {"applied_at": "...", "checksum": "..."}}`
- Consult the ledger before executing: already applied with a matching checksum → skip; already applied with a changed checksum → **error out and halt** (someone edited a historical migration — a danger signal)
- New migrations queue by sequence number; never rewrite historical migration files; changing the structure = adding `00X_*.sql`
- After executing a migration, run SQLite `VACUUM` / PG `ANALYZE` once (cheap for small databases)

**Rollback rehearsal**: before delivery, actually execute the last migration's down once, then up again, to confirm the rollback script is not decoration. Record the rehearsal result in report.md.

## 2. Data Quality Gates

After seeding, automatically run a set of assertions; on failure, report and stop the pipeline:

| Assertion | Default threshold |
|---|---|
| Row count per table | > 0 (after seed) and consistent with the source file's row count |
| Primary-key null rate | = 0 |
| Key-column null rate | < 5% (which columns count as "key" is set by the methodology/user; FK columns by default) |
| FK referential integrity | dangling references = 0 |
| Value-domain drift | type profile matches the pre-import profile (the import didn't turn text into truncated strings) |

The assertion script outputs `quality_report.json`; failed items list concrete row samples and ask the user to choose "clean and re-import" or "relax the threshold".

## 3. Incremental Import Mode (what when files are updated)

When the user says "the file was updated / there's new data", **never rebuild the database** — take the incremental path:

```
new file → infer_schema.py new profile
   → diff against the old profile (columns added/removed? type changes? row-count changes?)
   → column structure changed → generate a new migration per the methodology (expand-and-contract) → through the migration ledger
   → only new rows      → UPSERT import (deduplicate by primary key; existing rows are updated or skipped per user instruction)
   → after import, re-run the data quality gates → report: X rows added / Y rows updated / Z rows skipped (with reasons)
```

Conflict handling default: primary key already exists → skip and record to `skipped.csv` (conservative default); overwrite only when the user explicitly says "the new file wins".

## 4. Permissions & Security

### 4.1 Connection Credentials
- Database passwords/connection strings **never** go into code, SQL files, reports, or chat — they pass through environment variables or `.env` (added to `.gitignore`)
- When the agent needs a connection, read from environment variables; when credentials are missing, prompt the user to set them up — never request plaintext passwords in conversation
- Before sending the delivery package (data.db / dump.sql / snapshot.html), check: **contains no credentials and no unmasked PII** (see 4.3)

### 4.2 Least Privilege
- SQLite: filesystem permission 0600 (owner-only read/write); check before delivery
- PostgreSQL: day-to-day agent operations use a restricted role (only SELECT/INSERT/UPDATE/DELETE on the target database; no DROP/CREATEROLE); separate DDL from daily operations — builds and migrations use a dedicated admin connection, daily operations use the restricted one
- Supabase: for public-facing projects, ENABLE ROW LEVEL SECURITY on every table; every policy the agent generates is listed explicitly for user review

### 4.3 PII Handling
- The profiling stage (the semantic review of infer_schema.py output) identifies PII columns: emails, phone numbers, national IDs, addresses, birth dates
- Default action: **flag, don't mask** — the ERD and report annotate "PII: email (users table)"; in delivery snapshots, PII columns show only the first 3 characters plus a mask
- When the user explicitly asks to keep full PII, comply, but record in the report "plaintext PII included at user request"
- When delivering the database file itself (data.db), PII is not masked (otherwise the database would be unusable), but **remind** the recipient that the file contains PII and must not be shared publicly

### 4.4 Operation Audit
- `audit.log` (append-only, never overwritten): records the time, SQL (parameterized form), and affected row count of every write operation
- When the user asks "what has been done to this database", the full history can be replayed
- The audit log itself ships with every delivery package (transparency)

### 4.5 SQLite Execution Pitfalls (hit during real testing — mandatory to avoid)

- **Every connection** must execute `PRAGMA foreign_keys=ON` — SQLite does not enforce foreign keys by default; without it, dirty data silently enters the database (hit during the 2026-10-22 end-to-end test)
- **Transaction boundaries**: seed in committed batches — commit base tables (users/products) after import, then import referencing tables (orders); otherwise an orders-import failure rolls back the already-successful base data with it
- `chmod 600 data.db` before delivery; chat platforms may block binary .db files when sending — package as zip by default

## What This Skill Does Not Do (honest boundary)

The following are **generated as configs and scripts, but not executed**:

- Production deployment and monitoring/alerting (generate cron / systemd / slow-query log configs; execution and watch duty belong to humans)
- Load testing (generate million-row bulk-insert and concurrency test scripts; batch runs are handed to the user)
- Capacity planning (provide the estimation formula: row width × estimated rows × growth rate; forecasting needs business data)
- Credential custody and rotation (credentials stay with the user; the agent only reads them via environment variables)
