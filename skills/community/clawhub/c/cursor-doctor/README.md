# 🩺 Cursor Doctor — Cursor IDE Error Diagnostic & Repair Tool

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/minirr890112-byte/cursor-doctor?style=flat-square)](https://github.com/minirr890112-byte/cursor-doctor)

> **Cursor IDE 故障诊断与修复工具** — 一键诊断 Cursor 报错、崩溃、配置问题，并提供智能修复方案。  
> **Cursor IDE Error Diagnostic & Repair Tool** — One-command diagnosis and intelligent fix for Cursor errors, crashes, and configuration issues.

---

## 📦 Installation / 安装

> ⚠️ **cursor-doctor is NOT published on PyPI yet.** Use one of the methods below.

### Method 1: Install directly from GitHub (recommended)

```bash
pip install git+https://github.com/minirr890112-byte/cursor-doctor.git
```

### Method 2: Clone and install in editable mode

```bash
git clone https://github.com/minirr890112-byte/cursor-doctor.git
cd cursor-doctor
pip install -e .
```

### Prerequisites / 依赖

- Python 3.10+
- `pip` 21.0+

---

## 🚀 Quick Start / 快速开始

```bash
# Diagnose your Cursor environment / 诊断 Cursor 环境
cursor-doctor diagnose

# Auto-fix detected issues / 自动修复
cursor-doctor fix

# Browse built-in error signature database / 浏览错误签名库
cursor-doctor signatures

# Match an error message against known patterns / 匹配错误文本
cursor-doctor match --text "MCP Client Closed"
```

---

## ✨ Features / 功能

| Command | Description / 说明 |
|---------|---------------------|
| `cursor-doctor diagnose` | Full health scan of Cursor installation — detects version, system environment, log errors, and computes a health score. / 全面诊断 Cursor 健康状态。 |
| `cursor-doctor fix [category]` | Auto-fix common problems. Run without arguments for guided repair, or specify a category: `mcp_connection`, `crash`, `network_proxy`, `config_env`. / 自动修复常见问题。 |
| `cursor-doctor signatures` | Browse the 16 built-in error signatures across 6 categories. / 浏览 16 种内建错误签名。 |
| `cursor-doctor match --text "..."` | Match a raw error message against the signature database and get diagnosis + fix hints. / 将错误文本匹配到已知签名。 |

### Key Capabilities / 核心能力

- 🔌 **MCP client closed fix** — kill stale processes, clear MCP cache
- 💥 **Extension crash recovery** — detect corrupted extensions, clear cache safely
- 🌐 **Proxy conflict resolution** — detect and diagnose proxy/VPN conflicts
- 🔍 **Auto-detection** of Cursor installation path and config directory
- 📊 **16 error signatures** extracted from 77+ real-world community error reports

---

## 📖 Example Demos / 示例演示

### Demo 1: `cursor-doctor diagnose`

```
$ cursor-doctor diagnose

╭──────────────────────────────╮
│  🔍 Cursor Doctor 诊断报告   │
╰──────────────────────────────╯

Cursor 版本: Cursor 0.45.0 (Electron 29)
诊断分数: 45% - 需关注 ⚠️

系统环境:
 python      3.11.7
 node        v20.11.0
 npm         10.2.4
 git         git version 2.43.0
 shell       /bin/zsh
 disk_total  460.3 GB
 disk_free   82.1 GB

发现 3 条错误:

┌──────────┬──────────┬──────────────────────┬───────────────────┐
│ 严重度   │ 签名     │ 错误名               │ 来源              │
├──────────┼──────────┼──────────────────────┼───────────────────┤
│ CRITICAL │ MCP-001  │ MCP Client Closed    │ cursor-server.log │
│ HIGH     │ NET-001  │ 代理冲突导致连接失败  │ renderer.log      │
│ MEDIUM   │ SYNC-001 │ Cursor 同步冲突/失败  │ sync.log          │
└──────────┴──────────┴──────────────────────┴───────────────────┘

推荐修复:
  ■ MCP 连接修复: 重启Cursor / 检查端口 8090-8099 / 关闭VPN / 重置MCP配置
     使用: cursor-doctor fix mcp_connection
  ■ 网络/代理修复: 关闭系统代理 / 在 Cursor 设置中配置代理 / 使用系统代理模式
     使用: cursor-doctor fix network_proxy
```

### Demo 2: `cursor-doctor fix`

```
$ cursor-doctor fix

发现 3 类可修复问题:

  1. ■ MCP 连接修复: 重启Cursor / 检查端口 8090-8099 / 关闭VPN / 重置MCP配置
  2. ■ 网络/代理修复: 关闭系统代理 / 在 Cursor 设置中配置代理 / 使用系统代理模式
  3. ■ Cursor 同步冲突: 手动选择同步版本 / 关闭自动同步 / 清除云端同步数据

使用 'cursor-doctor fix <category>' 应用特定修复
或 'cursor-doctor fix mcp_connection' 修复 MCP 连接问题

$ cursor-doctor fix mcp_connection

╭──────────────────────────────╮
│ 正在执行: 🔌 MCP 连接修复    │
╰──────────────────────────────╯
✅ 已终止 Cursor 进程
✅ 已清除 MCP 缓存
💡 重启 Cursor 后重试 MCP 连接

╭──────────────────────────────╮
│ 完成: 🔌 MCP 连接修复        │
╰──────────────────────────────╯
```

### Demo 3: `cursor-doctor match`

```
$ cursor-doctor match --text "MCP Client Closed unexpectedly: connection refused on port 8095"

✅ 找到 1 个匹配:

╭─ 匹配模式: MCP\s*(Client|Server).*closed ──────────────────────╮
│ MCP Client Closed (MCP-001)                                     │
│ 严重度: CRITICAL                                                │
│ 分类: MCP/Agent 连接                                            │
│                                                                 │
│ 诊断: MCP (Model Context Protocol) 客户端与服务端连接断开。      │
│       常见原因：端口被占用、防火墙拦截、代理冲突。               │
│ 修复: 重启Cursor / 检查端口 8090-8099 / 关闭VPN / 重置MCP配置   │
╰─────────────────────────────────────────────────────────────────╯
```

---

## 📊 Error Signature Database / 错误签名数据库

Built from 77+ real-world Cursor error reports from the Chinese developer community. 16 signatures across 6 categories.  
基于中文开发者社区 77+ 条 Cursor 报错/崩溃信号分析提取，覆盖 6 大类 16 种错误签名。

| Category / 分类 | Count | Severity Range | Description |
|-----------------|-------|----------------|-------------|
| 🔌 MCP/Agent Connection / MCP/Agent 连接 | 3 | CRITICAL–HIGH | MCP Client Closed, Shell Parse Failure, Token Expired |
| 💥 Crash/Freeze / 崩溃/闪退 | 3 | CRITICAL–HIGH | Startup white-screen, Extension crash, OOM |
| 🤖 AI/Agent Malfunction / AI/Agent 功能异常 | 3 | HIGH–MEDIUM | AI timeout, Degraded completions, Agent infinite loop |
| 🌐 Network/Proxy / 网络/代理 | 2 | CRITICAL–HIGH | Proxy conflict, GFW/network unreachable |
| ⚙️ Config/Environment / 配置/环境 | 3 | HIGH–MEDIUM | Config corruption, Python not found, Node.js abnormal |
| 📁 File/Sync / 文件/同步 | 2 | MEDIUM–LOW | Sync conflict, File Watcher limit |

### Full Signature List / 完整签名列表

| ID | Name / 名称 | Category / 分类 | Severity / 严重度 | Community Frequency / 社区频率 |
|----|-------------|-----------------|-------------------|-------------------------------|
| MCP-001 | MCP Client Closed | MCP/Agent Connection | CRITICAL | 15 |
| MCP-002 | Shell Parse Failure | MCP/Agent Connection | CRITICAL | 12 |
| MCP-003 | Unauthorized / Token Expired | MCP/Agent Connection | HIGH | 10 |
| CRASH-001 | Startup Crash / White Screen | Crash/Freeze | CRITICAL | 8 |
| CRASH-002 | Plugin/Extension Crash | Crash/Freeze | HIGH | 6 |
| CRASH-003 | Out of Memory (OOM) | Crash/Freeze | HIGH | 5 |
| AI-001 | AI Request Failed / Timeout | AI/Agent Malfunction | HIGH | 12 |
| AI-002 | Completion Accuracy Degraded | AI/Agent Malfunction | MEDIUM | 8 |
| AI-003 | Agent Loop / Non-terminating | AI/Agent Malfunction | MEDIUM | 5 |
| NET-001 | Proxy Conflict | Network/Proxy | HIGH | 8 |
| NET-002 | GFW / Network Unreachable | Network/Proxy | CRITICAL | 5 |
| CFG-001 | Config Corruption | Config/Environment | HIGH | 7 |
| CFG-002 | Python Interpreter Not Found | Config/Environment | MEDIUM | 6 |
| CFG-003 | Node.js / npm Environment Error | Config/Environment | MEDIUM | 5 |
| SYNC-001 | Sync Conflict / Failure | File/Sync | MEDIUM | 4 |
| SYNC-002 | File Watcher Limit | File/Sync | LOW | 3 |

---

## 🧰 Available Fixes / 可用修复

| Fix Category | Command | What It Does |
|--------------|---------|--------------|
| 🔌 MCP Connection | `cursor-doctor fix mcp_connection` | Kill stale Cursor processes, clear MCP cache |
| 💥 Crash Recovery | `cursor-doctor fix crash` | Clear Cursor cache directories, restart Cursor |
| 🌐 Network/Proxy | `cursor-doctor fix network_proxy` | Detect proxy conflicts, suggest configuration |
| ⚙️ Config Reset | `cursor-doctor fix config_env` | Backup and reset settings.json to defaults |

---

## 🏗️ Project Structure / 项目结构

```
cursor-doctor/
├── cursor_doctor/
│   ├── __init__.py          # Package init, version
│   ├── cli.py               # CLI entry (click + rich)
│   ├── diagnose.py          # Core diagnostic engine
│   ├── signatures/
│   │   └── database.py      # 16 error signatures, matching logic
│   └── fixes/
│       └── apply.py         # Auto-fix implementations
├── pyproject.toml
└── README.md
```

---

## 🔗 Also Available on ClawHub

> 🚀 **cursor-doctor** will soon be available as a skill on **[ClawHub](https://clawhub.ai)** — the AI skills marketplace.  
> *Skill page coming soon — check back for updates!*

---

## 🌐 Related Projects / 相关项目

| 项目 | 说明 |
|------|------|
| [🧠 claude-intel-monitor](https://github.com/minirr890112-byte/claude-intel-monitor) | 检测 Claude/GPT/DeepSeek 是否降智 / Detect AI model degradation |
| [🔍 HermesMade](https://github.com/minirr890112-byte/HermesMade) | 自动化开发者痛点扫描平台 / Pain point intelligence platform |

---

## 📄 License / 许可证

MIT © [minirr890112-byte](https://github.com/minirr890112-byte)

---

## 🙏 Acknowledgments / 致谢

Error signatures extracted and categorized from 77+ community error reports in the Chinese Cursor/VS Code developer community.  
错误签名提取自中文 Cursor/VS Code 开发者社区的 77+ 条真实报错信号。

---

⭐ **觉得有用？[点颗星 Star](https://github.com/minirr890112-byte/cursor-doctor) — 让更多 Cursor 用户发现这个工具！**  
⭐ **Found this useful? [Star this repo](https://github.com/minirr890112-byte/cursor-doctor) — help more Cursor users save debugging hours!**
