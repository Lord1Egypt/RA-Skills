# AgentClear Skill for OpenClaw

> Give your AI agent the ability to discover, call, and pay for any API — with natural language.

## What is AgentClear?

[AgentClear](https://agentclear.dev) is the commerce layer for AI agents. Think **Stripe + DNS for autonomous tools**: semantic discovery, per-call micro-payments, and trust-scored APIs.

Your agent describes what it needs → AgentClear finds the right API → your agent calls it → billed per use.

## Install

Copy the `SKILL.md` file into your OpenClaw skills directory:

```bash
# From your OpenClaw workspace
mkdir -p skills/agentclear
curl -o skills/agentclear/SKILL.md https://raw.githubusercontent.com/dwflickinger/agentclear-skill/main/SKILL.md
```

Or clone the repo:

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/dwflickinger/agentclear-skill.git agentclear
```

Then restart your OpenClaw gateway.

## Get an API Key

1. Go to [agentclear.dev/login](https://agentclear.dev/login)
2. Sign in with GitHub
3. Get your `axk_` API key — comes with **$5 free credits**

Set it in your environment:
```bash
export AGENTCLEAR_API_KEY="axk_your_key_here"
```

## What Your Agent Can Do

Once installed, your OpenClaw agent can:

- **Discover APIs** — "Find me an API that parses invoices from PDFs"
- **Call services** — Proxy requests through AgentClear with automatic billing
- **Browse the marketplace** — List all available services
- **Chain services** — Use one API's output as another's input

## Example

```
You: "I need to extract data from this QuickBooks file"

Agent: *discovers qb-parser service on AgentClear*
Agent: *calls it via proxy for $0.005*
Agent: "Here's the parsed data: ..."
```

## Pricing

- Services: $0.001 – $1+ per call (provider-set)
- Platform fee: 2.5%
- New accounts: **$5 free credits**

## Links

- 🌐 [agentclear.dev](https://agentclear.dev)
- 📖 [API Docs](https://agentclear.dev/docs)
- 🏗️ [Bounty Board](https://agentclear.dev/bounties) — see what agents are searching for
- 🐙 [GitHub](https://github.com/dwflickinger/agentclear)
