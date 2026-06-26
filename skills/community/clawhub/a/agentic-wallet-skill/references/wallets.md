# Wallets

View your automatically provisioned agent wallets.

## List My Wallets

```bash
GET /v1/wallets/me
```

Returns the wallet addresses associated with your current session. The proxy service automatically handles wallet creation upon your first login.

### Response

```json
{
  "ethereum": "0x44449b3F1bf100F7Eb224b9d48C43a9A7359FF8D",
  "solana": "343sfda..."
}
```

## Wallet Chain Types

### First-Class Support
- `ethereum` — EVM chains (ETH, Base, Polygon, Arbitrum, etc.)
- `solana` — Solana mainnet/devnet

### Extended Support
- `cosmos` — Cosmos ecosystem
- `stellar` — Stellar network
- `sui` — Sui blockchain
- `aptos` — Aptos blockchain
- `tron` — Tron network
- `bitcoin-segwit` — Bitcoin SegWit
- `near` — NEAR Protocol
- `ton` — TON blockchain
- `starknet` — StarkNet L2
