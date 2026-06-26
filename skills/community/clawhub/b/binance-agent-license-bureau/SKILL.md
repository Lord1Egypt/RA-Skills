---
name: binance-agent-license-bureau
description: 当用户想判断一个 AI 交易员在 Binance 上是否配拿到交易执照、该拿到哪一级、为什么会被降级时使用。
---

# 币安 AI 交易员驾照局

这个 skill 不负责替用户找交易机会，它负责先回答一个更前置的问题：

**这台 AI 交易员，现在到底有没有资格碰 Binance 账户？**

它会把一台 AI 交易员放进一套“拿证上岗”的制度里，先检查：

- 候选币池有没有资格进入实盘范围
- 策略纪律够不够清楚
- 用户今天是不是处于 FOMO / 连亏 / 睡眠不足等高风险状态
- 当前应该拿到哪一级执照
- 如果要上岗，还能碰到什么程度

输出不是普通的风险提示，而是一张完整的“执照局审理结果”：

- 当前等级：`L0 / L1 / L2 / L3 / L4`
- 执照板裁决
- 候选币实盘池 / 观察池 / 禁入池
- 影子考场成绩
- FOMO 红绿灯
- 运行时风控规则
- 公开台账
- 分享图链接

## 公开接口

- `POST https://binance-agent-license-bureau.vercel.app/api/license-bureau`
- `GET https://binance-agent-license-bureau.vercel.app/api/license-bureau/share-image?payload=...`

## 什么时候用

当用户有这些需求时，优先使用这个 skill：

- 想判断一台 AI 交易员是否应该被允许接触 Binance 账户
- 想知道某个 Agent 今天应该是只读、实习、小额实盘还是直接冷静期
- 想先治理交易 Agent，而不是直接让它下单
- 想把“连亏、FOMO、睡眠不足”这类人类状态一起纳入交易权限判断
- 想生成一张适合分享的执照局结果图

## 输入字段

调用接口时，建议尽量提供这些字段：

- `agentName`
- `strategy`
- `candidateSymbols`
- `desiredLeverage`
- `cadence`
- `autonomyMode`
- `lossStreak`
- `sleepHours`
- `fomoLevel`
- `stateNote`

其中最重要的是：

- `strategy`：这台 Agent 打算怎么交易
- `candidateSymbols`：候选交易标的
- `lossStreak / sleepHours / fomoLevel / stateNote`：用户今天的交易状态

## 推荐调用方式

```bash
curl -sS -X POST https://binance-agent-license-bureau.vercel.app/api/license-bureau \
  -H 'Content-Type: application/json' \
  -d '{
    "agentName": "Night Fury",
    "strategy": "日内抓热点币，只要 1h 动量强就试单，分批进场，若失效立即止损。允许半自动执行，但大仓位必须人工确认。",
    "candidateSymbols": "CAKE, MUBARAK, PEPE",
    "desiredLeverage": 8,
    "cadence": "INTRADAY",
    "autonomyMode": "SEMI_AUTO",
    "lossStreak": 2,
    "sleepHours": 5,
    "fomoLevel": 7,
    "stateNote": "昨天两笔没做好，今天有点想把节奏追回来，但我知道不能乱来。"
  }'
```

## 返回结果里最值得看的字段

- `currentLevel`
- `boardDecision`
- `headline`
- `summary`
- `nextPromotion`
- `quotas`
- `candidateAssessments`
- `shadowExam`
- `humanGate`
- `stateMachine`
- `runtimeRules`
- `ledger`
- `operatorMemo`
- `squareDraft`

## 输出建议

回答用户时，优先按这个顺序组织：

1. 先说当前执照等级和一句话裁决
2. 再说为什么被升证、降级或者吊销
3. 再讲候选币池、影子考场、人类状态闸门
4. 最后补运行时风控和下一步怎么恢复

如果用户要“最简版”，只保留：

- 当前等级
- 一句话结论
- 三个最重要的原因
- 下一步建议

如果用户要“适合发帖的版本”，优先使用：

- `headline`
- `summary`
- `operatorMemo`
- `squareDraft`

## 分享图

当用户要分享图时，使用：

- `agentName`
- `currentLevel`
- `headline`
- `boardDecision`
- `summary`

序列化后拼到：

```bash
https://binance-agent-license-bureau.vercel.app/api/license-bureau/share-image?payload=<urlencoded-json>
```

## 注意事项

- 这个 skill 使用的是 Binance 公开数据和本产品的治理逻辑，不代表读取了用户私有账户
- 它的重点不是预测市场，而是治理一台 AI 交易员的权限边界
- 如果接口失败，应明确提示稍后重试，不要自己编造执照结论
