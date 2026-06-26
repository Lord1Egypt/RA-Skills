# 定时报告 Cron 配置模板

> ⚠️ **必须包含 delivery.to**：漏填会导致消息无法发送到飞书群，报错 `Delivering to Feishu requires target <chatId|user:openId|chat:chatId>`

## 日报 Cron（周一至周五）

```json
{
  "name": "<AGENT_ID>-daily-report",
  "schedule": { "kind": "cron", "expr": "0 <HOUR> * * 1-5", "tz": "Asia/Shanghai" },
  "payload": {
    "kind": "agentTurn",
    "message": "📋 <中文名>定时报告时间到！\n\n【记忆恢复】先读 ~/.openclaw/agents/<AGENT_ID>/workspace/memory/backup.md，了解当前状态。\n\n【执行任务】<具体任务内容>\n\n【发送前确认】整理完报告内容后，先发飞书 DM 给我确认（「发」或「改后发」），收到回复后再发送到群里。不要自动直接发群。\n\n【结束备份】把本次执行结果（时间、做了什么、下次待办）追加写入 ~/.openclaw/agents/<AGENT_ID>/workspace/memory/backup.md。",
    "timeoutSeconds": 120
  },
  "sessionTarget": "session:<AGENT_ID>",
  "delivery": {
    "mode": "announce",
    "channel": "feishu",
    "to": "<飞书群ID>"
  }
}
```

## 周报 Cron（周五合并到日报，不单独发）

```json
{
  "name": "<AGENT_ID>-weekly-report",
  "schedule": { "kind": "cron", "expr": "0 <HOUR> * * 5", "tz": "Asia/Shanghai" },
  "payload": {
    "kind": "agentTurn",
    "message": "📋 <中文名>周报时间到！\n\n【记忆恢复】先读 ~/.openclaw/agents/<AGENT_ID>/workspace/memory/backup.md，了解当前状态。\n\n【执行任务】本周总结 + 下周计划（注意：周五与日报合并发送，不要单独发一条）。\n\n【发送前确认】整理完周报内容后，先发飞书 DM 给我确认（「发」或「改后发」），收到回复后再发送到群里。不要自动直接发群。\n\n【结束备份】把本次执行结果（时间、做了什么、下次待办）追加写入 ~/.openclaw/agents/<AGENT_ID>/workspace/memory/backup.md。",
    "timeoutSeconds": 120
  },
  "sessionTarget": "session:<AGENT_ID>",
  "delivery": {
    "mode": "announce",
    "channel": "feishu",
    "to": "<飞书群ID>"
  }
}
```

## 备注

- `sessionTarget` 使用命名 session（`session:<AGENT_ID>`），确保报告历史可追溯
- `delivery.mode: "announce"` + `delivery.channel: "feishu"` + `delivery.to: "<群ID>"` 三者缺一不可
- cron 表达式格式：`分 时 日 月 周`
  - 每日 17:00：`0 17 * * 1-5`
  - 每周五 17:00：`0 17 * * 5`
