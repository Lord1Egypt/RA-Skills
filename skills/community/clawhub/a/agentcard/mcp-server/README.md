# @asgcard/mcp-server

MCP Server for [ASG Card](https://asgcard.dev) — give AI agents autonomous virtual card management via x402 protocol on Stellar.

## What is this?

This MCP server allows AI agents (Claude, Cursor, etc.) to create, fund, and manage virtual debit cards **fully autonomously** — no human-in-the-loop. Cards are paid with USDC on-chain via the x402 protocol.

## Tools

| Tool | Description |
|---|---|
| `create_card` | Create a new virtual card (pays on-chain via x402) |
| `fund_card` | Fund an existing card with more USDC |
| `list_cards` | List all cards for your wallet |
| `get_card` | Get card summary (balance, status) |
| `get_card_details` | Get card number, CVV, expiry (sensitive) |
| `freeze_card` | Temporarily freeze a card |
| `unfreeze_card` | Re-enable a frozen card |
| `get_pricing` | View available tier pricing |

## Setup

### Claude Code

```bash
claude mcp add asgcard -- node /path/to/mcp-server/dist/index.js \
  --env STELLAR_PRIVATE_KEY=S...
```

### Claude Desktop / Cursor

Add to your MCP config file (`~/.cursor/mcp.json` or Claude Desktop settings):

```json
{
  "mcpServers": {
    "asgcard": {
      "command": "npx",
      "args": ["-y", "@asgcard/mcp-server"],
      "env": {
        "STELLAR_PRIVATE_KEY": "YOUR_STELLAR_SECRET_KEY"
      }
    }
  }
}
```

### Manual (from source)

```bash
cd mcp-server
npm install
npm run build

STELLAR_PRIVATE_KEY=S... node dist/index.js
```

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `STELLAR_PRIVATE_KEY` | ✅ | — | Stellar secret key (S...) for signing x402 payments and wallet auth |
| `ASGCARD_API_URL` | ❌ | `https://api.asgcard.dev` | ASGCard API endpoint |
| `STELLAR_RPC_URL` | ❌ | `https://mainnet.sorobanrpc.com` | Soroban RPC for transaction submission |

## How it works

```
AI Agent (Claude / Cursor)
    ↕ stdio (MCP protocol)
@asgcard/mcp-server
    ↕ @asgcard/sdk (x402 create/fund)
    ↕ wallet-auth HTTP (list/get/freeze/unfreeze)
ASGCard API (api.asgcard.dev)
    ↕ x402 on Stellar (USDC)
4Payments → Visa/Mastercard Network
```

The server uses your Stellar private key to:
1. **Sign x402 payments** for card creation and funding (autonomous on-chain)
2. **Sign wallet-auth requests** for card management operations

## Security

- Your private key never leaves the local process
- All x402 payments require on-chain USDC — no credit risk
- Wallet-auth uses ed25519 signatures with 5-min timestamp windows
- Card details are encrypted at rest on the server (AES-256)

## License

MIT
