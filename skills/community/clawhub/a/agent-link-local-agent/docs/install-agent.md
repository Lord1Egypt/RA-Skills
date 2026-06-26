# 本地 Agent 安装说明

## 前置要求

- Python 3.7+
- OpenClaw 已安装并运行
- 中转服务器已部署并运行

## 快速安装

### 1. 获取文件

将以下文件复制到 OpenClaw 工作区：

```
skills/agent-link/scripts/local-agent/
├── agent_link.py
└── agent-link-config.example.json
```

### 2. 安装依赖

```bash
pip install websockets
```

### 3. 配置

复制配置示例文件：

```bash
cp agent-link-config.example.json agent-link-config.json
```

编辑 `agent-link-config.json`：

```json
{
  "relay_url": "ws://your-relay-server:8765",
  "secret": "your-secret-key-here",
  "instance_id": "instance-001",
  "agent_id": "healthguard",
  "auto_reconnect": true,
  "reconnect_interval": 5
}
```

**重要配置项说明：**

| 配置项 | 说明 | 必填 |
|--------|------|------|
| `relay_url` | 中转服务器 WebSocket 地址 | 是 |
| `secret` | 共享密钥（与中转服务器一致） | 是 |
| `instance_id` | 本地 OpenClaw 实例唯一标识 | 是 |
| `agent_id` | 当前 Agent ID（如 healthguard, main 等） | 是 |
| `auto_reconnect` | 是否自动重连 | 否 |
| `reconnect_interval` | 重连间隔（秒） | 否 |

### 4. 在代码中使用

#### 基本使用

```python
from agent_link import AgentLink, Message

# 创建客户端实例
link = AgentLink(
    relay_url="ws://your-relay-server:8765",
    secret="your-secret-key",
    instance_id="instance-001",
    agent_id="healthguard"
)

# 或者从配置文件创建
link = AgentLink.from_config("agent-link-config.json")

# 注册消息处理器
@link.on_message
def handle_message(msg: Message):
    print(f"收到来自 {msg.from_agent} 的消息: {msg.message}")
    print(f"时间: {msg.timestamp}")

# 连接并运行
import asyncio
asyncio.run(link.connect())
```

#### 发送消息

```python
# 发送给同一实例的其他 agent
await link.send("main", "你好，小包子！")

# 发送给其他实例的 agent
await link.send("instance-002/xiaobaozi", "你好，远程小包子！")
```

#### 完整示例

```python
import asyncio
from agent_link import AgentLink, Message

async def main():
    # 创建客户端
    link = AgentLink.from_config("agent-link-config.json")

    # 注册消息处理器
    @link.on_message
    def handle_message(msg: Message):
        print(f"\n📨 收到消息!")
        print(f"   来自: {msg.from_agent}")
        print(f"   内容: {msg.message}")
        print(f"   时间: {msg.timestamp}")

    # 连接并发送测试消息
    await link.connect()

if __name__ == "__main__":
    asyncio.run(main())
```

### 5. 测试模式

使用测试模式快速验证：

```bash
python3 agent_link.py --config agent-link-config.json --test
```

测试模式提供交互界面：

```
> send main 你好，小包子！
> quit
```

## 在 OpenClaw Agent 中集成

### 在 AGENTS.md 中添加

在你的 AGENTS.md 中添加 agent-link 的使用说明：

```markdown
## Agent Link 集成

使用 agent-link 与其他 agent 通讯：

```python
from agent_link import AgentLink, Message

# 初始化
link = AgentLink.from_config("agent-link-config.json")

# 发送消息
await link.send("main", "任务完成了！")
```
```

### 初始化集成

在你的 agent 启动代码中初始化：

```python
import asyncio
from agent_link import AgentLink, Message

async def setup_agent_link():
    link = AgentLink.from_config("agent-link-config.json")

    @link.on_message
    def handle_agent_message(msg: Message):
        # 处理来自其他 agent 的消息
        print(f"收到来自 {msg.from_agent} 的消息")

    # 后台运行连接
    asyncio.create_task(link.connect())
    return link
```

## 安全建议

1. **密钥安全**
   - 密钥与中转服务器保持一致
   - 不要将密钥提交到版本控制
   - 使用环境变量或密钥管理系统

2. **实例 ID**
   - 每个 OpenClaw 实例使用唯一的 instance_id
   - 建议格式：`device-location-number`（如 `macbook-office-001`）

3. **消息安全**
   - 不要在消息中发送敏感信息
   - 敏感信息考虑端到端加密

## 故障排除

### 无法连接中转服务器

- 检查中转服务器地址和端口
- 检查网络连接
- 检查密钥是否正确
- 查看中转服务器日志

### 消息发送失败

- 检查目标 agent 是否在线
- 检查实例 ID 和 agent ID 格式
- 查看本地和中转服务器日志

### 收不到消息

- 确认消息处理器已正确注册
- 检查 instance_id 和 agent_id 是否匹配
- 查看是否有错误日志

## 目录结构建议

```
~/.openclaw/
├── skills/
│   └── agent-link/          # Agent Link 技能
│       ├── scripts/
│       │   ├── relay-server/  # 中转服务器文件
│       │   └── local-agent/   # 本地 agent 文件
│       └── docs/
└── agent-link-config.json    # 配置文件（每个实例一个）
```

## 更新日志

- **1.0.0** (2026-04-04)
  - 初始版本
  - 支持连接中转服务器
  - 支持发送和接收消息
  - 支持消息签名验证
  - 支持自动重连
