# SQLite Mode

This mode upgrades local CLS persistence into a raw-first SQLite model.

## Current architecture

### Source of truth
- `telegraph_raw_main`
  - deduplicated raw-first main table
  - stores the original raw JSON plus many original NodeAPI fields

### Ingest audit log
- `telegraph_raw_log`
  - keeps every capture event
  - used for replay, audit, and debugging
  - current lifecycle policy: keep online for `30 days`, then delete directly (no archive retention)

### Query surface
- `v_telegraph_main`
  - query view built on top of `telegraph_raw_main`
  - exposes convenient derived fields such as:
    - `is_red`
    - `telegraph_type`
    - `published_at`

## Goals

- No duplicate records in the source-of-truth main table
- No missing records caused by short live windows, as long as ingest cadence is fast enough
- Preserve raw ingest logs for audit and replay
- Keep a richer raw field set in the main table
- Support fast queries for 1-hour / 24-hour / red / hot lookups through the view layer

## Current recommended cadence

Default: every 5 minutes.

## Stable direct source

Current stable direct source:
- `https://www.cls.cn/nodeapi/telegraphList`

Current constraints:
- single request currently returns about `20` telegraphs
- effective time coverage changes with news density
- direct use of `/v1/roll/get_roll_list` is blocked by signature validation (`签名错误`)

## 2026-03-30 live measurement

Current direct measurement using the project adapter (`fetch_telegraph_list`) shows:
- returned rows: `20`
- latest `ctime`: `2026-03-30 21:50:12`
- earliest `ctime`: `2026-03-30 21:28:20`
- effective single-batch span: about `21.87 minutes`

Practical implication:
- `5-minute` ingest is currently the safer default
- `10-minute` ingest has materially higher miss risk during active windows because the overlap margin is much smaller

## Ingest command

```bash
python3 skills/cailianpress-unified/scripts/cls_sqlite_ingest.py
```

## Query commands

```bash
python3 skills/cailianpress-unified/scripts/cls_sqlite_query.py telegraph --hours 1 --limit 20
python3 skills/cailianpress-unified/scripts/cls_sqlite_query.py red --hours 24 --limit 20
python3 skills/cailianpress-unified/scripts/cls_sqlite_query.py hot --hours 24 --min-reading 50000 --limit 20
python3 skills/cailianpress-unified/scripts/cls_sqlite_status.py
```

## Storage layout

```text
skills/cailianpress-unified/data/
  telegraph.db
```

## Core tables

- `telegraph_raw_main`: deduplicated raw-first main table
- `telegraph_raw_log`: every ingest event, kept for audit
- `telegraph_subjects`: subject relationships
- `telegraph_stocks`: stock relationships
- `telegraph_plates`: plate relationships
- `v_telegraph_main`: main query view

## Raw-first strategy

The main table now keeps more original NodeAPI structure, including:
- `raw_json`
- `tags_json`
- `sub_titles_json`
- `timeline_json`
- `ad_json`
- `assoc_fast_fact_json`
- `assoc_article_url`
- `assoc_video_title`
- `assoc_video_url`
- `assoc_credit_rating_json`
- `stock_list_json`
- `subjects_json`
- `plate_list_json`

This avoids losing useful fields too early.

## Suggested cron

```cron
*/5 * * * * cd /home/tim/.openclaw/workspace && python3 skills/cailianpress-unified/scripts/cls_sqlite_ingest.py >> /tmp/cls_sqlite_ingest.log 2>&1
17 3 * * * cd /home/tim/.openclaw/workspace && python3 skills/cailianpress-unified/scripts/cls_prune_raw_log.py >> /tmp/cls_prune_raw_log.log 2>&1
```

## Dedup strategy

- Source-of-truth main key: `id`
- Update rule: prefer `modified_time`, fallback to `content_hash`
- `telegraph_raw_log` keeps every capture event
- `v_telegraph_main` is the default query surface

## Operational notes

- query normal business lookups from `v_telegraph_main`
- inspect raw fidelity from `telegraph_raw_main.raw_json`
- inspect ingest behavior from `telegraph_raw_log`
- subject totals can exceed unique telegraph count because one telegraph can belong to multiple subjects

## Index strategy

Current performance-critical indexes on `telegraph_raw_main`:
- `idx_raw_main_ctime`
  - accelerates recent-window queries and time-desc scans
- `idx_raw_main_level`
  - accelerates red-record lookups using `level in ('A','B')`
- `idx_raw_main_reading_num`
  - accelerates hot/ranking lookups
- `idx_raw_main_date_key`
  - supports date-key based maintenance and date-bucket operations

Recommended query patterns:
- recent records: filter on `ctime`
- red records: filter on `level`
- hot records: filter/order on `reading_num`

Index maintenance rule:
- do not create duplicate semantic indexes with new names if an equivalent index already exists
- before adding a new index, always inspect `PRAGMA index_list('telegraph_raw_main')`
- after index changes, verify with `EXPLAIN QUERY PLAN`

Example verification:

```bash
sqlite3 skills/cailianpress-unified/data/telegraph.db "PRAGMA index_list('telegraph_raw_main');"
sqlite3 skills/cailianpress-unified/data/telegraph.db "EXPLAIN QUERY PLAN SELECT COUNT(*) FROM telegraph_raw_main WHERE ctime >= strftime('%s','2026-03-29 20:00:00');"
sqlite3 skills/cailianpress-unified/data/telegraph.db "EXPLAIN QUERY PLAN SELECT COUNT(*) FROM telegraph_raw_main WHERE level IN ('A','B');"
```
