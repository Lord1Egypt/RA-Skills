# Prediction Markets (Polymarket)

## Commands
| Command | Description |
|---------|------------|
| `aiusd-core pm buy --market "<slug>" --outcome <Yes\|No> --amount <N> [--price P]` | Buy prediction shares |
| `aiusd-core pm sell --market "<slug>" --outcome <Yes\|No> --amount <N> [--price P]` | Sell prediction shares |
| `aiusd-core pm cancel --order-id <ID>` | Cancel an open order |
| `aiusd-core pm positions` | List your positions |
| `aiusd-core pm orders` | List your open orders |
| `aiusd-core pm search -q "<query>"` | Search markets |

## Notes
- Market identifier: use the slug from search results.
- Price: 0-1 range (e.g., 0.65 = 65 cents per share). Omit for market order.
- Auto-funding: if balance insufficient on buy, CLI handles it automatically (two-step flow).

## Workflow: Sell Shares
1. Check positions: `aiusd-core pm positions`
2. Sell shares: `aiusd-core pm sell --market "<slug>" --outcome Yes --amount 50 --price 0.80`

## Examples
- "Bet $10 on Yes for Bitcoin 100k": `aiusd-core pm buy --market "will-bitcoin-hit-100k" --outcome Yes --amount 10`
- "Sell my Yes shares": `aiusd-core pm sell --market "will-bitcoin-hit-100k" --outcome Yes --amount 50 --price 0.80`
- "Cancel order": `aiusd-core pm cancel --order-id <ID>`
- "Search election markets": `aiusd-core pm search -q "election"`
