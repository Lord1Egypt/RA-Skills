# AdaptlyPost Agent Skill 📬

Schedule and manage social media posts across 9 platforms — Instagram, X (Twitter), Bluesky, TikTok, Threads, LinkedIn, Facebook, Pinterest, and YouTube — from a single API. AdaptlyPost is a SaaS tool: no self-hosting required.

This repo ships one skill in two layouts so it works with both **OpenClaw** and **Hermes Agent**:

- `SKILL.md` (repo root) — picked up by OpenClaw
- `skills/adaptlypost/SKILL.md` — standard layout for Hermes taps and installs

## Prerequisites

1. Sign up at [adaptlypost.com](https://adaptlypost.com/signup)
2. Go to **Settings → API Tokens** and generate a **dedicated, revocable** token for your agent
3. Connect only the social accounts the agent actually needs

## Install — OpenClaw

Install as usual from ClawHub, or point OpenClaw at this repo. Set the API key in your OpenClaw environment:

```bash
export ADAPTLYPOST_API_KEY="adaptly_your-token-here"
```

## Install — Hermes Agent

Add this repo as a tap (Hermes discovers the skill under `skills/`):

```bash
hermes skills tap add adaptlypost/adaptlypost-openclaw
hermes skills install adaptlypost
```

Or install directly:

```bash
hermes skills install adaptlypost/adaptlypost-openclaw/skills/adaptlypost
```

The skill declares `ADAPTLYPOST_API_KEY` in `required_environment_variables`, so the Hermes CLI prompts for it securely on first load and injects it into terminal sandboxes automatically.

> **Using Hermes through Telegram/Discord/WhatsApp?** Messaging platforms never prompt for secrets. Set the key on the host first via `hermes setup` or in `~/.hermes/.env`.

> **Note:** prefer the tap/repo install over a single-file `SKILL.md` URL install — URL installs don't download the `references/` docs (platform configs, full API reference).

## Alternative: MCP server

Hermes Agent (and any MCP client) can also connect to the hosted AdaptlyPost MCP server instead of using this skill — typed tools, no curl:

```json
{
  "mcpServers": {
    "adaptlypost": {
      "type": "http",
      "url": "https://mcp.adaptlypost.com/mcp",
      "headers": { "Authorization": "Bearer adaptly_your_key" }
    }
  }
}
```

See [adaptlypost/adaptlypost-mcp](https://github.com/adaptlypost/adaptlypost-mcp) for details.

## Repo layout / contributing

```
.
├── SKILL.md                       # canonical skill (OpenClaw reads this)
├── references/                    # platform configs + API reference
└── skills/
    └── adaptlypost/
        ├── SKILL.md               # synced copy (Hermes reads this)
        └── references/            # synced copy
```

`SKILL.md` at the repo root is the **canonical source**. After editing it (or `references/`), sync the Hermes copy before committing:

```bash
cp SKILL.md skills/adaptlypost/SKILL.md
rm -rf skills/adaptlypost/references && cp -R references skills/adaptlypost/references
```

## License

MIT
