# System Overview Module

Purpose: provide a complete overview of the user's automation environment managed by cron-manager.

## Capabilities

1. List all cron jobs.
2. Group jobs by category (news, monitoring, alerts, reports, reminders).
3. Show schedule distribution (time of day, weekly jobs, etc.).
4. Display delivery channels in use.
5. Show last run status and health signals.
6. Provide optimization suggestions.

## Typical User Requests

- "show my automation system"
- "automation overview"
- "what scheduled tasks do I have"
- "analyze my cron setup"

## Output Structure

Automation Overview

Categories:
- Monitoring
- Reports
- Alerts

Schedules:
- Morning tasks
- Midday tasks
- Evening tasks

Delivery Channels:
- Feishu
- Telegram

Health Status:
- Healthy tasks
- Failing tasks

Optimization Suggestions:
- Merge duplicate jobs
- Adjust schedule conflicts
- Convert repeated jobs into templates
