# Commands

## Install dependencies

```bash
python -m pip install -r /path/to/skill/scripts/requirements.txt
```

## Capture only

```bash
python /path/to/skill/scripts/run_capture_only.py --workspace /path/to/workspace
```

## Report only

```bash
python /path/to/skill/scripts/run_report_only.py --workspace /path/to/workspace
```

## Report only with explicit time window

```bash
python /path/to/skill/scripts/run_report_only.py --workspace /path/to/workspace --time-window "2026-03-15 00:00 to 2026-03-16 08:00"
```

## Report only without AI generation

```bash
python /path/to/skill/scripts/run_report_only.py --workspace /path/to/workspace --disable-ai
```

## Full workflow

```bash
python /path/to/skill/scripts/run_full_workflow.py --workspace /path/to/workspace
```

## Full workflow with time window

```bash
python /path/to/skill/scripts/run_full_workflow.py --workspace /path/to/workspace --time-window "2026-03-15 00:00 to 2026-03-15 18:00"
```

## Full workflow without AI generation

```bash
python /path/to/skill/scripts/run_full_workflow.py --workspace /path/to/workspace --disable-ai
```

## Direct scripts

```bash
python /path/to/skill/scripts/collect_feeds.py
python /path/to/skill/scripts/generate_company_report.py
python /path/to/skill/scripts/generate_international_report.py
```

## Required workspace files

- `config/sources.json`
- `config/international_sources.json`
- `companies.txt`

## Outputs

- `data/YYYY-MM-DD.jsonl`
- `data/domestic_raw_YYYY-MM-DD.jsonl`
- `data/international_raw_YYYY-MM-DD.jsonl`
- `data/international_YYYY-MM-DD.jsonl`
- `reports/company_mentions.xlsx`
- `reports/international_company_mentions.xlsx`
- merged daily Word brief in `reports/`

## Cloud troubleshooting

### No Word file generated

Check these outputs first:

- `reports/company_mentions.xlsx`
- `reports/international_company_mentions.xlsx`

If both Excel files are missing, the problem is earlier in the reporting pipeline.
Check:

- whether `ARK_API_KEY` is available
- whether `data/*.jsonl` exists
- whether the task is using the report-only prompt

If both Excel files exist but the Word file is missing, inspect the brief generation step and whether the target file is locked.

### International report is empty

Check in this order:

1. `data/international_raw_YYYY-MM-DD.jsonl`
2. `data/international_YYYY-MM-DD.jsonl`

If raw exists but filtered does not, the feed was captured but nothing matched the filter.
If raw does not exist, inspect `config/international_sources.json`, network access, and source health.

### Domestic count is too low

Check both:

- `data/YYYY-MM-DD.jsonl`
- `reports/company_mentions.xlsx`

If the data file has many rows but the Excel file has few matches, the issue is usually company matching coverage.
Review `companies.txt` aliases.

### AI fields are empty

Check:

- `ARK_API_KEY`
- whether the run used disable-AI mode
- model/API connectivity

Domestic AI fields are generated in `generate_company_report.py`.
International AI fields are generated in `generate_international_report.py`.

### International item is in Excel but not in Word

This can be expected.
The Word brief only includes:

- items inside the selected time window
- items with successful `AI??`
- only the top 5 international items by impact score

### Time window looks wrong

The report uses the published time stored in Excel, not the capture time.
Check `????` and confirm it falls inside the requested window.

### Duplicate ingestion or repeated items

Check `state/feed_state.json`.
If duplicates keep appearing, the cloud workspace is usually not persistent or multiple runs are using different workspaces.

### Historical data disappeared

Confirm the cloud workspace persists these folders:

- `data/`
- `reports/`
- `snapshots/`
- `state/`

### Recommended debugging order

1. `state/feed_state.json`
2. `data/*.jsonl`
3. `data/international_*.jsonl`
4. `reports/company_mentions.xlsx`
5. `reports/international_company_mentions.xlsx`
6. `reports/AI????_YYYY-MM-DD.docx`

## OpenClaw prompt templates

Capture job:

```text
Use $ai-news-pipeline to run capture only in the current workspace. Collect domestic RSS news and international RSS news, deduplicate them, write domestic raw and incremental files, write international raw and filtered incremental files, save feed snapshots, and update feed state metrics. Do not generate Excel or Word reports in this run.
```

Report delivery job:

```text
Use $ai-news-pipeline to run report generation only in the current workspace for the reporting window from yesterday 00:00 to today 08:00. Build the cumulative domestic Excel report, build the cumulative international Excel report with AI title, AI summary, and impact score, then generate the merged Word brief. The Word file should include all domestic items in the window and only the top 5 international items by impact score in the window. Exclude any international item that does not have a successful AI summary.
```

Report delivery job with explicit time window:

```text
Use $ai-news-pipeline to run report generation only in the current workspace for the time window "2026?3?15?0??2026?3?16?8?". Update the domestic Excel report, update the international Excel report with AI title, AI summary, and impact score, and rebuild the merged Word brief using only items whose published time falls inside that window.
```
