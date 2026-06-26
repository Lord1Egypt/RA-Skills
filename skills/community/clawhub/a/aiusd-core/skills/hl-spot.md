# HyperLiquid Spot Trading

## Commands
| Command | Description |
|---------|------------|
| `aiusd-core hl-spot buy --token <SYM> --amount <N> [--price P]` | Buy on HL spot |
| `aiusd-core hl-spot sell --token <SYM> --amount <N> [--price P]` | Sell on HL spot |

## Notes
- Token resolution is automatic (CLI resolves symbol to HL pair name).
- Funds must be in HL spot wallet. Transfer from perp wallet:
  `aiusd-core call genalpha_transfer_hl_usd -p '{"amount":50,"direction":"perp_to_spot"}'`
- Omit --price for market order.

## Examples
- "Buy 50 USDC of HYPE": `aiusd-core hl-spot buy --token HYPE --amount 50`
- "Sell PURR at $25": `aiusd-core hl-spot sell --token PURR --amount 100 --price 25`
