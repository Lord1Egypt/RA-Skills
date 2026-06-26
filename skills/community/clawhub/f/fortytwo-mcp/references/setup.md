# Setup & Wallet Configuration

## Wallet Setup

Provide the key via environment variable — never paste it into chat:
```bash
export evm_private_key="0x..."
```

Use a dedicated low-value wallet. Generate a new EVM wallet, transfer a few dollars of USDC on Base or Monad, and use it exclusively for Fortytwo.

Default public RPC endpoints:
- **Base** (chainId 8453): `https://mainnet.base.org`
- **Monad** (chainId 143): `https://rpc.monad.xyz`

Known USDC contract addresses:
- **Base**: `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`
- **Monad**: `0x754704Bc059F8C67012fEd69BC8A327a5aafb603`

## Pricing — Pay-Per-Token via x402 Escrow

Fortytwo Prime uses [x402](https://www.x402.org/) with an escrow contract for pay-per-token billing:

1. The 402 challenge returns an `amount` — this is the **escrow deposit ceiling**, not the price. It gets locked in an on-chain escrow contract.
2. Prime processes your query. Only tokens actually consumed are charged. See [Prime pricing](https://platform.fortytwo.network/prime) for current rates.
3. When the session closes, unused funds are **refunded automatically** via the escrow contract.

A simple query costs cents. A deep analysis costs more. You never pay more than you use.

**Errors are not charged.** If the server returns an error (JSON-RPC error or non-2xx upstream), the reservation is cancelled — no cost to the user.

## Preflight

Run `python scripts/preflight.py` to verify everything is ready.
Expected output: wallet address, USDC balance, and READY/NOT READY status.
