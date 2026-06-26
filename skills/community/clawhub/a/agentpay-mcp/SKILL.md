---
name: agentpay-mcp
description: MCP server that gives AI agents the ability to make payments, manage budgets, and handle billing -- directly from Claude Desktop, Cursor, Cline, or any MCP-compatible agent runtime.
version: 1.0.0
author: up2itnow
tags:
  - mcp
  - payments
  - crypto
  - usdc
  - ai-agents
  - billing
  - autonomous-trading
  - polygon
metadata:
  openclaw:
    requires:
      bins:
        - node
      env:
        - AGENT_PRIVATE_KEY
        - RPC_URL
---

# AgentPay MCP

Payment layer for AI agents via Model Context Protocol. AgentPay MCP gives your AI agent the ability to make payments, track spending, and manage payment channels -- without leaving the agent runtime.

Works with Claude Desktop, Cursor, Cline, Windsurf, and any MCP-compatible environment.

## What It Does

- **Make payments:** Send USDC on Polygon directly from agent tool calls
- **Budget management:** Hard spending limits enforced per-session and per-day
- **Payment channels:** Open Handshake58-style channels for sub-cent micropayments
- **CCTP bridge:** Cross-chain USDC settlement (Ethereum, Base, Polygon, Arbitrum)
- **Non-custodial:** Agent holds its own keys -- no third-party custody

## Installation

```bash
npm install -g agentpay-mcp
```

Add to your MCP config (`~/.config/claude/mcp.json` or equivalent):

```json
{
  "mcpServers": {
    "agentpay": {
      "command": "agentpay-mcp",
      "env": {
        "AGENT_PRIVATE_KEY": "0x...",
        "RPC_URL": "https://polygon-rpc.com",
        "MAX_TX_USDC": "25",
        "MAX_DAILY_USDC": "500"
      }
    }
  }
}
```

## Tools Exposed

| Tool | Description |
|---|---|
| `pay` | Send USDC to an address (enforces spend limits) |
| `check_balance` | Query agent wallet balance |
| `get_spending` | Current session and daily spend totals |
| `open_channel` | Open a micropayment channel (Handshake58 compatible) |
| `pay_channel` | Issue a signed payment voucher (zero gas) |
| `close_channel` | Settle and reclaim unused channel funds |
| `bridge_usdc` | Cross-chain USDC via CCTP |

## Usage Example

In Claude Desktop with AgentPay MCP configured:

> "Pay 5 USDC to 0xABC...123 for the API call results"

The agent calls `pay(to="0xABC...123", amount=5, token="USDC")`. If within limits, it executes immediately. If over limits, it returns a request for human approval.

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `AGENT_PRIVATE_KEY` | Yes | Agent's signing key (0x-prefixed) |
| `RPC_URL` | Yes | Polygon JSON-RPC endpoint |
| `MAX_TX_USDC` | No | Per-transaction limit in USDC (default: 25) |
| `MAX_DAILY_USDC` | No | Daily spending limit in USDC (default: 500) |

## GitHub

https://github.com/AI-Agent-Economy/agentpay-mcp

## License

MIT
