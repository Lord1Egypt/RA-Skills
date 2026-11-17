---
name: agentgates-wallet
description: "Pair an Agentgates wallet over MCP (OAuth) and act under owner-approved grants: read balances, propose sends, swaps and earn moves; the owner approves every money move."
---

# Agentgates Wallet over MCP: the agent proposes, the owner approves

Pair an Agentgates wallet with OAuth and act under owner-approved grants:
read balances, propose sends, swaps and earn moves. Every money move is a
proposal; the owner approves each one in their browser.

## Connect

- MCP endpoint: `https://mcp.agentgates.ai/api/mcp` (Streamable HTTP; also
  served at `https://agentgates.ai/mcp`). OAuth 2.0 with PKCE and dynamic
  client registration; the owner consents in the browser.
- Scopes: `wallet:read`, `wallet:propose:send`, `wallet:propose:earn`,
  `wallet:propose:swap`.
- How agents authenticate here: https://agentgates.ai/auth.md

## From a terminal

`agentgates login` pairs once. Then `agentgates balance`,
`agentgates send <amount> <asset> --to <address>`, `agentgates swap`,
`agentgates earn supply|withdraw` and `agentgates history`. Each money
move opens the owner's browser for approval.
