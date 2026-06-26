# Clawallex Skill

Pay for anything with USDC. Clawallex converts your stablecoin balance into virtual cards that work at any online checkout.

## Features

- **Flash Cards** — one-time use virtual cards for single payments
- **Stream Cards** — reloadable cards for subscriptions, top up with `refill`
- **Mode A** — pay from your USDC wallet balance
- **Mode B** — on-chain x402 payment for callers with self-custody wallets (agent or user) — signing is performed by the caller
- **Zero dependencies** — Python 3.9+ stdlib only

## Install

Copy the skill folder into your agent's skill directory:

```bash
git clone https://github.com/clawallex/clawallex-skill.git
```

## Quick Start

After installing the skill, just tell your Agent:

> "Sign up for Clawallex" — to create a new account via browser
>
> "Set up Clawallex" — to connect an existing account with your API keys

The Agent handles the rest.

## Manual Usage (for debugging / development)

```bash
# One-time payment
python3 scripts/clawallex.py pay --amount 50 --description "OpenAI API credits"

# Subscription
python3 scripts/clawallex.py subscribe --amount 100 --description "AWS monthly billing"

# Check balance
python3 scripts/clawallex.py wallet
```

## Commands

| Command | Description |
|---------|-------------|
| `signup` | Create a new account via browser — opens signup URL, polls for result, saves credentials |
| `signup-check` | Poll signup result using an existing token — use if `signup` polling failed |
| `setup` | Configure credentials |
| `whoami` | Check API Key binding status |
| `bootstrap` | Bind client_id to API Key |
| `pay` | Create a one-time flash card |
| `subscribe` | Create a reloadable stream card |
| `refill` | Top up a stream card |
| `wallet` | Check wallet balance |
| `recharge-addresses` | Get on-chain deposit addresses |
| `cards` | List virtual cards |
| `card-balance` | Check a card's balance |
| `batch-balances` | Check balances for multiple cards |
| `update-card` | Update card risk controls (tx limit, MCC whitelist/blacklist) |
| `card-details` | Get card details — masked PAN, expiry, balance, first/last name, delivery address, tx_limit, allowed/blocked MCC, encrypted PAN/CVV |
| `transactions` | View transaction history |
| `x402-address` | Get x402 on-chain payee address |

## For AI Agent Developers

See [SKILL.md](SKILL.md) for the full skill specification, including Mode B (x402 on-chain) flows, card data decryption, and agent integration details.

## License

MIT
