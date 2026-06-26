---
name: ai-news-pipeline
description: Run a self-contained Chinese and international AI news workflow inside the current workspace. Use when the user wants either high-frequency RSS capture only or scheduled report delivery only, with cumulative Excel outputs and a merged Word brief, without relying on an external local repository path.
---

# AI News Pipeline

## Overview

This skill is executable by itself. The actual workflow scripts are bundled in `scripts/`.
Run them against the current workspace or pass `--workspace /path/to/workspace` explicitly.

## Workspace Requirements

The target workspace should contain or accept these files and folders:

- `config/sources.json`
- `config/international_sources.json`
- `companies.txt`
- `data/`
- `reports/`
- `state/`

If the folders do not exist, the scripts create them.

## Install Dependencies

Install Python dependencies before first use:

```bash
python -m pip install -r /path/to/skill/scripts/requirements.txt
```

## Available Entrypoints

Use the bundled Python entrypoints depending on the job type.

### Capture Only

Use this for high-frequency collection jobs. It only captures feeds, updates deduplication state, and writes raw and incremental data.

```bash
python /path/to/skill/scripts/run_capture_only.py --workspace /path/to/workspace
```

### Report Only

Use this for scheduled delivery jobs. It reads already-collected data, calls the model for summaries and titles, updates the cumulative Excel files, and rebuilds the Word brief.

By default it uses the reporting window from yesterday 00:00 to today 08:00.

```bash
python /path/to/skill/scripts/run_report_only.py --workspace /path/to/workspace
```

Optional time window:

```bash
python /path/to/skill/scripts/run_report_only.py --workspace /path/to/workspace --time-window "2026-03-15 00:00 to 2026-03-16 08:00"
```

Optional skip-AI mode:

```bash
python /path/to/skill/scripts/run_report_only.py --workspace /path/to/workspace --disable-ai
```

## Full Workflow

```bash
python /path/to/skill/scripts/run_full_workflow.py --workspace /path/to/workspace
```

Optional time window:

```bash
python /path/to/skill/scripts/run_full_workflow.py --workspace /path/to/workspace --time-window "2026-03-15 00:00 to 2026-03-15 18:00"
```

Optional skip-AI mode:

```bash
python /path/to/skill/scripts/run_full_workflow.py --workspace /path/to/workspace --disable-ai
```

## What Each Entrypoint Does

`run_capture_only.py`
1. Collect domestic RSS items into `data/YYYY-MM-DD.jsonl`.
2. Collect domestic raw items into `data/domestic_raw_YYYY-MM-DD.jsonl`.
3. Collect international raw items into `data/international_raw_YYYY-MM-DD.jsonl`.
4. Filter international items into `data/international_YYYY-MM-DD.jsonl`.
5. Save per-source snapshots in `snapshots/`.
6. Update RSS deduplication and source metrics in `state/feed_state.json`.

`run_report_only.py`
1. Read the selected time window from collected data.
2. Build the cumulative domestic Excel output in `reports/company_mentions.xlsx`.
3. Build the cumulative international Excel output in `reports/international_company_mentions.xlsx`.
4. Call the model to generate domestic AI titles and AI summaries.
5. Call the model to generate international AI titles, AI summaries, and impact scores.
6. Build a merged daily Word brief in `reports/`.

`run_full_workflow.py`
1. Run capture.
2. Run domestic reporting.
3. Run international reporting.

## Inputs

- Domestic RSS config: `config/sources.json`
- International RSS config: `config/international_sources.json`
- Company list: `companies.txt`
- Volcengine key: `ARK_API_KEY`
- Optional model override: `ARK_MODEL`

## Security Review Notes

This skill is designed to run an AI news collection and reporting workflow inside a user-provided workspace.

It accesses external network resources for only two purposes:
1. reading user-configured RSS / Atom feeds to collect public news content;
2. calling a user-configured Volcengine model endpoint to generate AI titles, AI summaries, and impact scores.

It writes local files because it needs to:
1. store raw and incremental collected news data;
2. persist deduplication state so repeated runs do not duplicate items;
3. generate cumulative Excel reports and a Word brief;
4. save feed snapshots and logs for troubleshooting and completeness checks.

It does not upload arbitrary local files from the workspace and does not scan unrelated user content. External requests are limited to user-configured RSS URLs and the user-configured model endpoint.

Credentials are only taken from user-provided configuration, such as RSS authentication data and `ARK_API_KEY`. These credentials are used only at runtime for the intended service and are not forwarded to unrelated destinations.

## Important Behavior

- `state/feed_state.json` controls RSS deduplication.
- Excel files are cumulative.
- The Word brief is rebuilt per run.
- The Word international section only includes the top 5 items by impact score inside the selected time window.
- International items without a successful AI summary are excluded from the Word brief.
- AI cache files are deleted automatically after each run.

## Troubleshooting

1. If the workflow does not rerun old RSS items, check `state/feed_state.json`.
2. If AI columns are empty, check whether `ARK_API_KEY` is set in the execution environment.
3. If the user wants a full rebuild, delete the relevant daily `data` files and `state/feed_state.json`, then rerun.
4. If the user needs exact commands or cloud prompts, read `references/commands.md`.

## References

- `references/commands.md`
