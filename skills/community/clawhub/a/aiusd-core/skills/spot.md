# Spot Trading

## Commands
| Command | Description |
|---------|------------|
| `aiusd-core spot buy -b <TOKEN> -a <AMOUNT> [-q USDC] [-c solana]` | Buy token |
| `aiusd-core spot sell -b <TOKEN> -a <AMOUNT|all|50%> [-q USDC] [-c solana]` | Sell token |

## Defaults
- Quote: USDC (unless user specifies otherwise)
- Chain: solana
- Supported chains: solana, ethereum, bsc, base, arbitrum, polygon

## AIUSD
AIUSD is a centralized stablecoin (pegged 1:1 to USDT), available as user balance on any chain.

- Selling tokens for AIUSD: `aiusd-core spot sell -b SOL -q AIUSD -a all`
- Converting AIUSD to USDC: `aiusd-core spot buy -b USDC -q AIUSD -a 100`
- AIUSD can only directly buy stablecoins (USDC/USDT/USD1). For other tokens, the CLI returns `action_required` guiding a 2-step flow: AIUSD -> USDC, then USDC -> target token.
- Gas is auto-ensured before each spot trade.

## Examples
- "Buy $100 of SOL": `aiusd-core spot buy -b SOL -a 100`
- "Sell all TRUMP": `aiusd-core spot sell -b TRUMP -a all`
- "Sell 50% of ETH for AIUSD": `aiusd-core spot sell -b ETH -q AIUSD -a 50%`
- "Buy ETH on Base": `aiusd-core spot buy -b ETH -a 50 -c base`
