---
name: agent-cli
version: 2.1.0
description: Cursor CLI（agent）与 Qoder CLI（qodercli）安装与索引；核心用法见 cursorcli.md、qodercli.md。
author: optimized
---

# Agent CLI（Cursor + Qoder）

本目录统一管理两套命令行 Agent 的**安装与索引**：**Cursor** 核心操作见 `cursorcli.md`，**Qoder** 核心操作见 `qodercli.md`。

---

## Cursor CLI 安装

### 安装方式

#### 通用（macOS / Linux / WSL）

```bash
curl https://cursor.com/install -fsS | bash
```

#### macOS（Homebrew）

```bash
brew install --cask cursor-cli
```

### 初始化

#### 添加 PATH（macOS）

```bash
export PATH="$HOME/.local/bin:$PATH"
```

写入：

* zsh → `~/.zshrc`
* bash → `~/.bashrc`

```bash
source ~/.zshrc
```

### 验证安装

```bash
agent --version
```

### 环境要求

* macOS ≥ 10.15
* 支持 Intel / Apple Silicon

### 命令说明

* 主命令：`agent`
* 兼容命令：`cursor-agent`

### 登录

#### 浏览器登录

```bash
agent login
```

#### API Key

```bash
export CURSOR_API_KEY=your_api_key_here
```

### 更新

```bash
agent update
# 或
agent upgrade
```

---

## Qoder CLI 安装与索引

### 文档索引

完整文档目录（供发现所有页面）：

<https://docs.qoder.com/llms.txt>

### 安装

按官方当前方式安装（包管理器或安装脚本以官网为准），完成后验证：

```bash
qodercli --version
```

### 登录

在 TUI 内执行 `/login`，或按官方说明完成账号与 API 配置。

### 工作区

在项目根目录运行 `qodercli`；或指定目录：

```bash
qodercli -w /path/to/project
```
