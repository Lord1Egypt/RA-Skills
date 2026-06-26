# Agenter Coder — OpenClaw Skill

Delegate coding tasks to a separate autonomous agent instead of writing code
tool-by-tool. Your context window stays clean. The sub-agent validates its
output, retries on errors, and comes back with structured JSON results.

Powered by [Agenter](https://github.com/Moonsong-Labs/agenter) — a
backend-agnostic SDK for autonomous coding agents.

## How it compares

Other ClawHub coding skills are either prompt instructions (telling your agent
*how* to code) or wrappers around a single CLI. Agenter Coder is different:

| | Prompt-based skills | Codex Conductor | Codex Orchestrator | **agenter-coder** |
|---|---|---|---|---|
| Separate agent process | No | Yes (Codex PTY) | Yes (Codex PTY) | **Yes (Python SDK)** |
| Multi-backend | N/A | Codex only | Codex only | **4 backends** |
| Programmatic validation | No | Gate scripts | No | **AST + Bandit security** |
| Budget enforcement | None | Iteration limit | None | **Cost, tokens, time, iterations** |
| Structured output | Chat text | Status files | Log scraping | **JSON with status + cost** |

The trade-off: prompt-only skills are zero-dependency and work immediately.
Agenter Coder requires `python3`, `uv`, and `pip install agenter` — more
moving parts, but you get real validation and backend portability.

## Backends

Switch between AI providers with a single flag:

| Backend | Provider | Models |
|---------|----------|--------|
| `anthropic-sdk` | Anthropic | Claude Sonnet 4, Opus 4, Haiku |
| `claude-code` | Anthropic | Claude Code's native runtime |
| `codex` | OpenAI | gpt-5.4, gpt-5.4-mini |
| `openhands` | Any | Any model via litellm |

## Installation

### From ClawHub

```bash
clawhub install agenter-coder
```

### From this repo

```bash
git clone https://github.com/Moonsong-Labs/agenter.git
cp -r agenter/integrations/openclaw ~/.openclaw/workspace/skills/agenter-coder
```

### Configuration

Add to your `openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "agenter-coder": {
        "enabled": true,
        "env": {
          "ANTHROPIC_API_KEY": "your-key-here"
        }
      }
    }
  }
}
```

Install the Python dependency:

```bash
uv pip install agenter>=0.1.2
```

Restart your OpenClaw session after installing.

## Publishing to ClawHub

Prerequisites: OpenClaw CLI installed (`curl -sSL https://openclaw.ai/install | bash`),
GitHub account (1+ week old).

```bash
# 1. Authenticate (opens browser for GitHub OAuth — one time only)
clawhub login
clawhub whoami                # verify it worked

# 2. Publish directly from the skill directory
clawhub publish ./integrations/openclaw \
  --slug agenter-coder \
  --name "Agenter Coder" \
  --version 1.0.0 \
  --tags latest

# 3. Verify
clawhub list                  # should show agenter-coder
```

Users can then install with `clawhub install agenter-coder`.

## Usage

Once installed, just ask your OpenClaw agent to code:

> "Create a FastAPI app with a health check endpoint"

> "Fix the bug in the login handler"

> "Refactor the database module to use async queries"

Or use the slash command:

> `/code Create a REST API for managing todos`

The agent automatically selects appropriate budget limits based on task complexity.

## Links

- [Agenter SDK](https://github.com/Moonsong-Labs/agenter) — The underlying coding agent SDK
- [OpenClaw](https://openclaw.ai) — The AI agent platform
