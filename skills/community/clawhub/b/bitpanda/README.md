# Bitpanda Skill

A read-only OpenClaw skill for monitoring your Bitpanda crypto portfolio, wallet balances, and trade history.

## Features

- 📊 **Portfolio Summary** — grouped overview of all holdings (crypto/fiat/index)
- 💰 **Wallet Balances** — non-zero wallets with current balances
- 📜 **Trade History** — filter buy/sell trades with limits
- 🪙 **Asset Lookup** — current price + your balance for any asset

> **Note:** Assets in Bitpanda Earn/Staking are not exposed by the API and won't appear in balances.

## Setup

1. Generate an API key at [Bitpanda Account Settings](https://web.bitpanda.com/my-account/apikey)
   - Recommended scopes: **Balance**, **Trade**, **Transaction**
2. Either set an environment variable:
   ```bash
   export BITPANDA_API_KEY="your_api_key_here"
   ```
   Or save it to a credentials file (auto-detected):
   ```bash
   mkdir -p ~/.openclaw/credentials/bitpanda
   echo '{"api_key": "your_api_key_here"}' > ~/.openclaw/credentials/bitpanda/config.json
   chmod 600 ~/.openclaw/credentials/bitpanda/config.json
   ```

## Usage

```bash
bitpanda portfolio                    # Portfolio summary
bitpanda wallets                      # Non-zero wallet balances
bitpanda transactions --limit 20      # Recent trades
bitpanda transactions --flow buy      # Buy trades only
bitpanda asset BTC                    # Price + balance for an asset
```

## API Endpoints Used

- `GET /v1/wallets` — Crypto wallet balances
- `GET /v1/fiatwallets` — Fiat wallet balances
- `GET /v1/asset-wallets` — All wallets grouped by type
- `GET /v1/trades` — Trade history
- `GET /v1/ticker` — Current prices (public, no auth)

## Security

- **Read-only** — cannot make trades or transfers
- API key stays local (env var or credentials file)
- All requests over HTTPS

## Requirements

- `curl`, `jq`, `bc`
- Bitpanda API key

## License

MIT
