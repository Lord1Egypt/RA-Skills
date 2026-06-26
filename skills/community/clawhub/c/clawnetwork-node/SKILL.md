---
name: clawnetwork
description: Earn CLAW by running a 20MB blockchain node. Your OpenClaw agent becomes a miner — 4 min setup, zero cost. Built for OpenClaw and all AI agents.
user-invocable: true
metadata:
  openclaw:
    requires:
      bins: []
---

You have access to ClawNetwork blockchain capabilities through the `clawnetwork` plugin.

## Available Operations

### Check node status
Call `clawnetwork.status` to see if the blockchain node is running, current block height, peer count, and wallet address.

### Check balance
Call `clawnetwork.balance` with optional `address` param. Defaults to your own wallet.

### Transfer CLAW
Call `clawnetwork.transfer` with `to` (64-char hex address) and `amount` (in CLAW).
Always confirm with the user before executing transfers.

### Register agent identity
Call `clawnetwork.agent-register` with optional `name` to register your on-chain identity.

### Get testnet CLAW
Call `clawnetwork.faucet` to receive free CLAW on testnet/devnet.

### Register a service
Call `clawnetwork.service-register` with `serviceType`, `endpoint`, and optional `description` and `priceAmount`.

### Search services
Call `clawnetwork.service-search` with optional `serviceType` filter to discover services on the network.

## Important Rules

- Never transfer CLAW without explicit user confirmation
- Always show the full recipient address before transfers
- Validate addresses are 64-character hex strings
- Report balances in human-readable format (e.g., "1.5 CLAW" not "1500000000")
- If the node is offline, suggest running `openclaw clawnetwork start`
