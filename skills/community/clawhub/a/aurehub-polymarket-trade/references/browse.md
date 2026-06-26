# Browse Reference

## Command

```bash
node "$POLY_SCRIPTS_DIR/browse.js" "<keyword or market slug>"
```

## Output Format

```
Market: "Will BTC reach $100k by Dec 2025?"
Status: ACTIVE | neg_risk: false
YES: 0.72 ($0.72)   bid/ask: 0.71/0.73   liquidity: $12,450
NO:  0.28 ($0.28)   bid/ask: 0.27/0.29   liquidity: $8,200
Min order: $5.00
Token IDs:
  YES: 71321045679252212...
  NO:  52114319501245915...
```

## Fields

- **Prices** — current mid-market price (0-1, where 1 = $1 payout if YES resolves)
- **bid/ask** — best bid and ask in the CLOB orderbook
- **liquidity** — approximate total market depth (bid + ask notional)
- **Min order** — minimum order size in USDC.e (from CLOB API)
- **Token IDs** — ERC-1155 token IDs used for buy/sell orders; copy these for trade commands

## neg_risk Markets

Some markets are `neg_risk: true`. These use the `neg_risk_exchange` contract instead of `ctf_exchange`. The skill handles this automatically.

## Data Sources

- Market metadata and prices: Gamma API (`gamma-api.polymarket.com/markets`)
- Orderbook and min order size: CLOB API (`clob.polymarket.com`) — public endpoints, no auth
