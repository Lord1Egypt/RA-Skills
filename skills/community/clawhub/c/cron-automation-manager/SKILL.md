---
name: cron-automation-manager
description: Manage and create scheduled cron jobs, automated monitoring tasks, reminders, and periodic push notifications. Use when the user asks to create or manage any scheduled task, monitoring workflow, or automated push (daily reports, GitHub monitoring, AI news tracking, price alerts, etc.). Supports multiple delivery channels such as Feishu, Telegram, DingTalk, Slack, Discord, WhatsApp, Email, or the current chat.
tags: automation, cron, scheduler, monitoring, notifications, reminders, task-management
---

# Cron Automation Manager

This skill acts as an automation orchestrator for OpenClaw. It helps users create, manage, and monitor cron‑based automation tasks.

## When to use

Use this skill whenever the user expresses intent related to automation, scheduled tasks, monitoring, or recurring notifications.

Typical triggers include natural language such as:

- create a scheduled task
- set up a cron job
- every day / 每天 / daily reminder
- every week / weekly report
- monitor something automatically
- send me updates periodically
- automatically check something
- build a daily or weekly report
- track news, GitHub projects, prices, or keywords
- remind me regularly
- manage or inspect existing cron jobs

## Core Capabilities

1. Create cron jobs interactively
2. Manage existing tasks (list, modify, delete)
3. Deploy template automation systems
4. Route push notifications to supported delivery channels
5. Inspect automation health and detect failing tasks

## Workflow

1. Detect automation intent
2. Ask for missing parameters (schedule, target, delivery)
3. Generate cron job configuration
4. Confirm with user
5. Deploy job using the cron tool

IMPORTANT DEFAULT BEHAVIOR:

Every cron job created by this skill MUST automatically record its output into the daily intelligence log.

All jobs should append their results to:

intel/daily/YYYY-MM-DD.md

Rules:

- Each job must append a section with the job name and timestamp.
- The file acts as the persistent data layer for trend analysis.
- 7‑day, weekly, and 30‑day analysis jobs must read from the `intel/daily` directory instead of relying on live searches.
- If the daily file does not exist it must be created automatically.

Example structure:

# 2026-03-22

## Job: AI News Radar
Time: 12:00

(content)

---

## Job: GitHub Trending Radar
Time: 18:00

(content)

This ensures that all automation jobs contribute to a persistent intelligence dataset.

## Delivery Channels

On first use the system may initialize the delivery configuration automatically using:

`skills/cron-automation-manager/scripts/init-delivery-config.ps1`

This script will create `config/delivery-config.json` from the example template if it does not already exist.

Users may edit the file to enable or disable delivery channels.

## Delivery Channels

Delivery routing is controlled by configuration.

Primary configuration file:

`config/delivery-config.json`

If the configuration file does not exist, users should copy the template:

`config/delivery-config.example.json`

and rename it to:

`delivery-config.json`

Cron jobs should always generate reports locally first (intel/*).
The delivery router may distribute results to enabled channels defined in the config file.

Supported channels may include:

- Feishu
- Telegram
- Discord
- Web Console
- Email
- Local Files

## Templates

Predefined automation templates live in `templates/`. These allow one‑step deployment of complex automation systems.

Currently included templates:

- AI intelligence monitoring system
- GitHub trending monitor
- keyword news monitor
- price monitoring

New templates can be added without modifying the core skill.

## Example Automations

Common automation systems that can be created using this skill:

- AI news monitoring and daily tech intelligence reports
- GitHub trending project tracking
- Keyword-based news alerts
- Cryptocurrency / stock price monitoring
- Daily reminders and habit notifications
- Weekly or monthly summary reports
- System health monitoring

## Example Requests

These are common user requests that should trigger this skill (English or Chinese). The skill should activate whenever a user expresses intent related to automation, scheduling, reminders, monitoring, or recurring notifications:

English:
- create daily report
- monitor GitHub trending
- remind me every morning
- track AI news
- set up cron automation
- schedule a daily reminder
- automatically monitor something
- set up a weekly report
- create a periodic task
- help me build an automation workflow

Chinese:
- 创建定时任务
- 帮我做一个定时提醒
- 每天给我推送
- 每周生成报告
- 监控 GitHub 热门项目
- 监控 AI 新闻
- 自动检查某件事情
- 定期推送消息
- 帮我设置自动化任务
- 做一个 cron 定时任务
