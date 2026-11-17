---
name: bridge-cost-optimizer
description: Cross-chain bridge cost and time comparator for AI agents. Pulls live bridge quotes from Across, Stargate, Hop, Connext, Wormhole, and deBridge — returns the cheapest route (USD + time + hops) for a token transfer between any two EVM or non-EVM chains. No API key required for the public read endpoints. Use for: bridge comparison, cross-chain transfer, layer-bridge routing, base to arb, arb to op, eth to base, polygon bridge, USDC bridge, USDT bridge, gas-aware bridging, bridge aggregator, l2 bridge router, defi cross-chain, zk-bridge.
version: 1.0.0
author: ssyopros.zo.computer
---

# Bridge Cost Optimizer

Find the cheapest and fastest cross-chain bridge for any token+amount+source+destination.

## What this skill can do (working code, no promises)

- **Compare live quotes** from Across, Stargate, Hop, Connext, Wormhole, and deBridge public read endpoints.
- **Score** each route on: total USD cost, estimated delivery time, number of hops, and a composite "best" score.
- **Recommend** the optimal route given a user preference (`cheapest`, `fastest`, or `balanced`).
- **Filter** by token (USDC, USDT, ETH, WETH, DAI) and source/destination chain.

## What this skill cannot do (honest limits)

- It does **not** execute the bridge. It produces a recommendation and the calldata URL — you must sign and send via your own wallet.
- Quote APIs are pulled at request time; rates move. Always re-pull within 30 seconds of signing.
- Public endpoints can rate-limit. The skill has a built-in retry+timeout but no paid-tier fallback.
- Non-EVM chains are partially supported (Stargate handles Solana + some non-EVM; Wormhole covers more). The CLI defaults to EVM-only unless `--allow-non-evm` is passed.

## Install

```bash
pip install requests
```

## Usage

```bash
# Cheapest way to bridge 1000 USDC from Ethereum to Base
python scripts/bridge_optimizer.py compare --from ethereum --to base --token USDC --amount 1000

# Fastest route, prefer low time over cost
python scripts/bridge_optimizer.py compare --from arbitrum --to optimism --token ETH --amount 0.5 --prefer fastest

# All quotes, table view
python scripts/bridge_optimizer.py table --from polygon --to base --token USDC --amount 500
```

## Environment

- `BRIDGE_PREFERENCE` — default `balanced` (alternates between cheapest and fastest per call).
- `BRIDGE_TIMEOUT_SEC` — request timeout (default 10).

## Limitations to be aware of

- Bridge fee APIs do not always return USD-denominated fees; the script converts via CoinGecko's free public price endpoint.
- Some bridges (Wormhole portal) are not strictly "cheapest" — they exist for token coverage. Use them when the token isn't available on Stargate or Across.
