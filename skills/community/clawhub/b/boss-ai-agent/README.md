---
name: boss-ai-agent
title: "Boss AI Agent"
version: "9.0.0"
description: "Boss AI Agent — AI management advisor and team operations middleware. Use this skill whenever the user needs management advice, leadership guidance, or team operations help. 16 mentor philosophies, 9 culture packs, C-Suite board simulation, continuous learning. Works offline as advisor or connected to manageaibrain.com MCP for full 33-tool automation."
user-invocable: true
emoji: "🤖"
homepage: "https://manageaibrain.com"
metadata:
  openclaw:
    optional:
      env:
        - name: "MANAGEMENT_BRAIN_API_KEY"
          description: "Enables Team Operations Mode — 33 MCP tools, 6 cron jobs, message delivery to employees, bidirectional Notion/Sheets sync. Without this key the skill runs in Advisor Mode only (offline, zero network). Authenticates all MCP calls to manageaibrain.com/mcp. Scoped to one company; each API key maps to exactly one organization. Audit via web dashboard at manageaibrain.com."
        - name: "BOSS_AI_AGENT_API_KEY"
          description: "Adds read-only GET access to manageaibrain.com/api/v1/ for extended mentor configs and analytics dashboards. Separate from MCP authentication. Falls back to MANAGEMENT_BRAIN_API_KEY if not set. Only relevant in Team Operations Mode."
      config:
        - "~/.openclaw/skills/boss-ai-agent/config.json"
---

# Boss AI Agent

Your AI management advisor — works instantly after install, no account needed.

## Features

### Advisor Mode (works immediately)

- **16 mentor philosophies**: Musk, Inamori, Jack Ma, Dalio, Grove, Ren Zhengfei, Son, Jobs, Bezos, Buffett, Zhang Yiming, Lei Jun, Cao Dewang, Chu Shijian, Erin Meyer, Jack Trout
- **9 culture packs**: default, Philippines, Singapore, Indonesia, Sri Lanka, Malaysia, China, USA, India
- **C-Suite board simulation**: 6 AI executives (CEO/CFO/CMO/CTO/CHRO/COO) analyze any strategic topic
- **Management advice**: decisions, 1:1 prep, conflict resolution, check-in question design, report templates
- **Zero dependency**: no account, no cloud, no setup beyond mentor selection

### Team Operations Mode (connect MCP to unlock)

Everything in Advisor Mode, plus:

- **33 MCP tools**: real team queries, execution intelligence, AI recommendations, brain context, data sync, and message delivery via `manageaibrain.com/mcp`
- **12 automated scenarios**: daily check-in cycle, project health patrol, smart briefing, 1:1 meeting prep, signal scanning, knowledge base, emergency response, execution risk review, KPI health check, incentive review, AI recommendations, data sync
- **6 cron jobs**: automated check-ins, chases, summaries, briefings, signal scans, data sync
- **Bidirectional Notion/Sheets sync**: tasks, goals, projects, metrics synced every 30 minutes with conflict resolution
- **23+ messaging platforms**: Telegram, Slack, Lark, Signal, and more via OpenClaw
- **OpenClaw connector integration**: storage tools (Notion/Sheets), dev tools (GitHub/Linear/Calendar), communication tools (Slack/Discord/Lark) feed data into the company context layer
- **AI Recommendation Engine**: daily scans (enriched with employee memory patterns) + real-time triggers (sentiment, memory-based stress/blocker/growth/engagement patterns) generate prioritized management suggestions with one-click actions and feedback-driven learning
- **Web Dashboard**: real-time analytics at [manageaibrain.com](https://manageaibrain.com) — 20+ pages including Dashboard, Company State, KPI Metrics, Projects, Tasks, Incentives, Recommendations, Goals, Reviews, Skills, Training, Career Paths

## Install

```
clawhub install boss-ai-agent
```

## Quick Start

### Advisor Mode (no setup needed)

```
/boss-ai-agent
→ Running in Advisor Mode.
→ Which mentor? Musk / Inamori / Ma ...
→ You: "How should I handle a consistently late employee?"
→ [Musk-flavored management advice with action steps]
```

### Team Operations Mode (connect MCP first)

**Option A: CLI (stdio) — Recommended**

Add to your MCP config (Claude Code `settings.json`, Hermes Agent config, etc.):

> **Security**: Replace the placeholder key below with your real API key. Never commit real API keys to version control — use environment variables or a secrets manager instead.

```json
{
  "mcpServers": {
    "management-brain": {
      "command": "npx",
      "args": ["-y", "@tonykk/management-brain-mcp"],
      "env": {
        "MANAGEMENT_BRAIN_API_KEY": "mb_your_api_key_here",
        "MANAGEMENT_BRAIN_BASE_URL": "https://manageaibrain.com"
      }
    }
  }
}
```

**Option B: HTTP**

Connect to `https://manageaibrain.com/mcp` with `Authorization: Bearer <MCP_HTTP_API_KEY>`. For ChatGPT, Gemini, and web-based clients.

Then:

```
/boss-ai-agent
→ Running in Team Operations Mode — connected to your team.
→ How many people do you manage? 5
→ What communication tools? Telegram and GitHub
→ Done! Musk mode activated. First check-in at 9 AM tomorrow.
```

## How It Works

The skill auto-detects which mode to use based on whether MCP tools are available.

**Advisor Mode**: AI uses embedded mentor frameworks (decision matrices, culture packs, scenario templates) to answer management questions directly. No network communication — everything runs from the skill instructions.

**Team Operations Mode**: AI connects to the MCP server for real team operations. Two transport options:
- **CLI (stdio)**: `npx -y @tonykk/management-brain-mcp` — only needs `MANAGEMENT_BRAIN_API_KEY`. Recommended for Claude Code, Hermes Agent, and stdio-capable clients.
- **HTTP**: Connect to `manageaibrain.com/mcp` — needs `MCP_HTTP_API_KEY` Bearer auth. For ChatGPT, Gemini, and web-based clients.

Tool parameters (employee names, discussion topics, message content) are sent to the cloud server for processing. Write tools deliver messages to employees via connected platforms. Local files (`config.json`, chat history, memory) stay on your machine and are not transmitted to the server.

**Persistent behavior** (Team Operations only): Registers up to 6 cron jobs that run autonomously — including jobs that send messages to employees. Solo founder mode (team=0) only registers 3 (briefing, signalScan, sync). Review schedules in `config.json` before activating. Manage with `cron list` / `cron remove`.

## OpenClaw Integration Architecture

Boss AI Agent is the **brain layer** — it connects to its own backend (`manageaibrain.com/mcp`) for team data processing, while third-party tool integrations are handled by OpenClaw's MCP connectors.

```
OpenClaw Runtime (user environment)
  ├── MCP Connectors (user self-installs)
  │    ├── Storage: Notion / Google Sheets  ←── bidirectional sync targets
  │    ├── Development: GitHub / Linear / Calendar
  │    └── Communication: Telegram / Slack / Discord / Lark
  │
  └── Boss AI Agent Skill (brain layer + sync orchestrator)
       └── manageaibrain.com API
            ├── 33 MCP tools (daily ops + intelligence + sync)
            ├── Company Context Layer  ← foundation
            ├── Execution Intelligence ← signals + risks
            ├── Communication Parser   ← messages → events
            ├── Incentive Engine       ← context-aware scoring
            ├── AI Recommendations     ← proactive suggestions
            └── Sync Service           ← Notion/Sheets bidirectional sync
```

**Company Context Layer** is the foundation — all intelligence engines depend on it:
- Storage connectors (Notion/Jira/Sheets) → project updates, task status, documentation flow into context
- Dev connectors (GitHub/Linear) → PR activity, commit patterns, CI status feed into execution signals
- Communication connectors (Telegram/Slack/Discord/Lark) → employee messages are parsed into structured management events

**Key principle**: the skill does NOT manage tokens for third-party tools (Notion, GitHub, etc.) — OpenClaw handles those connections. The skill connects to its own `manageaibrain.com/mcp` backend (authenticated via `MANAGEMENT_BRAIN_API_KEY`) and consumes third-party connector data to build management intelligence.

## Mentors

| ID | Name | Tier | Style |
|----|------|------|-------|
| musk | Elon Musk | Full | First principles, urgency, 10x thinking |
| inamori | Kazuo Inamori (稻盛和夫) | Full | Altruism, respect, team harmony |
| ma | Jack Ma (马云) | Full | Embrace change, teamwork, customer-first |
| dalio | Ray Dalio | Standard | Radical transparency, principles-driven |
| grove | Andy Grove | Standard | OKR-driven, data-focused, high output |
| ren | Ren Zhengfei (任正非) | Standard | Wolf culture, self-criticism, striver-oriented |
| son | Masayoshi Son (孙正义) | Standard | 300-year vision, bold bets |
| jobs | Steve Jobs | Standard | Simplicity, excellence pursuit |
| bezos | Jeff Bezos | Standard | Day 1 mentality, customer obsession |
| buffett | Warren Buffett | Light | Long-term value, patience |
| zhangyiming | Zhang Yiming (张一鸣) | Light | Delayed gratification, data-driven |
| leijun | Lei Jun (雷军) | Light | Extreme value, user participation |
| caodewang | Cao Dewang (曹德旺) | Light | Industrial spirit, craftsmanship |
| chushijian | Chu Shijian (褚时健) | Light | Ultimate focus, resilience |
| meyer | Erin Meyer (艾琳·梅耶尔) | Light | Cross-cultural communication, culture map |
| trout | Jack Trout (杰克·特劳特) | Light | Positioning theory, brand strategy |

**Full** = complete 7-point decision matrix. **Standard** = check-in questions + core tags. **Light** = tags only (AI infers behavior).

## AI C-Suite Board

Convene 6 AI executives for cross-functional strategic analysis:

| Seat | Domain |
|------|--------|
| CEO | Strategy, vision, competitive positioning |
| CFO | Finance, budgets, ROI analysis |
| CMO | Marketing, growth, brand strategy |
| CTO | Technology, architecture, engineering |
| CHRO | People, culture, talent management |
| COO | Operations, process, efficiency |

- **Advisor Mode**: Stateless simulation — AI role-plays all 6 perspectives in conversation.
- **Team Operations Mode**: `board_discuss` tool for persistent history enriched with team data.

## MCP Tools (Team Operations Mode)

33 tools accessible via MCP:

### Read Tools — Daily Operations (9)

| Tool | Description |
|------|-------------|
| `get_team_status` | Today's check-in progress |
| `get_report` | Weekly/monthly performance with rankings |
| `get_alerts` | Alerts for consecutive missed check-ins |
| `switch_mentor` | Change management philosophy |
| `list_mentors` | All 16 mentors with expertise |
| `board_discuss` | AI C-Suite board meeting (persistent) |
| `chat_with_seat` | Direct chat with one C-Suite exec |
| `list_employees` | All active employees |
| `get_employee_profile` | Employee sentiment and history |

### Read Tools — Execution Intelligence (9)

| Tool | Description |
|------|-------------|
| `get_company_state` | Full operational snapshot: risks, tasks, events, blocked projects |
| `get_execution_signals` | AI risk signals: overload, delivery, engagement, anomalies |
| `get_communication_events` | Structured events from check-ins: blockers, completions, delays |
| `get_top_risks` | Highest-severity execution risks sorted by urgency |
| `get_working_memory` | AI situational awareness: focus areas, momentum, action items |
| `get_kpi_dashboard` | All KPI metrics with latest values vs targets |
| `get_overdue_tasks` | Tasks past due date with priority and assignee |
| `get_task_stats` | Task status breakdown: todo, in_progress, done, blocked |
| `get_incentive_scores` | Per-employee incentive scores with breakdowns |

### Read Tools — Brain Context (3)

| Tool | Description |
|------|-------------|
| `get_company_context` | Complete company context: org profile, priorities, risks, team, HR insights |
| `get_goal_state` | OKR/KPI progress: goals, key results, metric values vs targets |
| `create_execution_plan` | Generate prioritized action plan based on context, goals, signals |

### Write Tools (4 — sends messages)

| Tool | Description |
|------|-------------|
| `send_checkin` | Trigger check-in questions |
| `chase_employee` | Chase reminders for non-submitters |
| `send_summary` | Generate and send daily summary |
| `send_message` | Send custom message to an employee |

### Write Tools — Context (3)

| Tool | Description |
|------|-------------|
| `ingest_metric` | Record a KPI data point from external sources |
| `update_context` | Update strategic priorities, key risks, management style weights |
| `calculate_incentives` | Calculate incentive scores for all employees in a period |

### AI Recommendations (2)

| Tool | Description |
|------|-------------|
| `get_recommendations` | Get pending AI management suggestions with priority, evidence, actions |
| `execute_recommendation` | Execute a suggested action (send message, schedule meeting, etc.) |

### Sync Tools (3 — bidirectional Notion/Sheets sync)

| Tool | Description |
|------|-------------|
| `get_sync_manifest` | Get data changes since last sync for push to Notion/Sheets |
| `report_sync_result` | Report sync completion with stats and pulled items |
| `configure_sync` | Configure sync: storage type, entity types, frequency |

**MCP transport**: CLI (stdio) recommended — `npx -y @tonykk/management-brain-mcp` with `MANAGEMENT_BRAIN_API_KEY`. HTTP alternative: `https://manageaibrain.com/mcp` with `MCP_HTTP_API_KEY` Bearer auth.

## Web Dashboard (Team Operations Mode)

Professional management dashboard at [manageaibrain.com](https://manageaibrain.com), built with Vue3 + NaiveUI:

- **Observe**: Dashboard (health gauge, check-in status, submission trend, sentiment heatmap, AI recommendations summary), Company State, KPI Metrics, Alerts, Reports
- **Organize**: Team Members, Organization, Projects, Tasks, Skill Inventory, Mentor, C-Suite Board
- **Lead**: Sentiment Map, 1:1 Coaching, 1:1 Meetings, Reviews, Incentives, Training, Career Paths
- **Plan**: Board Records, Goals & KPIs
- **Analyze**: AI Insights, Weekly Digest, AI Recommendations (with one-click execute/dismiss)

## 中文说明

Boss AI Agent 是老板的 AI 管理中间件。安装后立即可用（Advisor 模式），无需注册账号。

**两种模式：**
- **顾问模式**（零依赖）— 16 位导师哲学框架（稻盛和夫、马云、马斯克等）、9 套文化包（中国、菲律宾、新加坡等）、C-Suite 董事会模拟、1:1 准备、管理决策建议。装了就能用，不联网。
- **团队运营模式**（连接 MCP）— 33 个 MCP 工具实现自动签到、追踪、报表、消息推送、执行力分析、KPI 仪表盘、任务管理、激励评分、AI 推荐引擎、Notion/Sheets 双向同步，6 个定时任务，23+ 平台支持。

**OpenClaw 集成架构：** Boss AI Agent 作为"大脑层 + 同步编排器"，与 OpenClaw MCP 连接器配合使用：
- **储存工具**（Notion / Google Sheets）→ 双向同步目标，任务/目标/项目/指标自动同步
- **开发工具**（GitHub / Linear / Calendar）→ PR、提交、CI 状态转化为执行力信号
- **沟通工具**（Telegram / Slack / Discord / Lark）→ 员工消息解析为结构化管理事件

**双向数据同步（v6.0 新增）：** 支持与 Notion 和 Google Sheets 双向同步。工作时间每 30 分钟自动同步，支持冲突检测和解决。

**MCP 连接方式（v6.2 新增）：** 支持两种 MCP 传输方式：
- **CLI (stdio)**（推荐）— `npx -y @tonykk/management-brain-mcp`，只需 `MANAGEMENT_BRAIN_API_KEY`，无需 HTTP 认证。适合 Claude Code、Hermes Agent。
- **HTTP** — 连接 `manageaibrain.com/mcp`，需要 `MCP_HTTP_API_KEY`。适合 ChatGPT、Gemini 等。

**数据说明：** 顾问模式不发送任何数据到云端。团队运营模式中，MCP 工具参数发送至 `manageaibrain.com` 处理。同步通过 OpenClaw 连接器访问 Notion/Sheets，Skill 不直接管理令牌。

安装：`clawhub install boss-ai-agent`

## Links

- Website: https://manageaibrain.com
- MCP Server — CLI (stdio): `npx -y @tonykk/management-brain-mcp` with `MANAGEMENT_BRAIN_API_KEY`
- MCP Server — HTTP: `https://manageaibrain.com/mcp` with `MCP_HTTP_API_KEY` Bearer auth
- GitHub: https://github.com/tonypk/ai-management-brain
- ClawHub: https://clawhub.ai/tonypk/boss-ai-agent
