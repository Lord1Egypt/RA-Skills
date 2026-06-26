---
name: edge
description: >
  Use when user asks about crypto tokens, trading, portfolios, or price alerts.
---

# Edge

Tools via `edge` MCP server (6 tools, 39 actions):

- **intelligence**: search tokens, screen by filters, list top tokens, trending swaps
- **tokens**: token details, pricing, top holders, top traders, dev tokens (sniper/insider flags)
- **pairs**: pair metrics, OHLCV candles, swaps, pair info
- **wallet**: holdings, swaps, PnL history, summary
- **orders**: `place_limit_order`, `place_spot_order`, list/cancel orders, entry/exit strategies
- **agent**: encrypted wallet management for the non-custodial flow

## Patterns

1. **Price before order**: `pairs pair_metrics` to compute target, then `orders place_limit_order`
2. **Token to pair**: `tokens token_info_with_pricing` returns `pairContractAddress`
3. **Chain IDs**: `8453` Base, `1` Ethereum, `42161` Arbitrum, `"solana"` Solana
4. **Alerts**: configure in the Edge webapp (Settings > Alerts); deliver to webhook, Redis, or Telegram

[Docs](https://edge-trade.gitbook.io/agents)
