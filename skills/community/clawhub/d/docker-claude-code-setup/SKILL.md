---
name: docker-claude-code-setup
description: |
  Guide for setting up Claude Code in Docker containers with ttyd web terminal, tmux session persistence, acpx multi-agent tool, and API configuration. Use when: (1) Installing Claude Code in Docker/OpenClaw environments, (2) Setting up web-accessible terminal with ttyd, (3) Configuring persistent sessions with tmux, (4) Installing acpx for multi-agent workflows, (5) Configuring API keys for different providers.

  在 Docker 容器中部署 Claude Code 的完整指南，包括 ttyd Web 终端、tmux 会话持久化、acpx 多代理工具和 API 配置。适用场景：(1) 在 Docker/OpenClaw 环境安装 Claude Code，(2) 配置 ttyd Web 终端，(3) 使用 tmux 保持会话持久化，(4) 安装 acpx 实现多代理工作流，(5) 配置不同 API 提供商的密钥。
---

# Docker Claude Code Setup / Docker 环境部署 Claude Code

Complete guide for deploying Claude Code in Docker containers with web terminal access and persistent sessions.

在 Docker 容器中完整部署 Claude Code 的指南，支持 Web 终端访问和会话持久化。

## Quick Start / 快速开始

### 1. Install Claude Code / 安装 Claude Code

```bash
# Install Node.js if needed / 如需要先安装 Node.js
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt-get install -y nodejs

# Install Claude Code / 安装 Claude Code
npm install -g @anthropic-ai/claude-code
```

See [references/claude-code-installation.md](references/claude-code-installation.md) for detailed configuration.

详细配置见 [references/claude-code-installation.md](references/claude-code-installation.md)。

### 2. Install ttyd + tmux / 安装 ttyd + tmux

```bash
# Install packages / 安装软件包
apt-get update && apt-get install -y ttyd tmux

# Run setup script / 运行启动脚本
bash scripts/start-ttyd.sh 6080
```

Access at http://localhost:6080 - sessions persist after browser close!

访问 http://localhost:6080 - 关闭浏览器后会话保持！

See [references/ttyd-tmux-setup.md](references/ttyd-tmux-setup.md) for configuration details.

配置详情见 [references/ttyd-tmux-setup.md](references/ttyd-tmux-setup.md)。

### 3. Install acpx (Optional) / 安装 acpx (可选)

```bash
# Install acpx / 安装 acpx
bash scripts/install-acpx.sh

# Usage / 使用
acpx claude-code "your task"
```

See [references/acpx-setup.md](references/acpx-setup.md) for multi-agent configuration.

多代理配置见 [references/acpx-setup.md](references/acpx-setup.md)。

### 4. Configure API / 配置 API

```bash
# Set environment variables / 设置环境变量
export ANTHROPIC_API_KEY="your-api-key"
export ANTHROPIC_BASE_URL="https://api.example.com/v1"  # Optional / 可选
export ANTHROPIC_MODEL="model-name"  # Optional / 可选

# Start Claude Code / 启动 Claude Code
claude
```

See [references/api-configuration.md](references/api-configuration.md) for provider-specific settings.

各提供商配置见 [references/api-configuration.md](references/api-configuration.md)。

## Docker Persistence / Docker 持久化

In Docker containers, map config directories to persistent storage:

在 Docker 容器中，将配置目录映射到持久化存储：

```bash
# Create persistent directories / 创建持久化目录
mkdir -p ~/workspace/claude-code/.claude
mkdir -p ~/workspace/.acpx
mkdir -p ~/workspace/.gradle  # For Android projects

# Create symlinks / 创建符号链接
ln -sf ~/workspace/claude-code/.claude ~/.claude
ln -sf ~/workspace/.acpx ~/.acpx
ln -sf ~/workspace/.gradle ~/.gradle
```

## Architecture Overview / 架构概览

```
┌─────────────────────────────────────────────────┐
│                   Web Browser                    │
│              http://HOST:6080                   │
└─────────────────────┬───────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────┐
│                    ttyd                          │
│            (Web Terminal Server)                │
└─────────────────────┬───────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────┐
│                   tmux                           │
│      (Session Persistence Layer)                │
│    - Survives browser close                     │
│    - Multiple windows/panes                     │
│    - Mouse scroll support                       │
└─────────────────────┬───────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────┐
│                Claude Code                       │
│          (AI Coding Assistant)                  │
│    - Multiple API providers                     │
│    - Project-level instructions (CLAUDE.md)     │
└─────────────────────────────────────────────────┘
```

## Scripts / 脚本

| Script | Description |
|--------|-------------|
| `scripts/start-ttyd.sh` | Start ttyd + tmux web terminal |
| `scripts/install-acpx.sh` | Install acpx multi-agent tool |

| 脚本 | 说明 |
|------|------|
| `scripts/start-ttyd.sh` | 启动 ttyd + tmux Web 终端 |
| `scripts/install-acpx.sh` | 安装 acpx 多代理工具 |

## Reference Documents / 参考文档

| Document | Content |
|----------|---------|
| [claude-code-installation.md](references/claude-code-installation.md) | Claude Code installation and configuration |
| [ttyd-tmux-setup.md](references/ttyd-tmux-setup.md) | Web terminal and session persistence |
| [acpx-setup.md](references/acpx-setup.md) | Multi-agent tool configuration |
| [api-configuration.md](references/api-configuration.md) | API provider settings |

| 文档 | 内容 |
|------|------|
| [claude-code-installation.md](references/claude-code-installation.md) | Claude Code 安装与配置 |
| [ttyd-tmux-setup.md](references/ttyd-tmux-setup.md) | Web 终端与会话持久化 |
| [acpx-setup.md](references/acpx-setup.md) | 多代理工具配置 |
| [api-configuration.md](references/api-configuration.md) | API 提供商设置 |

## tmux Quick Reference / tmux 快捷键

| Shortcut | Action |
|----------|--------|
| `Ctrl+B D` | Detach (keep session running) |
| `Ctrl+B C` | New window |
| `Ctrl+B N/P` | Next/Previous window |
| Mouse scroll | View history |

| 快捷键 | 功能 |
|--------|------|
| `Ctrl+B D` | 断开 (会话保持运行) |
| `Ctrl+B C` | 新建窗口 |
| `Ctrl+B N/P` | 下一个/上一个窗口 |
| 鼠标滚轮 | 查看历史 |
