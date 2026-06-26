# Detect Task Module

Purpose: determine whether a user request implies creation or management of a scheduled automation task.

## Typical triggers

This module should trigger whenever the user expresses intent related to scheduled automation, periodic monitoring, reminders, reports, or recurring notifications.


Natural language patterns that indicate automation intent:

Time based
- every day / 每天
- every week / 每周
- schedule / 定时
- cron
- periodically / 定期

Automation intent
- monitor / 监控
- remind / 提醒
- send me updates / 推送
- automatically check / 自动检查

Management intent
- show tasks
- list cron
- delete schedule
- modify schedule

## Behavior

If automation intent is detected:

1. Extract the task objective.
2. Check if schedule is specified.
3. Check if delivery target is specified.
4. If missing information → ask clarifying questions.
5. Pass task definition to scheduler module.
