---
name: claude-code-assist
version: 1.0.0
license: MIT
author: sallyface0
description: >
  One-click environment check and multi-provider setup for Claude Code. Detects Node.js/Git/npm, installs Claude Code CLI, configures provider (DeepSeek/Kimi/Qwen/SiliconFlow/OpenRouter etc.), auto-generates settings.json, verifies the setup. Win/Mac/Linux. 3-minute onboarding for Chinese developers using Claude Code with third-party APIs.
---

# Claude Code Assist — 一键环境检测与多 Provider 配置

> 国内开发者用 Claude Code 接第三方 API（DeepSeek/Kimi/Qwen…）的完整上车向导。3 分钟内从 0 到跑通。

## Overview

Claude Code 默认绑 Anthropic 计费。通过配置 `ANTHROPIC_BASE_URL` + `ANTHROPIC_AUTH_TOKEN` 可以路由到任何兼容 Anthropic 格式的第三方 API——但配置过程涉及环境变量、settings.json、模型名前缀后缀、平台差异、WSL2 前置条件等一堆坑。

本 skill 把整个过程拆成 5 个 Phase：**体检 → 安装 → 选 Provider → 写入配置 → 验证**。每一步都有明确的检测逻辑和错误处理。

| Phase | 名称 | 说明 |
|---|---|---|
| Phase 1 | 环境体检 | 检测 Node.js / npm / Git / Claude Code CLI 状态 |
| Phase 2 | 安装引导 | 缺什么装什么，按 Win / Mac / Linux 三路分发命令 |
| Phase 3 | Provider 选择 | 列出 10 个国内可用 Provider，用户选择后自动匹配配置 |
| Phase 4 | 配置写入 | 生成 settings.json 或指示用户写入环境变量 |
| Phase 5 | 验证 | 跑一条 claude 命令验证配置生效 |

## Trigger Conditions

- User says "配置 Claude Code"、"Claude Code 怎么用"、"Claude Code 接 DeepSeek"、"claude code setup"、"setup claude"、"configure claude code"
- User mentions "Claude Code API"、"第三方的 Claude Code"、"Claude Code 国内"
- User asks about ANTHROPIC_BASE_URL or ANTHROPIC_AUTH_TOKEN
- User explicitly invokes this skill

## System Architecture

```
用户请求 → Phase 1 环境体检 → 报告
    ↓
  缺组件? → Phase 2 安装引导（按平台给出命令）→ 用户确认
    ↓
  完毕 → Phase 3 Provider 选择（查表匹配 base URL + 认证方式 + 模型列表）
    ↓
  Phase 4 配置写入（settings.json 或 env var）
    ↓
  Phase 5 验证（claude --version + /status 检查）
    ↓
  成功 → 总结 + 提示常用命令
```

---

## Phase 1: 环境体检

### 检测项目

Creator 依次检查以下组件（使用 `exec` 命令）：

| 检查项 | 命令 | 成功标准 |
|---|---|---|
| Node.js | `node --version` | ≥ 18.x |
| npm | `npm --version` | ≥ 9.x |
| Git | `git --version` | 任意版本 |
| Claude Code CLI | `claude --version` | 已安装 |

**Windows 用户额外检查**：
- WSL2 或 Git for Windows 是否存在？（`wsl --status` 或 `git --version`）

### 输出体检报告

检查完后输出结构化报告：

```
📊 环境体检报告

✅ Node.js: v22.3.1
✅ npm: 10.5.0
✅ Git: 2.45.1
❌ Claude Code CLI: 未安装

⚠️ 需处理: 1 项（安装 Claude Code CLI）
📋 结论: 满足安装条件，需要安装 Claude Code CLI
```

**边界情况**：
- 如果 Node.js < 18 → 终止，提示升级
- 如果 Git 未安装 → Windows 提示安装 Git for Windows；Mac 提示 `xcode-select --install`
- 如果 Claude Code 已安装但版本过旧 → 提示 `npm update -g @anthropic-ai/claude-code`

---

## Phase 2: 安装引导

### 如果 Claude Code CLI 未安装

按平台给出安装命令：

| 平台 | 命令 |
|---|---|
| **所有平台** | `npm install -g @anthropic-ai/claude-code` |
| **Windows 额外** | 必须先安装 Git for Windows（https://git-scm.com/download/win），否则 npm 全局包可能出错 |

安装后执行 `claude --version` 验证。

### 如果 Node.js 未安装

| 平台 | 引导 |
|---|---|
| **Windows** | 下载 https://nodejs.org/ 的 LTS 版本 (.msi)，安装时勾选"Add to PATH" |
| **Mac** | `brew install node@20` 或下载 pkg |
| **Linux** | `sudo apt install nodejs npm` 或使用 nvm |

### 如果 Git 未安装

| 平台 | 引导 |
|---|---|
| **Windows** | https://git-scm.com/download/win |
| **Mac** | `xcode-select --install` |
| **Linux** | `sudo apt install git` |

> **执行原则**：Creator 只给出安装命令，不出手替用户执行（安装涉及系统权限、网络代理、个人偏好）。用户确认安装完成后，重新回到 Phase 1 验证。

---

## Phase 3: Provider 选择

### Provider 选择流程

Creator 向用户展示 Provider 列表，询问 2 个问题：

1. **想用哪个 API Provider？**（列出 10 个选项）
2. **API Key 已有？** 还是需要指引去获取？

```
🔧 选择你的 API Provider：

1. DeepSeek (最推荐 — 1M 上下文，v4-pro 推理，国内性价比最高)
2. Kimi (月之暗面 — 1M 上下文，kimi-k2 模型)
3. Qwen (阿里通义千问 — qwen3-coder)
4. SiliconFlow (硅基流动 — 多模型聚合，免费用)
5. OpenRouter (国际 — 多模型聚合，需海外卡)
6. 魔搭 ModelScope (国内 — 阿里生态)
7. 百川 Baichuan
8. 智谱 GLM
9. 字节豆包
10. 自定义（自己输入 base URL 和认证方式）
```

### Provider 信息表

详细配置见 [references/provider-table.md](references/provider-table.md)。

用户选择后，Creator 自动匹配：
- `ANTHROPIC_BASE_URL`
- 认证方式（`ANTHROPIC_AUTH_TOKEN` 或 `ANTHROPIC_API_KEY`）
- 推荐模型列表（含上下文后缀 `[1m]` 等）
- API Key 获取地址

---

## Phase 4: 配置写入

### 配置方式选择

Creator 询问用户：

```
配置写入有两种方式：

A. 环境变量（推荐 — 临时切换简单，不污染项目仓库）
B. settings.local.json（持久化 — 保存在项目 .claude/ 下，不丢 Git）

选哪个？
```

### 方式 A: 环境变量

根据用户选的操作系统和 Provider，输出对应的 export/set 命令：

**Mac / Linux (Bash/Zsh)**:
```bash
export ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic"
export ANTHROPIC_AUTH_TOKEN="你的API-Key"
export ANTHROPIC_MODEL="deepseek-v4-pro[1m]"
export ANTHROPIC_DEFAULT_OPUS_MODEL="deepseek-v4-pro[1m]"
export ANTHROPIC_DEFAULT_SONNET_MODEL="deepseek-v4-pro[1m]"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="deepseek-v4-flash"
export CLAUDE_CODE_SUBAGENT_MODEL="deepseek-v4-flash"
export CLAUDE_CODE_EFFORT_LEVEL="max"
```

**Windows (PowerShell)**:
```powershell
$env:ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic"
$env:ANTHROPIC_AUTH_TOKEN="你的API-Key"
$env:ANTHROPIC_MODEL="deepseek-v4-pro[1m]"
$env:ANTHROPIC_DEFAULT_OPUS_MODEL="deepseek-v4-pro[1m]"
$env:ANTHROPIC_DEFAULT_SONNET_MODEL="deepseek-v4-pro[1m]"
$env:ANTHROPIC_DEFAULT_HAIKU_MODEL="deepseek-v4-flash"
$env:CLAUDE_CODE_SUBAGENT_MODEL="deepseek-v4-flash"
$env:CLAUDE_CODE_EFFORT_LEVEL="max"
```

**Windows (CMD)**:
```cmd
set ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
set ANTHROPIC_AUTH_TOKEN=你的API-Key
set ANTHROPIC_MODEL=deepseek-v4-pro[1m]
set ANTHROPIC_DEFAULT_OPUS_MODEL=deepseek-v4-pro[1m]
set ANTHROPIC_DEFAULT_SONNET_MODEL=deepseek-v4-pro[1m]
set ANTHROPIC_DEFAULT_HAIKU_MODEL=deepseek-v4-flash
set CLAUDE_CODE_SUBAGENT_MODEL=deepseek-v4-flash
set CLAUDE_CODE_EFFORT_LEVEL=max
```

### 方式 B: settings.local.json

在当前项目目录下创建 `.claude/settings.local.json`：

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://api.deepseek.com/anthropic",
    "ANTHROPIC_AUTH_TOKEN": "你的API-Key",
    "ANTHROPIC_MODEL": "deepseek-v4-pro[1m]",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "deepseek-v4-pro[1m]",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "deepseek-v4-pro[1m]",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "deepseek-v4-flash",
    "CLAUDE_CODE_SUBAGENT_MODEL": "deepseek-v4-flash",
    "CLAUDE_CODE_EFFORT_LEVEL": "max"
  }
}
```

> **重要提醒**：`settings.local.json` 不进入 Git。如果用了 settings.json，务必确认 `.gitignore` 已加 `!.claude/settings.local.json` 或整个 `.claude/` 目录都不提交。

### 🚨 关键配置坑点（Creator 必须提醒用户）

1. **DeepSeek 用 `ANTHROPIC_AUTH_TOKEN` 不是 `ANTHROPIC_API_KEY`** — 这两个是不同的认证头，混用会报 401。
2. **上下文后缀 `[1m]`** — DeepSeek 和 Kimi 的模型名后面必须加 `[1m]` 才能解锁 1M 上下文（如 `deepseek-v4-pro[1m]`）。
3. **如果是纯 API Key 方式**（非 Token），用 `ANTHROPIC_API_KEY` 而非 `ANTHROPIC_AUTH_TOKEN`。对应关系：DeepSeek/Kimi → `ANTHROPIC_AUTH_TOKEN`；OpenRouter → `ANTHROPIC_API_KEY`。
4. **Windows WSL2 用户** — 如果在 WSL2 内运行 Claude Code，settings.json 应放在 WSL2 的 `~/.claude/` 而非 Windows 的 `C:\Users\` 路径。
5. **已有 Anthropic 登录的用户** — 如果之前登录过 Anthropic 账号，设置 `ANTHROPIC_BASE_URL` 后可能仍走 Anthropic API。解决：`ANTHROPIC_BASE_URL` 设为非 Anthropic 地址后会自动切换认证方式。

---

## Phase 5: 验证

### 验证步骤

配置写入后，Creator 指示用户执行验证：

```
🔍 验证配置是否生效，请在你的项目目录下运行：

  claude --version

成功后再运行：

  claude

进入 Claude Code 交互界面后，输入：

  /status

确认显示的模型是你选的 Provider 下的模型。
```

### 验证失败处理

如果验证失败，见 [references/troubleshooting.md](references/troubleshooting.md)。

Creator 按错误类型导向对应排坑方案：

| 症状 | 最可能原因 | 跳转 |
|---|---|---|
| `command not found: claude` | Claude Code CLI 未安装或 PATH 不对 | 排坑 §1 |
| `401 Unauthorized` | Token/Key 错误或用了错的认证变量 | 排坑 §2 |
| `403 Forbidden` | API Key 无效或余额不足 | 排坑 §3 |
| 上下文被截断/只显示 64K | `[1m]` 后缀没加 | 排坑 §4 |
| 模型列表不显示 DeepSeek 模型 | base URL 指向了 Anthropic 而非第三方 | 排坑 §5 |
| WSL2 中配置不生效 | settings.json 路径错误 | 排坑 §6 |

---

## Provider 信息表

See [references/provider-table.md](references/provider-table.md) for the full 10-provider configuration matrix.

## 排坑指南

See [references/troubleshooting.md](references/troubleshooting.md) for common issues and solutions.

## 安装指南

See [references/install-guide.md](references/install-guide.md) for per-platform Claude Code installation details.

---

## File References

- **[provider-table.md](references/provider-table.md)** — 10 个 Provider 的完整配置信息（base URL、认证方式、模型列表、上下文后缀、API Key 获取地址）
- **[troubleshooting.md](references/troubleshooting.md)** — 6 大类常见问题与解决方案
- **[install-guide.md](references/install-guide.md)** — Win/Mac/Linux 三平台 Claude Code 安装详情

## File Management

本 skill 不产生本地文件。所有操作在对话中完成。
