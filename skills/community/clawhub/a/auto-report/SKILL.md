---
name: auto-report
description: >
  Automated daily/weekly/monthly report generation with scheduled delivery.
  Use when: generating reports, creating cron-based report tasks, pushing
  structured summaries to chat channels, designing report templates.
  Triggers: "日报", "周报", "月报", "report", "定时报告", "复盘", "总结", "duty report", "standup"
metadata:
  {
    "openclaw":
      {
        "emoji": "📊",
        "tags": ["automation", "reporting", "cron", "productivity"],
        "category": "automation"
      }
  }
---

# 📊 Auto-Report — Automated Report Generation

Generate structured reports on schedule and deliver them to any chat channel.

## How It Works

```
Data Collection → Structured Summary → Template Rendering → Channel Delivery
```

## Report Types

| Type | Frequency | Best For |
|------|-----------|----------|
| Daily Report | Every day | Work summaries, market recaps, health tracking |
| Weekly Report | Once a week | Sprint reviews, trend analysis, planning |
| Monthly Report | Once a month | KPI reviews, budget tracking |
| Ad-hoc Report | On demand | Incident analysis, deep research |
| Standup Report | Daily/Weekly | Team check-ins, progress updates |

## Report Templates

### Daily Report
```markdown
## [Date] Daily Report

### Key Metrics
- Metric 1: value
- Metric 2: value

### Highlights
1. ...
2. ...

### Analysis
- ...

### Tomorrow's Focus
- ...
```

### Weekly Report
```markdown
## Week X Report (MM.DD - MM.DD)

### This Week
- Mon: ...
- Tue: ...

### Metrics Summary
| Metric | This Week | Last Week | Change |
|--------|-----------|-----------|--------|

### Lessons Learned
1. ...
2. ...

### Next Week Plan
- ...
```

## Scheduling with Cron

Create automated report tasks using OpenClaw cron:

```bash
# Daily report at 20:00 on workdays
openclaw cron add \
  --name "Daily Report" \
  --cron "0 20 * * 1-5" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --agent-turn "Generate the daily report. Read the relevant data sources, structure the findings, and deliver to the target channel."

# Weekly report every Friday at 16:00
openclaw cron add \
  --name "Weekly Report" \
  --cron "0 16 * * 5" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --agent-turn "Generate the weekly report covering this week's activity."
```

### Cron Best Practices

1. **Use `isolated` sessions** — prevents message duplication
2. **Use `agentTurn`** — not `systemEvent` (avoids triple-delivery bugs)
3. **Set `delivery.mode: "none"`** — let the agent handle messaging itself
4. **Keep prompts self-contained** — isolated sessions have no context
5. **Set reasonable timeouts** — 90-180s for simple reports, 300s for complex ones

## Channel Delivery

### Feishu (Lark) Interactive Card
```json
{
  "config": {"wide_screen_mode": true},
  "header": {
    "title": {"tag": "plain_text", "content": "📊 Daily Report — 2026-04-06"},
    "template": "blue"
  },
  "elements": [
    {"tag": "markdown", "content": "**Key Metrics**\n▸ Revenue: +12%\n▸ Users: 1.2k active"},
    {"tag": "hr"},
    {"tag": "markdown", "content": "**Highlights**\n1. Launched new feature\n2. Fixed critical bug"},
    {"tag": "hr"},
    {"tag": "markdown", "content": "**Tomorrow**\n▸ Ship v2.1\n▸ Team standup at 10am"}
  ]
}
```

Use the `message` tool: `action=send, channel=feishu, target=chat:<chat_id>, card=<json>`

### Plain Text (any channel)
Use the `message` tool with a `message` parameter for simple text delivery.

### Document Export
- Use `feishu_create_doc` to create persistent documents (for archives)
- Use `feishu_update_doc` to update existing documents

## Report Quality Standards

1. **Data first** — Collect real data before writing analysis
2. **Concise** — Daily: 300-500 words, Weekly: 800-1200 words
3. **Actionable** — Conclusions should drive decisions, not just describe
4. **Consistent format** — Same structure every time for scannability
5. **No fluff** — Skip filler phrases, lead with the most important info

## Common Cron Schedules

```
# After market close (workdays)
0 15 * * 1-5   Asia/Shanghai   # A-share close
0 16 * * 1-5   Asia/Shanghai   # Buffer for data collection

# Evening summaries
0 20 * * 1-5   Asia/Shanghai   # Workday evening
0 22 * * *     Asia/Shanghai   # Before sleep

# Weekly reports
0 16 * * 5     Asia/Shanghai   # Friday afternoon
0 8 * * 1      Asia/Shanghai   # Monday morning

# Monthly reports
0 9 1 * *      Asia/Shanghai   # 1st of month
```

## Advanced: Report Chains

For complex workflows, chain multiple cron jobs:

1. **Data collector** (15:00) — Fetch raw data, save to file
2. **Analyzer** (15:10) — Read data file, generate insights
3. **Publisher** (15:15) — Format and deliver to channels

This prevents timeout issues with complex reports.

## Examples

### Health Tracking Report
```bash
# Daily health summary at 22:00
openclaw cron add --name "Health Daily" \
  --cron "0 22 * * *" --tz "Asia/Shanghai" \
  --session isolated \
  --agent-turn "Read health/LOG.md and health/PROFILE.md. Generate a health summary covering: water intake, meals, exercise, sleep, weight trend. Deliver to user via message tool."
```

### Market Intelligence Report
```bash
# Market briefing at 07:00
openclaw cron add --name "Market Intel" \
  --cron "0 7 * * 1-5" --tz "Asia/Shanghai" \
  --session isolated \
  --agent-turn "Search for overnight US market data, commodity prices, and key news. Format as a structured briefing card and deliver to chat:oc_xxxxxx via message tool."
```

## Compatibility

- Works with **any OpenClaw channel** (Feishu, Telegram, Discord, Slack, etc.)
- No external dependencies required
- Works in both `main` and `isolated` session targets
