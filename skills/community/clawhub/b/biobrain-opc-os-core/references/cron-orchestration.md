# Cron Orchestration — 自动化引擎

All 7 departments run on cron. This reference provides battle-tested configurations.

## Daily Learning (07:30-08:30, Staggered)

Each department researches their domain's latest trends. Staggered at 10-minute intervals to avoid rate limiting.

```
Department    Time     Cron Expression (Asia/Shanghai)
DataCenter    07:30    30 7 * * *
Brand         07:40    40 7 * * *
Sales         07:50    50 7 * * *
Finance       08:00    0 8 * * *
Legal         08:10    10 8 * * *
Inspector     08:20    20 8 * * *
Admin         08:30    30 8 * * *
```

Cron payload template:
```json
{
  "name": "{Department}每日学习",
  "schedule": { "kind": "cron", "expr": "{expr}", "tz": "Asia/Shanghai" },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "执行今日学习任务：搜索{领域}最新趋势，输出300字学习笔记到 company/departments/{dept}/学习笔记_{YYYYMMDD}.md。使用zai/glm-4-flash模型，严格控制在300字以内。",
    "model": "zai/glm-4-flash",
    "lightContext": true,
    "timeoutSeconds": 300
  }
}
```

## Daily Reporting (22:00-22:15, Staggered)

Each department submits a daily report. Staggered to prevent Feishu rate limiting.

```
Department    Time     Offset from 22:00
DataCenter    22:00    +0 min
Brand         22:02    +2 min
Sales         22:04    +4 min
Finance       22:06    +6 min
Legal         22:08    +8 min
Inspector     22:10    +10 min
Admin         22:12    +12 min
```

Report format: One paragraph summarizing the day's output, issues, and tomorrow's priority.

## Weekly Inspection (Friday 22:00)

```json
{
  "name": "监察部·每周巡检",
  "schedule": { "kind": "cron", "expr": "0 22 * * 5", "tz": "Asia/Shanghai" },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "执行每周cron巡检：检查所有cron job的consecutiveErrors。连续2天失败的标记为异常，通知数据中心修复。生成巡检报告到 company/departments/inspector/巡检报告_{YYYYMMDD}.md",
    "model": "zai/glm-4-flash",
    "lightContext": true
  }
}
```

## Monthly Skill Maintenance (1st of Month, 10:00)

```json
{
  "name": "SkillHub月度维护",
  "schedule": { "kind": "cron", "expr": "0 10 1 * *", "tz": "Asia/Shanghai" },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "检查所有已发布SkillHub技能，对比本地版本。如有更新，重新publish。记录维护日志。",
    "model": "zai/glm-4-flash",
    "lightContext": true
  }
}
```

## Model Routing Rules

```
External output (customer-facing): deepseek/deepseek-v4-pro (or equivalent premium)
Internal ops (free tier): zai/glm-4-flash, doubao, baidu/ernie-speed
Learning/research (free tier): zai/glm-4-flash
Inspection/audit (light): zai/glm-4-flash + lightContext
```

## Failure Alert Configuration

Every cron job should have failure alerts configured:

```json
{
  "failureAlert": {
    "after": 2,
    "channel": "feishu",
    "to": "CEO",
    "cooldownMs": 3600000
  }
}
```

Rule: alert after 2 consecutive failures (not 1 — avoid noise from transient issues). Cooldown 1 hour to prevent alert storms.

## Anti-Patterns

- **No failure alerts** — Jobs fail silently for days. The most common cause of rot.
- **All jobs at same minute** — Rate limiting kills half of them. Always stagger.
- **CEO as cron debugger** — If you're manually checking job status, your automation is broken.
- **Premium model for internal ops** — Wasting money. Free models handle learning and inspection perfectly.
