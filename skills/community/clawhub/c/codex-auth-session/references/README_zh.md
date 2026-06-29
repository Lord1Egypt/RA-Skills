<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/zcz-user/codex-auth-session-refresh/main/assets/header-dark.svg">
    <img src="https://raw.githubusercontent.com/zcz-user/codex-auth-session-refresh/main/assets/header-light.svg" width="100%" alt="Codex Auth Session Refresh">
  </picture>
</p>

<p align="center">
  <b>中文</b>
  &nbsp;·&nbsp;
  <a href="./README.md">English</a>
  &nbsp;·&nbsp;
  <a href="https://github.com/zcz-user/codex-auth-session-refresh/issues">报告问题</a>
</p>

<p align="center">
  <img src="https://img.shields.io/github/stars/zcz-user/codex-auth-session-refresh?style=flat-square&logo=github" alt="Stars">
  <img src="https://img.shields.io/badge/Windows-0078D6?style=flat-square&logo=windows&logoColor=white" alt="Windows">
  <img src="https://img.shields.io/badge/Node.js-18+-339933?style=flat-square&logo=node.js" alt="Node.js">
  <img src="https://img.shields.io/badge/Playwright-45ba4b?style=flat-square&logo=playwright" alt="Playwright">
  <img src="https://img.shields.io/github/license/zcz-user/codex-auth-session-refresh?style=flat-square" alt="MIT">
  <img src="https://img.shields.io/github/last-commit/zcz-user/codex-auth-session-refresh?style=flat-square&logo=git" alt="最近更新">
</p>

---

## 💡 为什么需要这个工具

Codex CLI 需要在 `~/.codex/auth.json` 里有一个有效的 `access_token`。但标准 OAuth 登录在很多场景下走不通：

| 🚫 场景 | ⚡ 影响 |
|---------|--------|
| **公司代理/防火墙** | OAuth 重定向被拦截 |
| **WSL / Docker 容器** | 没有浏览器可用 |
| **远程桌面 / SSH** | 认证弹窗失败 |
| **Token 过期快** | 几小时就得重来一次 |

**这个工具解决了这个 gap** — 从你已有的 ChatGPT 浏览器会话中读取 token，直接写入 Codex 的 `auth.json`。

> 无需逆向。无需抓包。无需滥用 API。

---

## ✨ 特性一览

| | |
|---|---|
| 🔌 **一行安装** | `npm install && .\login-profile.ps1` — 搞定 |
| 🤖 **自动刷新** | Windows 定时任务，间隔可配 |
| 🛡️ **安全设计** | Token 永不记日志，每次更新前自动备份 |
| 🪟 **桌面快捷** | `create-desktop-toolbox.ps1` — 一键直达 |
| 🔍 **健康面板** | `status.ps1` — 任务 + token 状态一目了然 |
| 🔧 **完全可配** | 6 个环境变量，自定义路径 |

---

## 🚀 快速开始

```powershell
git clone https://github.com/zcz-user/codex-auth-session-refresh.git
cd codex-auth-session-refresh
npm install
.\login-profile.ps1     # → 弹窗 → 登录 ChatGPT → 回车
.\status.ps1            # → 验证 token 状态
```

<details>
<summary><b>📸 输出示例（点击展开）</b></summary>

```
=== Codex Auth Refresh Status ===

[TASK] Name: CodexAuthSessionRefresh
[TASK] State: Ready
[TASK] LastRunTime: 2026/6/10 19:55:00
[TASK] LastTaskResult: 0 (0 表示成功)

[AUTH] Path: C:\Users\你\.codex\auth.json
[AUTH] auth_mode: chatgpt
[AUTH] last_refresh: 2026-06-10T11:55:00.000Z
[AUTH] access_token length: 1024
[AUTH] account_id present: True

[LOG] Last entries:
{"time":"2026-06-10T11:55:00.000Z","status":"success"}
```

</details>

---

## 📋 命令速查

| 命令 | 说明 |
|------|------|
| `login-profile.ps1` | 首次登录 / 重登（弹浏览器） |
| `run-refresh.ps1` | 立即刷新（浏览器自动关） |
| `status.ps1` | 查看任务 + token 状态 |
| `install-scheduled-task.ps1` | 安装定时自动刷新 |
| `create-desktop-toolbox.ps1` | 桌面快捷工具箱 |

### 定时任务

```powershell
.\install-scheduled-task.ps1                # 每 4 小时
.\install-scheduled-task.ps1 -EveryHours 2  # 每 2 小时

# 卸载
Unregister-ScheduledTask -TaskName "CodexAuthSessionRefresh" -Confirm:$false
```

### 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `CODEX_AUTH_PATH` | `~/.codex/auth.json` | 目标 auth.json |
| `CODEX_AUTH_REFRESH_BROWSER` | 自动检测 | Chrome/Edge 路径 |
| `CODEX_AUTH_REFRESH_PROFILE` | `./browser-profile` | 浏览器配置目录 |
| `CODEX_AUTH_REFRESH_BACKUP` | `./backups` | 备份目录 |
| `CODEX_AUTH_REFRESH_LOG` | `./logs` | 日志目录 |

---

## 🛡️ 安全设计

| 攻击面 | 防护措施 |
|--------|---------|
| `.gitignore` | `browser-profile/`、`logs/`、`backups/`、`auth.json` 全部排除 |
| Token 泄漏 | 日志明确 `delete safe.token` 后再写入 |
| auth.json 损坏 | **每次写入前**带时间戳备份 |
| 会话过期 | 提供独立的 `login-profile.ps1` 重新登录 |

> **如果泄露：** 登出所有 ChatGPT 会话 → 删 `browser-profile/` → 改密码。

---

## 🏗️ 架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        你的 Windows 电脑                          │
│                                                                  │
│  ┌──────────────┐    ┌──────────────────┐    ┌───────────────┐  │
│  │   ChatGPT    │    │    Playwright    │    │   Codex CLI   │  │
│  │   浏览器会话   │───▶│  (浏览器引擎)     │───▶│  auth.json    │  │
│  └──────────────┘    └──────────────────┘    └───────────────┘  │
│                              │                                   │
│                              ▼                                   │
│                   ┌────────────────────┐                         │
│                   │  Windows 定时任务   │                         │
│                   │  (每 N 小时)        │                         │
│                   └────────────────────┘                         │
└─────────────────────────────────────────────────────────────────┘
```

**技术栈：** Node.js 18+ → Playwright Core → Chrome/Edge → ChatGPT API

---

## 📦 项目结构

```
codex-auth-session-refresh/
├── scripts/
│   └── refresh-codex-auth.js       # 核心引擎
├── .github/workflows/ci.yml        # CI 流水线
├── assets/
│   ├── header-light.svg            # README 横幅（亮色）
│   └── header-dark.svg             # README 横幅（暗色）
├── login-profile.ps1               # 首次登录
├── run-refresh.ps1                 # 手动刷新
├── status.ps1                      # 健康检查
├── install-scheduled-task.ps1      # 定时任务安装
├── create-desktop-toolbox.ps1      # 桌面快捷方式
├── README.md                       # 英文文档
└── README_zh.md                    # 本文
```

---

<p align="center">
  <a href="https://github.com/zcz-user/codex-auth-session-refresh/stargazers">
    <img src="https://img.shields.io/github/stars/zcz-user/codex-auth-session-refresh?style=social" alt="Stars">
  </a>
  <a href="https://github.com/zcz-user/codex-auth-session-refresh/network/members">
    <img src="https://img.shields.io/github/forks/zcz-user/codex-auth-session-refresh?style=social" alt="Forks">
  </a>
  <br>
  <sub>🪟 给困在防火墙后面的开发者准备的小工具</sub>
</p>
