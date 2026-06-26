# ICCF & ICMF Cross-Chain Communication Reference

## Table of Contents

- [Overview: ICCF vs ICMF](#overview-iccf-vs-icmf)
- [ICCF (Inter-Chain Confirmation Facility)](#iccf)
- [ICMF (Inter-Chain Messaging Facility)](#icmf)
- [Cross-Chain Asset Transfers](#cross-chain-asset-transfers)
- [Configuration](#configuration)
- [Common Mistakes](#common-mistakes)

---

## Overview: ICCF vs ICMF

| Feature | ICCF | ICMF |
|---|---|---|
| **Model** | Client-driven proof | Event-based pub/sub |
| **Scope** | Cross-cluster (different dapp clusters) | Within or across clusters |
| **Mechanism** | Client constructs proof, submits to target chain | Source emits events; target subscribes and polls |
| **Delivery** | No guarantee (client can fail, must retry) | Eventual delivery guaranteed, ordered |
| **Speed** | Faster (client-driven) | Asynchronous (waits for anchoring) |
| **Use case** | Asset transfers, proving a tx occurred | Messaging, state sync, notifications |

**Rule of thumb**: Use ICCF when you need to prove a specific transaction happened (asset transfers). Use ICMF when you need async data exchange between chains (event notifications, state sync).

---

## ICCF

### How It Works

1. User submits transaction on **source chain**
2. Source chain confirms tx in a block
3. Block is anchored to the **Cluster Anchoring Chain**
4. Anchoring chain validates and includes the block
5. **Client** constructs cryptographic proof of the transaction
6. Client submits proof to **target chain** as a new transaction
7. Target chain validates the proof via anchoring hierarchy

The user/client drives the entire process — it is not automatic.

### Configuration

Add the ICCF GTX module to `chromia.yml`:

```yaml
blockchains:
  my_dapp:
    module: main
    config:
      gtx:
        modules:
          - "net.postchain.d1.iccf.IccfGtxModule"
```

### Client-Side Proof Construction (TypeScript)

```typescript
import { createClient, createIccfProofTx } from "postchain-client";

const client = await createClient({
  nodeUrlPool: "<url>",
  managementBlockchainRid: "<management-brid>",
});

const { iccfTx, verifiedTx } = createIccfProofTx(
  client,
  txToProveRid,       // Buffer: RID of the tx to prove
  txToProveHash,      // Buffer: hash of the tx
  txToProveSigners,   // Pubkey[]: signers of the original tx
  sourceBlockchainRid,
  targetBlockchainRid
);

// Add the operation that needs the proof to iccfTx
// The iccf_proof operation is automatically included
// Sign and send iccfTx to the target chain
```

### Cross-Chain Transfer Flow (FT4 + ICCF)

FT4 asset transfers across chains use ICCF under the hood:

1. **`init_transfer`** on source chain — locks/burns assets
2. **`apply_transfer`** on target chain — requires `iccf_proof` operation to verify source tx
3. If expired: **`cancel_transfer`** + **`unapply_transfer`** to return funds

Key concepts:
- **Internal assets**: Minted on the local chain
- **External assets**: Used locally but minted on a different chain
- **Origin chain**: The chain from which an asset can be received
- Assets must be registered on both source and target chains before transfer

---

## ICMF

### How It Works

ICMF is event-based, pub/sub messaging:

1. **Source chain** posts a message to a **topic**
2. **Target chain** subscribes to that topic
3. Target chain polls the source for new events
4. Events are verified using the anchoring hierarchy
5. Target chain processes verified events

Communication channels:
- **Omnidirectional**: Source posts to topic, any chain can subscribe
- **Multidirectional**: All chains subscribe and listen to each other

### Typical Flow (Asset Transfer via ICMF)

1. User submits asset transfer request on chain B
2. Chain B validates tx, records in ledger, updates balances
3. Chain A queries chain B for events directed to chain A
4. Chain A verifies the authenticity of the transfer event
5. Chain A updates balances based on verified data

### Key Difference from ICCF

- ICMF: The **chain** does the work automatically (polls, verifies, processes)
- ICCF: The **client** does the work (constructs proof, submits)

---

## Cross-Chain Asset Transfers

### Key Operations

| Operation | Description |
|---|---|
| `init_transfer` | Start transfer on source chain. Locks/burns assets. |
| `apply_transfer` | Complete transfer on target chain. Requires ICCF proof. |
| `cancel_transfer` | Cancel an expired transfer on target chain. |
| `unapply_transfer` | Reverse a cancelled transfer on previous chains. |
| `recall_transfer` | Recall unclaimed transfer if recipient account doesn't exist. |

### Asset Registration (Required)

Before cross-chain transfers, register the asset on both chains:

```rell
// On the receiving chain — register the external asset
operation register_external_asset(
  name: text,
  symbol: text,
  decimals: integer,
  origin_chain_rid: byte_array,
  icon_url: text
) {
  require_admin();
  assets.Unsafe.register_asset(
    name, symbol, decimals, origin_chain_rid, icon_url, "ft4"
  );
}
```

---

## Configuration

### ICCF Config in chromia.yml

```yaml
blockchains:
  source_chain:
    module: source_module
    config:
      gtx:
        modules:
          - "net.postchain.d1.iccf.IccfGtxModule"
  target_chain:
    module: target_module
    config:
      gtx:
        modules:
          - "net.postchain.d1.iccf.IccfGtxModule"
```

### ICMF Config

ICMF configuration is handled at the cluster level. Chains within the same cluster can communicate via ICMF by default when properly configured in the directory chain.

---

## Common Mistakes

1. **Missing ICCF GTX module**: Forgetting to add `IccfGtxModule` to `gtx.modules` in config → proof verification fails.
2. **Asset not registered on target chain**: Cross-chain transfer fails silently if the asset isn't registered on the receiving chain.
3. **Not handling expired transfers**: If `apply_transfer` is not called within the expiry window, use `cancel_transfer` + `unapply_transfer` to recover funds.
4. **Confusing ICCF and ICMF**: ICCF is client-driven (you build proofs). ICMF is chain-driven (automatic polling). Choose the right one.
5. **Trying ICMF across clusters**: ICMF works within and across clusters, but ICCF is typically used for cross-cluster asset transfers via FT4.
