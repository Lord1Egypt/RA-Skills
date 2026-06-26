---
name: feishu-cron-delivery
description: Configure, repair, and validate OpenClaw scheduled outbound delivery to Feishu. Use when creating or fixing cron jobs that must proactively send user-visible messages to Feishu, especially for reminders, recurring status reports, 09:00 summaries, or any task where `main + systemEvent` did not deliver, `lastDeliveryStatus` shows `not-requested`, or `channel:last` announce delivery to Feishu returned 400.
---

# Feishu Cron Delivery

Use this skill to make OpenClaw cron jobs reliably send proactive messages to Feishu.

## Core rule

For strong-SLA Feishu delivery, do **not** use:
- `sessionTarget: "main"` + `payload.kind: "systemEvent"`
- `delivery.channel: "last"` as the final production route

Use this validated pattern instead:
- `sessionTarget: "isolated"`
- `payload.kind: "agentTurn"`
- `delivery.mode: "announce"`
- `delivery.channel: "feishu"`
- `delivery.accountId: <accountId>`
- `delivery.to: user:<open_id>` or another explicit Feishu destination

## What to check first

1. Run `openclaw cron list --json`.
2. Identify whether the job is:
   - a main-session system event job, or
   - an isolated agent-turn job.
3. Inspect the last run state:
   - `lastDeliveryStatus: not-requested` usually means it never entered outbound delivery.
   - `status/error` with Feishu 400 usually means delivery was attempted but the route/payload was rejected.

## Repair workflow

### Case 1: Job uses `main + systemEvent`

Treat it as an internal wakeup pattern, not user-visible delivery.

Repair it by changing to:
- `--session isolated`
- `--message "..."`
- `--announce`
- `--channel feishu`
- `--account <id>`
- `--to user:<open_id>`

### Case 2: Job uses `isolated + announce + channel:last`

Treat `last` as debugging-only for Feishu. If it fails or returns 400, replace it with explicit routing:
- `--channel feishu`
- `--account <id>`
- `--to user:<open_id>`

### Case 3: Delivery should stay internal

Use:
- `--session isolated`
- `--message "..."`
- `--no-deliver`

or set `delivery.mode: "none"`.

## Validation workflow

After creating or editing a Feishu cron job:

1. Create a one-shot smoke test with explicit Feishu routing.
2. Use `scripts/create_smoke_test.py` if you want a deterministic command generator.
3. Wait for the scheduled time.
4. Confirm the user actually received the Feishu message.
5. Check `openclaw cron runs --id <job-id>`.

Successful validation means:
- user received the message in Feishu
- run status is `ok`
- delivery is not `not-requested`

## Recommended CLI patterns

### One-shot smoke test

```bash
openclaw cron add \
  --name "Feishu delivery smoke test" \
  --at "2026-04-04T14:32:30" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --message "在本轮只输出这一句话：主动消息链路测试。" \
  --announce \
  --channel feishu \
  --account default \
  --to "user:OPEN_ID" \
  --delete-after-run
```

### Recurring 15-minute report

```bash
openclaw cron add \
  --name "xhs-progress-15m" \
  --cron "*/15 * * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --message "请输出一份发给老姚的中文进度报告..." \
  --announce \
  --channel feishu \
  --account default \
  --to "user:OPEN_ID"
```

### 09:00 morning summary

```bash
openclaw cron add \
  --name "daily-memory-report-0900" \
  --cron "0 9 * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --message "请向老姚发送一份中文晨报..." \
  --announce \
  --channel feishu \
  --account default \
  --to "user:OPEN_ID"
```

## When to keep a separate internal job

Split internal work from user-visible delivery when needed:
- 04:00 internal memory distillation → `delivery.mode: none`
- 09:00 outward user summary → explicit Feishu announce delivery

This avoids confusing internal maintenance with outward delivery.

## Packaging notes

Before publishing:
- replace any user-specific identifiers with placeholders
- keep examples parameterized (`OPEN_ID`, `ACCOUNT_ID`)
- run the smoke test workflow locally once
- validate and package the skill

## Reference

Read `references/validated-pattern.md` for the concrete failure modes and the validated fix pattern.
