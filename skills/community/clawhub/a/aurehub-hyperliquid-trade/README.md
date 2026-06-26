# hyperliquid-trade

Trade spot and perpetual futures on [Hyperliquid](https://hyperliquid.xyz) directly from your AI coding assistant.

## Prerequisites

- Node.js >= 20.19.0
- xaut-trade installed with WDK wallet setup completed (`~/.aurehub/.wdk_vault`)
- USDC deposited on Hyperliquid (via [app.hyperliquid.xyz](https://app.hyperliquid.xyz))

> **Unified Account Mode**: If enabled in Hyperliquid settings (default), spot USDC is automatically available as perp margin — no manual transfer needed. If disabled, transfer USDC to the perp account via the Hyperliquid UI before trading perps.

## Installation

```bash
npx skills add aurehub/skills
# Select hyperliquid-trade in the prompt
```

## First-time setup

hyperliquid-trade shares your WDK wallet with xaut-trade — no separate wallet creation needed.

Install xaut-trade first if you haven't already:
```bash
npx skills add aurehub/skills   # select xaut-trade, complete wallet setup
```

Then install hyperliquid-trade and say to your AI assistant:

> "Set up Hyperliquid"

The assistant will configure `~/.aurehub/hyperliquid.yaml` and verify your wallet.

## Usage examples

```
Buy 0.1 ETH spot
Sell 0.001 BTC spot
Open long ETH 0.1 with 5x leverage cross margin
Short BTC 0.01 with 10x isolated margin
Close my ETH position
Check my Hyperliquid balance
```

## Configuration

`~/.aurehub/hyperliquid.yaml` (auto-created from template):

```yaml
network: mainnet
api_url: https://api.hyperliquid.xyz

risk:
  confirm_trade_usd: 100   # trades below this execute without prompting
  large_trade_usd: 1000    # trades at or above this require double confirmation
  leverage_warn: 20        # leverage at or above this shows an extra warning
  slippage_pct: 5          # IOC market order slippage budget (%; does not affect GTC limit orders)
```

## Security

- Private key never stored in plaintext — WDK vault uses PBKDF2 + XSalsa20-Poly1305 encryption
- Trades at or above `confirm_trade_usd` (default $100) require explicit confirmation; trades below show a preview and execute automatically
- Runtime `PRIVATE_KEY` environment variable is rejected
