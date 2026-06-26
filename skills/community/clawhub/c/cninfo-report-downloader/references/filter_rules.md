# Filter Rules

Use this reference only when changing search behavior, title filtering, naming, or reset guidance.

## Input Source

- Read stock codes from the user-provided stock CSV.
- Use the first column only.
- Deduplicate codes.
- Keep only A-share 6-digit codes.

## Search Strategy

- Query CNInfo with `searchkey=<stock_code>`.
- Set `sdate=<year>-01-01`.
- Keep `isfulltext=false`.
- Use page-based traversal until no more pages remain.
- Download matches immediately after the page is processed.

## Title Matching

- Keep only formal Chinese annual and semiannual report titles for the target year.
- The exact regexes and keyword checks live in `scripts/cninfo_annual_reports/filters.py`.
- Allow revision suffixes such as revised, corrected, or updated variants.

## Rejections

Reject titles that are summaries, English variants, notices, roadshow announcements, independent-director reports, audit committee reports, ESG reports, or similar non-report documents.

## Output Naming

- Primary annual file: `{stock_code}_{year}_annual.pdf`
- Primary semiannual file: `{stock_code}_{year}_semiannual.pdf`
- Extra matched versions: `{stock_code}_{year}_{report_kind}_{announcement_id}.pdf`

## Runtime Files

- SQLite state: `runtime/state.db`
- Manifest: `runtime/manifest_<year>.csv`
- Logs: `runtime/logs/cninfo_<year>.log`

## Reset Guidance

- Delete `runtime/state.db`, `runtime/state.db-wal`, and `runtime/state.db-shm` to restart from scratch.
