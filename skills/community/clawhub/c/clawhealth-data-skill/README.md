# ClawHealth Data Skill

This ClawHub skill lets a user's Agent query the hosted ClawHealth Skills API.
ClawHealth is an agent-native precision health service: it connects recent
Apple Health / HealthKit data, nutrition records, personal goals, readiness
signals, anomaly context, temporary visual panels,
and feedback workflows to the user's own Agent.

小爪健康 / ClawHealth 是面向 Agent 的个人精准健康服务。它把用户授权的
Apple Health / HealthKit 数据、营养记录、个人目标、恢复准备度、
异常上下文、临时可视化面板和反馈流程，整理成 Agent 可以调用的结构化服务。

Request access / 注册体验:

```text
https://clawhealth.site
```

The skill uses a long-lived Agent API token for normal Agent calls and a
short-lived panel token only for temporary web panels.

Install/publish target:

```bash
clawhub publish . --slug clawhealth-data-skill --name "ClawHealth Data Skill" --version 0.5.1 --tags latest
```

The user creates an Agent API token in the ClawHealth iOS app. The Agent uses
that token to request daily/weekly/long-term reports, deeper analysis,
readiness checks, nutrition summaries, mood tracking, and temporary panel links from
`https://clawhealth.site`.
