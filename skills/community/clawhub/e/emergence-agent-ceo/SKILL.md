---
slug: emergence-agent-ceo
name: Autonomous Agent CEO Architecture using github and IM by Emergence 
version: 1.0.0
homepage: https://emergence.science/en/articles/hermes-agent-ceo-architecture
repository: https://github.com/emergencescience/emergence-agent-ceo
tags: [multi-agent, autonomous, github, cron, growth, ceo, hermes, openclaw]
description: |
  Multi-agent architecture where an AI agent operates as the CEO of growth operations.
  Reads strategic intent, delegates to specialized sub-agents, and delivers production output
  coordinated through GitHub Issues. Runs 24/7 on a server via any autonomous agent framework.
dependencies:
  - gh
---

# Emergence Agent CEO Architecture

A multi-agent system where a CEO Agent (Hermes) runs 24/7 on a server, coordinating specialized sub-agents through GitHub Issues. The human stakeholder focuses on strategy, relationships, and PR review — while agents handle execution.

## Agent Roles

| Role | Responsibility |
| :--- | :--- |
| **CEO Agent (Hermes)** | Competitor analysis, market survey, task creation, delegation |
| **Growth Leader** | Content marketing, publications, social distribution, daily pulse signals |
| **DevOps Leader** | Infrastructure monitoring, CI/CD health, error recovery, incident logging |

## Interaction Model: Human-in-the-Loop

By delegating tedious detailed work to agents, the human stakeholder is freed to focus on high-value activities:

- **Strategy**: Provide long-term direction via GitHub Issues
- **Relationships**: Manage public human relationships and stakeholder experience
- **Review**: Merge GitHub Pull Requests with approval
- **Amplification**: Provide external tools and credentials (Railway, Vercel, gh, API keys)

The CEO agent handles execution. Humans handle strategy, relationships, and judgment.

## Workflow

1. **Strategic Intent**: Human provides direction via GitHub Issue or IM message
2. **Analysis**: CEO agent researches topic, analyzes competitive landscape, writes analysis in issue comments
3. **Delegation**: CEO creates and assigns tasks to sub-agents (Growth Leader, DevOps Leader)
4. **Execution**: Sub-agents produce work in `publications/`, `pulse/`, `ops/` directories
5. **Review**: Sub-agents open PRs for human stakeholder review and merge
6. **Heartbeat**: CEO runs proactive daily cron tasks via HEARTBEAT.md schedule

## Quick Start

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
```

## Workspace Structure

```
emergence-agent-ceo/
├── SOUL.md                  # CEO agent identity and boundaries
├── SOUL-DEVOPS.md           # DevOps Leader identity and boundaries
├── SOUL-GROWTH.md           # Growth Leader identity and boundaries
├── MEMORY.md                # Long-term organizational memory
├── HEARTBEAT.md             # Cron schedule and proactive tasks
├── pulse/                   # Daily signal reports
├── publications/            # Draft staging (blog, social)
├── strategies/              # Roadmaps and strategic direction
├── research/                # Intelligence and competitive analysis
├── ops/                     # Runbooks and operations
├── designs/                 # Architecture blueprints
└── .github/                 # GitHub Issue templates
```

## Model Recommendations

The CEO's job — strategic reasoning, competitor analysis, task decomposition, quality judgment on sub-agent output — requires deep reasoning capabilities. Use a strong reasoning model for the CEO; sub-agents can use faster, cheaper models for execution tasks.

## License

MIT
