# 盯盘定时任务配置手册

## 任务体系总览

| 任务 | 时间 | 方式 | 说明 |
|------|------|------|------|
| 盘前分析 | 工作日 9:15 | cron isolated | 拉竞价数据，给操作指令 |
| 开盘播报 | 工作日 9:35 | cron isolated | 开盘5分钟走势确认，补充指令 |
| 盘中异动监控 | 工作日 10:00~14:30 每小时 | cron isolated | 检查持仓价格vs止损线 |
| 收盘复盘 | 工作日 16:05 | cron isolated | 完整复盘+明日计划 |
| 心跳学习沉淀 | 每天 | heartbeat | 从对话提炼知识写learnings.md |

---

## 1. 盘前分析任务

**触发时间**：工作日 9:15（提前15分钟，用竞价数据判断）

```json
{
  "name": "盘前分析",
  "schedule": { "kind": "cron", "expr": "15 9 * * 1-5", "tz": "Asia/Shanghai" },
  "payload": {
    "kind": "agentTurn",
    "message": "现在是盘前9:15。请执行盘前分析：\n1. 拉取所有持仓股和关注股实时数据（含昨收、今竞价）\n2. 判断今日大盘情绪\n3. 给出每只持仓股的当日操作指令\n指令格式：【买入/卖出/观望】股票 价格 数量 理由 止损价\n数据来源：MEMORY.md持仓记录",
    "timeoutSeconds": 120
  },
  "sessionTarget": "isolated",
  "delivery": { "mode": "announce" }
}
```

## 2. 开盘确认任务

**触发时间**：工作日 9:35（开盘5分钟后确认走势）

```json
{
  "name": "开盘走势确认",
  "schedule": { "kind": "cron", "expr": "35 9 * * 1-5", "tz": "Asia/Shanghai" },
  "payload": {
    "kind": "agentTurn",
    "message": "现在是9:35，开盘已5分钟。请拉取持仓股和关注股实时数据，对比盘前分析判断：\n1. 走势是否符合预期\n2. 是否需要修改操作指令\n3. 有无异动（涨跌>3%或量能突变）立即标注",
    "timeoutSeconds": 120
  },
  "sessionTarget": "isolated",
  "delivery": { "mode": "announce" }
}
```

## 3. 盘中异动监控

**触发时间**：工作日 10:00、11:00、13:30、14:00、14:30

```json
{
  "name": "盘中监控",
  "schedule": { "kind": "cron", "expr": "0 10,11 * * 1-5", "tz": "Asia/Shanghai" },
  "payload": {
    "kind": "agentTurn",
    "message": "盘中监控：拉取所有持仓股实时价格。检查：\n1. 是否有股票跌破止损线？→ 立即播报【止损警报】\n2. 是否有股票涨幅>5%？→ 播报【异动提醒】\n3. 量能是否突变（>3x均量）？→ 播报【量能异动】\n无异动则回复 MONITOR_OK",
    "timeoutSeconds": 60
  },
  "sessionTarget": "isolated",
  "delivery": { "mode": "announce" }
}
```

午盘另设一个（13:30~14:30）：
```json
{
  "name": "午盘监控",
  "schedule": { "kind": "cron", "expr": "0 13,14 * * 1-5", "tz": "Asia/Shanghai" },
  "payload": {
    "kind": "agentTurn",
    "message": "盘中监控：拉取所有持仓股实时价格。检查：\n1. 是否有股票跌破止损线？→ 立即播报【止损警报】\n2. 是否有股票涨幅>5%？→ 播报【异动提醒】\n3. 量能是否突变（>3x均量）？→ 播报【量能异动】\n无异动则回复 MONITOR_OK",
    "timeoutSeconds": 60
  },
  "sessionTarget": "isolated",
  "delivery": { "mode": "announce" }
}
```

## 4. 收盘复盘任务

**触发时间**：工作日 16:05

```json
{
  "name": "收盘复盘",
  "schedule": { "kind": "cron", "expr": "5 16 * * 1-5", "tz": "Asia/Shanghai" },
  "payload": {
    "kind": "agentTurn",
    "message": "现在收盘，请执行完整复盘（参考 review-template.md 结构）：\n1. 昨日判断自我校验（每只股票对比实际）\n2. 更新持仓浮亏浮盈\n3. 关注股扫描（是否触及入场价位）\n4. 明日操作计划\n5. 错误和教训写入 memory/learnings.md\n6. 日志写入 memory/YYYY-MM-DD.md",
    "timeoutSeconds": 300
  },
  "sessionTarget": "isolated",
  "delivery": { "mode": "announce" }
}
```

---

## 快速注册命令（在主session执行）

用 `cron` 工具逐个添加上述任务。添加后用 `cron list` 确认。

**注意**：非交易日（周末/节假日）cron 仍会触发，agent 拉到的数据是上一个交易日的。
处理方式：在 prompt 里加一句"如果今日非交易日（周末或数据与昨日相同），回复 MARKET_CLOSED 即可"。

---

## 盯盘异动判断标准

| 条件 | 动作 |
|------|------|
| 持仓股跌破止损线 | 立即播报【止损警报】，给卖出指令 |
| 持仓股单日涨>5% | 播报【异动提醒】，评估是否止盈 |
| 持仓股量能>3x | 播报【量能异动】，分析是主力进场还是出货 |
| 关注股触及入场价 | 播报【入场机会】，快速跑五关论证 |
| 大盘跌>2% | 播报【大盘预警】，检查持仓止损安全边际 |
