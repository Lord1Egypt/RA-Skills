---
name: a2a-msg
description: 通过 Redis 消息队列与其他 OpenClaw 实例通信（需自备 Redis 服务器）
metadata: { "openclaw": { "emoji": "📨", "requires": { "bins": ["python3"], "env":["A2A_REDIS_HOST","A2A_REDIS_PORT","A2A_REDIS_PASSWORD","A2A_MY_ID","A2A_PEER_ID"] } } }
---

# a2a-msg Skill

通过 Redis 消息队列与其他 OpenClaw 实例（A2A）通信。支持 AI 理解并自动处理消息。

## 功能

- 发送消息给另一个 Agent
- 接收来自另一个 Agent 的消息
- 查看消息队列状态
- **AI 自动处理消息**（auto 模式）

## 前置要求

**⚠️ 需要自备 Redis 服务器**

本 skill 需要一台运行 Redis 的服务器。你可以使用自己的服务器、VPS 或 Docker 安装。

### Docker 安装 Redis（推荐）

创建 `docker-compose.yml` 文件：

```yaml
version: '3.8'
services:
  redis:
    image: redis:alpine
    container_name: redis-a2a
    ports:
      - "6379:6379"
    command: redis-server --requirepass 你的密码
    restart: unless-stopped
```

启动 Redis：
```bash
docker-compose up -d
```

## 配置（重要！）

**必须设置环境变量**，请添加到 `~/.openclaw/.env` 文件：

```bash
# Redis 配置
A2A_REDIS_HOST=你的Redis服务器地址
A2A_REDIS_PORT=6379
A2A_REDIS_PASSWORD=你的Redis密码

# Agent ID 配置
A2A_MY_ID=你的ID（例如 daodao）
A2A_PEER_ID=对方ID（例如 bibi）
```

示例 `.env` 文件：
```bash
A2A_REDIS_HOST=your.redis.server.ip
A2A_REDIS_PORT=6379
A2A_REDIS_PASSWORD=your_password_here
A2A_MY_ID=your_agent_id
A2A_PEER_ID=peer_agent_id
```

> 注意：Port 默认值是 6379，如果你的 Redis 也是默认端口，可以不填

## 使用方法

### 发送消息

```
告诉 bibi xxx
发给 bibi xxx
send to bibi xxx
```

### 接收消息

```
接收消息
查看消息
check messages
poll
```

### 队列状态

```
队列状态
queue status
```

### AI 自动处理（重要！）

```
自动处理
auto
```

收到消息后，AI 会：
1. 理解消息意思
2. 执行对应操作
3. 自动回复结果给发送者

支持的命令：
- `列出技能` / `show skills` → 列出所有技能
- `天气` / `weather` → 天气查询
- `搜索xxx` / `search xxx` → 搜索功能
- `告诉xxx xxx` → 发消息给xxx
- `队列状态` / `queue status` → 查看队列

## 命令行用法

```bash
# 发送消息
python scripts/a2a.py send --to bibi --content "你好"

# 接收消息（只收不处理）
python scripts/a2a.py poll

# 自动处理模式（收消息 + AI理解 + 回复）
python scripts/a2a.py auto

# 查看队列
python scripts/a2a.py queue
```

## 定时任务

可以设置定时自动检查消息：
```bash
# 每天 23:00 自动运行
schtasks /create /tn "A2A_Poll" /tr "python scripts/a2a.py auto" /sc daily /st 23:00
```
