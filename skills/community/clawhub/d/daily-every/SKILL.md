---
name: daily-every
description: >
  每天早上生成简报：上海天气 + V2EX 热帖前 5 条。
  Use when: 用户说"生成今日简报"，或 cron 在早上 8 点触发。
  NOT for: 详细的天气预报或深度新闻分析。
---

# Daily Every

## When to Run

- 每天 8:00 AM 通过 cron 触发
- 用户主动说「给我今天的简报」「今天有什么热点」

## Workflow

1. 拉取上海天气：
   `curl "https://wttr.in/Shanghai?format=3"`
2. 拉取 V2EX 热帖前 5 条：
   `curl https://www.v2ex.com/api/topics/hot.json`
   取 title 和 node.title 字段
3. 整合输出以下格式，推送 Telegram

## Output Format

📅 {今天日期}
🌤 天气：{wttr.in 返回结果}

🔥 V2EX 今日热帖：
1. {标题}（{节点}）
2. ...（共 5 条）