---
name: "CronForge — Visual Cron Job Builder for OpenClaw"
description: "Human-readable cron job templates for OpenClaw. Stop googling cron syntax. Pre-built schedules for daily reports, hourly checks, weekly summaries, and custom intervals."
author: "@TheShadowRose"
version: "1.0.0"
tags: ["cron", "scheduling", "automation", "templates", "timer", "agent-ops"]
license: "MIT"
---

# CronForge — Visual Cron Job Builder for OpenClaw

Stop googling cron syntax. Pick a template, fill in your task, deploy.

## Quick Reference

| Schedule | Cron Expression | Template |
|----------|----------------|----------|
| Every 30 minutes | `*/30 * * * *` | `interval-30m.md` |
| Every hour | `0 * * * *` | `interval-1h.md` |
| Daily at 9 AM | `0 9 * * *` | `daily-morning.md` |
| Weekdays at 6 PM | `0 18 * * 1-5` | `weekday-evening.md` |
| Monday morning | `0 9 * * 1` | `weekly-monday.md` |
| First of month | `0 9 1 * *` | `monthly-first.md` |

## Common Tasks (Ready to Deploy)

- **Daily email summary** — 8 AM, summarize inbox
- **Weekly project report** — Friday 5 PM, status of all repos
- **Hourly system check** — disk, memory, services
- **Morning briefing** — 7 AM, weather + calendar + news
- **Social post scheduler** — configurable times, queued content

See README.md for full documentation.
