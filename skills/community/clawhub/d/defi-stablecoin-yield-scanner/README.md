# DeFi Stablecoin Yield Scanner

Finds the best current stablecoin (USDC/USDT/DAI/etc.) yields across DeFi, using the free public DeFiLlama pools API. No API key needed.

## Why

Directional crypto trading skills are everywhere. Non-directional stablecoin yield — "where can I park cash and earn the most without price risk" — is a common, distinct question that most trading-focused skills don't answer.

## Usage

```bash
python3 scripts/scan_yields.py --min-tvl 5000000 --top 10
```

See `SKILL.md` for the full command reference.

## How it works

1. Fetches all pools from `https://yields.llama.fi/pools`.
2. Filters to pools where every asset in the pool symbol is a known stablecoin (or DeFiLlama already flags it `stablecoin: true`).
3. Applies your TVL floor and APY range filters.
4. Sorts by APY descending and prints a table (or raw JSON with `--json`).

## Limitations

- Read-only: it does not execute deposits/withdrawals or manage a wallet.
- APY figures are protocol-reported; always cross-check on the protocol's own site before allocating real capital.
- Symbol-based stablecoin detection can occasionally miscategorize an obscure or de-pegged asset — treat results as a shortlist to verify, not a final answer.
