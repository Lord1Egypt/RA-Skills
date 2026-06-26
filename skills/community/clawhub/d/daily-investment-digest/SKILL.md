---
name: daily-investment-digest
description: Fetch financing event lists from the iYiou skill API and generate daily or recent-N-days financing reports in Markdown to stdout. Use when the task asks to pull investment/financing events via `https://api.iyiou.com/skill/info?page=...&pageSize=...`, deduplicate records, default to yesterday for single-day reports, and support recent 2-7 day windows by fetching up to the hard limit of 250 records and filtering by `createdAt`.
---

# Daily Investment Digest

## Overview

- Pull investment/financing events from `https://api.iyiou.com/skill/info`.
- Normalize fields, deduplicate rows, and generate a structured Chinese investment report.

## Workflow

1. One-command full report (recommended, default uses yesterday).
```bash
node "{baseDir}/scripts/run_full_report.mjs" \
  --max-page 5
```

2. If user explicitly asks for today's report, pass today's date.
```bash
node "{baseDir}/scripts/run_full_report.mjs" \
  --report-date 2026-03-11 \
  --max-page 5
```

3. If user asks for recent 2-7 days, use `--recent-days`.
```bash
node "{baseDir}/scripts/run_full_report.mjs" \
  --recent-days 7
```

4. Direct output mode (stdout only, no file).
```bash
node "{baseDir}/scripts/fetch_events.mjs" \
  --recent-days 3 \
  --stdout-json | \
node "{baseDir}/scripts/generate_report.mjs" \
  --input-json - \
  --top-n 0 \
  --stdout
```

## Path Safety

- Always call scripts with quoted `{baseDir}` paths to avoid whitespace-path issues.
- Scripts resolve relative input paths against the skill root directory.

## Required API Rules

- Use `pageSize=10`.
- Start at `page=1`.
- Increment `page` by 1 each request.
- Single-day mode: stop when `page>5` or API event list is empty.
- Recent-N-days mode (`N=2..7`): fetch up to the hard limit of 250 records, i.e. `pageSize=10` and `page<=25`, then filter by `createdAt`.
- Parse response strictly by schema: `response.code` -> `response.data.posts`.
- Treat non-zero `code` as API failure.
- Retry failed requests up to 3 times before skipping a page.

## Script Interfaces

### `scripts/run_full_report.mjs`

- One-command pipeline: fetch + generate
- Defaults to full output (`top-n=0`)
- Supports `--report-date`, `--recent-days`, `--max-page`, `--page-size`, `--timeout-seconds`, `--retry`, `--delay-seconds`
- Supports `--top-n` (`0` means all events)

### `scripts/fetch_events.mjs`

- `--page-size` default `10`
- `--max-page` default `5` for single-day mode, forced to `25` for recent-N-days mode
- `--report-date` default yesterday (`YYYY-MM-DD`) and acts as range end date
- `--recent-days` supports `1..7`; `1` means a single-day report, `2..7` means recent-N-days report
- `--timeout-seconds` default `15`
- `--retry` default `3`
- `--delay-seconds` default `0`
- Always prints JSON to stdout (`--stdout-json` kept only for compatibility)
- Numeric args are bounded for safety: `recent-days[1,7]`, `page-size[1,100]`, `max-page[1,25]`, `retry[1,10]`

### `scripts/generate_report.mjs`

- `--input-json` required
- `--top-n` default `0` (`0` means all events)
- Always prints report text to stdout (`--stdout` kept only for compatibility)
- Numeric args are bounded for safety: `top-n[0,500]`

## Output Files

- Disabled by design. This skill is stdout-only and does not write report artifacts to disk.

## Data Mapping

- Follow [field_mapping.md](references/field_mapping.md) for source-to-target mapping and fallback rules.
- To reduce context size, the fetch output keeps only: `brief`, `createdAt`, `originalLink`, `postTitle`, `tags`.

## Failure Handling

- Continue on single-page failure after retries.
- Use progressive retry backoff (`0.5s`, `1.0s`, `1.5s`, ...).
- Record page-level errors in output JSON `meta.errors`.
- Generate a report even when no events are found, and clearly mark it as an empty-day report.

## Output Policy

- Date policy: default to yesterday for single-day reports; only use today when the user explicitly asks for today.
- Window policy: support `最近两天`、`最近三天` ... `最近一周` by mapping to `--recent-days 2..7`.
- If user asks full detail, run with `--top-n 0`.
- Use script stdout as the main body and keep event entries unchanged.
- The scripts are responsible only for fetching, filtering, deduplicating, and rendering the event list plus basic statistics.
- The ending section `投资事件总结` must be added by the AI in the final response, not by the scripts.
- Output order is mandatory:
1. First output the full event list.
2. Each event must include: `公司简称`、`轮次`、`投资方`、`事件摘要`、`来源链接`.
3. After the full event list, the final AI response must append one ending section titled `投资事件总结`.
- Do not place `投资事件总结` before event entries.

## Quick Checks

1. Run fetch step and confirm `meta.total_unique_events > 0` on active days.
2. In recent-N-days mode, confirm `meta.recent_days` and `meta.range_start_date` are present and `max_page=25`.
2. Run report step and confirm stdout contains:
- `核心数据概览`
- `融资事件按行业分类`
3. In final AI response, confirm order:
- Event list appears first and each item includes `公司简称`、`轮次`、`投资方`、`事件摘要`、`来源链接`.
- `投资事件总结` appears only after the event list.
- `投资事件总结` appears exactly once at the end.
4. In final AI response, confirm the AI appends:
- `投资事件总结`

## Example End-to-End Command

```bash
node "{baseDir}/scripts/run_full_report.mjs" \
  --recent-days 7
```
