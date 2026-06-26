# claude-code-switchboard

A Claude Code skill for managing Telegram message routing in OpenClaw. Switch between Claude CLI backends and API providers with simple commands.

## Install

```bash
# Copy the skill to your Claude Code skills directory
cp SKILL.md ~/.claude/skills/telegram-routing/SKILL.md
```

Then use `/telegram-routing` in any Claude Code session.

## Commands

```
/telegram-routing status       # Show current routing config
/telegram-routing model opus   # Switch primary model
/telegram-routing logs         # Show recent message processing logs
/telegram-routing fallback     # Switch to lightweight API mode
/telegram-routing restore      # Restore default CLI-based routing
```

## How it works

Messages flow through the OpenClaw Gateway → configured model provider → appropriate backend:

- **CLI providers** (`claude-cli/opus`, `claude-cli/sonnet`): Use local Claude Code with full tool access
- **API providers** (`anthropic/claude-haiku-4-5`, `openai/gpt-4.1-mini`): Direct API calls, faster but no tools

Config lives in `~/.openclaw/openclaw.json` under `agents.defaults`.

## Model shortcuts

| Shorthand | Resolves to |
|-----------|-------------|
| `opus` | `claude-cli/opus` |
| `sonnet` | `claude-cli/sonnet` |
| `haiku` | `anthropic/claude-haiku-4-5` |

## Requirements

- [OpenClaw](https://openclaw.ai) with Telegram channel enabled
- Claude Code CLI

## License

MIT
