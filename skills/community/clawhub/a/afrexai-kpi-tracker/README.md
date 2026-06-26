# 📊 KPI Tracker — OpenClaw Skill

Track key business metrics, set targets, and get status reports — all through your AI agent.

## Why

Most KPI tools are overbuilt dashboards you stop checking after a week. This skill turns your agent into a lightweight metrics tracker that actually tells you when something's off.

No SaaS subscription. No dashboard login. Just ask your agent "how are we doing?" and get a straight answer.

## What You Get

- **Define KPIs** with targets and red/yellow/green thresholds
- **Record values** conversationally ("MRR hit $48K this week")
- **Status reports** with color-coded health indicators
- **Trend analysis** — are you on track to hit target at current pace?
- **Proactive alerts** — agent flags red KPIs before you ask

## Quick Start

1. Install: `clawhub install afrexai-kpi-tracker`
2. Create `kpi-config.json` with your metrics (see SKILL.md for format)
3. Tell your agent: "Record [metric] at [value]"
4. Ask: "KPI report" any time

## Example Report

```
📊 KPI Report — Week of Feb 10

🟢 MRR: $48,200 / $50,000 (96.4%)
🔴 Churn: 8.1% / 3.0% — needs attention
🟡 Lead Conversion: 11% / 15% — trending up
```

## Works Great With

- **Cron jobs** — automated weekly reports every Monday morning
- **Slack/Telegram** — get KPI summaries delivered to your channel
- **[AfrexAI Context Packs](https://afrexai-cto.github.io/context-packs/)** — pre-built KPI frameworks for Fintech, Healthcare, SaaS, Legal, and 7 more industries. Drop-in configs with industry-specific metrics already defined.

## Built by AfrexAI 🖤💛

We build AI agent tools that actually work. Check out our free tools:
- [AI Revenue Calculator](https://afrexai-cto.github.io/ai-revenue-calculator/) — see if AI agents make financial sense for your business
- [Agent Setup Wizard](https://afrexai-cto.github.io/agent-setup/) — get configured in 5 minutes
- [Context Packs Store](https://afrexai-cto.github.io/context-packs/) — industry-specific AI agent configs

License: MIT
