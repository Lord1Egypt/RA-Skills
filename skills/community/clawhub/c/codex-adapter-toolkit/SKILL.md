---
name: codex-adapter-toolkit
description: >
  Codex Adapter Toolkit - Multi-provider API adapter for Codex.
  Use when: user wants to switch Codex API provider, set up local adapter
  for DeepSeek/MiniMax/OpenAI/Gemini, configure failover, or manage multiple providers.
allowed-tools: read_file, write_to_file, execute_command, list_dir, glob
---

## 功能概述

Codex Adapter Toolkit 提供统一的本地 API 适配器，支持多种大模型 Provider：

| Provider | 类型 | 认证方式 |
|----------|------|----------|
| DeepSeek | deepseek | Bearer Token |
| MiniMax | minimax | API Key |
| OpenAI | openai | Bearer Token |
| Google Gemini | gemini | API Key |
| xAI Grok | grok | Bearer Token |
| Ollama (本地) | ollama | 无 |
| Claude Direct | claude_direct | Bearer Token |
| OpenRouter | openrouter | Bearer Token |

## 工作原理

```
Codex (Responses API) → http://127.0.0.1:<port>/v1/responses
         ↓ 本地适配器（协议转换）
第三方 API (Chat Completions API)
```

- 适配器是轻量 Python HTTP 服务，监听 `127.0.0.1:<port>`
- 将 Codex 的 `Responses API` 转换为各厂商的 `Chat Completions API`
- 内置熔断器模式（Circuit Breaker）
- 支持故障自动切换（Failover）

## 默认端口

| Provider | 端口 |
|----------|------|
| DeepSeek | 18669 |
| MiniMax | 18667 |
| 讯飞 | 18666 |
| 自定义 | 可配置 |

## 安装脚本

### 一键安装
```powershell
.\scripts\setup.ps1
```

### 安装指定 Provider
```powershell
.\scripts\install-adapter.ps1 -Provider deepseek -ApiKey "your-api-key"
```

### 切换 Provider
```powershell
.\scripts\switch-provider.ps1 -Provider openai
```

### 查看帮助
```powershell
.\scripts\diagnose.ps1
```

## 启动适配器

### 方式一：使用统一适配器框架
```bash
python adapters/universal_adapter.py <端口> <provider类型> [api_key] [failover备选...]
```

示例：
```bash
# DeepSeek 主节点
python adapters/universal_adapter.py 18669 deepseek "sk-xxxx"

# 带故障切换（DeepSeek 主，OpenAI/Gemini 备选）
python adapters/universal_adapter.py 18669 deepseek "sk-xxxx" openai gemini

# 本地 Ollama
python adapters/universal_adapter.py 18669 ollama
```

### 方式二：使用独立适配器
```powershell
# 启动 DeepSeek 适配器
python deepseek_codex_adapter.py

# 启动 MiniMax 适配器
python minimax_codex_adapter.py
```

## 运维脚本

| 脚本 | 功能 |
|------|------|
| `setup.ps1` | 一键安装所有组件 |
| `install-adapter.ps1` | 安装适配器 |
| `switch-provider.ps1` | 切换 Provider |
| `monitor-adapter.ps1` | 进程监控（自动重启）|
| `failover.ps1` | 故障切换测试 |
| `diagnose.ps1` | 智能诊断 |
| `notify.ps1` | 通知系统配置 |
| `backup.ps1` | 备份与恢复 |
| `apikey.ps1` | API Key 管理 |
| `usage-stats.ps1` | 使用统计 |
| `logs.ps1` | 日志查看 |
| `dashboard-server.ps1` | Web 监控面板 |
| `register-startup.ps1` | 注册开机启动 |

## 配置目录

适配器配置文件位于用户目录下：
- Windows: `%USERPROFILE%\.cc-switch\`
- 配置: `settings.json`

## 熔断器模式

当 Provider 失败达到阈值时自动熔断：
- **失败阈值**: 3 次
- **恢复超时**: 60 秒
- **半开尝试**: 2 次成功恢复

熔断状态可通过健康检查端点查看：
```bash
curl http://127.0.0.1:18669/health
```

## 故障切换

配置 failover providers：
```bash
python universal_adapter.py 18669 deepseek "key" openai gemini
```

主节点故障时自动切换到备选节点。

## Web 监控面板

启动 Dashboard 服务器：
```powershell
.\scripts\dashboard-server.ps1
```

然后访问 `http://localhost:18670` 查看实时状态。

## 通知系统

配置通知渠道：
```powershell
# 钉钉
.\notify.ps1 -Config -Channel dingtalk -ConfigAction set -ConfigValue "https://oapi.dingtalk.com/..."

# 邮件
.\notify.ps1 -Config -Channel email -ConfigAction set -ConfigValue "smtp:port:user:pass:from:to"
```

发送测试通知：
```powershell
.\notify.ps1 -Test -Channel dingtalk
```

## 备份恢复

```powershell
# 备份
.\backup.ps1

# 列出备份
.\backup.ps1 -Action list

# 恢复
.\backup.ps1 -Action restore latest
```

## 验证安装

```powershell
# 1. 检查进程
Get-Process python | Where-Object { $_.CommandLine -like "*adapter*" }

# 2. 健康检查
curl http://127.0.0.1:18669/health

# 3. 诊断
.\diagnose.ps1
```

## 版本

v1.0.0