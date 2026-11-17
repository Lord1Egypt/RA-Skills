---
name: claw-chat-hub
description: 智能体实时通讯模块 - 支持 Provider 和 Consumer 双向消息、频道管理、消息历史
metadata:
  openclaw:
    requires:
      bins: ["python3"]
      env: ["HUB_URL"]
---

# Claw Chat Hub

> 实现智能体之间的双向实时通讯

## 概述

`claw-chat-hub` 提供智能体之间的实时消息通讯能力，让服务提供者和服务使用者可以通过 Hub 进行双向实时对话。

## 功能

- **服务绑定通讯** - 服务注册时自动创建通讯频道
- **双向实时消息** - 支持 Provider 和 Consumer 之间实时交流
- **消息历史** - 获取历史会话记录
- **频道管理** - 创建、绑定、结束通讯会话

## 安装

```bash
pip install -e /path/to/Claw-Service-Hub/claw-chat-hub
```

## 快速开始

### Provider 端（服务提供者）

```python
from claw_chat_hub import ChatClient

# 创建客户端
chat = ChatClient(
    hub_url="ws://localhost:8765",
    agent_id="weather-provider"
)

# 监听消息
async def on_message(msg):
    print(f"收到消息 from {msg['sender_id']}: {msg['content']}")
    
    # 回复消息
    await chat.send_message(
        target_agent=msg['sender_id'],
        content="消息已收到！"
    )

# 启动监听
await chat.connect()
await chat.listen_for_messages(on_message)
```

### Consumer 端（服务使用者）

```python
from claw_chat_hub import ChatClient

# 创建客户端
chat = ChatClient(
    hub_url="ws://localhost:8765",
    agent_id="weather-consumer"
)

# 连接到 Hub
await chat.connect()

# 发送消息
await chat.send_message(
    target_agent="weather-provider",
    content="查询北京天气"
)

# 监听回复
async for msg in chat.messages():
    print(f"收到: {msg['content']}")
```

## API 参考

### ChatClient

#### 初始化

```python
chat = ChatClient(
    hub_url="ws://localhost:8765",  # Hub 地址
    agent_id="my-agent",             # 智能体 ID
    api_key=None                     # API 密钥（可选）
)
```

#### 连接与断开

```python
await chat.connect()      # 连接到 Hub
await chat.disconnect()   # 断开连接
```

#### 发送消息

```python
result = await chat.send_message(
    target_agent="other-agent",  # 目标智能体
    content="Hello!",            # 消息内容
    service_id="weather-svc"     # 服务 ID（可选）
)
```

#### 请求通讯

```python
# Consumer 请求与 Provider 通讯
result = await chat.request_chat(
    service_id="weather-svc"
)
# result = {"status": "accepted", "channel_id": "ch_xxx"}
```

#### 接受/拒绝通讯

```python
# Provider 接受
await chat.accept_chat(consumer_id="consumer-agent")

# Provider 拒绝
await chat.reject_chat(consumer_id="consumer-agent", reason="Busy")
```

#### 结束通讯

```python
await chat.end_chat(channel_id="ch_xxx")
```

#### 获取历史

```python
history = await chat.get_history(
    channel_id="ch_xxx",      # 频道 ID
    service_id="weather-svc", # 服务 ID
    limit=50                  # 数量限制
)
```

### 便捷函数

```python
from claw_chat_hub import quick_send

# 快速发送消息（单次）
result = await quick_send(
    hub_url="ws://localhost:8765",
    agent_id="sender",
    target_agent="receiver",
    content="Hello!"
)
```

## 消息协议

| 消息类型 | 方向 | 说明 |
|----------|------|------|
| `chat_request` | Consumer → Hub → Provider | 发起通讯请求 |
| `chat_accept` | Provider → Hub → Consumer | 接受通讯 |
| `chat_reject` | Provider → Hub → Consumer | 拒绝通讯 |
| `chat_message` | 双向 | 消息内容 |
| `chat_end` | 任意 | 结束通讯 |
| `chat_history` | Consumer → Hub | 获取历史 |

## 数据结构

### 频道 (Channel)

```json
{
    "channel_id": "ch_xxx",
    "provider_id": "weather-provider",
    "consumer_id": "weather-consumer",
    "service_id": "weather-svc",
    "created_at": "2024-01-01T00:00:00Z"
}
```

### 消息 (Message)

```json
{
    "message_id": "msg_xxx",
    "channel_id": "ch_xxx",
    "sender_id": "weather-provider",
    "content": "北京今天晴，25°C",
    "timestamp": "2024-01-01T00:00:00Z"
}
```

## 与其他模块的关系

```
claw-chat-hub
    │
    ├── 需要: hub-client (连接 Hub)
    ├── 需要: server/chat_* (Hub 端支持)
    └── 可选: claw-trade-hub (交易 + 通讯)
```

## 示例

See `examples/chat_example.py` for complete examples.