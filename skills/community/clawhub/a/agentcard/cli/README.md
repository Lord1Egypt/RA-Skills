# @asgcard/cli

Command-line interface for [ASG Card](https://asgcard.dev) — manage virtual MasterCard cards for AI agents from your terminal.

## Install

```bash
npm install -g @asgcard/cli
```

## Quick Start

```bash
# 1. Configure your Stellar wallet
asgcard login

# 2. View pricing
asgcard pricing

# 3. Create a $10 card
asgcard card:create -a 10 -n "AI Agent" -e agent@example.com

# 4. List your cards
asgcard cards
```

## Commands

| Command | Description |
|---------|-------------|
| `asgcard login [key]` | Save your Stellar secret key |
| `asgcard whoami` | Show your wallet address |
| `asgcard cards` | List all your cards |
| `asgcard card <id>` | Get card summary |
| `asgcard card:details <id>` | Get PAN, CVV, expiry |
| `asgcard card:create` | Create a card (x402 payment) |
| `asgcard card:fund <id>` | Fund a card (x402 payment) |
| `asgcard card:freeze <id>` | Freeze a card |
| `asgcard card:unfreeze <id>` | Unfreeze a card |
| `asgcard pricing` | View pricing tiers |
| `asgcard health` | Check API status |

## Authentication

The CLI authenticates using your Stellar private key. Two options:

1. **Interactive login** (recommended):
   ```bash
   asgcard login
   # Enter key when prompted → saved to ~/.asgcard/config.json (0600)
   ```

2. **Environment variable**:
   ```bash
   export STELLAR_PRIVATE_KEY=S...
   asgcard cards
   ```

## Card Creation

```bash
# Available amounts: 10, 25, 50, 100, 200, 500
asgcard card:create --amount 50 --name "Shopping Agent" --email agent@co.com

# ✅ Card created!
#   card_abc123
#   Name:    Shopping Agent
#   Balance: $50
#   Status:  ● active
#
# 🔒 Card Details (one-time):
#   Number: 5395 78** **** 1234
#   CVV:    123
#   Expiry: 12/2027
#
#   TX: abc123...def456
```

## Configuration

Config is stored in `~/.asgcard/config.json` with `0600` permissions.

```bash
# Custom API URL
asgcard login --api-url https://custom-api.example.com

# Custom Stellar RPC
asgcard login --rpc-url https://custom-rpc.example.com
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `STELLAR_PRIVATE_KEY` | Stellar secret key (overrides config) |
| `ASGCARD_API_URL` | Custom API URL |
| `STELLAR_RPC_URL` | Custom Stellar RPC URL |

## License

MIT
