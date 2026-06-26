# FastClaw Deployer 使用指南

> 30分钟部署轻量级 AI Agent 运行时

---

## 目录

1. [功能特点](#功能特点)
2. [系统要求](#系统要求)
3. [Windows 安装](#windows-安装)
4. [macOS/Linux 安装](#macoslinux-安装)
5. [初始化配置](#初始化配置)
6. [多 Agent 配置](#多-agent-配置)
7. [故障排除](#故障排除)
8. [卸载](#卸载)

---

## 功能特点

- **单二进制** — 无需 Node.js、Python 或 Docker
- **SOUL.md 兼容** — 与 OpenClaw 生态完全兼容
- **极低内存** — <10MB 内存占用
- **内置 Web UI** — http://localhost:18953
- **多模型支持** — OpenRouter / Ollama / OpenAI / Anthropic / 自定义
- **多 Agent** — 同时运行多个独立 Agent
- **本地存储** — JSONL 文件存储，无需数据库

---

## 系统要求

| 组件 | 要求 |
|------|------|
| 操作系统 | Windows 10+, macOS 10.14+, Ubuntu 18.04+ |
| 内存 | 最低 512MB，可用 2GB+ 推荐 |
| 磁盘 | 100MB 可用空间 |
| 网络 | 互联网连接（用于 LLM API 调用）|

---

## Windows 安装

### 方式一：PowerShell 一键安装（推荐）

以管理员身份打开 PowerShell，运行：

```powershell
irm https://raw.githubusercontent.com/fastclaw-ai/fastclaw/main/install.ps1 | iex
```

### 方式二：手动安装

**第一步：下载**

访问 https://github.com/fastclaw-ai/fastclaw/releases/latest
下载 `fastclaw_windows_amd64.zip`

**第二步：解压**

解压到目录，例如：`D:\AI\FastClaw\`

**第三步：运行**

双击 `fastclaw.exe`

或命令行运行：
```powershell
cd D:\AI\FastClaw
.\fastclaw.exe
```

**第四步：打开 Web 界面**

浏览器访问：http://localhost:18953

---

## macOS/Linux 安装

### 方式一：终端一键安装

```bash
curl -fsSL https://raw.githubusercontent.com/fastclaw-ai/fastclaw/main/install.sh | bash
```

### 方式二：手动安装

**第一步：下载**

```bash
# macOS (Apple Silicon)
curl -LO https://github.com/fastclaw-ai/fastclaw/releases/latest/fastclaw_darwin_arm64.tar.gz

# Linux
curl -LO https://github.com/fastclaw-ai/fastclaw/releases/latest/fastclaw_linux_amd64.tar.gz
```

**第二步：解压**

```bash
# macOS
tar -xzf fastclaw_darwin_arm64.tar.gz
sudo mv fastclaw /usr/local/bin/

# Linux
tar -xzf fastclaw_linux_amd64.tar.gz
sudo mv fastclaw /usr/local/bin/
```

**第三步：运行**

```bash
fastclaw
```

---

## 初始化配置

### 首次启动向导

1. 启动后，浏览器打开 http://localhost:18953
2. 点击 **Get Started**
3. **LLM Provider**：选择 `openrouter`（推荐）
4. **API Key**：填入你的 OpenRouter API Key
   - 注册地址：https://openrouter.ai
   - 注册后：https://openrouter.ai/keys
5. **API Base URL**：保持默认 `https://openrouter.ai/api/v1`
6. **Model**：推荐选择 `google/gemini-3.1-flash-lite-preview`（有免费额度）
7. 点击 **Test Connection** 确认连接成功
8. 点击 **Next** → 完成

### 配置文件位置

配置文件在用户目录：

```
Windows:  %USERPROFILE%\.fastclaw\
macOS:    ~/.fastclaw/
Linux:    ~/.fastclaw/
```

目录结构：
```
.fastclaw/
├── fastclaw.json       # 全局配置
├── apikeys.json        # API 密钥
├── agents/             # Agent 配置
│   └── default/        # 默认 Agent
│       └── agent/
│           ├── SOUL.md
│           ├── IDENTITY.md
│           └── MEMORY.md
└── skills/            # 安装的技能包
```

---

## 多 Agent 配置

FastClaw 支持同时运行多个 Agent：

### 通过 Web 界面

1. 打开 http://localhost:18953
2. 进入 **Agents** 页面
3. 点击 **New Agent**
4. 填写 Agent 名称和描述
5. 为 Agent 创建独立的 SOUL.md

### 通过配置文件

在 `~/.fastclaw/agents/` 目录下创建新 Agent：

```
~/.fastclaw/agents/
├── default/           ← 默认 Agent（已创建）
├── coder/             ← 新建：编程 Agent
│   └── agent/
│       ├── SOUL.md
│       └── agent.json
└── writer/            ← 新建：写作 Agent
    └── agent/
        ├── SOUL.md
        └── agent.json
```

---

## 与 OpenClaw 联动

FastClaw 与 OpenClaw 是互补关系：

| 场景 | 推荐工具 |
|------|---------|
| 消息渠道自动化（飞书/微信） | OpenClaw |
| 轻量图形化 AI 应用 | FastClaw |
| SOUL.md 生态扩展 | 两者均支持 |
| 24/7 长期运行 Agent | OpenClaw |
| 快速原型测试 | FastClaw |

---

## 故障排除

### 端口被占用

如果 18953 端口被其他程序占用：

1. 修改 `~/.fastclaw/fastclaw.json`
2. 添加或修改 `"port": 18954`
3. 重启 FastClaw

### API 连接失败

1. 确认 API Key 正确且有余额
2. 确认网络可访问 OpenRouter
3. 尝试更换模型（如从 GPT-5.4 换成 Gemini）

### 内存占用高

1. 关闭其他 FastClaw 窗口
2. 减少 concurrent sessions 数量
3. 使用 `file` 存储而非 `postgres`

### 数据目录

所有数据存储在 `~/.fastclaw/`，如需完全清除：

```bash
# 停止 FastClaw 后执行
rm -rf ~/.fastclaw
```

---

## 卸载

### Windows

1. 停止 FastClaw（关闭程序或结束进程）
2. 删除安装目录（如 `D:\AI\FastClaw\`）
3. （可选）删除用户数据目录：`%USERPROFILE%\.fastclaw\`

### macOS/Linux

```bash
# 停止
pkill fastclaw

# 删除程序
sudo rm /usr/local/bin/fastclaw

# （可选）删除用户数据
rm -rf ~/.fastclaw
```

---

## 更新

FastClaw 会自动检查更新。手动更新：

```bash
# macOS/Linux
curl -fsSL https://raw.githubusercontent.com/fastclaw-ai/fastclaw/main/install.sh | bash

# Windows - 重新下载最新版本即可
```

---

*本指南由 FastClaw Deployer 技能包提供 | 2026-04-21*
