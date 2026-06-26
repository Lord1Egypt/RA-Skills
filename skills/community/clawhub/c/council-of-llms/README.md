# Council of LLMs

Multi-model council deliberation for OpenClaw. Spawn 3 parallel subagents with different models and perspectives, then synthesize their outputs into a unified verdict.

## Why This Exists

Single-model "councils" — where one subagent roleplays 3 experts — fail repeatedly. They produce context overflow (300-600k tokens), shallow analysis, and empty outputs. Real deliberation requires genuinely different models providing independent perspectives.

## How It Works

1. **Spawn 3 parallel subagents**, each with a different model:
   - **Strategos** (kimi-k2.6) — strategy, business impact, feasibility
   - **Analyticos** (deepseek-v4-pro) — data quality, technical correctness, edge cases
   - **Creativos** (gemma4:31b) — creative alternatives, UX, novel approaches

2. **Each agent analyzes independently** with their specific lens

3. **Synthesize** — merge verdicts into consensus, disagreements, blind spots, and action items

## Quick Start

```python
# Spawn all 3 in parallel
sessions_spawn(model="kimi-k2.6:cloud", label="Council-Strategos", ...)
sessions_spawn(model="deepseek-v4-pro:cloud", label="Council-Analyticos", ...)
sessions_spawn(model="gemma4:31b-cloud", label="Council-Creativos", ...)

# Wait for all 3 to complete, then synthesize
```

## Critical Rules

- **Paste ALL context inline** — agents have no conversation history
- **Keep task descriptions under 2000 words** — longer = context overflow = failure
- **Use `lightContext: true`** — always
- **Set `runTimeoutSeconds: 900`** — councils need time
- **Wait for ALL 3 to complete** — don't synthesize early

## Configuration

Models are read from `~/.openclaw/council-config.json`:

```json
{
  "council_models": [
    "ollama/kimi-k2.6:cloud",
    "ollama/deepseek-v4-pro:cloud",
    "ollama/gemma4:31b-cloud"
  ],
  "default_timeout": 900,
  "max_tokens": 8192
}
```

## Companion Skill

- **[Subagent Orchestration](https://github.com/wahajahmed010/subagent-orchestration)** — Core delegation patterns, sandbox constraints, timeout strategy, and failure mode reference. Council of LLMs builds on these patterns for multi-agent deliberation.

## Install

```bash
# Install both skills together
clawhub install council-of-llms
clawhub install subagent-orchestration

# Or from GitHub
openclaw skills install wahajahmed010/council-of-llms
openclaw skills install wahajahmed010/subagent-orchestration
```

## ClawHub

Published at: https://clawhub.com/skills/council-of-llms

## License

MIT-0