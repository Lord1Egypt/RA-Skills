---
name: boc-forex-monitor
description: Configurable Bank of China forex monitor with per-currency thresholds, price columns, and optional OpenClaw notifications. Use when you want to set up, configure, or troubleshoot a BOC forex cron monitor with quiet hours, baseline comparison, and deduped alerts.
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - openclaw
    envVars:
      - name: BOC_FOREX_NOTIFY_CHANNEL
        required: false
        description: Optional OpenClaw message channel such as feishu.
      - name: BOC_FOREX_NOTIFY_TARGET
        required: false
        description: Optional OpenClaw message target such as user:ou_xxx.
      - name: BOC_FOREX_NOTIFY_ACCOUNT_ID
        required: false
        description: Optional account id for multi-account messaging setups.
---

# BOC Forex Monitor

Set up a configurable Bank of China foreign-exchange monitor with per-currency thresholds and price columns.

## What this skill provides

- Fetch BOC forex data from https://www.boc.cn/sourcedb/whpj/
- Track any configured currency using any price column (现汇买入价/现钞买入价/现汇卖出价/现钞卖出价/中行折算价)
- Compare current values against a rolling baseline
- Skip monitoring during quiet hours (default 23:00-09:00 Asia/Shanghai)
- Trigger on per-currency configurable thresholds:
  - Rise, drop, or both directions
  - Configurable threshold values (default 0.5)
- Deduplicate notifications using local state files
- Support optional OpenClaw message delivery (for example Feishu)

## Files in this skill

- `scripts/boc_forex_check.py`: fetch + parse + compare + trigger generation
- `scripts/boc_forex_cron_runner.py`: stable cron entrypoint; runs the checker, formats output, deduplicates, and optionally sends a notification
- `references/configuration.md`: configuration knobs and install patterns

## Setup workflow

1. Read `references/configuration.md`.
2. Create `.openclaw-state/boc-forex-monitor-config.json` in your workspace with your desired monitoring targets.
3. Copy both scripts into `<workspace>/scripts/`.
4. Make both scripts executable.
5. Create or update a cron job with the OpenClaw `cron` tool.
6. Prefer a short `agentTurn` payload that only executes the runner script and returns stdout verbatim.
7. Verify with a manual script run before claiming success.

## Cron payload pattern

Use an isolated `agentTurn` job. Keep the prompt minimal.

Recommended payload message:

```text
Workdir is <workspace>. Execute:
python3 scripts/boc_forex_cron_runner.py [--notify-channel <channel>] [--notify-target <target>] [--notify-account-id <id>]

Requirements:
1) Reply with stdout only.
2) Do not add explanation.
3) If stdout is empty, reply: ❌ 汇率检查执行失败
```

## Recommended schedule

Use this cron schedule for every 5 minutes during local daytime trading-watch hours:

```json
{ "kind": "cron", "expr": "*/5 9-22 * * *", "tz": "Asia/Shanghai" }
```

## Validation

Before finishing:

1. Run `python3 scripts/boc_forex_cron_runner.py` from the target workspace.
2. Confirm it returns one of:
   - `✅ 汇率检查完成`
   - `⏭️ 汇率检查跳过`
   - `🔔 已触发阈值并发送...`
3. If notifications are enabled, verify dedupe state is written to `.openclaw-state/boc-forex-alert-notify-state.json`.

## Safety

- Never publish private recipient ids inside the skill bundle.
- Keep notification destinations as runtime parameters or environment variables.
- Do not send routine success messages to chat channels unless the user explicitly wants them.
