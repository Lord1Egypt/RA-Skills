# Emergence Agent CEO Architecture

A multi-agent architecture where an AI agent operates as the CEO of your growth operations — reading strategic intent, delegating to specialized sub-agents, and delivering production output — all coordinated through GitHub Issues.

The CEO agent runs 24/7 on a server via any autonomous agent framework (OpenClaw, Claude Code agents, etc.) with cron for proactive tasks.

## Quick Start

### MVP Mode (IM-only, no IDE required)

Interact with the CEO agent entirely through IM channels or mobile GitHub. Perfect for getting started in 30 minutes.

```bash
# 1. Clone this repo to your server
git clone https://github.com/emergencescience/emergence-agent-ceo.git
cd emergence-agent-ceo

# 2. Scaffold the workspace
./scripts/scaffold.sh /path/to/your/workspace

# 3. Configure your environment
cp .env.example .env
# Edit .env with your LLM API key and GitHub repo info

# 4. Start the agent (choose your runtime)
# openclaw gateway start          # OpenClaw
# claude run --agent hermes       # Claude Code agent mode
# (any autonomous agent framework with cron support works)

# 5. Send your first message (via IM or create a GitHub Issue)
# "Research the AI agent infrastructure landscape"
```

### Full Two-Tier Mode (Laptop + VPS)

When you're ready to graduate from IM to full workspace review:

1. **Laptop**: Use Cursor, Google Anti-gravity, or any IDE with CLI access
2. **VPS**: Run the CEO Agent from this workspace
3. **Bridge**: GitHub Issues for coordination, PRs for review

See [docs/two-tier-setup.md](docs/two-tier-setup.md) for detailed instructions.

## Architecture

```
Human Stakeholder                    VPS (Agent Team)
─────────────────                    ──────────────────
IM / Mobile GitHub / IDE             CEO Agent (Hermes)
                                     ├── cron heartbeat
CLIs (optional)                      ├── market survey
  Railway / Vercel / gh              ├── task creation & delegation
                                     ├── Growth Leader (content)
                                     └── DevOps Leader (infra)
                │
                │ GitHub Repository (shared state)
                │
```

## Agent Roles

| Role | Model | Responsibility |
| :--- | :--- | :--- |
| **CEO Agent (Hermes)** | DeepSeek-V4 Pro / Claude Sonnet / GLM-5.1 | Competitor analysis, market survey, task creation, delegation |
| **Growth Leader** | DeepSeek-V4 Flash | Content marketing, publications, social distribution, daily pulse |
| **DevOps Leader** | DeepSeek-V4 Flash | Infrastructure monitoring, CI/CD, error recovery |

> **Why the CEO needs a logic model**: The CEO's job — strategic reasoning, competitor analysis, task decomposition, quality judgment on sub-agent output — requires deep reasoning capabilities that cheap models cannot reliably provide. Sub-agents can use Flash-tier models for execution tasks, but the brain should think.

## How This Differs from Existing CEO Skills

| Skill | What it is | Key difference |
| :--- | :--- | :--- |
| **ceo-advisor** | Executive leadership guidance, board management | Advisory/prompt-level — not a runnable multi-agent system |
| **ceo-delegation** | CEO-style task delegation workflow (Chinese) | Prompt pattern only — no infrastructure, no GitHub coordination, no cron |
| **ceo** | Strategic planning, financial modeling roleplay | Roleplay framework — not a deployed agent architecture |
| **ai-company-ceo-2-0-0** | AI Company CEO architecture with 5-layer Hub-and-Spoke | Prompt framework with KPIs and guardrails — no production workspace, no 24/7 deployment |
| **emergence-agent-ceo** | **Full multi-agent system with infrastructure scaffolding** | **Deployable agent team with GitHub PR workflow, cron heartbeat, runbooks, and content pipeline** |

## Workspace Structure

```
emergence-agent-ceo/
├── SOUL.md                  # Agent identity and boundaries
├── MEMORY.md                # Long-term organizational memory
├── HEARTBEAT.md             # Cron schedule and proactive tasks
├── pulse/                   # Daily signal reports
├── growth/                  # Content factory
├── publications/            # Draft staging (blog, social)
├── strategies/              # Roadmaps and strategic direction
├── research/                # Intelligence and competitive analysis
├── ops/                     # Runbooks and operations
├── designs/                 # Architecture blueprints
└── .github/                 # GitHub Issue templates
```

## Model Cost Guide

| Configuration | Monthly Est. | Best For |
| :--- | :--- | :--- |
| CEO: DeepSeek-V4 Pro + Sub: Flash | ~$100-150 | Production, strategic depth |
| CEO: Claude Sonnet + Sub: Flash | ~$150-250 | Highest quality reasoning |
| All Flash tier | ~$50-80 | Budget mode, lower CEO quality |

## Getting Started

1. **[30-min quickstart](docs/quickstart.md)** — MVP mode, IM-only interaction
2. **[Full setup guide](docs/two-tier-setup.md)** — Laptop IDE + VPS architecture
3. **[Runbooks](ops/)** — Daily operations for each agent role
4. **[Issue templates](.github/ISSUE_TEMPLATE/)** — Ready-to-use strategic directives

## License

MIT
