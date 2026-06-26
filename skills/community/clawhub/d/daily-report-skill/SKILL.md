---
name: daily-report
description: |
  Daily report skill - Generate and send daily work summary.
  Keywords: daily report, work summary, end of day.
  Use when: End of day reporting, or manually triggered with "generate daily report".
license: agpl-3.0
version: 2.0.0
---

# Daily Report Skill

## Trigger

- Configure via OpenClaw cron to auto-execute at your preferred time
- Or manual trigger: "generate daily report"

## Workflow

1. **Load config**
   - Read `config/daily-report.json` (workspace root)
   - Fall back to defaults or prompt user if missing
   - See [references/config.example.md](references/config.example.md)

2. **Collect data**
   - Read `memory/YYYY-MM-DD.md` (today's journal)
   - Read conversation logs, task status (optional)

3. **Generate report**
   - Load template: `assets/template.md`
   - Replace variables: `{{date}}`, `{{time}}`, `{{recipient}}`, `{{agent_name}}`
   - Fill sections: work, learning, review, suggestions, evolution

4. **Save file**
   - Write to `memory/daily-reports/YYYY-MM-DD.md`

5. **Send notification**
   - Iterate through configured `channels`
   - Call corresponding message API per channel type
   - Supports parallel multi-channel delivery

## Configuration

Config file: `config/daily-report.json` (workspace root, not included in skill package)

Required fields:
- `recipient.name` - Report recipient name
- `channels` - Notification channels (at least one)
- `agent_name` - Agent name

See [references/config.example.md](references/config.example.md) for details.

## Template

Report template at [assets/template.md](assets/template.md)

Supported variables:
- `{{date}}` - Date (YYYY-MM-DD)
- `{{time}}` - Time (HH:MM)
- `{{recipient}}` - Recipient name
- `{{agent_name}}` - Agent name

## Manual Invocation

```
generate daily report
```

Or with temporary overrides:

```
generate daily report and send to feishu ou_xxx
```