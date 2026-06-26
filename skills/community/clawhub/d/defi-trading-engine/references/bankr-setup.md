# Bankr CLI Setup Guide

## Installation

```bash
npm install -g @bankr/cli
```

## Authentication

```bash
bankr login
# Enter email and API key when prompted
# Get API key at https://bankr.bot
```

Config saved to `~/.bankr/config.json`.

## Fund Your Wallet

After login, get your wallet address:

```bash
bankr balance
```

Transfer ETH to your EVM address on Base chain. Minimum recommended: 0.1 ETH ($200+) for testing.

**Funding options:**
- Bridge from Ethereum mainnet via <https://superbridge.app>
- Transfer from Coinbase (supports Base natively)
- Bridge from other L2s

## Key Commands

| Command | Description |
|---------|-------------|
| `bankr balance` | Show all token balances |
| `bankr swap <amount> <from> <to>` | Market swap |
| `bankr limit <amount> <from> <to> --price <price>` | Limit order |
| `bankr stop <amount> <token> --stop-price <price>` | Stop-loss order |
| `bankr trailing-stop <amount> <token> --trail <pct>` | Trailing stop |
| `bankr dca <total> <token> --interval <mins> --splits <n>` | Dollar cost average |
| `bankr twap <amount> <token> --duration <mins>` | Time-weighted average |
| `bankr price <token>` | Check token price |
| `bankr trending` | Show trending tokens |

## Supported Chains

- **Base** (primary, recommended for low fees)
- Ethereum mainnet
- Polygon
- Solana (separate SOL address)
- Unichain

## Tips

- Always test with small amounts first ($5-10 swaps)
- Base has ~$0.01 gas fees — ideal for frequent trading
- Use `--dry-run` flags in scripts before live execution
- Monitor at <https://basescan.org> using your wallet address
