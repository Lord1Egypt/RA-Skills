# BridgeNode Skill & Examples

[![PyPI version](https://img.shields.io/pypi/v/bridgenode-llm.svg)](https://pypi.org/project/bridgenode-llm/)
[![Downloads](https://img.shields.io/pypi/dm/bridgenode-llm.svg)](https://pypi.org/project/bridgenode-llm/)
[![npm version](https://img.shields.io/npm/v/@bridgenode/llm.svg)](https://www.npmjs.com/package/@bridgenode/llm)
[![npm version](https://img.shields.io/npm/v/@bridgenode/mcp.svg)](https://www.npmjs.com/package/@bridgenode/mcp)
[![License: MIT-0](https://img.shields.io/badge/License-MIT--0-yellow.svg)](https://opensource.org/license/mit-0/)
[![CI](https://img.shields.io/github/actions/workflow/status/bridgenode-ai/bridgenode-skill/ci.yml)](https://github.com/bridgenode-ai/bridgenode-skill/actions)
[![BridgeNode on x402-list](https://x402-list.com/badge/bridgenode.svg)](https://x402-list.com/services/bridgenode?utm_source=badge&utm_medium=referral&utm_campaign=embed)
[![BridgeNode uptime on x402-list](https://x402-list.com/badge/bridgenode.svg?data=uptime)](https://x402-list.com/services/bridgenode?utm_source=badge&utm_medium=referral&utm_campaign=embed)
[![BridgeNode on ClawHub](https://img.shields.io/badge/ClawHub-Skill-blue)](https://clawhub.ai/bridgenode/skills/bridgenode)
[![GitHub Stars](https://img.shields.io/github/stars/bridgenode-ai/bridgenode-skill?style=social)](https://github.com/bridgenode-ai/bridgenode-skill)

Agent skill and buyer-side examples for [BridgeNode](https://bridgenode.cc) — AI inference bridge for AI agents. Pay per request with Solana USDC via [x402](https://docs.x402.org). No API keys, no registration.

> This repository contains only the **public agent skill and usage examples**. No server code.

## Why BridgeNode

| | BridgeNode | API keys (OpenAI etc.) | Other x402 gateways |
|---|---|---|---|
| **Setup** | None — pay per request | Sign up, billing, keys | Varies |
| **Auth** | x402 on-chain payment | API key (secret management) | x402 (some require third-party facilitators) |
| **Gas** | Sponsored — agent needs no SOL | — | Often agent pays gas |
| **Models** | DeepSeek, Groq — one endpoint | One provider each | Varies |
| **Refunds** | Full refund on provider failure | Credit-based | Varies |
| **Discovery** | `/v1/models` live pricing | Fixed plans | Varies |

## Quick start

```bash
# Install the skill (teaches any agent how to pay & call)
npx skills add bridgenode-ai/bridgenode-skill
```

```bash
# Or use the SDKs
pip install bridgenode-llm        # Python
npm i @bridgenode/llm             # TypeScript
npm i -g @bridgenode/mcp          # MCP server (automatic x402 payments)
```

The x402 flow is automatic in the SDKs: the first request gets a `402` with payment requirements, the agent signs a USDC transfer (fees sponsored), and the request completes as a normal OpenAI-compatible response. See `examples/` for curl, Python, TypeScript, and MCP walkthroughs.

## Install the skill

The skill teaches AI agents how to use BridgeNode: endpoints, models, pricing, and the x402 payment flow.

```bash
npx skills add bridgenode-ai/bridgenode-skill
```

## Install the SDKs

- **Python SDK:** `pip install bridgenode-llm` ([PyPI](https://pypi.org/project/bridgenode-llm)) — or the full toolkit: `pip install bridgenode`
- **CLI:** `pip install bridgenode-cli` ([PyPI](https://pypi.org/project/bridgenode-cli))
- **TypeScript SDK:** `npm i @bridgenode/llm` ([npm](https://www.npmjs.com/package/@bridgenode/llm))
- **MCP wrapper:** `npm i @bridgenode/mcp` ([npm](https://www.npmjs.com/package/@bridgenode/mcp)) — stdio MCP server with automatic x402 payments

## What's inside

- `SKILL.md` — the agent skill
- `examples/` — buyer-side examples (curl, Python, TypeScript, MCP)

## Learn more

- Website: https://bridgenode.cc
- Agent map: https://bridgenode.cc/llms.txt
- Models & pricing: https://bridgenode.cc/v1/models

## Community

- Smithery: [smithery.ai/servers/applefanaimail/bridgenode](https://smithery.ai/servers/applefanaimail/bridgenode)
- Moltbook agent profile: https://moltbook.com/u/bridgenode_eli
- Discord: https://discord.gg/HUpVKxJxhG
- X (Twitter): https://x.com/eliBNx

⭐ **Star this repo** — it helps AI agents discover BridgeNode.

## License

MIT-0