---
name: cross-channel-daily-review
description: Create a simple, repeatable daily review workflow across whatever conversation surfaces are available. Use when a user wants one raw note per source, one merged daily summary, index maintenance, verification, and an optional short management update for a preferred destination. Best for recurring 24-hour review workflows that should stay reusable, channel-agnostic, easy to verify, and safe to publish.
---

# Cross-Channel Daily Review

## Overview

Use this skill to run a reusable, channel-agnostic daily review workflow:

1. Discover or accept a set of channels.
2. Create one raw review file per channel.
3. Generate one synthesized cross-channel review.
4. Update a machine-readable index.
5. Generate a boss-mode summary for one primary delivery channel.
6. Verify outputs before claiming success.

Default design:
- **Primary destination:** use the configured preferred destination if present
- **Delivery mode:** `boss-primary`
- **Review window:** last 24 hours
- **Missing sources:** record explicitly; never silently skip them.

## When to use this skill

Use this skill when the user asks for any of the following:
- “做全渠道每日复盘 / daily cross-channel review”
- “把不同渠道分别复盘，再统一汇总”
- “老板模式摘要 / boss summary / management summary”
- “把 raw、synthesized、index 都生成出来”
- “让这个流程可复用、可发布、可适配不同渠道”
- “每天固定时间自动复盘并推送”

## Workflow

### Step 1 — Resolve channels

First decide the channel set:

- Prefer **auto-discovery** from available sessions, delivery contexts, or user-provided channel list.
- If the user explicitly names channels, trust that list.
- Do **not** hardcode a small fixed list of apps as the only valid sources.
- Normalize source names to lowercase slugs that match the environment.

Read `references/channel-adapter-spec.md` before implementing or extending channel handling.

### Step 2 — Collect and normalize channel evidence

For each candidate channel, gather:
- time window
- source references (session path, session key, channel id, or equivalent)
- conversational **scope** inside the channel (DM / group / thread / room / topic)
- participant shape (single bot, multi-bot, workflow group chat, etc.) when knowable
- a concise raw excerpt or evidence summary
- collection status: `active` | `configured` | `missing` | `collection_failed`

Normalize each channel into the common object shape described in `references/channel-adapter-spec.md`.

Important:
- do **not** assume one channel has only one bot
- do **not** assume one channel maps to one conversation
- support multiple bots and multiple sessions inside the same channel scope

### Step 3 — Write raw review files

Write one file per channel under:

```text
memory/daily-review/raw/YYYY/MM/<channel>_YYYY-MM-DD.md
```

Use `scripts/write_raw_reviews.py` with normalized JSON when possible.

Rules:
- Always write one file per resolved channel.
- If a channel has no confirmed data, still write a file with `状态：未检出` or failure reason.
- Include the checked sources. Do not silently omit missing channels.

Template: `assets/raw-template.md`

### Step 4 — Generate the synthesized review

Create exactly one synthesized report for the date:

```text
memory/daily-review/synthesized/YYYY/MM/YYYY-MM-DD.md
```

The report must cover these 5 dimensions:
1. ❌ 做错了什么
2. ⚠️ 没做好的地方
3. ✅ 做得好的地方
4. 📝 遗漏事项
5. 💡 改进建议

Use `assets/synthesized-template.md` and `references/review-dimensions.md`.

### Step 5 — Update the index

Update or append the record in:

```text
memory/daily-review/index.json
```

Prefer `scripts/update_index.py`.

Index records should capture at least:
- date
- active channels
- missing channels
- synthesized file path
- boss summary path (if built)
- verification status

### Step 6 — Build boss-mode summary

Build a shorter management summary from the synthesized report.

Default behavior:
- `delivery_mode = boss-primary`
- `boss_channel = primary`

If the user configured a preferred destination, use it.
If that destination is unavailable, fallback to the first verified available destination and state that clearly.

Use `scripts/build_boss_summary.py` and `assets/boss-summary-template.md`.

### Step 7 — Verify before reporting success

Run verification with `scripts/verify_outputs.py` before claiming completion.

Minimum checks:
- raw files exist for all resolved channels
- synthesized file exists and is non-empty
- index updated successfully
- boss summary exists if requested
- delivery target resolved successfully

Never report “done” without verification output.

## Delivery modes

Read `references/delivery-modes.md` when choosing output behavior.

Supported modes:
- `boss-primary` — send only to one primary channel; default
- `broadcast` — send to multiple channels
- `generate-only` — write outputs but do not push externally

## Formatting rules

Read `references/formatting-standard.md` when generating user-visible summaries.

Hard rules:
- Keep sections clearly separated.
- One major numbered point per paragraph block.
- Do not collapse everything into one dense wall of text.
- Put the final action checklist in a standalone `text` code block when needed.

## Failure handling

Read `references/failure-handling.md` when anything is missing or degraded.

Important:
- Distinguish `missing` from `collection_failed`.
- Distinguish “no recent data” from “channel not configured”.
- If delivery falls back from a preferred destination to another verified destination, state it explicitly.

## Resources

### scripts/
- `discover_channels.py` — scan real OpenClaw session transcripts and produce channel candidates
- `score_discovery_confidence.py` — attach confidence scores to channel/scope inference results
- `normalize_channel_data.py` — normalize channel metadata to one schema
- `write_raw_reviews.py` — write per-channel raw review markdown files
- `update_index.py` — create/update `index.json` (daily / weekly / monthly)
- `synthesize_review.py` — generate one synthesized cross-channel review from normalized scope-aware data
- `render_periodic_summary.py` — generate weekly or monthly rollup summaries
- `plan_retention.py` — produce retention/archive candidates from index policy
- `verify_retention_readiness.py` — check whether a month is ready for archive/cleanup
- `archive_daily_layer.py` — archive eligible daily raw / synthesized / boss outputs into archive tree
- `mark_archived_records.py` — mark archived daily records inside index metadata
- `render_cron_plan.py` — render the recommended cron automation chain for this skill
- `run_retention_cycle.py` — run planner + readiness + archive + mark as one lifecycle step
- `build_boss_summary.py` — render management summary markdown from synthesized metadata
- `resolve_delivery_target.py` — resolve requested destination with safe fallback
- `verify_outputs.py` — verify expected outputs exist and are non-empty

### references/
- `architecture.md` — system model and data flow
- `channel-adapter-spec.md` — normalized channel schema and adapter contract
- `review-dimensions.md` — criteria for the 5 review dimensions
- `delivery-modes.md` — boss-primary / broadcast / generate-only
- `formatting-standard.md` — user-visible formatting rules
- `failure-handling.md` — status model and fallback behavior
- `lifecycle-automation.md` — archive-first lifecycle stages and recommended automation chain
- `release-readiness.md` — what is strong now vs what is still pre-release
- `known-limitations.md` — current gaps and intentionally disabled behavior
- `validation-report.md` — verified behaviors and remaining checks before public upload

### assets/
- `raw-template.md`
- `synthesized-template.md`
- `boss-summary-template.md`
- `index-template.json`
