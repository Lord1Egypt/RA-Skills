---
name: competitive_analysis
description: Poll competitive crawl triggers, aggregate the last 6 months of product, review, and QA data by category, produce structured analysis context and a report skeleton, upload outputs to OSS, then send a DingTalk summary. Use for database-driven scheduled competitor analysis in OpenClaw.
compatibility: Requires Python 3.10+, PostgreSQL access, OSS access, and a DingTalk webhook.
metadata: {"openclaw":{"requires":{"bins":["python3"],"env":["COMPETITIVE_ANALYSIS_DSN","DINGTALK_WEBHOOK","OSS_ENDPOINT","OSS_BUCKET","OSS_ACCESS_KEY_ID","OSS_ACCESS_KEY_SECRET"]}},"owner":"bbt","skillType":"enterprise","reportTemplate":".docs/竞品分析/BUBBLETREE儿童枕市场机会分析报告.pdf"}
---

# Competitive Analysis

## Use When

- The competitor analysis tables already exist.
- You need to poll `competitive_crawl_trigger` on a schedule.
- You need standardized reports grouped by `category`.
- You need to send summaries to a DingTalk robot.

Do not use this skill for:

- one-off ad hoc analysis
- open-ended research without database inputs
- flexible report generation without a fixed template

## Required Inputs

- Database connection: `COMPETITIVE_ANALYSIS_DSN`
- OSS endpoint: `OSS_ENDPOINT`
- OSS bucket: `OSS_BUCKET`
- OSS access key id: `OSS_ACCESS_KEY_ID`
- OSS access key secret: `OSS_ACCESS_KEY_SECRET`
- DingTalk webhook: `DINGTALK_WEBHOOK`
- Optional DingTalk signing secret: `DINGTALK_SECRET`
- In OpenClaw, prefer environment injection through `skills.entries.competitive_analysis.env`

## Goal

1. Find unconsumed trigger rows where `status='success'`.
2. Load the last 6 months of product, review, and QA data.
3. Aggregate results by `category`.
4. Produce `analysis_context.json` for the host to continue narrative generation.
5. Generate a `Markdown/HTML` skeleton that follows the reference PDF structure.
6. Send a DingTalk summary.
7. Mark trigger rows as consumed after success.

## Entry Points

Primary command:

`python3 {baseDir}/scripts/run_report.py`

Common arguments:

- `--category CATEGORY`
- `--since-months 6`
- `--limit 20`

## Files

- `SKILL.md`: skill entry instructions
- `references/report-outline.md`: report structure contract
- `references/data-contract.md`: data contract and field expectations
- `references/openclaw-setup.md`: OpenClaw setup example
- `scripts/run_report.py`: main CLI
- `scripts/render_report.py`: Markdown/HTML rendering
- `scripts/send_dingtalk.py`: DingTalk delivery
- `analysis_context.json`: structured analysis context for the host runtime

## Rules

- Follow the reference PDF for section order.
- If fields are missing, keep the section and mark values as `未采集` or `待补充`.
- Keep the CLI stateless and let an external scheduler trigger it.
- Do not call any external LLM API from the script.
- Let the host runtime generate deeper narrative content from `analysis_context.json` and `references/report-outline.md`.
- In OpenClaw, prefer host-managed environment injection over `.env`.

## Minimal Workflow

1. Read `references/data-contract.md`.
2. Confirm that the trigger table already includes the consumption fields.
3. Configure `skills.entries.competitive_analysis.env` as shown in `references/openclaw-setup.md`.
4. Start a new OpenClaw session so the skill reloads.
5. Run `python3 {baseDir}/scripts/run_report.py` or invoke it from an external scheduler.
6. Read the generated `analysis_context.json`.
7. Let the host runtime generate the final narrative based on `references/report-outline.md`.
8. Validate the final output against the report outline.

## Success Criteria

- New successful trigger rows are detected.
- Reports are generated per `category`.
- Section structure matches the reference report.
- DingTalk receives the summary message.
- Trigger rows are marked as consumed.
