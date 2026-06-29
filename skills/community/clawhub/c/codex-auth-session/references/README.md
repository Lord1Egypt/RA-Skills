<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/zcz-user/codex-auth-session-refresh/main/assets/header-dark.svg">
    <img src="https://raw.githubusercontent.com/zcz-user/codex-auth-session-refresh/main/assets/header-light.svg" width="100%" alt="Codex Auth Session Refresh">
  </picture>
</p>

<p align="center">
  <b><a href="./README_zh.md">中文</a></b>
  &nbsp;·&nbsp;
  <a href="https://github.com/zcz-user/codex-auth-session-refresh/issues">Report Bug</a>
  &nbsp;·&nbsp;
  <a href="https://github.com/zcz-user/codex-auth-session-refresh/discussions">Discussion</a>
</p>

<p align="center">
  <img src="https://img.shields.io/github/stars/zcz-user/codex-auth-session-refresh?style=flat-square&logo=github" alt="Stars">
  <img src="https://img.shields.io/badge/Windows-0078D6?style=flat-square&logo=windows&logoColor=white" alt="Windows">
  <img src="https://img.shields.io/badge/Node.js-18%2B-339933?style=flat-square&logo=node.js" alt="Node.js">
  <img src="https://img.shields.io/badge/Playwright-45ba4b?style=flat-square&logo=playwright" alt="Playwright">
  <img src="https://img.shields.io/github/license/zcz-user/codex-auth-session-refresh?style=flat-square" alt="MIT">
  <img src="https://img.shields.io/github/last-commit/zcz-user/codex-auth-session-refresh?style=flat-square&logo=git" alt="Last commit">
  <img src="https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square" alt="PRs Welcome">
</p>

---

## 💡 Why This Exists

Codex CLI needs a valid `access_token` in `~/.codex/auth.json`. The standard OAuth login flow doesn't work in many real-world setups:

| 🚫 Scenario | ⚡ Impact |
|------------|-----------|
| **Corporate proxy** | OAuth redirects blocked by firewall |
| **WSL / Docker** | No browser available to complete flow |
| **Remote desktop (SSH)** | Auth popups fail silently |
| **Short token TTL** | Must re-authenticate every few hours |

**This tool bridges the gap** — it reads your own ChatGPT browser session to extract a fresh token and writes it directly to Codex's `auth.json`.

> No reverse engineering. No MITM. No API abuse. Just your browser doing what it already does.

---

## ✨ Features

| | |
|---|---|
| 🔌 **One command setup** | `npm install && .\login-profile.ps1` — done |
| 🤖 **Auto-refresh** | Windows Scheduled Task, configurable interval |
| 🛡️ **Safe by design** | Token never logged, backup before every write |
| 🪟 **Desktop shortcuts** | `create-desktop-toolbox.ps1` — click to run |
| 🔍 **Health dashboard** | `status.ps1` — task + token state at a glance |
| 🔧 **Fully configurable** | 6 environment variables for custom paths |
| 📦 **Zero runtime deps** | Only `playwright-core` — no bloated framework |

---

## 🚀 Getting Started

### One-liner install

```powershell
git clone https://github.com/zcz-user/codex-auth-session-refresh.git && cd codex-auth-session-refresh && npm install
```

### First use

```powershell
.\login-profile.ps1
# → Browser opens → Login to ChatGPT → Press Enter
.\status.ps1
# → Verify token is active
```

<details>
<summary><b>📸 What you'll see (click to expand)</b></summary>

```
=== Codex Auth Refresh Status ===

[TASK] Name: CodexAuthSessionRefresh
[TASK] State: Ready
[TASK] LastRunTime: 6/10/2026 7:55:00 PM
[TASK] LastTaskResult: 0 (0 means success)
[TASK] NextRunTime: 6/10/2026 11:55:00 PM

[AUTH] Path: C:\Users\you\.codex\auth.json
[AUTH] auth_mode: chatgpt
[AUTH] last_refresh: 2026-06-10T11:55:00.000Z
[AUTH] access_token length: 1024
[AUTH] account_id present: True

[LOG] Last entries:
{"time":"2026-06-10T11:55:00.000Z","status":"success"}
```

</details>

---

## 📋 Reference

### All Commands

| Command | What it does |
|---------|-------------|
| `login-profile.ps1` | First login / re-login (opens browser) |
| `run-refresh.ps1` | Refresh token now (browser auto-closes) |
| `status.ps1` | Check task + token state |
| `install-scheduled-task.ps1` | Set up auto-refresh every N hours |
| `create-desktop-toolbox.ps1` | Create desktop shortcuts |

### Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `CODEX_AUTH_PATH` | `~/.codex/auth.json` | Target auth file |
| `CODEX_AUTH_REFRESH_BROWSER` | _auto-detect_ | Chrome/Edge path override |
| `CODEX_AUTH_REFRESH_PROFILE` | `./browser-profile` | Browser profile storage |
| `CODEX_AUTH_REFRESH_BACKUP` | `./backups` | Auth file backup dir |
| `CODEX_AUTH_REFRESH_LOG` | `./logs` | Operation log dir |

### Scheduled Task

```powershell
.\install-scheduled-task.ps1               # Every 4h
.\install-scheduled-task.ps1 -EveryHours 2  # Every 2h

# Uninstall
Unregister-ScheduledTask -TaskName "CodexAuthSessionRefresh" -Confirm:$false
```

---

## 🛡️ Security Model

| Attack Vector | Mitigation |
|---------------|------------|
| `.gitignore` | `browser-profile/`, `logs/`, `backups/`, `*.log`, `auth.json` all excluded |
| Token leak | Logs explicitly `delete safe.token` before writing |
| Corrupted auth | Backup with timestamp **before every write** |
| Stale session | Separate `login-profile.ps1` for clean re-auth |

> **If compromised:** Sign out all ChatGPT sessions → delete `browser-profile/` → rotate credentials.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Your Windows Machine                          │
│                                                                  │
│  ┌──────────────┐    ┌──────────────────┐    ┌───────────────┐  │
│  │   ChatGPT    │    │    Playwright    │    │   Codex CLI   │  │
│  │   Session    │───▶│  (persistent)    │───▶│  auth.json    │  │
│  └──────────────┘    └──────────────────┘    └───────────────┘  │
│                              │                                   │
│                              ▼                                   │
│                   ┌────────────────────┐                         │
│                   │  Scheduled Task    │                         │
│                   │  (every N hours)   │                         │
│                   └────────────────────┘                         │
└─────────────────────────────────────────────────────────────────┘
```

**Stack:** Node.js 18+ → Playwright Core → Chrome/Edge → ChatGPT API

---

## 📦 Project Structure

```
codex-auth-session-refresh/
├── scripts/
│   └── refresh-codex-auth.js       # Core engine
├── .github/workflows/ci.yml        # CI pipeline
├── assets/
│   ├── header-light.svg            # README banner (light)
│   └── header-dark.svg             # README banner (dark)
├── login-profile.ps1               # First login flow
├── run-refresh.ps1                 # Manual refresh
├── status.ps1                      # Health check
├── install-scheduled-task.ps1      # Auto-refresh setup
├── create-desktop-toolbox.ps1      # Desktop shortcuts
├── SECURITY.md                     # Security deep-dive
├── CONTRIBUTING.md                 # Contribution guide
├── README.md                       # This file
└── README_zh.md                    # 中文文档
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
  <sub>Made with 🔥 for developers stuck behind firewalls</sub>
</p>
