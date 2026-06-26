# Auto-Updater (Gateway Cron)

Daily auto-update routine for ClawHub skills using OpenClaw Gateway Cron scheduler.

## Features

- ✅ **Automatic updates** — Daily at 04:00
- ✅ **Version tracking** — Before/after comparison
- ✅ **Report delivery** — Feishu/Telegram notifications
- ✅ **Isolated execution** — Doesn't pollute main session
- ✅ **Skills only** — No Clawdbot本体 updates (safe)

## Quick Start

### 1. Install

```bash
npx clawhub install auto-updater-gateway
```

### 2. Configure cron job

```bash
openclaw cron add \
  --name "Daily auto-update (ClawHub skills)" \
  --cron "0 4 * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --wake now \
  --deliver \
  --channel feishu \
  --to "ou_xxxxxxxxxxxx" \
  --message "执行 npx clawhub update --all，更新所有 ClawHub 技能，发送更新报告"
```

### 3. Test

```bash
openclaw cron run <job-id>
```

## What it does

1. Captures current skill versions
2. Runs `npx clawhub update --all`
3. Compares before/after versions
4. Sends summary report to configured channel

## Example output

```
📦 技能更新报告 | 2026-03-24 04:00

✅ 更新完成

已更新技能 (2):
- tavily-search: 1.0.1 → 1.0.2
- github: 2.1.0 → 2.1.1

未更新技能 (10):
- pdf, xlsx, docx, pptx, ... (已是最新)

总计：12 个技能，2 个已更新
```

## License

MIT-0 — Free to use, modify, and redistribute. No attribution required.
