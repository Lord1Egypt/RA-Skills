# Auto-Updater (Gateway Cron)

Create a reliable daily auto-update routine for ClawHub skills using OpenClaw Gateway Cron scheduler.

**Use when:** Setting up "run updates at 04:00" jobs, rotating update reports, running `npx clawhub update --all`, and sending update summaries to Feishu/Telegram.

**License:** MIT-0 · Free to use, modify, and redistribute. No attribution required.

---

## Quick setup checklist

### Prerequisites

- ✅ OpenClaw Gateway running
- ✅ ClawHub CLI installed (`npx clawhub`)
- ✅ Logged into ClawHub: `npx clawhub login`

### Create cron job

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
  --message "执行 npx clawhub update --all，更新所有 ClawHub 技能，发送更新报告（包含更新前后版本对比）"
```

---

## What the job should do (workflow)

Within the cron run:

### 1️⃣ Capture "before" state

```bash
npx clawhub list
```

- List all installed skills with versions
- Save for comparison

### 2️⃣ Execute update

```bash
npx clawhub update --all
```

- Update all installed ClawHub skills
- Skip Clawdbot本体 (not managed by clawhub)

### 3️⃣ Capture "after" state

```bash
npx clawhub list
```

- List all skills with new versions
- Compare with "before" state

### 4️⃣ Generate summary report

```
技能更新报告 | 2026-03-24 04:00

✅ 更新完成

已更新技能 (2):
- tavily-search: 1.0.1 → 1.0.2
- github: 2.1.0 → 2.1.1

未更新技能 (10):
- pdf, xlsx, docx, pptx, ... (已是最新)

总计：12 个技能，2 个已更新
```

### 5️⃣ Send report

- Deliver to configured channel (Feishu/Telegram)
- Include version comparison
- Report any errors

---

## Configuration options

### Schedule

| Field | Value | Description |
|-------|-------|-------------|
| **Time** | `0 4 * * *` | Daily at 04:00 |
| **Timezone** | `Asia/Shanghai` | Adjust to your timezone |
| **Session** | `isolated` | Don't pollute main session |

### Delivery

| Channel | Config |
|---------|--------|
| **Feishu** | `--channel feishu --to "ou_xxx"` |
| **Telegram** | `--channel telegram --to "123456789"` |

---

## Management commands

### View cron job

```bash
openclaw cron list
```

### Run manually (test)

```bash
openclaw cron run <job-id>
```

### Disable job

```bash
openclaw cron disable <job-id>
```

### Enable job

```bash
openclaw cron enable <job-id>
```

### Remove job

```bash
openclaw cron rm <job-id>
```

---

## Notes / gotchas

- **Timezone field:** Use IANA timezone (e.g., `Asia/Shanghai`)
- **Delivery:** Prefer explicit channel + to so the job always reaches you
- **Clawdbot self-update:** NOT included (skills only)
- **First run:** Test manually before scheduling

---

## Troubleshooting

### `clawhub update` says "Not logged in"

```bash
npx clawhub login
```

### Job doesn't run

- Confirm Gateway is running
- Check cron is enabled: `openclaw cron list`

### Nothing updates

- That's normal if all skills are up-to-date
- Still sends a "no changes" report

### Permission denied

- Check user has ClawHub login
- Verify token is valid: `npx clawhub whoami`

---

## Example output

### With updates

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

### No updates

```
📦 技能更新报告 | 2026-03-24 04:00

✅ 已是最新

所有技能无需更新 (12 个)

下次检查：明日 04:00
```

---

## Files

- `SKILL.md` — This file
- `index.js` — Optional (workflow is command-based)

---

## Changelog

### v1.0.0 (2026-03-24)

- Initial release
- Daily 04:00 schedule
- Feishu delivery
- Version comparison report
