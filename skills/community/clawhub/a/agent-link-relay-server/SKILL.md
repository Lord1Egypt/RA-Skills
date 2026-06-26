---
name: agent-link
version: 1.0.0
description: 智能体互联技能 - 支持不同电脑上的 OpenClaw 实例和 Agent 通过中转服务器进行安全可靠的通讯。包含中转服务器组件和本地 Agent 组件。
when: "当用户需要实现跨设备的 Agent 通讯、或者需要部署中转服务器时使用。"
examples:
  - "安装 agent-link 中转服务器"
  - "配置本地 Agent 连接中转服务器"
  - "通过中转服务器发送消息给其他 Agent"
metadata:
 {
   "openclaw": {
     "requires": { "bins": ["python3", "python", "openclaw"], "anyBins": ["python3", "python"] },
     "emoji": "🔗",
     "primaryEnv": null
   }
 }
---

# Agent Link - 智能体互联

> 跨设备 OpenClaw 实例和 Agent 的安全可靠通讯解决方案

---

## 架构设计

### 核心组件

| 组件 | 部署位置 | 角色 | 功能 |
|------|----------|------|------|
| **中转服务器 (Relay Server)** | 公网服务器 | 消息中转 | 接收、验证、转发消息 |
| **本地 Agent (Local Agent)** | 各个电脑 | 消息收发 | 连接中转服务器、发送/接收消息 |

### 通讯流程

```
本地 Agent A → 本地 OpenClaw → 中转服务器 → 远程 OpenClaw → 远程 Agent B
     ↑                                                            ↓
     └────────────────────────── 确认回执 ──────────────────────┘
```

---

## 功能特性

### ✅ 中转服务器功能
- 消息接收和转发
- Agent 身份注册和验证
- 消息签名验证，防止伪造
- 消息路由分发
- 连接状态监控

### ✅ 本地 Agent 功能
- 连接中转服务器
- 发送消息给其他 Agent
- 接收来自其他 Agent 的消息
- 消息签名和验证
- 断线自动重连

### ✅ 安全机制
- 每个 OpenClaw 实例需要在中转服务器注册
- 每个 Agent 需要在本地 OpenClaw 注册
- 消息签名验证（HMAC-SHA256）
- 中转服务器只做转发，不保存消息内容

---

## 安装说明

### 中转服务器安装

详见 [docs/install-relay.md](docs/install-relay.md)

### 本地 Agent 安装

详见 [docs/install-agent.md](docs/install-agent.md)

---

## 快速开始

### 1. 安装中转服务器

```bash
# 在公网服务器上
cd skills/agent-link/scripts/relay-server
python3 relay_server.py --port 8765 --secret "your-secret-key"
```

### 2. 配置本地 Agent

```bash
# 在本地电脑上
cd skills/agent-link/scripts/local-agent
python3 setup.py --relay-url "ws://your-relay-server:8765" --secret "your-secret-key"
```

### 3. 发送消息

```python
from agent_link import AgentLink

link = AgentLink(agent_id="xiaodingding")
link.send("xiaobaozi", "你好，小包子！")
```

---

## 配置文件

### 中转服务器配置 (relay-config.json)

```json
{
  "port": 8765,
  "secret": "your-secret-key",
  "registered_instances": [
    {
      "instance_id": "instance-001",
      "name": "晨辉的 MacBook",
      "public_key": "..."
    }
  ]
}
```

### 本地 Agent 配置 (agent-link-config.json)

```json
{
  "relay_url": "ws://your-relay-server:8765",
  "secret": "your-secret-key",
  "instance_id": "instance-001",
  "agent_id": "healthguard",
  "auto_reconnect": true
}
```

---

## API 参考

### 中转服务器 API

#### 注册实例
```
POST /api/v1/register
{
  "instance_id": "instance-001",
  "public_key": "...",
  "name": "晨辉的 MacBook"
}
```

#### 发送消息
```
POST /api/v1/send
{
  "from": "instance-001/healthguard",
  "to": "instance-002/xiaobaozi",
  "message": "你好，小包子！",
  "signature": "..."
}
```

### 本地 Agent API

#### 初始化
```python
link = AgentLink(config_path="agent-link-config.json")
```

#### 发送消息
```python
link.send(to_agent="xiaobaozi", message="你好！")
```

#### 接收消息
```python
@link.on_message
def handle_message(from_agent, message):
    print(f"收到来自 {from_agent} 的消息: {message}")
```

---

## 安全说明

1. **密钥管理**
   - 中转服务器和本地 Agent 使用共享密钥
   - 密钥需要安全保存，不要泄露

2. **消息签名**
   - 所有消息使用 HMAC-SHA256 签名
   - 防止消息伪造和篡改

3. **数据隐私**
   - 中转服务器只做消息转发
   - 不保存消息内容
   - 消息传输使用 WSS (WebSocket Secure)

---

## 故障排除

### 中转服务器无法启动
- 检查端口是否被占用
- 检查防火墙设置
- 查看日志文件

### 本地 Agent 无法连接
- 检查中转服务器地址是否正确
- 检查网络连接
- 检查密钥是否匹配

### 消息发送失败
- 检查目标 Agent 是否在线
- 检查消息签名是否正确
- 查看中转服务器日志

---

## 更新日志

- **1.0.0** (2026-04-04)
  - 初始版本发布
  - 支持中转服务器和本地 Agent 通讯
  - 支持消息签名验证
  - 支持断线自动重连
