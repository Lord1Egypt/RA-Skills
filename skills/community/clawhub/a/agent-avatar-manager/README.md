# agent-avatar-manager

> Change your **OpenClaw Agent's avatar** in seconds — drop an image, paste a
> URL, or describe a style and let Freepik vector search find candidates for
> you.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-only-blue.svg)](https://docs.openclaw.ai)

## Why

OpenClaw Agents have an avatar saved at `~/.openclaw/workspace/avatars/` and
referenced from `IDENTITY.md`. Replacing it manually is 5 steps
(download → rename → put in the right folder → run `openclaw agents
set-identity` → update IDENTITY.md). This skill collapses it to one
sentence.

## Install

### OpenClaw

```bash
npx -y skills add Songhonglei/better-agent-skills/skills/agent-avatar-manager
```

or via clawhub:

```bash
npx -y clawhub install agent-avatar-manager
```

## Three modes

| Mode | What you say | Needs API key |
|---|---|---|
| **A. Direct image** | drop an image file in chat | ❌ |
| **B. Direct URL** | "use this https://..." | ❌ |
| **C. Auto search** | "I want a friendly cartoon avatar" | ✅ Freepik (free) |

## Get a free Freepik API key (mode C only)

1. Visit https://www.freepik.com/developers/dashboard/api-key
2. Sign up (free)
3. Copy the key
4. Paste it to the agent in chat — it auto-saves to your `TOOLS.md` for next
   time

> The Freepik free tier has a daily quota — usually plenty for personal use.

## Example session

```
You: 给我换个友善的女性卡通头像
Agent: [searches Freepik vector library]
       Here are 4 candidates 👇
       [4 inline images displayed]
You: 选 2
Agent: ✅ Avatar updated to Ashley22.jpg! Refresh to see your new look 🦋
```

## Compatibility

**OpenClaw only.** This skill relies on:
- `openclaw agents set-identity` CLI
- `~/.openclaw/workspace/avatars/` directory layout
- `IDENTITY.md` Avatar field convention
- `TOOLS.md` for API key persistence

Other agents (Claude Code / Codex / Cursor) are **not supported** in v1.0.

## License

MIT — see [LICENSE](./LICENSE).

## Related

Part of the [better-agent-skills](https://github.com/Songhonglei/better-agent-skills) collection.
