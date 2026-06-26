# Daily Hotspot Push

A self-contained OpenClaw skill for scheduled daily news and hotspot delivery.

## What it does

This skill lets a user create, query, update, and remove scheduled news subscriptions.

Typical use cases:
- push international tech and military news every day at 12:00
- send a daily hotspot brief on workdays
- schedule a one-off news push in 5 minutes for testing

## Features

- self-contained, no dependency on other local skills
- timezone management per target
- Chinese natural-time parsing
- OpenClaw cron integration
- subscription state storage
- suitable for QQBot delivery workflows

## Installation

Place the skill in your OpenClaw workspace skills directory, or install it from ClawHub.

Typical local path:

```text
~/.openclaw/workspace/skills/daily-news-push
```

After installation, make sure your OpenClaw runtime can use:
- `openclaw cron`
- your target delivery channel, for example QQBot
- web/news fetching at execution time

## Usage

Examples use the bundled script:

```bash
python scripts/manage_daily_news.py set-timezone --to "<qq-target>" --timezone "Asia/Shanghai"
python scripts/manage_daily_news.py add --to "<qq-target>" --time "每天中午12点" --topics "国际科技,国际军事"
python scripts/manage_daily_news.py add --to "<qq-target>" --time "5分钟后" --topics "今日新闻"
python scripts/manage_daily_news.py test --to "<qq-target>" --topics "今日新闻"
python scripts/manage_daily_news.py list --to "<qq-target>"
python scripts/manage_daily_news.py update --id "<job-id>" --time "每天晚上8点"
python scripts/manage_daily_news.py remove --id "<job-id>"
```

## Example user requests

These are the kinds of user phrases this skill should handle well:

- `每天中午12点给我推送国际科技和国际军事热点`
- `工作日早上8点发一份今日热点简报`
- `把我的新闻订阅改成每天晚上9点`
- `以后每天给我推送国际科技新闻`
- `取消我的每日新闻推送`
- `先测试一下，五分钟后给我推送一条今日新闻`

## Notes

- Runtime-generated subscription data is intentionally ignored from git.
- The skill depends on OpenClaw runtime capabilities like `openclaw cron` and available web/news access at execution time.
