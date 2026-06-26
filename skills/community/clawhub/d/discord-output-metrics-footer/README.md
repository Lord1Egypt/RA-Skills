# Discord Output Metrics Footer

Compact runtime telemetry for OpenClaw Discord responses.

This skill installs an OpenClaw extension that appends a one-line footer under Discord outputs showing context usage, output tokens, live/cached Codex quota, model used, and optional subagent token aggregate.

```text
_🟢 ↑54k ↓157 · 21%ctx · 5h 89% · kimi-k2.6:cloud_
```

With subagents:

```text
_🟢 ↑54k ↓157 · 21%ctx · 5h 89% · openai-codex/gpt-5.5 · sub ↑31k ↓4k_
```

## What it shows

- `↑54k`: input/context tokens used for the turn.
- `↓157`: assistant output tokens for the turn.
- `21%ctx`: current context window usage.
- `5h 89%`: live/cached OpenAI Codex short-window quota remaining.
- `kimi-k2.6:cloud`: model used for the turn.
- `sub ↑31k ↓4k`: optional best-effort aggregate of nearby subagent usage.

## Color status

- `🟢`: context under 50% and quota over 50%.
- `🟡`: context 50-80% or quota 20-50%.
- `🔴`: context over 80% or quota under 20%.

If context and quota disagree, the footer shows the worse status.

## Install

Install this skill into your OpenClaw workspace, then copy the bundled extension template:

```bash
mkdir -p ~/.openclaw/extensions/discord-output-metrics-footer
cp -R assets/extension-template/* ~/.openclaw/extensions/discord-output-metrics-footer/
```

Add the plugin to `~/.openclaw/openclaw.json`:

```json
{
  "plugins": {
    "allow": ["discord-output-metrics-footer"],
    "load": {
      "paths": ["~/.openclaw/extensions/discord-output-metrics-footer"]
    },
    "entries": {
      "discord-output-metrics-footer": {
        "enabled": true,
        "config": {
          "cacheMs": 120000,
          "quotaCacheMs": 60000,
          "contextReserveTokens": 40000,
          "appendSubagents": true,
          "disabledConversations": []
        }
      }
    }
  }
}
```

Validate and restart:

```bash
openclaw config validate
openclaw gateway restart
```

## Channel deployment

The extension works for any Discord channel. Use `disabledConversations` to suppress the footer in specific Discord channel IDs.

Recommended:

- Enable in work channels such as `#general`, `#coding`, `#reasoning`, and audit channels.
- Disable in status-only or incident channels such as `#feed` and `#system` if you want less noise.

## Configuration

| Field | Default | Purpose |
| --- | --- | --- |
| `cacheMs` | `120000` | Window for matching recent LLM output and subagent output. |
| `quotaCacheMs` | `60000` | Minimum interval between Codex quota refreshes. |
| `contextReserveTokens` | `40000` | Safety reserve for context calculations. |
| `appendSubagents` | `true` | Append `sub ↑x ↓y` when nearby subagent usage is detected. |
| `disabledConversations` | `[]` | Discord channel IDs where no footer should be appended. |

## Privacy

The extension must never print:

- OAuth tokens.
- API keys.
- Email addresses.
- Auth profile names.
- Local auth file paths.

If Codex quota cannot be fetched, the footer omits the quota field rather than blocking delivery.

## Files

```text
discord-output-metrics-footer/
├── SKILL.md
├── README.md
├── assets/
│   └── extension-template/
│       ├── index.ts
│       ├── openclaw.plugin.json
│       └── package.json
└── references/
    └── implementation.md
```

## Publish to ClawHub

```bash
clawhub publish . --slug discord-output-metrics-footer --name "Discord Output Metrics Footer" --version 0.1.0 --changelog "Initial skill with bundled OpenClaw extension template"
```

## License

MIT

