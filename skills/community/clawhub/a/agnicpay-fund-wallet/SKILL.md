---
name: fund-wallet
description: >
  Get instructions for funding your Agnic wallet with USDC. Use when the
  user wants to add funds, deposit USDC, top up, or needs more balance.
  Covers "add funds", "deposit", "top up", "fund my wallet",
  "how do I get USDC", "need more balance".
user-invocable: true
disable-model-invocation: false
allowed-tools:
  - "Bash(npx agnic@latest status*)"
  - "Bash(npx agnic@latest address*)"
  - "Bash(npx agnic@latest balance*)"
---

# Funding the Agnic Wallet

Provide instructions for adding USDC to the user's Agnic wallet on Base.

## Authentication

Run `npx agnic@latest status --json` to verify. If not authenticated:
- **Headless (CI/server/agent)**: Set `AGNIC_TOKEN` env var or pass `--token <token>`
- **Interactive (has browser)**: Run `npx agnic@latest auth login`

See the `authenticate-wallet` skill for details.

## Get Wallet Address

```bash
npx agnic@latest address
```

## Funding Options

### Option 1: Agnic Dashboard (Recommended)

1. Go to [app.agnic.ai](https://app.agnic.ai)
2. Sign in with the same account used in the CLI
3. Navigate to the dashboard
4. Use the **"Add Funds"** button to add USDC via card or on-chain funding

### Option 2: Direct USDC Transfer

Send USDC directly to the wallet address on **Base network**:

1. Get the address: `npx agnic@latest address`
2. From any wallet (MetaMask, Coinbase, Phantom, etc.), send USDC on **Base** to that address
3. Verify arrival: `npx agnic@latest balance --network base`

**Important**: Send USDC on **Base network** only. USDC on other chains (Ethereum mainnet, Arbitrum, etc.) will not appear in the balance.

### Option 3: Bridge from Another Chain

If the user has USDC on Ethereum, Arbitrum, or Optimism, they can bridge to Base using:
- [bridge.base.org](https://bridge.base.org) (official Base bridge)
- Any cross-chain bridge that supports Base

## Verify Balance

After funding, confirm the deposit arrived:

```bash
npx agnic@latest balance --network base
```

## Important Notes

- Agnic wallets use **USDC** (not ETH) for payments
- **Base network** is the primary chain
- Minimum recommended balance: **$1.00 USDC** for testing
- Small amounts of ETH on Base may be needed for gas (auto-handled in most cases)

## Error Handling

Common errors:

- "Not authenticated" -- Run `npx agnic@latest auth login` or set `AGNIC_TOKEN`
- Balance shows 0 after transfer -- Verify the transfer was on Base network (not Ethereum mainnet)
- Transfer pending -- Base transactions typically confirm in 2-3 seconds
