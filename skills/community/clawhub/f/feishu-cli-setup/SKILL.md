---
name: Feishu CLI Setup
description: |
  Step-by-step AI agent guide for installing and configuring lark-cli (飞书/Lark CLI).
  Designed for Claude, Manus, and OpenClaw to proactively guide users through:
  prerequisites check → npm install → Feishu app config → OAuth login → verification → first commands.
  Handles the browser-based OAuth flow by extracting authorization URLs and presenting them to the user.
  Covers all 20 built-in lark-cli Agent Skills across Calendar, IM, Docs, Base, Sheets, Tasks, Mail, and more.
keywords:
  - feishu
  - lark
  - lark-cli
  - feishu-cli
  - install
  - setup
  - 飞书
  - 飞书cli
  - 飞书安装
  - 飞书配置
  - lark install
  - lark setup
  - claude
  - manus
  - openclaw
  - ai agent
  - agent setup
  - npm install
  - oauth
  - auth login
  - 认证
  - 安装向导
  - calendar
  - im
  - docs
  - sheets
  - 日历
  - 消息
  - 文档
  - 表格
  - 任务
  - automation
  - 自动化
  - 集成
metadata:
  openclaw:
    runtime:
      node: ">=18"
---

# Feishu CLI Setup

An AI-native installation guide for **lark-cli** — the official Lark/Feishu CLI tool (6.7k ⭐, maintained by larksuite). Enables Claude, Manus, and OpenClaw to proactively guide users from zero to a fully authenticated lark-cli in minutes.

> **Why does this skill exist?** Installing lark-cli involves a browser OAuth step that AI agents cannot complete on behalf of users. This skill provides the exact prompts and workflows for agents to extract authorization URLs from CLI output and present them to users at the right moment — making the otherwise tricky setup seamless.

## What is lark-cli?

| Item | Detail |
|------|--------|
| Repo | [github.com/larksuite/cli](https://github.com/larksuite/cli) |
| Latest | v1.0.4 |
| Commands | 200+ |
| Agent Skills | 20 built-in (Calendar, IM, Docs, Base, Sheets, Tasks, Mail, Wiki, …) |
| License | MIT |
| Install | `npm install -g @larksuite/cli` |

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/check.js` | Detect OS, Node.js version, and lark-cli install state |
| `scripts/install.js` | Guide `npm install -g @larksuite/cli` + skills add |
| `scripts/config.js` | Guide `lark-cli config init --new` — extracts browser URL for user |
| `scripts/auth.js` | Guide `lark-cli auth login --recommend` — extracts OAuth URL for user |
| `scripts/verify.js` | Run `lark-cli auth status` and summarize available Agent Skills |
| `scripts/learn.js` | Show first commands to try (calendar, im, docs, tasks) |
| `scripts/setup.js` | Full guided pipeline — runs all steps in sequence |

## Usage

```bash
# Full guided setup (recommended)
node scripts/setup.js

# Individual stages
node scripts/check.js          # detect current state
node scripts/install.js        # install lark-cli
node scripts/config.js         # configure Feishu app credentials
node scripts/auth.js           # authenticate via OAuth
node scripts/verify.js         # verify and list available skills
node scripts/learn.js          # first commands guide

# Language options
node scripts/setup.js --lang en
node scripts/setup.js --lang zh    # default
```

## Agent Workflow (4 Steps)

```
Step 1 — Install
  npm install -g @larksuite/cli
  npx skills add larksuite/cli -y -g

Step 2 — Configure app credentials (run in background, extract URL → send to user)
  lark-cli config init --new

Step 3 — Login (run in background, extract URL → send to user)
  lark-cli auth login --recommend

Step 4 — Verify
  lark-cli auth status
```

## 20 Built-in Agent Skills (after setup)

| Skill | Domain |
|-------|--------|
| `lark-shared` | Auth, config, identity (auto-loaded) |
| `lark-calendar` | Calendar, agenda, events |
| `lark-im` | Messages, group chats, reactions |
| `lark-doc` | Documents (Markdown) |
| `lark-drive` | Files, uploads, downloads |
| `lark-sheets` | Spreadsheets |
| `lark-base` | Tables, records, views, dashboards |
| `lark-task` | Tasks, subtasks, reminders |
| `lark-mail` | Email (send, reply, search) |
| `lark-contact` | User search by name/email/phone |
| `lark-wiki` | Knowledge spaces & nodes |
| `lark-event` | WebSocket event subscriptions |
| `lark-vc` | Meeting records & minutes |
| `lark-whiteboard` | Whiteboard/chart DSL |
| `lark-minutes` | Meeting AI artifacts |
| `lark-openapi-explorer` | API documentation explorer |
| `lark-skill-maker` | Custom skill framework |
| `lark-approval` | Approval tasks & workflows |
| `lark-workflow-meeting-summary` | Meeting summary workflow |
| `lark-workflow-standup-report` | Standup report workflow |

## Security Notes

lark-cli runs under your Feishu/Lark user identity. Keep these in mind:
- Do not share your `LARK_APP_ID` / `LARK_APP_SECRET` in public repos
- Use `--dry-run` for commands with side effects before executing
- Do not add the bot to group chats if you want to avoid permission exposure
- Credentials are stored in the OS native keychain (not plaintext)

---

*Version: 1.0.0 · Source: [github.com/larksuite/cli](https://github.com/larksuite/cli) · Updated: 2026-04-05*
