# HyperLiquid Perpetuals

## Commands
| Command | Description |
|---------|------------|
| `aiusd-core perp long --asset <SYM> --size <N> [--leverage N] [--price P] [--tp P] [--sl P]` | Open long |
| `aiusd-core perp short --asset <SYM> --size <N> [--leverage N] [--price P] [--tp P] [--sl P]` | Open short |
| `aiusd-core perp close --asset <SYM>` | Close position (market order) |
| `aiusd-core perp deposit --amount <N>` | Deposit USDC to HL |
| `aiusd-core perp withdraw --amount <N>` | Withdraw USDC from HL |

## Defaults
- Order type: market (omit --price). Specify --price for limit.
- Leverage: HL default for the asset.

## Take-Profit / Stop-Loss
- `--tp <price>`: take-profit trigger price
- `--sl <price>`: stop-loss trigger price
- Can use both, either, or neither.

## Workflow
1. Check if HL has funds: `aiusd-core balances` (look for HyperLiquid section)
2. If insufficient: `aiusd-core perp deposit --amount <N>`
3. Place order: `aiusd-core perp long --asset ETH --size 0.1 --leverage 10`
4. CLI returns `action_required` if funds are insufficient, with deposit command in `next_steps`.

## Examples
- "Long 0.1 ETH 10x": `aiusd-core perp long --asset ETH --size 0.1 --leverage 10`
- "Short BTC at $70k": `aiusd-core perp short --asset BTC --size 0.01 --price 70000`
- "Long ETH with TP/SL": `aiusd-core perp long --asset ETH --size 0.1 --tp 2500 --sl 2000`
- "Close ETH position": `aiusd-core perp close --asset ETH`
