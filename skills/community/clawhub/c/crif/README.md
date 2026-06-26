# CRIF - Crypto Research Interactive Framework

**CRIF** is a prompt engineering framework for crypto research that transforms AI into a structured research partner. Built entirely in Markdown — zero code, fully customizable.

## The Problem

When you use AI for research, you typically hand off a task and get back a completed report. The quality is inconsistent — AI may focus on the wrong aspects, miss critical angles, or produce generic output. Running it again costs more tokens with no guarantee of improvement.

The core issue: **you can't control the research process, only the input and output.**

## The CRIF Approach

CRIF introduces continuous human-AI interaction throughout the research process:

```
You direct  →  AI researches  →  AI checks in  →  You review & refine  →  Repeat
```

- **Collaborative by default** — AI pauses at meaningful milestones for your feedback
- **Domain knowledge injection** — Contribute expertise at any checkpoint
- **Structured workflows** — 19 research workflows with defined methodology and output templates
- **Autonomous when needed** — Skip checkpoints for routine tasks

## Requirements

An AI assistant with file read/write capabilities:

- [Claude Code / Codex](https://claude.ai/code)
- [OpenClaw](https://openclaw.ai/) (Telegram)
- Any AI CLI tool with filesystem access

## Quick Start

### Option 1: Paste the repo link (fastest)

Give your AI assistant this link:

```
https://github.com/kudodefi/crif
```

The AI will clone the repo and activate CRIF automatically.

### Option 2: Clone manually

```bash
git clone https://github.com/kudodefi/crif.git
cd crif
```

Then start your AI assistant in the `crif/` directory.

### Start researching

Just describe what you need in natural language:

```
Analyze Hyperliquid for investment decision
```

CRIF activates automatically — identifies the subject, suggests a workflow, asks for your preferences, and begins research.

## How It Works

### 1. You request → Orchestrator routes

The Orchestrator reads your request and matches it to the right workflow. If unclear, it presents options.

### 2. AI embodies expert persona

Each workflow is assigned a specialized agent (Market Analyst, Project Analyst, Technology Analyst, Content Creator, QA Specialist, or Image Creator). The AI fully adopts the persona's expertise and thinking approach.

### 3. Research with checkpoints (Collaborative mode)

AI researches autonomously, then pauses at meaningful milestones:

```
CHECKPOINT: Competitive Landscape
─────────────────────────────────

Key findings:
- Hyperliquid leads with 70% open interest...
- Lighter emerging as competitive threat...

Your feedback:
a. Continue
b. Expand — add depth on specific area
c. Adjust — change focus
d. Insight — share domain knowledge
```

### 4. Output delivered

Structured report written to workspace, following the workflow's template.

## Workflows

### Market Intelligence
| Workflow | Description |
|----------|-------------|
| `sector-overview` | Sector structure, mechanics, participants |
| `sector-landscape` | Complete player mapping and categorization |
| `competitive-analysis` | Head-to-head comparison of 2-5 projects |
| `trend-analysis` | Trend identification and forecasting |

### Project Fundamentals
| Workflow | Description |
|----------|-------------|
| `project-snapshot` | Quick project overview |
| `product-analysis` | Product mechanics, PMF, innovation |
| `team-and-investor-analysis` | Team quality, investor backing |
| `tokenomics-analysis` | Token economics, sustainability |
| `traction-metrics` | Growth, retention, unit economics |
| `social-sentiment` | Community health, sentiment |

### Technical
| Workflow | Description |
|----------|-------------|
| `technology-analysis` | Architecture, security, code quality |
| `topic-analysis` | Universal topic research |

### Quality & Content
| Workflow | Description |
|----------|-------------|
| `qa-review` | Research quality validation |
| `devil-review` | Adversarial stress-testing |
| `create-content` | Blog, X thread, TikTok/YouTube script |
| `create-image-prompt` | AI image prompt generation |

### Planning & Exploration
| Workflow | Description |
|----------|-------------|
| `create-research-brief` | Define research scope and plan |
| `open-research` | Flexible research on any topic |
| `brainstorm` | Interactive ideation session |

## Multi-Workflow Research

For comprehensive analysis, CRIF plans and coordinates multiple workflows:

```
RESEARCH PLAN: Hyperliquid Investment Analysis

PARALLEL BATCH 1:
├── product-analysis → Project Analyst
├── tokenomics-analysis → Project Analyst
├── team-and-investor-analysis → Project Analyst
└── technology-analysis → Technology Analyst

SEQUENTIAL BATCH 2:
└── competitive-analysis → Market Analyst

SYNTHESIS:
└── Investment Thesis → Orchestrator
```

## MCP Data Sources (Optional)

For real-time data, configure MCP servers. CRIF works without them — AI falls back to web search.

| Server | Data | API Key |
|--------|------|---------|
| **CoinGecko** | Prices, market cap, volume, charts | Free tier available |
| **CoinMarketCap** | Rankings, metadata, global metrics | Free tier available |
| **DeFiLlama** | TVL, revenue, yields, DEX volumes | Not required |
| **Dune** | On-chain SQL analytics | Required |
| **Exa** | Neural web search | Required |

See `references/core/mcp-servers.md` for installation details.

## Project Structure

```
crif/
├── SKILL.md                    # Entry point — AI reads this to activate
├── references/
│   ├── core/                   # Orchestrator, config, state templates, MCP
│   ├── agents/                 # 6 expert personas
│   ├── workflows/              # 19 research workflows
│   ├── components/             # Execution protocols
│   └── guides/                 # Methodology references
└── workspaces/                 # Research outputs (auto-created)
    └── {project}/
        ├── .orchestrator       # Session state
        ├── documents/          # Your source materials
        └── outputs/            # Research deliverables
```

## Customization

CRIF is pure Markdown — everything is readable and editable:

- **User settings** — `references/core/core-config.md` (name, language, timezone)
- **Workflows** — Add new workflows in `references/workflows/`
- **Agent personas** — Modify expertise in `references/agents/`
- **Output templates** — Customize report structure in each workflow's `template.md`
- **Content style** — Adjust writing standards in `references/guides/content-style.md`

## Contributing

Found issues or have suggestions? [Open an issue](https://github.com/kudodefi/crif/issues) or submit a pull request.

## License

MIT License — See LICENSE file for details.

## Credits

**Created by:** [Kudo](https://x.com/kudodefi)
**Framework Version:** 0.1.1
