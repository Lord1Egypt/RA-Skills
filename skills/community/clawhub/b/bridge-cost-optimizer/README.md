# Bridge Cost Optimizer

A Python CLI for AI agents that need to pick the cheapest / fastest cross-chain bridge at quote time. No API key required.

## Why this exists

ClawHub search for "bridge" returns mostly chat bridges (Feishu, channel, A2H), not crypto cross-chain bridges. Search for "l2 bridge" returns nothing. Search for "arbitrage" returns price arbitrage, not bridge arbitrage. So an agent that needs to move USDC from Ethereum to Base has no good tool to pick the cheapest bridge on the marketplace.

This skill fills that gap.

## Capabilities (verified working)

| Command | What it does |
|---|---|
| `compare` | Picks the best bridge for a route, prints summary |
| `table` | Prints every quote as a sortable table |

## Bridges consulted

- **Across** (across.to) — fast optimistic bridge, often cheapest for popular pairs
- **Stargate** (LayerZero) — deep liquidity, good for stablecoins
- **Hop** (hop.exchange) — old but reliable for L2 <-> L1
- **Connext** (connext.network) — modular, low fee
- **Wormhole** — broadest chain coverage
- **deBridge** (debridge.finance) — DLN, competitive on exotic pairs

## Quick start

```bash
pip install requests
python scripts/bridge_optimizer.py compare --from ethereum --to base --token USDC --amount 1000
```

## What it does NOT do

- It does not sign or send transactions.
- It does not custody funds.
- It is not a router that aggregates; it queries each bridge's public quote endpoint in parallel and picks the best.

## Files

- `SKILL.md` — the agent-facing manifest
- `scripts/bridge_optimizer.py` — the CLI

## License

MIT
