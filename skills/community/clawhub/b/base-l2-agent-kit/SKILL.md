---
awp: "0.4.0"
type: skill
name: base-l2-agent-kit
description: MCP server providing Base L2 DeFi tools for AI agents
version: 1.0.0
author: manteclaw
license: MIT
tags:
  - base
  - l2
  - defi
  - mcp
  - wallet
  - swap
  - liquidity
  - blockchain
  - ethereum
  - agent
---

# Base L2 Agent Kit

MCP server providing Base L2 DeFi tools for AI agents. Includes wallet management, token swaps, liquidity provision, price feeds, contract interaction, and flash loan arbitrage.

## What it does

- **Wallet Management**: Create, manage, and interact with Base L2 wallets
- **Token Swaps**: Execute swaps via DEX aggregators on Base
- **Liquidity Provision**: Add/remove liquidity to pools
- **Price Feeds**: Real-time token prices on Base L2
- **Contract Interaction**: Read/write to smart contracts
- **Flash Loans**: Execute flash loan arbitrage strategies

## Installation

```bash
pip install base-l2-agent-kit
```

Or run directly:
```bash
python -m base_l2_agent_kit.server
```

## Usage

### As MCP Server

```json
{
  "command": "python3",
  "args": ["-m", "base_l2_agent_kit.server"],
  "env": {
    "BASE_RPC_URL": "https://mainnet.base.org"
  }
}
```

### Available Tools

| Tool | Description | Auth Required |
|------|-------------|---------------|
| `wallet_balance` | Get wallet balance on Base | No |
| `tx_history` | Get transaction history | No |
| `send` | Send ETH/tokens | Yes |
| `swap` | Swap tokens via DEX | Yes |
| `add_liquidity` | Add liquidity to pool | Yes |
| `remove_liquidity` | Remove liquidity from pool | Yes |
| `token_price` | Get token price | No |
| `gas_price` | Get current gas price | No |
| `call_contract` | Call read-only contract | No |
| `send_contract_tx` | Send contract transaction | Yes |
| `estimate_gas` | Estimate gas for tx | No |
| `flash_loan` | Execute flash loan | Yes |

## Environment Variables

- `BASE_RPC_URL` - Base L2 RPC endpoint (default: https://mainnet.base.org)
- `WALLET_PRIVATE_KEY` - Private key for write operations (optional, uses Bankr API if not set)
- `BANKR_API_KEY` - Bankr API key for managed wallets

## Links

- **GitHub**: https://github.com/manteclaw/base-l2-agent-kit-mcp
- **PyPI**: https://pypi.org/project/base-l2-agent-kit/
- **MCP.so**: https://mcp.so/server/base-l2-agent-kit

## License

MIT
