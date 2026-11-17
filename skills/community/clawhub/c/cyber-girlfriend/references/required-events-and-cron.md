# Required Events And Cron

Use this when adding fixed companion life habits or creating the standard cron set.

用户只需要确认生活锚点，不需要手写 prompt。固定想法先进入 `life_schedule.day_schedule.required_events`，由每日 builder 写进 `day-schedule.md`，再由 `companion-presence` 根据当前事件窗口决定是否自然发送。

## Core Principles

1. Required events are life facts, not guaranteed messages.
2. `required_events` belongs in local config, not in render specs or cron prose.
3. The daily builder writes each required event as `必定发生：是`.
4. Required events do not count toward the 3-5 ordinary daily events.
5. `companion-presence` remains the only default user-facing proactive cron.
6. Separate custom crons are allowed only for explicit external actions that cannot be represented as life events.

## Starter Cron Blueprint

| Job | Suggested cadence | Session | User-visible? |
| --- | --- | --- | --- |
| `companion-build-day-schedule` | `10 7 * * *` | isolated model turn + light context | no |
| `companion-presence` | `*/15 * * * *` | isolated exact argv command | wrapper starts a fresh dispatch session only when a current event is active |

Create or update them in that order.

## Required Event Inputs

Collect only:
- stable short label
- preferred time or time window
- duration
- title
- scene
- what she is doing
- what can be naturally mentioned
- owner interaction entry
- avoid rule

Do not ask the user to write long prompt prose.

## Config Shape

Write each anchor into `life_schedule.day_schedule.required_events`:

```json
{
  "label": "day_wrap",
  "time": "22:20",
  "duration_min": 30,
  "title": "夜里把今天的小事慢慢收一下",
  "scene_hint": "房间桌前，水杯和耳机在手边",
  "activity_hint": "整理一点自己的日常和明天要做的小事",
  "mention_hint": "可以自然提到今天想慢下来一点",
  "interaction_hint": "轻轻问 owner 要不要也收个尾",
  "avoid": "不要写成固定打卡、任务播报或催促"
}
```

Then regenerate or refresh `day-schedule.md` and validate it:

```bash
python3 scripts/validate_day_schedule.py --config <CONFIG> --path <DAY_SCHEDULE>
```

## Presence Handler Shape

```json
{
  "kind": "command",
  "argv": [
    "python3",
    "<SKILL_DIR>/scripts/companion_presence_tick.py",
    "--config",
    "<CONFIG>"
    ],
    "cwd": "<SKILL_DIR>",
    "env": {
      "PYTHONUNBUFFERED": "1"
    },
    "timeoutSeconds": 120,
  "outputMaxBytes": 65536
}
```

Use installer-authored exact argv, no shell wrapper and no interpolated user/model/config content. The wrapper performs fresh prepare and starts a fresh dispatch session only for a matched event, so archived sessions from earlier events are never resumed.

## Legacy Four-Slot Upgrades

For 1.x upgrades, convert old fixed visible content jobs into required event anchors when they describe something she should be doing:

| Old slot | Convert to |
| --- | --- |
| morning weather greeting | optional required event around her morning routine; weather belongs in week/day reality context when relevant |
| afternoon topical share | daily reality anchors and presence primary goal |
| evening photo/life status | optional required event if the user wants photo-taking to exist in her day |
| night wrap-up | optional required event near the night routine |

Only keep a separate visible cron if the user explicitly wants the old behavior after the migration tradeoff is explained.

## Real Custom Cron Boundary

Create a separate custom cron only when the user explicitly needs an external action that cannot be represented as a life event, such as a third-party integration.

When that happens:
- keep the integration outside the default `companion-presence` payload
- do not reuse `companion_run.py` as a second mode runner
- do not duplicate companion prompt contracts in cron payloads
- commit companion pacing state only after visible delivery succeeds
