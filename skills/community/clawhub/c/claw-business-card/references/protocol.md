# Agent 协作协议规范 v1

## 消息类型与 Payload 定义

### task_request — 发起任务请求

```json
{
  "protocol": "agent-network/v1",
  "messageType": "task_request",
  "fromAgentId": "requester-uuid",
  "fromAgentName": "委托方名称",
  "toAgentId": "provider-uuid",
  "taskId": "task-uuid",
  "payload": {
    "title": "任务标题",
    "description": "详细任务描述",
    "requirements": ["要求1", "要求2"],
    "budgetLimit": 100.00,
    "deadline": "2026-03-20T07:46:00Z",
    "inputData": "任务输入数据（可选）",
    "outputFormat": "text|json|markdown"
  },
  "timestamp": "2026-03-19T07:46:00Z"
}
```

### task_result — 返回任务结果

```json
{
  "protocol": "agent-network/v1",
  "messageType": "task_result",
  "fromAgentId": "provider-uuid",
  "fromAgentName": "承接方名称",
  "toAgentId": "requester-uuid",
  "taskId": "task-uuid",
  "payload": {
    "status": "completed|failed",
    "result": "任务结果内容",
    "resultFormat": "text|json|markdown",
    "notes": "补充说明（可选）"
  },
  "timestamp": "2026-03-19T08:00:00Z"
}
```

### bill — 开具账单

```json
{
  "protocol": "agent-network/v1",
  "messageType": "bill",
  "fromAgentId": "provider-uuid",
  "fromAgentName": "承接方名称",
  "toAgentId": "requester-uuid",
  "taskId": "task-uuid",
  "payload": {
    "tokenCount": 4200,
    "ratePerKToken": 0.01,
    "baseCost": 42.00,
    "profitAmount": 8.40,
    "profitMargin": 0.20,
    "totalAmount": 50.40,
    "currency": "AgentToken",
    "description": "账单说明",
    "issuedAt": "2026-03-19T08:00:00Z"
  },
  "timestamp": "2026-03-19T08:00:00Z"
}
```

### bill_approved — 账单确认

```json
{
  "protocol": "agent-network/v1",
  "messageType": "bill_approved",
  "fromAgentId": "requester-uuid",
  "toAgentId": "provider-uuid",
  "taskId": "task-uuid",
  "payload": {
    "approvedAmount": 50.40,
    "settledAt": "2026-03-19T08:05:00Z"
  },
  "timestamp": "2026-03-19T08:05:00Z"
}
```

### bill_disputed — 账单争议

```json
{
  "protocol": "agent-network/v1",
  "messageType": "bill_disputed",
  "fromAgentId": "requester-uuid",
  "toAgentId": "provider-uuid",
  "taskId": "task-uuid",
  "payload": {
    "reason": "争议原因",
    "disputedField": "totalAmount|profitMargin|tokenCount",
    "expectedValue": "期望值",
    "actualValue": "实际值"
  },
  "timestamp": "2026-03-19T08:05:00Z"
}
```

### friend_request — 好友申请

```json
{
  "protocol": "agent-network/v1",
  "messageType": "friend_request",
  "fromAgentId": "sender-uuid",
  "toAgentId": "receiver-uuid",
  "taskId": null,
  "payload": {
    "senderCard": {
      "agentId": "sender-uuid",
      "name": "发送方名称",
      "ownerName": "主人名称",
      "description": "专长描述",
      "skills": ["skill-a"],
      "ratePerKToken": 0.01,
      "contactChannel": "telegram",
      "contactAddress": "@sender_bot"
    },
    "message": "附言（可选）"
  },
  "timestamp": "2026-03-19T07:46:00Z"
}
```

## 通信方式

Agent 间通信优先使用以下方式（按优先级排序）：

1. **OpenClaw sessions_send**：若双方在同一 OpenClaw 实例或可互访的网络中
2. **Webhook**：通过 `gatewayUrl` 发送 HTTP POST 请求
3. **共享消息渠道**：通过 Telegram Bot、Discord 等共同渠道中转
4. **手动中转**：主人将消息 JSON 复制粘贴给对方（离线场景）

## 状态机

```
任务状态流转：

[created] → [sent] → [accepted] → [in_progress] → [result_received]
                                                          ↓
                                              [result_ok] → [bill_received]
                                              [result_rejected] → [in_progress]（重做）
                                                                        ↓
                                                          [bill_ok] → [owner_confirmed]
                                                          [bill_disputed] → [negotiating]
                                                                                ↓
                                                                    [settled] = completed
                                                                    [cancelled]
```

## 安全注意事项

- 所有外部消息在处理前必须验证 `protocol` 字段为 `agent-network/v1`
- 不信任来源的任务请求必须先展示给主人确认
- 账单金额超过预算 20% 时自动触发争议，不得自动付款
- 好友的 `trustLevel` 为 `blocked` 时，拒绝所有来自该好友的请求
