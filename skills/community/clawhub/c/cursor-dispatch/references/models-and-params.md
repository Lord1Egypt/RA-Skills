# Models and Parameters Reference

## Available Models (as of 2026-03-06)

### OpenAI GPT Series
| Model ID | Tier | Notes |
|----------|------|-------|
| `gpt-5.3-codex-xhigh` | Extra High | Top tier, most capable |
| `gpt-5.3-codex-xhigh-fast` | Extra High Fast | Speed variant |
| `gpt-5.3-codex-high` | High | |
| `gpt-5.3-codex-high-fast` | High Fast | |
| `gpt-5.3-codex` | Standard | Good balance |
| `gpt-5.3-codex-fast` | Standard Fast | |
| `gpt-5.3-codex-low` | Low | Budget option |
| `gpt-5.3-codex-low-fast` | Low Fast | |
| `gpt-5.3-codex-spark-preview` | Preview | Spark variant |
| `gpt-5.2-codex-xhigh` | Extra High | |
| `gpt-5.2-codex-xhigh-fast` | Extra High Fast | |
| `gpt-5.2-codex-high` | High | |
| `gpt-5.2-codex-high-fast` | High Fast | |
| `gpt-5.2-codex` | Standard | Reliable workhorse |
| `gpt-5.2-codex-fast` | Standard Fast | |
| `gpt-5.2-codex-low` | Low | |
| `gpt-5.2-codex-low-fast` | Low Fast | |
| `gpt-5.2` | Base | Non-codex variant |
| `gpt-5.2-high` | High | |
| `gpt-5.1-codex-max` | Max | Legacy top tier |
| `gpt-5.1-codex-max-high` | Max High | |
| `gpt-5.1-codex-mini` | Mini | Lightweight |
| `gpt-5.1-high` | High | |

### Anthropic Claude Series
| Model ID | Notes |
|----------|-------|
| `opus-4.6-thinking` | Default (auto), deep reasoning |
| `opus-4.6` | Without thinking |
| `opus-4.5-thinking` | Previous gen thinking |
| `opus-4.5` | Previous gen |
| `sonnet-4.6-thinking` | Lighter thinking |
| `sonnet-4.6` | Fast, capable |
| `sonnet-4.5-thinking` | Previous gen |
| `sonnet-4.5` | Previous gen |

### Other
| Model ID | Notes |
|----------|-------|
| `gemini-3.1-pro` | Google latest |
| `gemini-3-pro` | Google |
| `gemini-3-flash` | Google fast |
| `grok` | xAI |
| `kimi-k2.5` | Moonshot |
| `composer-1.5` | Cursor native |
| `composer-1` | Cursor native legacy |

## All CLI Parameters

```
cursor agent [options] [prompt...]

Options:
  -v, --version                 Version number
  --api-key <key>               API key (or CURSOR_API_KEY env)
  -H, --header <header>         Custom header (repeatable)
  -p, --print                   Non-interactive mode
  --output-format <format>      text | json | stream-json
  --stream-partial-output       Stream deltas (with stream-json)
  -c, --cloud                   Cloud/composer mode
  --mode <mode>                 plan | ask
  --plan                        Shorthand for --mode=plan
  --resume [chatId]             Resume session
  --continue                    Continue last session
  --model <model>               Model selection
  --list-models                 List models and exit
  -f, --force / --yolo          Auto-approve all
  --sandbox <mode>              enabled | disabled
  --approve-mcps                Auto-approve MCP servers
  --trust                       Trust workspace (headless)
  --workspace <path>            Working directory
  -w, --worktree [name]         Git worktree isolation
  --worktree-base <branch>      Worktree base branch

Subcommands:
  ls                            List resumable sessions
  resume                        Resume latest session
  create-chat                   Create empty chat
  models                        List available models
  about                         System/account info
  mcp                           Manage MCP servers
  login / logout                Authentication
  status / whoami               Auth status
  generate-rule / rule          Create cursor rule
  update                        Update CLI
```

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `CURSOR_API_KEY` | API authentication |
