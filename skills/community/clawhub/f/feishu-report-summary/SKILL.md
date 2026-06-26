---
name: feishu-report-summary
description: Read Feishu work-report data through the Report v1 API and turn it into daily or weekly summaries. Use when Codex needs to work with `oa.feishu.cn/report/...` entries, summarize team日报/周报, inspect report rules, or automate recurring digest generation from Feishu reports because the stock OpenClaw Feishu plugin does not expose report tools directly.
---

# Feishu Report Summary

Use this skill when the user wants a summary of Feishu 汇报 data and the source link is under `oa.feishu.cn/report/...`. The bundled script calls the Feishu Report API directly, using the same credentials already stored in `~/.openclaw/openclaw.json`.

## Workflow

1. Run `scripts/fetch_report_tasks.js` for the target day or range.
2. Prefer `--format json` when you will analyze the results in-model.
3. Prefer `--format markdown` when the output will be reviewed or copied directly.
4. Summarize with the structure in [references/summary-template.md](references/summary-template.md) unless the user asks for a different format.
5. If the user wants the digest published back to Feishu, use existing `feishu_doc` or `feishu_chat` tools after the summary is drafted.

## Quick Start

Fetch today's local-calendar reports as JSON:

```bash
node scripts/fetch_report_tasks.js --format json
```

Fetch one day and cap the export:

```bash
node scripts/fetch_report_tasks.js --date 2026-03-14 --max-items 50 --format json
```

Fetch one rule for the last 7 days and render Markdown:

```bash
node scripts/fetch_report_tasks.js --days 7 --rule-name "研发团队工作日报" --format markdown
```

Write the export to a file for later review:

```bash
node scripts/fetch_report_tasks.js --date 2026-03-14 --output /tmp/feishu-report.md
```

## Script Notes

- The script reads Feishu credentials from `~/.openclaw/openclaw.json` by default.
- Use `--account-id` when multiple Feishu accounts are configured.
- `--date`, `--start-date`, `--end-date`, and `--days` use the machine's local timezone.
- Use `FEISHU_APP_ID` and `FEISHU_APP_SECRET` only when you need to override config values.
- The script resolves `--rule-name` to a rule ID before querying tasks so the final query stays precise.

## Expected Output

The JSON payload contains:

- query range metadata
- resolved filters
- task counts grouped by rule and reporter
- normalized task entries with field names and pretty-printed field values

Use that payload to produce a concise digest that highlights:

1. common themes
2. completed work
3. blockers or risks
4. next actions
5. people or teams that need follow-up
