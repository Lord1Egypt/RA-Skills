---
name: agent-handshake
description: 通用 Agent 握手 — 自动发现、注册、打通任意服务器上的 AI Agent。服务器侧生成身份牌（自动识别 OpenCode/LangChain/CrewAI/通用FastAPI/MCP），本地侧持久化记忆，Cloudflare Tunnel 穿透 NAT。触发词：握手、连接 agent、发现 agent、快速握手、注册服务器、打通隧道、打洞、内网穿透。
agent_created: true
---

# Agent Handshake Skill (通用 Agent 握手)

双向握手通道：服务器侧注册身份牌 → 本地侧接收并记忆 → 后续一键握手，全程知道"连接的是哪台服务器"。

## 块式握手通道架构 (v2)

```
┌─────────────────────────────────────────────────────────────────┐
│              通用 Agent 握手通道 (双向)                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   服务器侧 (NAS/云主机)                      本地侧 (Mac/WorkBuddy)
│   ┌─────────────────────┐                  ┌──────────────────┐ │
│   │ ① register.sh       │    身份牌 JSON    │ ② accept.sh      │ │
│   │   生成机器身份牌      │ ─────────────→   │   验证 + 记忆     │ │
│   │   hostname/IP/OS/    │   (复制/共享)     │   存入 servers/   │ │
│   │   Agent ver/SSH   │                  │   更新 _index     │ │
│   └─────────────────────┘                  └──────────────────┘ │
│                                                      │          │
│                           ┌──────────────────────────┘          │
│                           ▼                                      │
│                  ┌──────────────────┐                           │
│                  │ ③ discover.sh    │                           │
│                  │   网络扫描        │                           │
│                  │   + 匹配已知身份   │                           │
│                  │   告知连接的是谁   │                           │
│                  └──────────────────┘                           │
│                           │                                      │
│                           ▼                                      │
│                  ┌──────────────────┐                           │
│                  │ ④ handshake.sh   │                           │
│                  │   展示服务器详情   │                           │
│                  │   建会话 + 发任务  │                           │
│                  │   收结果          │                           │
│                  └──────────────────┘                           │
│                                                                 │
│   记忆层: references/servers/<hostname>.json (持久化)             │
└─────────────────────────────────────────────────────────────────┘
```

## 何时使用

- 用户说"握手 opencode"、"连接 opencode"、"发现 opencode"、"opencode 握手"、"快速握手"
- 用户说"注册 opencode 服务器"
- 在服务器上新装了 OpenCode CLI + 此 skill，想注册到本地
- 用户想在 Mac 上直连 NAS/服务器上的 OpenCode Serve，并知道连接的是哪台机器

## 首次部署：完整的双向流程

### 服务器侧（只做一次）

在安装了 OpenCode CLI 的服务器上运行：

```bash
bash scripts/register.sh
```

输出示例：
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🖥️  服务器身份牌已生成
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  主机名: lvliefeng
  系统:   Debian GNU/Linux 12 (6.18.18.c877-trim)
  架构:   x86_64 | Intel(R) N305
  内存:   15Gi

  🔗 OpenCode Serve 在跑 (v1.18.3, :4096)

  🌐 局域网 IP:
     → 192.168.5.2:4096

  📄 身份牌已保存: references/servers/lvliefeng.json
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

此时 `references/servers/lvliefeng.json` 已生成，包含完整的机器身份。

### 传递身份牌到本地

三种方式任选其一：

- **方式 A（复制文件）**：把服务器上的 `references/servers/lvliefeng.json` 复制到本地的 skill 同目录
- **方式 B（快捷命令）**：本地运行 `bash scripts/accept.sh lvliefeng 192.168.5.2:4096 opencode:opencode123`
- **方式 C（管道）**：SSH 到服务器跑 register.sh，输出管道到本地的 accept.sh

### 本地侧：接受 + 记忆

```bash
# 方式 A/B 都已自动完成，或手动运行：
bash scripts/accept.sh lvliefeng http://192.168.5.2:4096
```

运行后：
1. 验证服务器可达性（GET /global/health）
2. 保存身份牌到 `references/servers/lvliefeng.json`
3. 更新 `references/servers/_index.json`（服务器索引）
4. 保存最佳地址到 `~/.agent-handshake`（全局配置）

### 后续使用：一键握手（自动展示服务器身份）

```bash
bash scripts/handshake.sh auto "列出 NAS 上的 docker 项目"
```

输出示例：
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🔗 通用 Agent 握手
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  地址: http://192.168.5.2:4096
  消息: 列出 NAS 上的 docker 项目
  主机: lvliefeng  Debian GNU/Linux 12 (6.18.18)
  配置: Intel(R) N305 | 内存 15Gi
  Agent: 1.18.3 (serve端口:4096)
  SSH: SHA256:xxxxx

  ✓ 服务在线 (v1.18.3)
  ✓ 会话: ses_xxx

  📨 回复
  (agent 执行工具后的中文结果)
```

## 无公网 IP 时：隧道打通

当服务器在 NAT 后面、没有公网 IP、也不在同一局域网时，用 Cloudflare Quick Tunnel 一行命令打通。

### 原理

```
服务器 (NAT后)                     Cloudflare 全球网络                 本地 (任意网络)
┌──────────────────┐              ┌──────────────────┐              ┌──────────────────┐
│ Agent :4096   │──出站连接──→│ trycloudflare.com │←──HTTPS────│ WorkBuddy/Mac    │
│ cloudflared      │   (隧道)     │ 随机子域名        │              │ handshake.sh     │
└──────────────────┘              └──────────────────┘              └──────────────────┘
```

服务器主动出站连接 Cloudflare（不需要开放入站端口），Cloudflare 分配一个 `https://xxx.trycloudflare.com` 公网地址。本地直接连这个地址，Cloudflare 转发到服务器。

**优势**：零账号、零配置、自动 HTTPS、免费、穿透任意 NAT/防火墙。

### 服务器侧：启动隧道

```bash
bash scripts/tunnel.sh start
```

一行命令：自动安装 cloudflared（如果未装）、建立隧道、返回公网地址。示例输出：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✅ 隧道已建立
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🌍 公网地址: https://random-name.trycloudflare.com
  📋 PID:      12345

  本地握手地址:
  handshake.sh https://random-name.trycloudflare.com "你的问题"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

同时自动更新 `references/servers/<hostname>.json` 身份牌，记录隧道 URL。

### 本地侧：用隧道地址接受服务器

```bash
# 服务器启动隧道后，本地用隧道 URL 接受
bash scripts/accept.sh lvliefeng https://random-name.trycloudflare.com
```

### 后续：一键握手自动走隧道

`handshake.sh auto` 会自动检测隧道地址并优先使用。输出会标注 `🌍 隧道`。

```bash
bash scripts/tunnel.sh status    # 查看隧道状态
bash scripts/tunnel.sh stop      # 停止隧道
```

### 隧道管理

| 命令 | 作用 |
|------|------|
| `tunnel.sh start [port]` | 启动隧道（默认 4096 端口） |
| `tunnel.sh stop` | 停止隧道 |
| `tunnel.sh status` | 查看隧道状态和 URL |

### 注意事项

- 隧道 URL 是**临时的**，cloudflared 进程停止后失效，重连会换新地址
- Cloudflare 限 200 并发请求、不支持 WebSocket（Agent 自动降级 HTTPS 可用）
- 仅适用于**开发和测试**，生产环境建议注册 Cloudflare 账号绑定固定域名
- 隧道走 Cloudflare 中转，延迟取决于服务器到 Cloudflare 边缘节点的距离

## VPS 轻量部署：握手当 SSH 用

无需 SSH 登录 VPS，HTTP 握手直接调 agent 执行任务。部署方式：

### 一行部署

```bash
# 把 skill 目录拷到 VPS，然后：
bash scripts/deploy.sh 4096 user:pass
```

自动完成：拷 agent_shell.py → 写 systemd 服务 → 开机自启 → 启动验证。

### 架构

```
Mac (WorkBuddy)                      VPS
  │  POST /run {"task":"ls /"}        │  agent_shell.py (~40MB)
  │ ──────────────────────────────→   │    │ fork opencode exec
  │                                   │    │ bash / read / write
  │ ←──────────────────────────────   │    ▼
  │  {"success":true,"output":"..."}   │  VPS 文件系统
```

### 手动启动

```bash
python3 scripts/agent_shell.py --port 4096 --auth user:pass
```

### 握手端点

| 端点 | 方法 | 说明 |
|---|---|---|
| `/health` | GET | 健康检查，返回 hostname 和 agent 信息 |
| `/run` | POST | 执行任务，body: `{"task":"你的任务"}`，返回 output |

### 注册到本地

```bash
bash scripts/accept.sh my-vps http://VPS公网IP:4096 user:pass
```

### 日常使用

```bash
# 等价于 SSH 上去敲命令，但不经 SSH
curl -X POST http://my-vps:4096/run -u user:pass \
  -d '{"task":"查看磁盘: df -h && free -h"}'

curl -X POST http://my-vps:4096/run -u user:pass \
  -d '{"task":"更新系统: apt update && apt upgrade -y"}'

curl -X POST http://my-vps:4096/run -u user:pass \
  -d '{"task":"列出 /var/log 下最大的文件"}'
```

Agent 可以读文件、写文件、跑任何命令——跟 SSH 一样，但不暴露 22 端口，换成了 HTTP Basic Auth。

| 脚本 | 位置 | 作用 |
|------|------|------|
| `scripts/register.sh [agent_type]` | **服务器侧** | 采集机器身份 + **自动检测 agent 类型**（opencode/langchain/crewai/generic/mcp），生成含协议的 JSON 身份牌 |
| `scripts/accept.sh` | **本地侧** | 接收服务器身份牌（任意 agent 类型），验证可达性，持久化到 skill 记忆 |
| `scripts/discover.sh` | **本地侧** | 三层网络扫描 + **通用 agent 检测**（不限于 Agent），自动匹配已知服务器 |
| `scripts/tunnel.sh` | **服务器侧** | 一行命令打通 Cloudflare 隧道，穿透 NAT（与 agent 类型无关） |
| `scripts/config.sh` | **本地侧** | 手动保存指定地址 |
| `scripts/handshake.sh` | **本地侧** | 一键握手——自动识别 agent 类型和地址类型（隧道/公网/局域网）|

## 支持 Agent 类型

| agent_type | 健康检查 | 协议 | 检测方式 |
|---|---|---|---|
| `opencode` | `GET /global/health` | `POST /session` → `/session/:id/message` | 返回 `{"healthy":true}` |
| `langchain` | `GET /health` | `POST /chat` (FastAPI) | `/openapi.json` 含 langchain/langserve |
| `crewai` | `GET /health` | `POST /chat` (FastAPI) | `/openapi.json` 含 crewai |
| `generic-fastapi` | `GET /health` | 有 `/docs` (Swagger) | FastAPI 自动文档 |
| `generic` | `GET /health` | 标准 `{"status":"ok"}` | 任意 HTTP agent |
| `mcp` | `GET /health` | MCP 协议 | `/mcp` 端点 |

**通用原则**：只要 agent 提供 `GET /health` 端点（返回 HTTP 200 + JSON 含 status/healthy 字段），就能被发现和注册。`register.sh` 自动识别类型，手动指定用 `register.sh opencode` 或 `register.sh langchain`。

## 记忆层：references/servers/

```
references/servers/
├── _index.json          ← {"servers":{"lvliefeng":{...}},"total":1}
├── lvliefeng.json       ← register.sh 生成的身份牌
├── my-vps.json          ← 另一台服务器的身份牌
└── ...
```

每个 `<hostname>.json` 包含完整的机器身份：hostname、**agent_type**、**protocol**（health端点/会话端点/认证方式）、OS、kernel、arch、CPU、内存、磁盘、LAN IPs、公网 IP、Agent/agent 版本、端口、SSH 指纹、隧道 URL、生成时间戳。

`_index.json` 是自动维护的索引，方便快速列出所有已知服务器。

## 环境变量覆盖

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `OPENCODE_AUTH` | `opencode:opencode123` | Basic Auth 认证 |
| `OPENCODE_PORT` | `4096` | OpenCode Serve 端口 |
| `OPENCODE_PROVIDER` | `zen` | 模型提供商 |
| `OPENCODE_MODEL` | `deepseek-v4-flash-free` | 模型 ID |
| `OPENCODE_SKILL_DIR` | skill 自身目录 | skill 安装路径 |

## 块式面板输出格式

当完成发现和握手后，向用户展示如下面板，明确告知连接的是哪台服务器：

```
┌──────────────────────────────────────────┐
│          Agent 握手通道                │
├──────────────────────────────────────────┤
│  🖥️  主机: lvliefeng (Debian 12)         │
│  🏠 地址: http://192.168.5.2:4096       │
│  🔗 隧道: https://xxx.trycloudflare.com │
│  🔗 Agent: v1.18.3                    │
│  📋 模型:  zen/deepseek-v4-flash-free   │
│  💰 成本:  免费                          │
│  📄 身份:  references/servers/lvliefeng  │
│  🔑 SSH:    SHA256:xxxx                  │
├──────────────────────────────────────────┤
│  已记忆 1 台服务器 | 隧道 🌍 在线          │
│  一键握手: handshake.sh auto "任务"       │
└──────────────────────────────────────────┘
```
