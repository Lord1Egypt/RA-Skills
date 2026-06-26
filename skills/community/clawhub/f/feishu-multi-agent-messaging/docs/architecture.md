# 架构设计

## 系统架构

```
┌────────────────────────────────────────────────────────────────┐
│                         飞书平台                                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │  主Bot   │  │ 码农Bot  │  │ 审核Bot  │  │  ...Bot  │       │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘       │
└───────┼─────────────┼─────────────┼─────────────┼─────────────┘
        │             │             │             │
        ▼             ▼             ▼             ▼
┌────────────────────────────────────────────────────────────────┐
│                       OpenClaw Gateway                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    Message Router                         │  │
│  │  - accountId 匹配                                        │  │
│  │  - target 解析                                           │  │
│  │  - 消息路由                                               │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐          │
│  │ 主Agent │  │码农Agent│  │审核Agent│  │ ...Agent│          │
│  │ (main)  │  │ (coder) │  │(reviewer)│ │         │          │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘          │
└────────────────────────────────────────────────────────────────┘
        │
        ▼
┌────────────────────────────────────────────────────────────────┐
│                     sessions_spawn 调度                         │
│                                                                 │
│  主Agent ──────► sessions_spawn ──────► 子Agent                 │
│     │                                        │                  │
│     │◄─────────── announce ─────────────────┘                  │
└────────────────────────────────────────────────────────────────┘
```

## 核心组件

### 1. 多飞书 Bot 配置

每个 Agent 对应一个独立的飞书 Bot：

```json
{
  "channels": {
    "feishu": {
      "accounts": {
        "default": { "appId": "cli_xxx", "appSecret": "xxx" },
        "coder": { "appId": "cli_yyy", "appSecret": "yyy" },
        "reviewer": { "appId": "cli_zzz", "appSecret": "zzz" }
      }
    }
  }
}
```

### 2. Agent 绑定

将 Agent 与飞书账号绑定：

```json
{
  "bindings": [
    { "agentId": "main", "match": { "channel": "feishu", "accountId": "default" } },
    { "agentId": "coder", "match": { "channel": "feishu", "accountId": "coder" } },
    { "agentId": "reviewer", "match": { "channel": "feishu", "accountId": "reviewer" } }
  ]
}
```

### 3. 消息路由

发送消息时指定 `accountId`，Gateway 会路由到对应的飞书 Bot：

```
message action=send channel=feishu accountId="coder" target="ou_xxx" message="..."
                                              │
                                              ▼
                                        码农Bot 发送消息
```

## 数据流

### 私聊消息流

```
子Agent 调用 message tool
        │
        ▼
指定 accountId="coder"
        │
        ▼
Gateway 查找 coder 对应的飞书 Bot
        │
        ▼
使用 coder Bot 的身份发送消息
        │
        ▼
用户收到消息（显示来自码农Bot）
```

### 群聊消息流

```
子Agent 调用 message tool
        │
        ▼
指定 accountId="coder" target="oc_group_id"
        │
        ▼
Gateway 使用 coder Bot 发送到群聊
        │
        ▼
群聊显示消息来自码农Bot
```

## 关键设计决策

### 1. 为什么需要用户 ID 映射表？

**问题：** 每个飞书 Bot 看到的用户 open_id 不同

**原因：** 飞书的安全设计，不同应用对同一用户的标识隔离

**解决：** 维护映射表，发送时使用对应 Bot 看到的 open_id

### 2. 为什么 message tool 不支持 union_id？

**现状：** 飞书 API 的 union_id 获取需要额外权限

**折中：** 使用 open_id + 映射表的方式

### 3. 为什么用户必须先和 Bot 建立会话？

**原因：** 飞书 Bot 无法主动给用户发送私聊消息

**要求：** 用户需要先主动给 Bot 发过消息，建立会话后 Bot 才能回复
