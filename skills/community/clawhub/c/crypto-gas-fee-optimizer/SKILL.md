---
name: crypto-gas-fee-optimizer
description: Check live gas prices across Ethereum, Base, Arbitrum, Optimism, and Polygon in one call using free public RPC endpoints (no API key required), rank chains by estimated USD transaction cost, and get a general low-traffic timing note. Built for crypto traders, DeFi users, and smart contract deployers who want to pick the cheapest chain or time before sending a transaction. Complements trading, defi, and smart contract skills by covering the operational cost side of on-chain activity — useful before bridging, swapping, claiming an airdrop, deploying a contract, or moving whale-sized positions where gas costs compound across many transactions.
compatibility: Created for Zo Computer
metadata:
  author: ssyopros.zo.computer
allowed-tools: Bash
---

# Crypto Gas Fee Optimizer

Queries live `eth_gasPrice` and `eth_getBlockByNumber` from free public RPC endpoints across five major EVM chains, converts to an estimated USD cost using live ETH/MATIC prices from CoinGecko, and ranks chains cheapest-first.

## When to use

- Deciding which chain to execute a transaction, swap, or bridge on right now
- Estimating the USD cost of a batch of transactions (e.g. an airdrop claim, NFT mint, or contract deployment) before committing
- Checking whether current gas is unusually high or low before a time-sensitive on-chain action
- Comparing gas across Ethereum, Base, Arbitrum, Optimism, and Polygon in a single call

## Commands

```bash
python3 scripts/gas_check.py                                  # All 5 chains, simple-transfer gas limit
python3 scripts/gas_check.py --chains ethereum,base            # Just the chains you care about
python3 scripts/gas_check.py --gas-limit 150000                # Price out a contract call, not just a transfer
python3 scripts/gas_check.py --json                            # Raw JSON output
```

## Output

A table (or JSON) of chain, gas price in gwei, base fee, and estimated USD cost for the given gas limit, sorted cheapest-first. Includes a timing note based on typical low-traffic UTC hours (~02:00-09:00 UTC, the US-overnight/early-Asia window) — this is a general historical pattern, not a live congestion prediction, so treat it as a rough heuristic alongside the live gas numbers, not a substitute for them.

## Notes

- Data sources: publicnode.com free RPC endpoints (Ethereum, Base, Arbitrum, Optimism, Polygon) and CoinGecko's free simple-price endpoint for USD conversion. No API keys required.
- Requests use a curl-style User-Agent header — some public RPC providers 403 the default Python User-Agent, so this is required for the script to work, not cosmetic.
- Read-only: this tool does not sign or broadcast transactions, it only estimates cost. Actual gas cost depends on your specific transaction's gas usage, which can differ from the estimate.
