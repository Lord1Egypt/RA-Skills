# Agent Maker

Intelligent toolkit for creating autonomous AI agents for [OpenClaw](https://openclaw.ai).

Unlike a simple script runner, Agent Maker **guides you through a discovery process** — clarifying your agent's purpose, personality, workflow, tools, channels, automation, and security before generating a fully configured workspace.

## Features

- **Guided Discovery Flow** — Interview-style process to understand what you really need
- **Complete Workspace Generation** — SOUL.md, AGENTS.md, IDENTITY.md, TOOLS.md, USER.md, HEARTBEAT.md
- **Smart Model Recommendations** — Suggests the right model based on your workload
- **Autonomy Tiers** — Configure read-only, active, or fully proactive agents
- **Tool Policy** — Fine-grained allow/deny lists for agent tools
- **Heartbeat & Cron** — Built-in periodic monitoring and scheduled tasks
- **Sandbox Support** — Security isolation for untrusted environments
- **Channel Bindings** — Route WhatsApp, Telegram, Discord, Slack to specific agents
- **Multi-Agent Coordination** — Inter-agent communication via sessions

## Installation

### Prerequisites
- [OpenClaw](https://openclaw.ai) installed and configured
- Node.js/npm via nvm (for OpenClaw)
- `jq` for JSON processing

### Install Skill

```bash
# Clone the repo
git clone https://github.com/itsahedge/agent-maker.git
cd agent-maker

# Copy to OpenClaw skills directory
cp -r . ~/.openclaw/skills/agent-maker/

# Enable skill in config
openclaw gateway config.patch --raw '{
  "skills": {
    "entries": {
      "agent-maker": {"enabled": true}
    }
  }
}'
```

## Quick Start

### Option 1: Guided Creation (Recommended)

Just tell your OpenClaw agent what you need:

> "I want to create a research agent that does competitive analysis"

The agent-maker skill will guide you through:
1. **Purpose & Identity** — Name, emoji, specialty, model selection
2. **Personality & Behavior** — Communication style, autonomy level, boundaries
3. **Workflow & Tools** — What triggers the agent, what tools it needs
4. **Channels** — How users interact with it (WhatsApp, Telegram, etc.)
5. **Automation** — Heartbeat monitoring, cron schedules, memory management
6. **Security** — Sandbox mode, tool restrictions

### Option 2: Direct Script

```bash
scripts/create-agent.sh \
  --name "Watson" \
  --id "watson" \
  --emoji "🔬" \
  --specialty "Deep research and competitive analysis" \
  --model "anthropic/claude-opus-4-6" \
  --workspace "$HOME/agents/watson" \
  --personality "Thorough, analytical, cites sources" \
  --autonomy "tier2" \
  --tools-deny "exec,image_generate" \
  --heartbeat-every "30m" \
  --heartbeat-active-hours "08:00-22:00" \
  --sandbox "off"
```

## What Gets Created

```
agents/watson/
├── SOUL.md              # Personality, purpose, guidelines
├── AGENTS.md            # Operating instructions & rules
├── IDENTITY.md          # Name, emoji, vibe
├── TOOLS.md             # Tool access notes & conventions
├── USER.md              # User context
├── HEARTBEAT.md         # Periodic check instructions
├── memory/
│   └── 2026-03-24.md   # Initial memory log
└── skills/              # Agent-specific skills (optional)
```

Plus gateway configuration:
- Agent entry in `agents.list`
- Model, identity, sandbox, tools policies
- Heartbeat configuration (if enabled)

## Script Reference

### create-agent.sh

**Required:**
| Argument | Description |
|----------|-------------|
| `--name` | Agent display name |
| `--id` | Agent ID (lowercase, hyphenated) |
| `--emoji` | Agent emoji |
| `--specialty` | One-line description of what the agent does |
| `--model` | LLM to use (`provider/model-name`) |
| `--workspace` | Path to agent workspace |

**Optional:**
| Argument | Default | Description |
|----------|---------|-------------|
| `--personality` | Professional & helpful | Communication style and traits |
| `--boundaries` | Safe defaults | What the agent should NOT do |
| `--workflow` | Generic 5-step flow | Step-by-step workflow |
| `--tools-allow` | (all) | Comma-separated list of allowed tools |
| `--tools-deny` | (none) | Comma-separated list of denied tools |
| `--autonomy` | `tier2` | `tier1` (read-only), `tier2` (active), `tier3` (proactive) |
| `--heartbeat-every` | (disabled) | Heartbeat interval (e.g., `30m`, `1h`) |
| `--heartbeat-target` | `none` | Where to deliver alerts (`last`, `none`, channel) |
| `--heartbeat-active-hours` | (always) | Active window (e.g., `08:00-22:00`) |
| `--sandbox` | `off` | Sandbox mode (`off`, `non-main`, `all`) |

## Autonomy Tiers

| Tier | Mode | Description |
|------|------|-------------|
| `tier1` | Read-only & Draft | Observes, analyzes, proposes. Does not execute. |
| `tier2` | Active Execution | Can read, write, search, act. Confirms before high-impact actions. |
| `tier3` | Fully Proactive | Operates autonomously on schedules and standing orders. |

## Model Recommendations

| Use Case | Model | Why |
|----------|-------|-----|
| Deep research, complex reasoning | `anthropic/claude-opus-4-6` | Most capable |
| General tasks, balanced | `anthropic/claude-sonnet-4-6` | Best cost/quality ratio |
| Fast responses, high volume | `anthropic/claude-haiku-4-5` | Fastest, cheapest |
| Multimodal (images) | `google/gemini-2.5-flash` | Strong image capabilities |
| Budget coding tasks | `deepseek/deepseek-chat` | Cost-effective |

## Examples

**Research agent (deep analysis):**
```bash
scripts/create-agent.sh \
  --name "Watson" --id "watson" --emoji "🔬" \
  --specialty "Deep research and competitive analysis" \
  --model "anthropic/claude-opus-4-6" \
  --workspace "$HOME/agents/watson" \
  --autonomy "tier2" \
  --tools-deny "exec,image_generate"
```

**Family group bot (restricted):**
```bash
scripts/create-agent.sh \
  --name "FamilyBot" --id "family-bot" --emoji "👨‍👩‍👧‍👦" \
  --specialty "Family group assistant" \
  --model "anthropic/claude-sonnet-4-6" \
  --workspace "$HOME/agents/family-bot" \
  --autonomy "tier1" \
  --tools-allow "read,web_search,sessions_list" \
  --tools-deny "write,edit,exec,browser,apply_patch" \
  --sandbox "all"
```

**Health tracker (proactive):**
```bash
scripts/create-agent.sh \
  --name "Nurse Joy" --id "nurse-joy" --emoji "💊" \
  --specialty "Health tracking and medication reminders" \
  --model "anthropic/claude-sonnet-4-6" \
  --workspace "$HOME/agents/nurse-joy" \
  --autonomy "tier3" \
  --heartbeat-every "2h" \
  --heartbeat-target "last" \
  --heartbeat-active-hours "07:00-22:00"
```

**Creative agent (image generation):**
```bash
scripts/create-agent.sh \
  --name "Picasso" --id "picasso" --emoji "🎨" \
  --specialty "Image generation, editing, and visual design" \
  --model "google/gemini-2.5-flash" \
  --workspace "$HOME/agents/picasso" \
  --autonomy "tier2" \
  --tools-allow "read,write,image_generate,image,web_search,memory_search"
```

## Agent Coordination

### List Active Agents
```typescript
sessions_list({ kinds: ["agent"], limit: 10, messageLimit: 3 })
```

### Send Messages to Agents
```typescript
sessions_send({ label: "watson", message: "Research competitor X" })
```

### Spawn Sub-Agent Tasks
```typescript
sessions_spawn({
  agentId: "watson",
  task: "Deep analysis of market trends. Write report to reports/market.md",
  runTimeoutSeconds: 3600,
  cleanup: "delete"
})
```

### Channel Bindings

Route specific channels to your agent:
```bash
openclaw gateway config.patch --raw '{
  "bindings": [{
    "agentId": "watson",
    "match": { "channel": "telegram", "accountId": "watson-bot" }
  }]
}'
```

## Documentation

See [SKILL.md](./SKILL.md) for the complete discovery flow and detailed workflows.

## Community

- **OpenClaw Docs:** https://docs.openclaw.ai
- **OpenClaw Discord:** https://discord.com/invite/clawd
- **Skill Catalog:** https://clawhub.com

## Contributing

Contributions welcome! Please:
1. Fork the repo
2. Create a feature branch
3. Make your changes
4. Submit a PR with clear description

## License

MIT License - see [LICENSE](./LICENSE) file for details
