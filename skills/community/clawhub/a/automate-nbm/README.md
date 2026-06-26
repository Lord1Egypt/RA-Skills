# Automate — AI Agent Agency + Task Automation

A persistent subagent system combining **61 specialized AI agents** across 8 departments with **GitHub-native secure task automation**.

## What Is This?

**Automate** is a private, self-contained AI agency and task automation platform. It fuses:

- 🤖 **Agency Agents** — 61 specialized AI agent personas (engineering, design, marketing, product, PM, testing, support, specialized)
- 🔄 **Orchestrator** — Multi-agent pipeline that breaks down complex projects and delegates to specialists
- ⚡ **GitHub Actions Automation** — Issue-driven task execution, scheduled jobs, and secure communication
- 🔒 **Security-First** — SSH keys, encrypted secrets, sender validation, full audit trail

## Architecture

```
automate-nbm/
├── .github/
│   ├── workflows/
│   │   ├── agent-task.yml          # AI agent-powered task processing
│   │   ├── orchestrator.yml        # Multi-agent orchestration pipeline
│   │   ├── task-runner.yml         # Basic task execution on issues
│   │   ├── scheduled.yml           # Cron-based automation
│   │   └── secure-comm.yml         # Encrypted message relay
│   └── ISSUE_TEMPLATE/
│       ├── task.md                 # Generic task template
│       └── agent-task.md           # Agent-specific task template
├── agents/                         # 61 AI Agent definitions
│   ├── engineering/                # 7 agents: frontend, backend, mobile, AI, devops...
│   ├── design/                     # 7 agents: UI, UX, brand, visual...
│   ├── marketing/                  # 8 agents: growth, content, social...
│   ├── product/                    # 3 agents: sprint, trends, feedback
│   ├── project-management/         # 5 agents: PM, shepherd, ops...
│   ├── testing/                    # 7 agents: QA, reality-checker, perf...
│   ├── support/                    # 6 agents: support, analytics, finance...
│   └── specialized/                # 6 agents: orchestrator, data, LSP...
├── orchestrator/
│   └── SKILL.md                    # Multi-agent orchestration engine
├── scripts/
│   ├── run-task.sh                 # Task executor
│   ├── agent-dispatch.sh           # Agent selection + dispatch
│   └── notify.sh                   # Notification helper
├── config/
│   └── automate.yml                # Agent + automation config
├── docs/
│   └── QUICKSTART.md               # Getting started guide
├── SKILL.md                        # OpenClaw skill definition
├── AGENTS.md                       # Agent registry & quick reference
└── package.json                    # Metadata
```

## How It Works

### 0. Issue-Driven Tasks
Create a GitHub Issue → label it → Automate picks it up, selects the right agent(s), and posts results back.

### 1. Agent Selection
Tag your issue with an agent or department label:
- `agent:frontend-developer` — routes to the frontend specialist
- `department:engineering` — routes to the engineering team
- `orchestrate` — triggers the full multi-agent pipeline

### 2. Orchestrated Projects
For complex tasks, the Orchestrator:
0. **Analyzes** requirements
1. **Decomposes** into tasks
2. **Assigns** to specialist agents
3. **Runs dev→QA loops** with quality gates
4. **Delivers** integrated results

### 3. Scheduled Automation
Cron workflows run periodic tasks — health checks, reports, data collection.

### 4. Secure Communication
`repository_dispatch` events with sender validation enable encrypted, authenticated messaging.

## Available Agents (61)

| Department | Count | Key Agents |
|---|---|---|
| 💻 Engineering | 7 | frontend-developer, backend-architect, mobile-app-builder, ai-engineer, devops-automator, rapid-prototyper, senior-developer |
| 🎨 Design | 7 | ui-designer, ux-researcher, ux-architect, brand-guardian, visual-storyteller, whimsy-injector, image-prompt-engineer |
| 📢 Marketing | 8 | growth-hacker, content-creator, twitter-engager, tiktok-strategist, instagram-curator, reddit-community-builder, app-store-optimizer, social-media-strategist |
| 📊 Product | 3 | sprint-prioritizer, trend-researcher, feedback-synthesizer |
| 🎬 Project Mgmt | 5 | studio-producer, project-shepherd, studio-operations, experiment-tracker, senior-pm |
| 🧪 Testing | 7 | evidence-collector, reality-checker, test-results-analyzer, performance-benchmarker, api-tester, tool-evaluator, workflow-optimizer |
| 🛟 Support | 6 | support-responder, analytics-reporter, finance-tracker, infrastructure-maintainer, legal-compliance-checker, executive-summary-generator |
| 🎯 Specialized | 6 | orchestrator, data-analytics-reporter, lsp-index-engineer, sales-data-extraction, data-consolidation, report-distribution |

## Quick Start

### Submit a Task
0. Create an Issue using the **Agent Task** template
1. Select the agent/department
2. Describe your task clearly
3. Automate processes it and posts results

### Trigger Orchestration
0. Create an Issue with the `orchestrate` label
1. Describe the full project scope
2. The Orchestrator breaks it down and manages the pipeline

### Manual Run
Go to **Actions → Agent Task Runner → Run workflow** and provide:
- Agent name
- Task description

## Security

| Layer | Method |
|---|---|
| Authentication | SSH ed25519 keys |
| Secrets | GitHub Encrypted Secrets |
| Communication | `repository_dispatch` with sender validation |
| Audit | GitHub Actions logs + issue comments |
| Permissions | Minimum-scope workflow tokens |

### Required Secrets
| Secret | Purpose |
|---|---|
| `OPENCLAW_TOKEN` | AI-powered task processing |
| `AUTOMATE_SSH_KEY` | SSH back to host server |
| `ALLOWED_SENDERS` | Whitelist for secure-comm |

## License

Private — authorized use only.

Based on [agency-agents](https://github.com/msitarzewski/agency-agents) by @msitarzewski (MIT).
