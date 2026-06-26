---
name: check-balance
description: >
  Check USDC balance across networks (Base, Solana). Use when the user
  wants to check balance, see how much USDC is available, view funds,
  or verify wallet balance. Covers "check my balance", "how much do I have",
  "show funds", "wallet balance".
user-invocable: true
disable-model-invocation: false
allowed-tools:
  - "Bash(npx agnic@latest status*)"
  - "Bash(npx agnic@latest balance*)"
---

# Checking USDC Balance

Use `npx agnic@latest balance` to check USDC balance across supported networks.

## Authentication

Run `npx agnic@latest status --json` to verify. If not authenticated:
- **Headless (CI/server/agent)**: Set `AGNIC_TOKEN` env var or pass `--token <token>`
- **Interactive (has browser)**: Run `npx agnic@latest auth login`

See the `authenticate-wallet` skill for details.

## Command Syntax

```bash
npx agnic@latest balance [--network <network>] [--json]
```

## Options

| Option             | Description                               |
| ------------------ | ----------------------------------------- |
| `--network <name>` | Filter by network (default: all networks) |
| `--json`           | Output result as JSON                     |

## Supported Networks

| Network         | Description            |
| --------------- | ---------------------- |
| `base`          | Base mainnet (primary) |
| `base-sepolia`  | Base testnet           |
| `solana`        | Solana mainnet         |
| `solana-devnet` | Solana devnet          |

## Examples

```bash
# Check balance on all networks
npx agnic@latest balance --json

# Check balance on Base mainnet only
npx agnic@latest balance --network base --json
```

## Expected Output

```
Network       Balance      Address
base          125.50 USDC  0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb7
base-sepolia    0.00 USDC  0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb7
solana          0.00 USDC  N/A
solana-devnet   0.00 USDC  N/A
```

## Error Handling

Common errors:

- "Not authenticated" -- Run `npx agnic@latest auth login` or set `AGNIC_TOKEN`
- Network timeout -- Try again or specify a single network with `--network base`
