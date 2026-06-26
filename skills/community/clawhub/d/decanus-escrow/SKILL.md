---
name: escrow-mcp
description: "Onchain dual-deposit escrow for agent-to-agent task settlement on Base L2 via MCP. Use when: creating escrow agreements, accepting work contracts, delivering work with proof, completing/releasing escrow payments, disputing escrow terms, refunding expired escrows, or checking escrow status. Triggers on: escrow, deposit, stake, settlement, arbitration, delivery proof, agent payment, onchain payment, Base L2 payment. NOT for: simple token transfers, ERC-20 swaps, NFT minting, or non-escrow payment flows."
homepage: https://github.com/decanus-labs/escrow-mcp
metadata:
  {
    "openclaw":
      {
        "emoji": "🔒",
        "requires": { "bins": ["npx"], "env": ["PRIVATE_KEY"] },
        "install":
          [
            {
              "id": "npm",
              "kind": "npm",
              "package": "@decanus-labs/escrow-mcp",
              "bins": ["escrow-mcp"],
              "label": "Install @decanus-labs/escrow-mcp (npm)",
            },
          ],
      },
  }
---

# Escrow MCP Server

Dual-deposit escrow on Base Sepolia via the `@decanus-labs/escrow-mcp` MCP server. Both buyer and seller deposit -- if the seller doesn't deliver, their stake burns.

## Start the Server

```bash
PRIVATE_KEY=0x... npx -y @decanus-labs/escrow-mcp
```

Or configure as an MCP server in `config.yaml`:

```yaml
plugins:
  entries:
    escrow:
      type: mcp
      config:
        command: npx
        args: ["-y", "@decanus-labs/escrow-mcp"]
        env:
          PRIVATE_KEY: "0x..."
```

Optional env vars: `RPC_URL` (default: `https://sepolia.base.org`), `CONTRACT_ADDRESS` (default: v2 deployment).

## Tools

### Write Tools

#### `create_escrow`
Buyer creates an escrow, depositing ETH as payment.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `seller` | string | yes | Seller's Ethereum address |
| `arbiter` | string | yes | Arbiter's Ethereum address (dispute resolver) |
| `paymentAmountEth` | string | yes | Payment in ETH (e.g. `"0.01"`) |
| `durationSeconds` | number | yes | Deadline in seconds from now |

#### `accept_escrow`
Seller accepts by depositing a stake >= the payment amount.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `escrowId` | number | yes | Escrow ID |
| `stakeAmountEth` | string | yes | Stake in ETH (must be >= payment) |

#### `deliver_work`
Seller submits delivery proof. Starts a 24h buyer review window.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `escrowId` | number | yes | Escrow ID |
| `deliveryHash` | string | yes | bytes32 hex or plain string (auto-hashed via keccak256) |

#### `complete_escrow`
Buyer approves delivery. Releases payment + seller stake to seller.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `escrowId` | number | yes | Escrow ID |

#### `dispute_escrow`
Either party raises a dispute. Arbiter must resolve.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `escrowId` | number | yes | Escrow ID |
| `reason` | string | no | Human-readable reason (stored off-chain) |

#### `refund_expired_escrow`
Anyone triggers after deadline. Buyer gets payment back, seller stake burns.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `escrowId` | number | yes | Escrow ID |

### Read Tools

#### `get_escrow`
Fetch escrow state. Returns state label, participants, amounts, deadlines (ISO + relative), delivery hash, and suggested next actions.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `escrowId` | number | yes | Escrow ID |

#### `list_escrows`
Paginated scan of recent escrows.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `limit` | number | no | Max results (default 10, max 50) |
| `state` | string | no | Filter: `AWAITING_SELLER`, `FUNDED`, `DELIVERED`, `COMPLETED`, `DISPUTED`, `REFUNDED`, `BURNED` |
| `participant` | string | no | Filter by address (buyer, seller, or arbiter) |

## Escrow States

```
AWAITING_SELLER → FUNDED → DELIVERED → COMPLETED
                    ↓          ↓
                 DISPUTED   DISPUTED
                    ↓
                 BURNED (after deadline)
```

- **AWAITING_SELLER** -- buyer deposited, waiting for seller to stake
- **FUNDED** -- both deposited, seller can deliver or deadline triggers burn
- **DELIVERED** -- seller submitted proof, 24h grace for buyer to approve or dispute
- **COMPLETED** -- buyer approved, seller received payment + stake
- **DISPUTED** -- arbiter must resolve
- **BURNED** -- deadline expired while FUNDED, buyer refunded, seller stake locked permanently

## Common Flows

### Happy path: hire an agent, pay on delivery

```
1. create_escrow(seller=0x..., arbiter=0x..., paymentAmountEth="0.01", durationSeconds=86400)
2. Seller calls: accept_escrow(escrowId=0, stakeAmountEth="0.01")
3. Seller calls: deliver_work(escrowId=0, deliveryHash="ipfs://QmProof...")
4. Buyer calls: complete_escrow(escrowId=0)
   → Seller receives 0.02 ETH (payment + stake returned)
```

### Dispute path

```
1. create_escrow(...) → accept_escrow(...)
2. Buyer or seller calls: dispute_escrow(escrowId=0, reason="Work incomplete")
   → State moves to DISPUTED, arbiter must resolve via contract
```

### Expired refund (seller no-show)

```
1. create_escrow(...) → accept_escrow(...)
2. Deadline passes with no delivery
3. Anyone calls: refund_expired_escrow(escrowId=0)
   → Buyer gets payment back, seller stake burned (locked in contract)
```

### Check status

```
get_escrow(escrowId=0)
→ Returns state, deadlines, next valid actions
```

## Notes

- All ETH amounts are strings to avoid precision issues. Use `"0.01"` not `0.01`.
- The `deliveryHash` field accepts either a raw bytes32 hex string or a plain string (which gets keccak256-hashed automatically).
- Write tool responses include `txHash` and `explorerUrl` for verification.
- Each server instance uses one signer (the `PRIVATE_KEY`). Run separate instances for buyer and seller roles.
- Currently Base Sepolia testnet only. ETH-native, not stablecoin.
