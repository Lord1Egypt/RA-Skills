---
name: cninfo-report-downloader
description: >-
  Batch-download formal A-share annual and semiannual report PDFs from
  CNInfo (巨潮资讯) using a stock-code CSV. Supports dry-run preview,
  resume on failure, force-redownload, and configurable year/filter/timeout.
  Use when the user needs to fetch, re-fetch, or inspect CNInfo report
  PDFs for A-share listed companies.
---

# CNInfo Report Downloader（巨潮资讯报告下载）

批量下载A股上市公司年报/半年报 PDF（数据源：巨潮资讯 cninfo.com.cn）。

## When to activate

- User wants to download A-share annual or semiannual reports
- User mentions 巨潮、cninfo、年报下载、半年报、annual report
- User needs to batch-fetch report PDFs from a stock-code list

## Prerequisites

```bash
pip install -r requirements.txt
```

## Workflow

1. Confirm that a stock CSV exists and that its **first column** contains stock codes (6-digit A-share codes).
2. If unsure, run `--dry-run` first to preview matches without downloading.
3. Run the command from the skill directory. The script tracks progress in SQLite and can resume after interruption.
4. Check `runtime/manifest_<year>.csv` and `runtime/logs/cninfo_<year>.log` after the run.
5. Consult [references/filter_rules.md](references/filter_rules.md) only when adjusting title matching, naming, or reset behavior.

## Commands

**Normal download (default year 2025):**

```bash
python scripts/run_cninfo_reports.py --stock-csv <path-to-csv>
```

**Dry-run (preview only, no download):**

```bash
python scripts/run_cninfo_reports.py --stock-csv <path-to-csv> --dry-run
```

**Specify year:**

```bash
python scripts/run_cninfo_reports.py --stock-csv <path-to-csv> --year 2024
```

**Force redownload (ignore cache):**

```bash
python scripts/run_cninfo_reports.py --stock-csv <path-to-csv> --force-redownload
```

**Full CLI options:**

| Argument | Default | Description |
|---|---|---|
| `--year` | 2025 | Target report year |
| `--stock-csv` | `上市公司基础信息.csv` | CSV with stock codes in column 1 |
| `--output-dir` | `downloads/<year>` | PDF output directory |
| `--runtime-dir` | `runtime` | State, manifest, logs directory |
| `--page-size` | 20 | Search results per page |
| `--sleep-seconds` | 1.2 | Min delay between requests |
| `--timeout-seconds` | 30 | HTTP timeout |
| `--max-retries` | 5 | HTTP retry attempts |
| `--dry-run` | false | Preview matches without downloading |
| `--force-redownload` | false | Re-download even if file exists |

## Features

- **Smart title filtering** — regex-based matching for formal annual/semiannual reports; auto-rejects summaries, English variants, ESG reports, notices, etc.
- **Breakpoint resume** — SQLite state tracks search progress and download status per announcement; resumes after interruption.
- **Manifest output** — `runtime/manifest_<year>.csv` with full metadata for every eligible report.
- **Idempotent naming** — `{code}_{year}_{kind}.pdf` for primary files, extra variants get `_{announcement_id}` suffix.

## Architecture

```
scripts/
  run_cninfo_reports.py          # Entry point
  cninfo_annual_reports/
    cli.py                       # Argument parsing & logging
    config.py                    # AppConfig dataclass
    service.py                   # Core orchestration logic
    repository.py                # SQLite state management
    http_client.py               # CNInfo API & file download
    models.py                    # Data models
    filters.py                   # Title evaluation & regex
references/
  filter_rules.md                # Detailed filter/reset docs
agents/
  openai.yaml                    # Codex integration config
```

## Reset

To restart from scratch, delete state files:

```bash
rm runtime/state.db runtime/state.db-wal runtime/state.db-shm
```
