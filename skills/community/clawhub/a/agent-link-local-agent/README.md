# Agent Link - 智能体互联技能

> 跨设备 OpenClaw 实例和 Agent 的安全可靠通讯解决方案

---

## 📦 技能概览

### 功能特性

- ✅ **中转服务器** - 部署在公网服务器，负责消息中转和分发
- ✅ **本地 Agent** - 部署在各个电脑，连接中转服务器收发消息
- ✅ **安全验证** - 消息签名验证（HMAC-SHA256），防止伪造
- ✅ **自动重连** - 断线自动重连机制
- ✅ **实例注册** - OpenClaw 实例身份注册和管理

### 架构设计

```
本地 Agent A → 本地 OpenClaw → 中转服务器 → 远程 OpenClaw → 远程 Agent B
     ↑                                                            ↓
     └────────────────────────── 确认回执 ──────────────────────┘
```

---

## 🚀 快速开始

### 第一步：部署中转服务器

1. 上传中转服务器文件到公网服务器
2. 安装依赖：`pip install websockets`
3. 配置 `relay-config.json`
4. 启动服务

详见：[docs/install-relay.md](docs/install-relay.md)

### 第二步：配置本地 Agent

1. 复制本地 Agent 文件到 OpenClaw 工作区
2. 安装依赖：`pip install websockets`
3. 配置 `agent-link-config.json`
4. 在代码中集成使用

详见：[docs/install-agent.md](docs/install-agent.md)

---

## 📁 文件结构

```
agent-link/
├── SKILL.md                          # 技能说明文档
├── README.md                          # 本文件
├── _meta.json                         # 技能元数据
├── docs/
│   ├── install-relay.md                # 中转服务器安装说明
│   └── install-agent.md                # 本地 Agent 安装说明
└── scripts/
    ├── relay-server/                  # 中转服务器端
    │   ├── relay_server.py              # 中转服务器核心代码
    │   └── relay-config.example.json   # 中转服务器配置示例
    └── local-agent/                   # 本地 Agent 端
        ├── agent_link.py               # 本地 Agent 核心代码
        └── agent-link-config.example.json  # 本地 Agent 配置示例
```

---

## 💻 使用示例

### 发送消息

```python
from agent_link import AgentLink

# 创建客户端
link = AgentLink.from_config("agent-link-config.json")

# 发送给同一实例的其他 agent
await link.send("main", "你好，小包子！")

# 发送给其他实例的 agent
await link.send("instance-002/xiaobaozi", "你好，远程小包子！")
```

### 接收消息

```python
from agent_link import AgentLink, Message

link = AgentLink.from_config("agent-link-config.json")

@link.on_message
def handle_message(msg: Message):
    print(f"收到来自 {msg.from_agent} 的消息: {msg.message}")

# 连接并运行
import asyncio
asyncio.run(link.connect())
```

---

## 🔒 安全机制

### 1. 共享密钥

中转服务器和所有本地 Agent 使用相同的共享密钥。

### 2. 消息签名

所有消息使用 HMAC-SHA256 签名，防止伪造和篡改。

### 3. 实例注册

每个 OpenClaw 实例需要在中转服务器注册身份。

### 4. 数据隐私

- 中转服务器只做消息转发
- 不保存消息内容
- 推荐使用 WSS (WebSocket Secure)

---

## 📊 两个安装包

### 中转服务器安装包

包含文件：
- `scripts/relay-server/relay_server.py`
- `scripts/relay-server/relay-config.example.json`
- `docs/install-relay.md`

### 本地 Agent 安装包

包含文件：
- `scripts/local-agent/agent_link.py`
- `scripts/local-agent/agent-link-config.example.json`
- `docs/install-agent.md`

---

## 🛠️ 配置示例

### 中转服务器配置

```json
{
  "port": 8765,
  "secret": "your-strong-secret-key",
  "registered_instances": [
    {
      "instance_id": "instance-001",
      "name": "晨辉的 MacBook",
      "public_key": ""
    }
  ]
}
```

### 本地 Agent 配置

```json
{
  "relay_url": "ws://your-relay-server:8765",
  "secret": "your-strong-secret-key",
  "instance_id": "instance-001",
  "agent_id": "healthguard",
  "auto_reconnect": true
}
```

---

## 🆘 故障排除

### 中转服务器问题

- 检查端口是否被占用
- 检查防火墙设置
- 查看日志文件

### 本地 Agent 问题

- 检查中转服务器地址
- 检查网络连接
- 检查密钥是否匹配

详见各安装文档中的故障排除章节。

---

## 📚 相关文档

- [SKILL.md](SKILL.md) - 完整技能说明
- [docs/install-relay.md](docs/install-relay.md) - 中转服务器安装
- [docs/install-agent.md](docs/install-agent.md) - 本地 Agent 安装

---

## 📝 版本历史

- **1.0.0** (2026-04-04)
  - 初始版本发布
  - 支持中转服务器和本地 Agent 通讯
  - 支持消息签名验证
  - 支持断线自动重连

---

## 📄 许可证

MIT-0 - 可自由使用、修改和分发，无需署名。

---

**由小豆丁 (healthguard) 为晨辉创建** 🛡️
