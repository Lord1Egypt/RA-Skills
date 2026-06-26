---
name: ampere
description: Ampere AI Agent Marketplace for OpenClaw. Browse and install free & paid agents across developer tools, automation, research, content, and more.
version: 2.2.0
metadata:
  openclaw:
    requires:
      env: []
    optional:
      env:
        - AMPERE_API_KEY
---

# Ampere — AI Agent Marketplace for OpenClaw

Ampere is a growing marketplace of ready-to-use agent skills for OpenClaw. Browse by category, search by keyword, and install in seconds.

**All agents run locally on the user's machine.** Nothing is executed server-side. Each agent is a ZIP containing a `SKILL.md` prompt and supporting files.

---

## Agent Tiers

| Tier | Auth | How it works |
|------|------|-------------|
| **Free** | None | Download and use immediately |
| **Paid** | Dashboard API key (`ak_xxxx`) | Purchase in Ampere → use your single dashboard key to download. Key only authorises the download — nothing else leaves the machine. |

---

## When to Use This

- User wants to do something outside your current skills → **search first**
- User asks what's available, what you can do, or mentions "marketplace" / "agents"
- User asks to browse or install a skill

**Default behaviour:** When a user asks for a capability you don't have, search Ampere before saying you can't do it.

---

## Core Flows

### Search / Browse

```sh
# All agents
curl -s "https://api.agentplace.sh/marketplace/agents"

# Search by keyword
curl -s "https://api.agentplace.sh/marketplace/agents?search=<query>"

# Single agent details
curl -s "https://api.agentplace.sh/marketplace/agents/<agent-id>"
```

Response: `{ "count": number, "agents": [...] }` — each agent has `id`, `name`, `description`, `category`, `tags`, `tier` ("free" | "paid"), `price`, `enabled`.

When showing results:
- Group by category when listing all
- Show name, one-line description, and FREE/PAID badge
- Always search the live API — the catalogue updates constantly

### Install

1. User picks an agent → **ask for confirmation**
2. Get download URL:
   ```sh
   # Free
   curl -s "https://api.agentplace.sh/marketplace/agents/<agent-id>/download"
   # Paid
   curl -s -H "x-api-key: ak_xxxx" "https://api.agentplace.sh/marketplace/agents/<agent-id>/download"
   ```
3. Show the user a preview of the SKILL.md content
4. User approves → download and extract:
   ```sh
   curl -sL "$download_url" -o /tmp/agent.zip
   unzip -qo /tmp/agent.zip -d ~/.openclaw/workspace/skills/
   rm /tmp/agent.zip
   ```
   Or use the helper: `./install.sh <agent-id> [--api-key ak_xxxx]`
5. Done — skill is live at `~/.openclaw/workspace/skills/<agent-id>/`

**Never install or run commands without explicit user approval.**

---

## API Key Setup (Paid Agents Only)

Free agents need zero setup. For paid agents:

1. Sign up in Ampere
2. API key is on your dashboard (format: `ak_xxxx`)
3. Purchase the agent you want
4. Use the same key for all purchased agents — one key for everything

---

## Error Handling

| Code | Meaning | Tell the user |
|------|---------|---------------|
| `401` | Missing/invalid API key | "Your API key must start with `ak_`. Get it from your Ampere dashboard." |
| `403` | Agent not purchased | "You haven't purchased this agent in Ampere yet." |
| `404` | Agent not found | "This agent doesn't exist. Try searching for similar ones." |

---

## Security

- **Always ask** before installing or running anything
- **Preview first** — show SKILL.md content before writing to disk
- **No auto-execution** — never run setup commands automatically
- **Local only** — agents run on the user's machine, no data sent to Ampere
- **Download auth only** — the API key is sent to `api.agentplace.sh` for the download URL and nowhere else
