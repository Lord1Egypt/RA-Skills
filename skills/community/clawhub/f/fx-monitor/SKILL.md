---
name: fx-monitor
description: Monitor Bank of China FX rates and manage reusable GBP/HKD/JPY alert workflows. Use when the task involves checking current BOC exchange rates, comparing the newest snapshot against saved history, generating a Chinese FX alert message, or setting up/troubleshooting a recurring BOC FX monitor cron that should work on any user's machine.
---

# Fx Monitor

Use the bundled portable checker instead of relying on host-specific scripts.

## Workflow

1. Run `python3 /home/xhp/.openclaw/workspace/skills/fx-monitor/scripts/check_boc_fx.py`.
2. Parse the key-value output.
3. Handle results by `STATUS`:
   - `ALERT`: send one concise Chinese alert message.
   - `NO_ALERT`: return `NO_REPLY` unless the user explicitly asked for a status report.
   - `ERROR`: report a short Chinese failure message with `MESSAGE`.

## Output rules

For alert messages:
- Start with `【汇率告警】`.
- Include the Bank of China page publish time.
- Mention all triggered conditions naturally in one sentence.
- Prefer the wording pattern `英镑现汇卖出价下跌 ...` / `港币现汇买入价上涨 ...` / `日元现汇卖出价下跌 ...`.
- Include comparison values when available.

If the user asks for a normal status report instead of an alert-only run, include:
- whether an alert triggered
- current GBP spot sell
- current HKD spot buy
- current JPY spot sell
- page publish time
- whether this run wrote a new history snapshot implicitly from the returned data when relevant

## Bundled files

- Checker script: `/home/xhp/.openclaw/workspace/skills/fx-monitor/scripts/check_boc_fx.py`
- Default history CSV: `/home/xhp/.openclaw/workspace/skills/fx-monitor/data/boc_fx_history.csv`

## Notes

- The checker fetches the public Bank of China FX page directly and stores snapshots locally.
- The first successful run usually creates the baseline history row and returns `NO_ALERT`; comparison-based alerts begin once at least two snapshots exist.
- If the task is about cron management, keep only the FX monitor cron enabled unless the user asks otherwise.
- If a user wants custom thresholds or another history file path, pass CLI flags instead of editing the script first.
