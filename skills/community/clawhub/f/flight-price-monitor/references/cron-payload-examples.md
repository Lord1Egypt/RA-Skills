# 定时任务 payload 示例（OpenClaw 等）

采用「`cron.add` + `agentTurn`」一类形态时：**把自然语言写全**，让调度到的代理回合执行 **`flyai search-flight`**、解析 JSON、写历史、再决定是否提醒用户。

> 若当前环境 **没有** `cron.add`，请改用系统 crontab 或外部调度，仅保留「同一套命令与历史路径」即可。

## 每日早 9 点（单程 + 阈值）

```json
{
  "name": "机票监控-北京-三亚-2026-04-15",
  "schedule": {
    "kind": "cron",
    "expr": "0 9 * * *",
    "tz": "Asia/Shanghai"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "按 flight-price-monitor skill：执行 flyai search-flight --origin 北京 --destination 三亚 --dep-date 2026-04-15 --journey-type 1 --sort-type 3；取最低价，若低于 1500 则提醒用户并附预订链接；将结果追加到 memory/flight-monitor/北京-三亚-2026-04-15.md 价格表。"
  },
  "sessionTarget": "isolated"
}
```

## 每 12 小时

将 `expr` 改为 `0 */12 * * *`（具体 cron 语法以平台为准）。

## 往返示例

在 `message` 中补充 `--back-date 2026-04-20`，并写明往返语义，避免代理漏参。

## 注意

- **message** 应包含：**城市、日期、是否往返、阈值、历史文件路径**。
- 频率过高可能被限流；远日期出行建议每天 1 次或更少。
