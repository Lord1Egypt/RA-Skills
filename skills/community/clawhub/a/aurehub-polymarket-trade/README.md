# polymarket-trade

Trade on Polymarket prediction markets on Polygon. Non-custodial — private key stays in your WDK vault.

## Quick Start

**Prerequisites:**
- Node.js ≥ 18
- **xaut-trade skill installed and set up first** — it creates the WDK wallet vault (`~/.aurehub/.wdk_vault`) that this skill requires. Run `npx skills add aurehub/skills` and select `xaut-trade`, then complete its setup before using polymarket-trade.
- POL on Polygon for gas (≥ 0.01 POL)

**1. Install**

```bash
npx skills add aurehub/skills   # select both xaut-trade and polymarket-trade
```

**2. Start trading** — the Agent will check prerequisites and prompt you to run any missing setup steps:

```
What are the current odds on bitcoin markets?
```

---

## Usage

Just talk to the Agent in natural language:

### Browse Markets

```
What are the current odds on bitcoin markets?
Browse prediction markets about the US election
What are the odds on Trump winning?
```

### Buy Shares

```
Buy $10 of YES on the bitcoin 100k market
Buy $5 of NO on will Trump win
```

### Sell Shares

```
Sell my YES shares on the bitcoin market
Sell 5 NO shares on the election market
```

### Check Balance & Positions

```
Check my Polymarket balance
Show my open positions
```

## Trade Flow

```
Browse market → Preview (price, shares, cost) → [Confirmation if needed] → Auto-swap POL→USDC.e if required → Submit order → Result
```

If your USDC.e balance is insufficient, the Agent will offer to auto-swap POL → USDC.e before placing the order.

## Safety Gates

| Amount | Action |
|--------|--------|
| < $50 | Proceeds automatically |
| $50–$499 | Single confirmation required |
| ≥ $500 | Double confirmation required |

Hard-stops: POL gas < 0.01, market CLOSED, amount below minimum order size.

## Geo-restriction

Polymarket blocks users in the US, UK, Singapore, and [other regions](https://docs.polymarket.com/polymarket-learn/FAQ/geoblocking). If you see a **403 Forbidden** error, enable a VPN with a supported country node and retry.

## Configuration

### `~/.aurehub/.env`

| Variable | Description | Example |
|----------|-------------|---------|
| `POLYGON_RPC_URL` | Polygon JSON-RPC endpoint | `https://polygon.drpc.org` |

### `~/.aurehub/polymarket.yaml`

Key adjustable parameters:

```yaml
polymarket:
  clob_url: https://clob.polymarket.com
  gamma_url: https://gamma-api.polymarket.com

safety:
  warn_threshold_usd: 50       # Single-confirm threshold (USD)
  confirm_threshold_usd: 500   # Double-confirm threshold (USD)
```

## Security & Privacy

| Service | When | Data Sent |
|---------|------|-----------|
| Polymarket Gamma API | Browse / resolve markets | Search query |
| Polymarket CLOB API | Order submission | Signed order, wallet address |
| Polygon RPC | Balance checks, on-chain txs | Wallet address, transaction data |
| Uniswap V3 (Polygon) | POL → USDC.e swap | Transaction data |

All API calls use HTTPS. Private key never leaves the local WDK vault.
