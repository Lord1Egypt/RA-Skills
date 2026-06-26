# Agency Agents Router

An OpenClaw skill that discovers agents configured in `openclaw.json` and orchestrates them -- single, parallel, sequential, or DAG-style -- to handle complex tasks. Just describe what you need and the skill figures out which agents to use and how to run them.

215 agent descriptions sourced from [agency-agents-zh](https://github.com/jnMetaCode/agency-agents-zh) and [agency-agents](https://github.com/msitarzewski/agency-agents).

Skill in ClawHub [Agency Agents Router — ClawHub](https://clawhub.ai/staok/agency-agents-router)。

## Prerequisites

The agents themselves must be installed first. Follow the [agency-agents-zh setup guide](https://github.com/jnMetaCode/agency-agents-zh#%E5%BF%AB%E9%80%9F%E5%BC%80%E5%A7%8B):

```bash
git clone https://github.com/jnMetaCode/agency-agents-zh.git
cd agency-agents-zh
./scripts/convert.sh --tool openclaw   # Convert to OpenClaw format
./scripts/install.sh --tool openclaw   # Install to ~/.openclaw/
```

Restart the OpenClaw gateway `openclaw gateway restart` . Verify agents appear in `agents.list` in `~/.openclaw/openclaw.json`.

## Installation

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/Staok/agency-agents-router-skill.git
cd agency-agents-router
python3 scripts/rebuild_index.py --clone
# Restart OpenClaw gateway
```

The `--clone` flag automatically clones agency-agents-zh to `/tmp` to extract detailed descriptions from each agent's markdown frontmatter. Alternatively, use `--repo /path/to/agency-agents-zh` if the repo is already cloned locally.


Or download and use skill from ClawHub: [Agency Agents Router — ClawHub](https://clawhub.ai/staok/agency-agents-router).

## Usage

Once installed, describe your task in natural language. The skill automatically analyzes the task, selects the right agents, and orchestrates them:

```
"Review this PR for security and performance issues"
"Design a database schema for an e-commerce platform"
"Plan a Bilibili content strategy for a tech channel"
"Evaluate the feasibility of building an AI note-taking app"
```

The main agent handles orchestration -- single agent, parallel, sequential pipeline, or DAG with branches and merge points.

Explicit commands are also available:

```
/agents                        # List all agents by department
/agents engineering            # Filter by department
/agent search embedded         # Search by keyword
/agent engineering-code-reviewer Review this PR
```

## How It Works

1. `rebuild_index.py` parses `~/.openclaw/openclaw.json` to find all configured agents
2. Cross-references with agency-agents-zh README and individual agent .md files for names, descriptions, and expertise
3. Outputs `agents.json` -- the lookup table
4. SKILL.md injects agent awareness and orchestration logic into the main agent's prompt
5. Main agent uses `sessions_spawn(agentId=xxx)` to delegate and orchestrate

## Updating

```bash
# With local repo:
python3 scripts/rebuild_index.py --repo /path/to/agency-agents-zh --fetch

# Auto-clone:
python3 scripts/rebuild_index.py --clone --fetch
```

## Dependencies

- Python 3.6+
- Network access (only for `--fetch`/`--clone`, which download agency-agents-zh)

## License

MIT
