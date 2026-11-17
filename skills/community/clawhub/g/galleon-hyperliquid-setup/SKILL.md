---
name: hyperliquid-setup
description: "Connect an agent's available tools to Hyperliquid workflows and complete a first public market read. Use when installing this pack, asking how to get started, diagnosing missing data or tools, or checking whether analysis, account monitoring, planning, or execution is available. Setup does not authorize trading or configure private keys."
license: MIT
compatibility: "Any Agent Skills harness. Public reads need HTTP access or Node.js 20+. Account work needs a user-provided public account address; execution needs a separately configured trusted signer."
metadata:
  version: "0.4.0"
  protocol: "hyperliquid"
---

# Hyperliquid setup

Take a new agent from installed instructions to a verified first read and a precise next step.

## Tool selection

When connecting or choosing tools, read [official tools](references/official-tools.md). Reuse a suitable maintained upstream capability before implementing new integration code; tool adoption stays optional and never supplies wallet authority.

## First task and connected workflow

Inventory real tool capabilities and complete one public market read without account credentials. Read [agent integration and handoffs](references/agent-integration.md) on first use or when a tool or related skill is missing.

## Workflow

1. Inventory the tools actually exposed by the harness: browser/HTTP, shell/Node, account reads, unsigned ticket building, signer submission, and reconciliation. Do not assume a named MCP server or wallet exists because a skill mentions it.
2. Read [connections and first-run procedure](references/connections.md). Select mainnet or testnet explicitly. Public market analysis needs no wallet or secret. Reuse the user's environment choice; ask only if it changes the task.
3. Run one public read for the exact requested market. From this skill's own directory, run `node scripts/market-snapshot.mjs --coin ETH --network mainnet`, substituting the requested market. Without a shell, use the two documented HTTP requests. Do not use a fixture as current evidence.
4. Validate network, coin, metadata precision, book freshness, and response coverage. Report mark/oracle price, spread, reported funding, observation time, and limitations. Missing data is unavailable, not zero. A successful public read establishes analysis access only.
5. Map requested workflows to [capabilities and handoffs](references/agent-integration.md). For account reads, request the public user/subaccount address; never substitute an API wallet address. For execution, require an existing trusted signer with the documented capabilities. Never handle secrets or approve an API wallet during setup.
6. Produce a readiness record: network, exact tool names, operations each tool supports, evidence, missing capabilities, available workflows, and one next action. Route to the appropriate installed skill; if absent, use the local handoff contract or offer its explicit installation command.

## Completion

The first read must have a dated result or an explicit diagnostic failure. Setup is complete when the agent can name what it can do now and what remains unavailable. It is not proof of a connected account, complete trading integration, or authority to act.
