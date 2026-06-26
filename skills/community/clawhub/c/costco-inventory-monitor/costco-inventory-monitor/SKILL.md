---
name: costco-inventory-monitor
description: Monitor Costco inventory by ZIP and run it safely with OpenClaw cron. Keep secrets outside the skill directory.
---

# Costco Inventory Monitor

## Goal

Provide a repeatable workflow to check Costco inventory for one or more products across multiple ZIP codes, then write a report for downstream channels (for example WeCom).

## Repository Safety Rules

- The `skills/costco-inventory-monitor` directory must contain scripts, templates, and docs only.
- Never store real AK/SK, tokens, passwords, or proxy credentials inside `skills/`.
- Real runtime secrets must be stored in `/root/.openclaw/workspace/.secrets/costco-monitor.env`.
- `.secrets/` must stay in `.gitignore` and should not be committed.

## Files

- Runner: `scripts/run_monitor.sh`
- Inventory checker: `scripts/check_costco_inventory.py`
- Config template (safe to commit): `config/monitor.env.example`
- Standard reference: `references/costco-inventory-standard.md`

## Runtime Setup

1. Create the real secret config from template:

```bash
mkdir -p /root/.openclaw/workspace/.secrets
cp /root/.openclaw/workspace/skills/costco-inventory-monitor/config/monitor.env.example /root/.openclaw/workspace/.secrets/costco-monitor.env
chmod 600 /root/.openclaw/workspace/.secrets/costco-monitor.env
```

2. Edit `/root/.openclaw/workspace/.secrets/costco-monitor.env` and fill real values:
- `PRODUCT_1`, `PRODUCT_2`, ...
- `ZIP_CODES`
- `PROXY_URL`
- output paths (`OUTPUT_JSONL`, `STATE_FILE`, `REPORT_FILE`, `LOG_FILE`)

3. Run once to validate:

```bash
/root/.openclaw/workspace/skills/costco-inventory-monitor/scripts/run_monitor.sh
```

## OpenClaw Cron (every 5 minutes)

Use OpenClaw cron, not system crontab, for this skill.

```bash
openclaw cron create \
  --name costco-inventory-monitor-5m \
  --every 5m \
  --session isolated \
  --model hunyuan/hunyuan-t1-latest \
  --delivery none \
  --message 'Run /root/.openclaw/workspace/skills/costco-inventory-monitor/scripts/run_monitor.sh and then return only the contents of /root/.openclaw/workspace/ops/costco-monitor/latest_report.txt.'
```

Existing production job id (created): `29515da3-2b5b-491b-b516-69875b4376a6`.

## Example Products and ZIPs

- Product: `4000362984|TCL 55" Q77K|https://www.costco.com/p/-/tcl-55-class-q77k-series-4k-uhd-qled-smart-tv-allstate-3-year-protection-plan-bundle-included-for-5-years-of-total-coverage/4000362984?langId=-1`
- ZIPs: `03051`, `97230`

## Output Locations

- Report: `/root/.openclaw/workspace/ops/costco-monitor/latest_report.txt`
- Log: `/root/.openclaw/workspace/ops/costco-monitor/monitor.log`
- Snapshot JSONL: `/root/.openclaw/workspace/ops/costco-monitor/snapshots.jsonl`
- State: `/root/.openclaw/workspace/ops/costco-monitor/state.json`

## GitHub Checklist

- Commit: `skills/costco-inventory-monitor/**` and optional ops wrapper scripts.
- Do not commit: `/root/.openclaw/workspace/.secrets/**`, real proxy/account credentials, runtime logs, local state files.
