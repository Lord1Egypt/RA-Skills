# Crypto Gas Fee Optimizer

Live gas price checker across five major EVM chains (Ethereum, Base, Arbitrum, Optimism, Polygon), using only free public RPC endpoints — no API key required.

## Why

Trading, DeFi, and smart-contract skills are well covered on ClawHub, but the operational question "which chain should I use right now, and what will this actually cost me" wasn't. Gas costs compound fast for whales and active traders running many transactions.

## Usage

```bash
python3 scripts/gas_check.py --chains ethereum,base,arbitrum,optimism,polygon
```

See `SKILL.md` for full options.

## How it works

1. Sends `eth_gasPrice` (and `eth_getBlockByNumber` for base fee) to publicnode.com's free RPC endpoint for each requested chain.
2. Fetches live ETH and MATIC USD prices from CoinGecko's free simple-price endpoint.
3. Converts gas price × gas limit into an estimated USD cost per chain.
4. Sorts cheapest-first and adds a general timing note based on typical low-traffic UTC hours.

## Limitations

- The timing note is a general historical pattern (US-overnight / early-Asia UTC hours tend to be quieter), not a live congestion forecast — always check the live gas numbers, don't rely on the note alone.
- Actual transaction cost depends on the gas your specific transaction consumes; the script estimates using a gas-limit you supply (default 21000, a simple transfer).
- Public RPC endpoints can occasionally rate-limit or have brief downtime; the script reports per-chain errors rather than failing the whole run.
