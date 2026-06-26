---
name: cc-log-viewer
description: "实时 Log Viewer，捕获 Claude Code 终端输出，通过 WebSocket 推送到浏览器页面实时显示。用于远程/移动设备上观察 CC 执行任务的过程，或者将 CC 终端嵌入监控面板。同时也提供 CC 进程管理和命令行发送功能。"
metadata:
  tags: ["claude-code", "terminal", "monitoring", "websocket", "xterm"]
  version: 1.0.0
homepage: https://github.com/openclaw/cc-log-viewer
---

# Cc Log Viewer

实时捕获 Claude Code 终端输出，通过 WebSocket 推送到浏览器。支持远程/移动设备观察 CC 执行任务，也可嵌入监控面板。

## 快速开始

### 前置条件

| 条件 | 说明 |
|------|------|
| Node.js ≥ v18 | 运行后端服务 |
| npm | 包管理 |
| Claude Code CLI | 需 `claude` 命令可用 |
| C++ 编译工具 | node-pty 编译需要（Linux: `build-essential`, macOS: Xcode CLT） |

### 网络要求

服务端和浏览器之间需要网络可达：

| 场景 | 方案 |
|------|------|
| 同一台机器 | `http://localhost:18798/`，无需额外配置 |
| 局域网（同 WiFi） | 用服务端局域网 IP，如 `http://192.168.1.x:18798/` |
| 远程/移动设备 | 推荐装 **Tailscale**，手机连上后通过 Tailscale IP 访问，无需公网 IP 或端口转发 |

> ⚠️ 手机和服务端不在同一网络且没有 Tailscale 时，浏览器会显示空白或反复重连。

### 安装

```bash
cd ~/.openclaw/workspace/skills/cc-log-viewer
cd assets && npm install && cd ..
bash assets/start-all.sh
```

### 验证

```bash
curl http://localhost:18798/api/status
# → {"running":true,"clients":0,"bufferLines":87}
```

### 访问浏览器

```
http://localhost:18798/
嵌入模式：http://localhost:18798/?embed=1
```

## HTTP API

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `/api/status` | 状态查询 |
| `POST` | `/api/send` | 向 CC 发命令（body: `{"command":"..."}`） |
| `POST` | `/api/restart` | 重启 CC 进程 |

## 技术架构

```
log-streamer.js (单进程，端口可配置 — 默认 18798)
  ├─ node-pty — 为 CC 提供真实 pty 环境
  │    ↓ stdout
  ├─ 环形缓冲 (1000行)
  │    ↓ 100ms 轮询
  ├─ WebSocket Server — 实时推送
  │    ↓
  ├─ xterm.js (自托管 /cdn/) — 浏览器终端渲染
  └─ HTTP API
```

## 停止

```bash
kill $(lsof -t -i:18798) 2>/dev/null
# 仅重启 CC 不停服务：
curl -X POST http://localhost:18798/api/restart
```

## 文件

| 路径 | 说明 |
|------|------|
| `scripts/log-streamer.js` | 后端服务（HTTP + WebSocket + CC 进程管理） |
| `assets/index.html` | 前端 xterm.js 页面 |
| `assets/start-all.sh` | 一键启动脚本 |
| `assets/package.json` | npm 依赖 |
