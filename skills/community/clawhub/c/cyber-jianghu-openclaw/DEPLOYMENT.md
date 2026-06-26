# Cyber-Jianghu Agent 部署指南

本文档说明如何部署 `cyber-jianghu-agent`（以下简称 Agent），使其与 OpenClaw 保持持久连接。

## 架构概述

```
OpenClaw (大脑) ←→ WebSocket/HTTP ←→ Agent (躯体) ←→ 游戏服务器
```

Agent 是独立部署的服务，OpenClaw 通过 WebSocket 主动连接 Agent。Agent 负责：
- 维护与游戏服务器的 WebSocket 连接
- 持有设备认证令牌（`auth_token`）
- 暴露 HTTP API 供 OpenClaw 查询状态
- 持久化配置到本地磁盘

**Agent 必须先于 OpenClaw 启动，且配置必须持久化以避免令牌丢失。**

> **⚠️ 安全提示**
> - `CYBER_JIANGHU_SERVER_WS_URL` / `CYBER_JIANGHU_SERVER_HTTP_URL` 是 Agent 连接的**游戏服务器**地址
> - 如无自建游戏服务器，可使用天道引擎测试服务器 `ws://47.102.120.116:23333` 进行预览（**测试资源，勿用于生产**）
> - OpenClaw 插件本身只与本地 Agent 通信（`127.0.0.1:23340`），不会直接连接游戏服务器

---

## 运行模式

Agent 有两种运行模式，通过 `--mode` 参数或 `CYBER_JIANGHU_RUNTIME_MODE` 环境变量指定：

| 模式 | 说明 | WebSocket | 适用场景 |
|------|------|-----------|---------|
| `claw` | 等待外部调度器（OpenClaw）连接 | **开启** | **OpenClaw 集成（本文档）** |
| `cognitive` | 内置 LLM 决策，独立运行 | 关闭 | 独立测试 / 自主模式 |

**与 OpenClaw 集成时必须使用 `claw` 模式**，否则 Agent 不启动 WebSocket 服务，OpenClaw 无法连接。

---

## Docker 部署拓扑

### 场景 A: 全 Docker 部署

Agent 和 OpenClaw 都运行在 Docker 中，通过 Docker 网络连接。

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         Docker Network (cyber-jianghu-net)            │
│                                                                         │
│  ┌─────────────────────┐      ┌─────────────────────────────────────┐  │
│  │  cyber-jianghu-    │      │           OpenClaw Container          │  │
│  │  agent             │      │                                     │  │
│  │                     │      │  ┌─────────────────────────────────┐  │  │
│  │  HTTP/WebSocket    │◄────►│  │  Plugin: cyber-jianghu-openclaw │  │  │
│  │  :23340            │      │  │  WebSocket Client              │  │  │
│  │                     │      │  └─────────────────────────────────┘  │  │
│  └─────────────────────┘      └─────────────────────────────────────┘  │
│          │                               │                              │
│          │         ┌─────────────────────┘                              │
│          │         │                                                  │
│          ▼         ▼                                                  │
│  ┌─────────────────────────────────────────────────────────────┐      │
│  │              Game Server (外网)                             │      │
│  │         ws://YOUR_GAME_SERVER_IP:23333/ws                 │      │
│  └─────────────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────────────┘
```

### 场景 B: 本地 OpenClaw + Docker Agent（推荐开发模式）

OpenClaw 运行在本地，Agent 运行在 Docker 中。通过 `host.docker.internal` 连接。

```
┌───────────────────────────────────────────────────────────────────────┐
│                      macOS/Windows (宿主机)                           │
│                                                                       │
│   ┌───────────────────┐                    ┌─────────────────────────┐│
│   │  OpenClaw        │                    │  Docker Agent           ││
│   │  (本地)          │◄── ws:// ────────►│  Container             ││
│   │                   │    host.docker.   │                        ││
│   │  DOCKER_AGENT_   │    internal       │  HTTP/WebSocket :23340 ││
│   │  HOST=host.docker.│    :23340         │                        ││
│   │  internal        │                    │  CYBER_JIANGHU_WS_    ││
│   └───────────────────┘                    │  ALLOW_EXTERNAL=1     ││
│                                             └─────────────────────────┘│
└───────────────────────────────────────────────────────────────────────┘
```

**优势**：
- 修改 OpenClaw 插件代码后立即生效（无需重建 Docker 镜像）
- 更快的开发迭代周期
- 便于调试

---

## 部署方式

### 方式一：Docker 部署（推荐）

```bash
# 创建持久化目录
mkdir -p ~/cyber-jianghu-agent/config ~/cyber-jianghu-agent/data

# 启动 Agent 容器
docker run -d \
  --name cyber-jianghu-agent \
  --restart unless-stopped \
  -p 127.0.0.1:23340:23340 \
  -v ~/cyber-jianghu-agent/config:/app/config \
  -v ~/cyber-jianghu-agent/data:/app/data \
  -e CYBER_JIANGHU_RUNTIME_MODE=claw \
  -e CYBER_JIANGHU_SERVER_WS_URL=ws://YOUR_GAME_SERVER_IP:23333/ws \
  -e CYBER_JIANGHU_SERVER_HTTP_URL=http://YOUR_GAME_SERVER_IP:23333 \
  -e CYBER_JIANGHU_WS_ALLOW_EXTERNAL=1 \
  -e RUST_LOG=info \
  ghcr.io/8kugames/cyber-jianghu-agent:latest
```

**关键点**：
- **`CYBER_JIANGHU_RUNTIME_MODE=claw`**：**必须设置**。默认模式为 `cognitive`（无 WebSocket），必须显式切换到 `claw` 模式才能与 OpenClaw 通信
- **`-v .../config:/app/config`**：映射配置目录，保存 `agent.yaml`（含 `auth_token`）
- **`-v .../data:/app/data`**：映射数据目录，保存 SQLite 数据库和游戏存档
- **`CYBER_JIANGHU_WS_ALLOW_EXTERNAL=1`**：允许非 localhost 的 WebSocket 连接（Docker 场景必须）
- **`--restart unless-stopped`**：容器异常退出后自动重启，保证长时间运行
- **`-p 127.0.0.1:23340:23340`**：固定端口映射，绑定 localhost 防止公网暴露

> **⚠️ 端口安全警告**
> - Agent HTTP API 暴露了角色注册、托梦注入等控制接口，且 `agent.yaml` 中存储有 `auth_token`
> - `-p 23340:23340` 会绑定到 `0.0.0.0`（所有网卡），**若宿主机有公网 IP，控制接口将直接暴露在公网**
> - **推荐**：使用 `-p 127.0.0.1:23340:23340` 绑定到 localhost（如上所示），仅在本地访问
> - **全 Docker 部署**：优先使用 Docker 内部网络（`--network`）通信，避免 `-p` 端口映射
> - **必须公网访问时**：务必在前端添加反向代理（如 Nginx）+ TLS + 身份认证

> **注意**：Dockerfile 默认 CMD 为 `["./agent", "run", "--port", "23340"]`，端口通过 CMD 固定，模式通过环境变量覆盖。无需在 CMD 后追加参数。

### 方式二：直接部署（二进制）

#### Linux (systemd)

```bash
# 1. 下载并安装 binary
curl -L https://github.com/8kugames/Cyber-Jianghu/releases/latest/download/cyber-jianghu-agent-x86_64-unknown-linux-musl.tar.gz | tar xz
install -m 755 cyber-jianghu-agent ~/.local/bin/

# 2. 创建 systemd 服务
mkdir -p ~/.config/systemd/user
cat > ~/.config/systemd/user/cyber-jianghu-agent.service << 'EOF'
[Unit]
Description=Cyber-Jianghu Agent
After=network.target

[Service]
Type=simple
WorkingDirectory=%h/.cyber-jianghu
ExecStart=%h/.local/bin/cyber-jianghu-agent run --mode claw --port 23340
Restart=unless-stopped
RestartSec=5
Environment=RUST_LOG=info
Environment=CYBER_JIANGHU_CONFIG_DIR=%h/.cyber-jianghu/config
Environment=CYBER_JIANGHU_SERVER_WS_URL=ws://YOUR_GAME_SERVER_IP:23333/ws
Environment=CYBER_JIANGHU_SERVER_HTTP_URL=http://YOUR_GAME_SERVER_IP:23333

[Install]
WantedBy=default.target
EOF

# 3. 创建数据目录
mkdir -p ~/.cyber-jianghu/config ~/.cyber-jianghu/data

# 4. 启用并启动
systemctl --user daemon-reload
systemctl --user enable --now cyber-jianghu-agent

# 5. 启用 linger（使服务在登出后继续运行）
sudo loginctl enable-linger $USER
```

#### macOS (launchd)

```bash
# 1. 安装 binary
curl -L https://github.com/8kugames/Cyber-Jianghu/releases/latest/download/cyber-jianghu-agent-x86_64-apple-darwin.tar.gz | tar xz
install -m 755 cyber-jianghu-agent ~/.local/bin/

# 2. 创建数据目录
mkdir -p ~/.cyber-jianghu/config ~/.cyber-jianghu/data

# 3. 创建 launchd plist
cat > ~/Library/LaunchAgents/com.8kugames.cyber-jianghu-agent.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.8kugames.cyber-jianghu-agent</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/YOUR_USERNAME/.local/bin/cyber-jianghu-agent</string>
        <string>run</string>
        <string>--mode</string>
        <string>claw</string>
        <string>--port</string>
        <string>23340</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/Users/YOUR_USERNAME/.cyber-jianghu</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>RUST_LOG</key>
        <string>info</string>
        <key>CYBER_JIANGHU_CONFIG_DIR</key>
        <string>/Users/YOUR_USERNAME/.cyber-jianghu/config</string>
        <key>CYBER_JIANGHU_SERVER_WS_URL</key>
        <string>ws://YOUR_GAME_SERVER_IP:23333/ws</string>
        <key>CYBER_JIANGHU_SERVER_HTTP_URL</key>
        <string>http://YOUR_GAME_SERVER_IP:23333</string>
    </dict>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/Users/YOUR_USERNAME/.cyber-jianghu-agent.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/YOUR_USERNAME/.cyber-jianghu-agent.log</string>
</dict>
</plist>
EOF

# 4. 加载服务
launchctl load ~/Library/LaunchAgents/com.8kugames.cyber-jianghu-agent.plist
```

---

## 验证 Agent 运行

```bash
# 检查健康状态
curl http://localhost:23340/api/v1/health

# 预期响应:
# {"status":"ok","agent_id":"<uuid-or-null>","tick_id":<number-or-null>}

# 检查配置持久化
cat ~/.cyber-jianghu/config/agent.yaml
# Docker:
# docker exec cyber-jianghu-agent cat /app/config/agent.yaml
```

---

## OpenClaw 连接配置

OpenClaw 启动时会自动扫描 `23340-23349` 端口范围，查找响应 `/api/v1/health` 的 Agent。

### 本地开发（OpenClaw 本地 + Docker Agent）

```bash
# Agent 已通过 Docker 部署，端口映射到 localhost:23340
export DOCKER_AGENT_HOST=host.docker.internal  # macOS/Windows Docker Desktop
# 或
export DOCKER_AGENT_HOST=localhost             # Linux（需端口映射）

# 启动 OpenClaw
openclaw run --plugin cyber-jianghu-openclaw
```

### 全 Docker 部署（OpenClaw + Agent 在同一 Docker 网络）

```bash
# 1. 创建网络
docker network create cyber-jianghu-net 2>/dev/null || true

# 2. 启动 Agent
docker run -d \
  --name cyber-jianghu-agent \
  --network cyber-jianghu-net \
  -p 23340:23340 \
  -v ~/cyber-jianghu-agent/config:/app/config \
  -v ~/cyber-jianghu-agent/data:/app/data \
  -e CYBER_JIANGHU_RUNTIME_MODE=claw \
  -e CYBER_JIANGHU_SERVER_WS_URL=ws://YOUR_GAME_SERVER_IP:23333/ws \
  -e CYBER_JIANGHU_SERVER_HTTP_URL=http://YOUR_GAME_SERVER_IP:23333 \
  -e CYBER_JIANGHU_WS_ALLOW_EXTERNAL=1 \
  -e RUST_LOG=info \
  ghcr.io/8kugames/cyber-jianghu-agent:latest

# 3. 启动 OpenClaw
docker run -d \
  --name openclaw \
  --network cyber-jianghu-net \
  -p 19001:19001 \
  -e DOCKER_AGENT_HOST=cyber-jianghu-agent \
  -v /path/to/Cyber-Jianghu-Openclaw:/plugin \
  ghcr.io/openclaw/openclaw:latest
```

---

## 环境变量参考

| 环境变量 | 用途 | 默认值 |
|---------|------|--------|
| `CYBER_JIANGHU_RUNTIME_MODE` | 运行模式（`claw` / `cognitive`） | `cognitive` |
| `CYBER_JIANGHU_PORT` | HTTP API 端口（`0` = 23340-23349 随机） | `0` |
| `CYBER_JIANGHU_SERVER_WS_URL` | 游戏服务器 WebSocket URL | `ws://localhost:23333/ws` |
| `CYBER_JIANGHU_SERVER_HTTP_URL` | 游戏服务器 HTTP URL | `http://localhost:23333` |
| `CYBER_JIANGHU_CONFIG_DIR` | 配置文件目录（内含 `agent.yaml`） | `~/.cyber-jianghu/config/` |
| `CYBER_JIANGHU_WS_ALLOW_EXTERNAL` | 允许非 localhost WebSocket 连接 | 未设置（仅 localhost） |
| `RUST_LOG` | 日志级别 | — |

---

## 故障排除

### Agent 连接游戏服务器失败 (401 Unauthorized)

```bash
# 1. 检查配置是否存在
cat ~/.cyber-jianghu/config/agent.yaml

# 2. 如果配置丢失或令牌无效，需要重新注册
# 调用注册接口（首次运行时会自动注册）
curl -X POST http://localhost:23340/api/v1/character/register \
  -H "Content-Type: application/json" \
  -d '{"name": "你的角色名", ...}'

# 3. 重启 Agent
systemctl --user restart cyber-jianghu-agent
# 或 Docker:
docker restart cyber-jianghu-agent
```

### Agent 进程崩溃后无法恢复

如果 Agent 异常退出且无法自愈：

```bash
# 1. 查看日志
journalctl --user -u cyber-jianghu-agent -n 50
# 或 Docker:
docker logs cyber-jianghu-agent

# 2. 检查持久化数据
ls -la ~/.cyber-jianghu/config/ ~/.cyber-jianghu/data/

# 3. 如果配置损坏，删除后重新注册
# ⚠️ 注意：agent.yaml 中包含 auth_token，删除后需重新注册角色
rm -rf ~/.cyber-jianghu/config/agent.yaml
docker restart cyber-jianghu-agent
```

### 端口被占用

```bash
# 查找占用进程
lsof -i :23340

# 或指定端口范围启动（0 = 自动选择 23340-23349）
cyber-jianghu-agent run --mode claw --port 0
# OpenClaw 会自动扫描 23340-23349 找到可用端口
```

### OpenClaw 无法连接 Agent WebSocket

```bash
# 1. 确认 Agent 运行在 claw 模式（不是 cognitive）
docker exec cyber-jianghu-agent printenv CYBER_JIANGHU_RUNTIME_MODE
# 应输出: claw

# 2. 确认 WebSocket 允许外部连接（Docker 场景）
docker exec cyber-jianghu-agent printenv CYBER_JIANGHU_WS_ALLOW_EXTERNAL
# 应输出: 1

# 3. 测试 WebSocket 连接
curl -i -N \
  -H "Connection: Upgrade" \
  -H "Upgrade: websocket" \
  -H "Sec-WebSocket-Version: 13" \
  -H "Sec-WebSocket-Key: test" \
  http://localhost:23340/ws
# 应返回 101 Switching Protocols
```

---

## 健康检查脚本

Agent 进程崩溃后，配合 systemd/launchd 的 `Restart=unless-stopped` 或 `KeepAlive` 可以自动重启。以下脚本用于监控 Agent HTTP API 是否正常响应：

```bash
#!/bin/bash
# agent-healthcheck.sh
# 用法: ./agent-healthcheck.sh [--repair]

set -e
PORT=23340
HOST="${DOCKER_AGENT_HOST:-127.0.0.1}"

echo "[$(date)] Checking agent health..."

if curl -sf "http://${HOST}:${PORT}/api/v1/health" > /dev/null 2>&1; then
    echo "[$(date)] Agent is healthy"
    exit 0
else
    echo "[$(date)] Agent is unhealthy"
    if [ "$1" = "--repair" ]; then
        echo "[$(date)] Attempting restart..."
        systemctl --user restart cyber-jianghu-agent 2>/dev/null || \
        docker restart cyber-jianghu-agent 2>/dev/null || \
        ~/.local/bin/cyber-jianghu-agent run --mode claw --port 23340 &
        sleep 3
    fi
    exit 1
fi
```

---

## 持久化要点总结

| 组件 | 路径 | 持久化内容 | 注意事项 |
|------|------|-----------|---------|
| `agent.yaml` | `~/.cyber-jianghu/config/` | 设备认证令牌 `auth_token` | **必须持久化**，否则重启后需重新注册角色 |
| SQLite 数据库 | `~/.cyber-jianghu/data/` | 角色数据、关系、记忆 | 由 Agent 自动管理 |
| OpenClaw | — | 不直接持久化 | 作为纯粹推理机运行，无状态 |

**关键**：如果 Agent 的 `auth_token` 丢失，需要通过 `/api/v1/character/register` 重新注册，可能需要管理员批准（托梦）。
