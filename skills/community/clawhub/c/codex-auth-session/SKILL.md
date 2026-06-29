---
name: codex-auth
description: 🧩 Codex Skill — Refresh your Codex CLI auth.json from a local ChatGPT web session. Essential for Codex users behind firewalls, in WSL/containers, or on remote desktops.
tags:
  - codex
  - codex-cli
  - auth
  - chatgpt
  - token
  - windows
  - playwright
---

# 🧩 Codex Skill: Codex Auth Session Refresh

> **This is an [OpenClaw skill](https://clawhub.com/skill/codex-auth-session) for [Codex CLI](https://github.com/openai/codex).**
> It provides Windows tooling to refresh Codex's `auth.json` with a fresh ChatGPT session token.

**適用於 Codex · For Codex CLI users**

---

## 🎯 Who Is This For?

**Codex CLI users** who are stuck with any of these:

| 😤 Pain | 💥 Why it sucks |
|---------|----------------|
| Codex OAuth won't complete | Proxies, WSL, containers — browser never opens |
| OpenAI 2FA every time | Token expires every few hours |
| Forced to use API proxies | Can't get official auth working, settle for third-party |
| Token dies mid-session | Lose context, workflow destroyed |

## What This Does

Extracts a fresh `access_token` from your existing ChatGPT browser session and writes it directly to Codex's `~/.codex/auth.json`. No reverse engineering. No MITM. No API abuse.

**适用于 Codex CLI！Codex 走不了 OAuth 时的救星。**

## Quick Install (on Windows)

```powershell
git clone https://github.com/zcz-user/codex-auth-session-refresh.git
cd codex-auth-session-refresh
npm install
.\login-profile.ps1        # Login ChatGPT → press Enter
.\status.ps1               # Check Codex auth state
```

Then Codex will see the fresh token in `~/.codex/auth.json`.

## Installation via ClawHub

```bash
clawhub install codex-auth-session
```

## Commands (for Codex auth management)

| Command | What it does |
|---------|-------------|
| `login-profile.ps1` | First login / re-login into ChatGPT (for Codex) |
| `run-refresh.ps1` | Refresh Codex's access token now |
| `status.ps1` | Check Codex auth.json status |
| `install-scheduled-task.ps1` | Auto-refresh Codex auth every N hours |
| `create-desktop-toolbox.ps1` | Desktop shortcuts for Codex auth management |

## How It Works

```
You (browser login to ChatGPT)
        │
        ▼
Playwright → chatgpt.com/api/auth/session → accessToken
                                                  │
                                                  ▼
                                        ~/.codex/auth.json
                                        (backup created before update)
                                                  │
                                                  ▼
                                  Windows Scheduled Task
                                  (auto-refresh, so Codex never loses auth)
```

## Security

- Token values are **never** logged — `delete safe.token` before write
- `auth.json` backed up with timestamp before every update
- All sensitive paths excluded via `.gitignore`

## Requirements

- **OS:** Windows 10/11
- **Runtime:** Node.js 18+
- **Browser:** Chrome or Microsoft Edge
- **Target:** [Codex CLI](https://github.com/openai/codex) by OpenAI
