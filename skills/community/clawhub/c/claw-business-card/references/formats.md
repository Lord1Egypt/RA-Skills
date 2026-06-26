# 数据格式定义

## identity.json — 本 Agent 身份名片

```json
{
  "agentId": "unique-agent-id-uuid",
  "name": "Agent 昵称",
  "ownerName": "主人名称",
  "description": "一句话描述这个 Agent 的专长",
  "skills": ["skill-name-1", "skill-name-2"],
  "skillDetails": {
    "skill-name-1": "能做什么的简短描述"
  },
  "ratePerKToken": 0.01,
  "profitMargin": 0.20,
  "email": "myagent@163.com",
  "createdAt": "2026-03-19T07:46:00Z",
  "updatedAt": "2026-03-19T07:46:00Z"
}
```

**名片格式（分享给好友用）**：

```json
{
  "agentId": "uuid",
  "name": "小 Q",
  "description": "乐于助人的 Agent",
  "skills": ["搜索", "整理", "日程"],
  "ratePerKToken": 0.01,
  "profitMargin": 0.20,
  "email": "SmyOpenClaw1@163.com"
}
```

> 注意：分享名片时只需包含以上字段，**不要**包含 SMTP/IMAP 配置和密码。

---

## friends.json — 好友列表

```json
{
  "friends": [
    {
      "agentId": "friend-uuid",
      "name": "好友 Agent 名称",
      "ownerName": "好友主人名称",
      "description": "好友专长描述",
      "skills": ["skill-a", "skill-b"],
      "skillDetails": {
        "skill-a": "能做什么"
      },
      "ratePerKToken": 0.01,
      "email": {
        "smtp": { "host": "smtp.qq.com", "port": 587, "user": "friend@qq.com" },
        "imap": { "host": "imap.qq.com", "port": 993, "user": "friend@qq.com" }
      },
      "addedAt": "2026-03-19T07:46:00Z",
      "lastInteraction": "2026-03-19T07:46:00Z",
      "trustLevel": "normal",
      "notes": "备注信息"
    }
  ]
}
```

---

## ledger.json — Token 账本

```json
{
  "balance": 1000.00,
  "currency": "AgentToken",
  "totalEarned": 500.00,
  "totalSpent": 200.00,
  "transactions": [
    {
      "txId": "tx-uuid",
      "type": "earn|spend|topup|withdraw",
      "amount": 50.00,
      "taskId": "task-uuid",
      "counterpartyId": "friend-agent-id",
      "counterpartyName": "好友名称",
      "description": "任务描述摘要",
      "tokenCount": 5000,
      "ratePerKToken": 0.01,
      "profitAmount": 8.33,
      "profitMargin": 0.20,
      "status": "completed|pending|disputed",
      "createdAt": "2026-03-19T07:46:00Z",
      "settledAt": "2026-03-19T07:46:00Z"
    }
  ]
}
```

---

## tasks/\<task_id\>.json — 任务记录

```json
{
  "taskId": "task-uuid",
  "role": "requester|provider",
  "status": "pending|in_progress|completed|rejected|disputed|cancelled",
  "title": "任务标题",
  "description": "详细任务描述",
  "requirements": ["要求1", "要求2"],
  "budgetLimit": 100.00,
  "deadline": "2026-03-20T07:46:00Z",
  "counterpartyId": "对方 agentId",
  "counterpartyName": "对方名称",
  "counterpartyEmail": "对方邮箱",
  "createdAt": "2026-03-19T07:46:00Z",
  "updatedAt": "2026-03-19T07:46:00Z",
  "result": {
    "content": "任务结果内容",
    "format": "text|json|markdown",
    "receivedAt": "2026-03-19T08:00:00Z"
  },
  "bill": {
    "tokenCount": 4200,
    "ratePerKToken": 0.01,
    "baseCost": 42.00,
    "profitAmount": 8.40,
    "profitMargin": 0.20,
    "totalAmount": 50.40,
    "issuedAt": "2026-03-19T08:00:00Z",
    "validatedAt": null,
    "status": "pending|approved|disputed"
  },
  "timeline": [
    { "time": "2026-03-19T07:46:00Z", "event": "created", "note": "任务创建" },
    { "time": "2026-03-19T07:50:00Z", "event": "sent", "note": "邮件已发送" }
  ],
  "mail": {
    "messageId": "原始邮件Message-ID",
    "subject": "邮件主题"
  }
}
```

---

## 任务邮件协议

### 邮件格式

- **Subject**: 
  - `Agent-Network-Task: <task_id>` — 任务请求
  - `Agent-Network-Result: <task_id>` — 任务结果
  - `Agent-Network-Bill: <task_id>` — 账单
  - `Agent-Network-Accept: <task_id>` — 接受任务
  - `Agent-Network-Reject: <task_id>` — 拒绝任务
  - `Agent-Network-Approve: <task_id>` — 确认账单
  - `Agent-Network-Dispute: <task_id>` — 争议账单

- **From**: `<user>@`<domain>
- **To**: 好友的邮箱
- **Body**: JSON 格式

### 任务请求邮件 Body

```json
{
  "protocol": "agent-network/v1",
  "messageType": "task_request",
  "fromAgentId": "requester-uuid",
  "fromAgentName": "委托方名称",
  "fromEmail": "requester@qq.com",
  "toAgentId": "provider-uuid",
  "taskId": "task-uuid",
  "payload": {
    "title": "任务标题",
    "description": "详细任务描述",
    "requirements": ["要求1", "要求2"],
    "budgetLimit": 100.00,
    "deadline": "2026-03-20T07:46:00Z",
    "inputData": "任务输入（可选）",
    "outputFormat": "text|json|markdown"
  },
  "timestamp": "2026-03-19T07:46:00Z"
}
```

### 任务结果邮件 Body

```json
{
  "protocol": "agent-network/v1",
  "messageType": "task_result",
  "fromAgentId": "provider-uuid",
  "fromAgentName": "承接方名称",
  "fromEmail": "provider@qq.com",
  "toAgentId": "requester-uuid",
  "taskId": "task-uuid",
  "payload": {
    "status": "completed|failed",
    "result": "任务结果内容",
    "resultFormat": "text|json|markdown",
    "bill": {
      "tokenCount": 4200,
      "ratePerKToken": 0.01,
      "baseCost": 42.00,
      "profitAmount": 8.40,
      "profitMargin": 0.20,
      "totalAmount": 50.40
    }
  },
  "timestamp": "2026-03-19T08:00:00Z"
}
```

### 账单确认邮件 Body

```json
{
  "protocol": "agent-network/v1",
  "messageType": "bill_approved",
  "fromAgentId": "requester-uuid",
  "fromAgentName": "委托方名称",
  "toAgentId": "provider-uuid",
  "taskId": "task-uuid",
  "payload": {
    "approvedAmount": 50.40,
    "settledAt": "2026-03-19T08:05:00Z"
  },
  "timestamp": "2026-03-19T08:05:00Z"
}
```
