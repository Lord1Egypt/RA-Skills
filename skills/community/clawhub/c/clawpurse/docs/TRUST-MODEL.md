# ClawPurse Trust Model

This document explains how AI agents, automation systems, and individual operators can establish trust in ClawPurse wallets and verify the integrity of transactions.

## Core Principles

1. **Keys never leave the machine** – Private keys are encrypted at rest using AES-256-GCM with scrypt key derivation. The mnemonic is only shown once during wallet creation.

2. **Blockchain is the source of truth** – Local receipts are convenience artifacts; the Neutaro blockchain is the authoritative record for all transactions.

3. **Operator-configurable guardrails** – Each node can set its own safety limits (max send amounts, confirmation thresholds, destination allowlists).

4. **Full auditability** – Every send generates a structured receipt with transaction hash, block height, timestamp, and amounts.

---

## Trust Levels

| Level | Description | Use Case |
|-------|-------------|----------|
| **1. Chain-only** | Verify tx hash directly on Neutaro chain | Minimum trust bar |
| **2. Receipt + chain** | Sender shares receipt; recipient cross-checks | Recommended for automation |
| **3. Allowlist enforcement** | Only process transactions from pre-approved addresses | Higher trust environments |
| **4. Multi-signature** (future) | Multiple operators must approve large transactions | Treasury operations |

---

## How Other Nodes Can Verify a Payment

### Step 1: Obtain Transaction Details

The sender provides:
- Transaction hash (e.g., `79EC3BC17965A0987F4B7462C40B5FAC...`)
- Expected amount and recipient address
- Optional: memo and receipt JSON snippet

### Step 2: Query the Blockchain Directly

```bash
# Via REST API
curl "https://api2.neutaro.io/cosmos/tx/v1beta1/txs/<TX_HASH>"

# Or via RPC
curl "https://rpc2.neutaro.io/tx?hash=0x<TX_HASH>"
```

### Step 3: Validate Transaction Fields

Verify that the on-chain transaction matches expectations:

```json
{
  "body": {
    "messages": [{
      "@type": "/cosmos.bank.v1beta1.MsgSend",
      "from_address": "neutaro1abc...",  // ← Sender's registered wallet
      "to_address": "neutaro1def...",    // ← Your address
      "amount": [{
        "denom": "uneutaro",
        "amount": "1000000"              // ← 1.0 NTMPI (6 decimals)
      }]
    }],
    "memo": "payment for service X"
  }
}
```

### Step 4: Cross-Reference with Receipt

If the sender shares a receipt, confirm:
- `txHash` matches the on-chain transaction hash
- `height` matches the on-chain block height
- `amount` and `toAddress` match expectations

### Step 5: Record for Your Audit Trail

Store the tx hash, verified amount, and timestamp for accounting.

---

## Wallet Integrity Verification

### For Operators Running ClawPurse

**Verify keystore security:**
```bash
# Check file permissions (should be 0600 - owner read/write only)
ls -la ~/.clawpurse/keystore.enc
# Expected: -rw------- 1 user user ... keystore.enc
```

**Verify address consistency:**
```bash
# This should always return the same address
clawpurse address
```

**Verify chain connection:**
```bash
clawpurse status
# Should show: Status: 🟢 CONNECTED
```

### For Nodes Receiving Payments from ClawPurse Wallets

1. **Register the sender's address** – Add it to your local allowlist with appropriate limits
2. **Monitor the chain** – Use a block explorer or indexer to watch for incoming transactions
3. **Verify each payment** – Cross-check tx hash before processing

---

## Security Model

### What ClawPurse Protects

| Threat | Protection |
|--------|------------|
| Key theft via file access | AES-256-GCM encryption with password-derived key |
| Brute-force password attacks | scrypt with high N/r/p parameters |
| Accidental large sends | Configurable `maxSendAmount` limit |
| Sends to wrong addresses | Destination allowlist with enforcement mode |
| Unencrypted key exposure | Mnemonic shown only once at creation |

### What ClawPurse Does NOT Protect

| Threat | Operator Responsibility |
|--------|------------------------|
| Weak passwords | Use 12+ character passwords with high entropy |
| Lost mnemonic | Back up immediately after `init`; store offline |
| Malware/keyloggers | Secure the host machine |
| Social engineering | Never share mnemonic or keystore file |
| Password reuse | Use unique password for ClawPurse |

### Password Recommendations

- **Minimum**: 12 characters
- **Recommended**: 16+ characters with mixed case, numbers, symbols
- **Best**: Generated passphrase (e.g., `correct-horse-battery-staple-neutaro`)

---

## Receipt Format

Every `clawpurse send` command generates a receipt:

```json
{
  "id": "send-79EC3BC1-1770478262438",
  "type": "send",
  "txHash": "79EC3BC17965A0987F4B7462C40B5FAC0889C5D3F9DD63C72B59571987E40F7D",
  "fromAddress": "neutaro1fnpesef2y2lzt48xvtqeh4dts6ztdeuq86vgt3",
  "toAddress": "neutaro16us2fdzl8vf2lvn5tqsswajkqtelfpspxj9hvx",
  "amount": "400000",
  "displayAmount": "0.400000 NTMPI",
  "denom": "uneutaro",
  "memo": "test tx",
  "height": 13835843,
  "gasUsed": 87567,
  "timestamp": "2026-02-07T15:31:02.434Z",
  "status": "confirmed"
}
```

**Key fields for verification:**
- `txHash` – Unique identifier; query this on-chain
- `height` – Block number; confirms finality
- `status` – Should be `confirmed` after broadcast
- `memo` – Optional context for the payment

---

## Establishing Trust Between Nodes

### Scenario: Node A wants to pay Node B

1. **Node B shares their address**: `neutaro1xyz...`

2. **Node A adds to allowlist**:
   ```bash
   clawpurse allowlist add neutaro1xyz... --name "Node B" --max 100
   ```

3. **Node A sends payment**:
   ```bash
   clawpurse send neutaro1xyz... 10.0 --memo "service payment" --yes
   ```

4. **Node A shares receipt with Node B** (via secure channel)

5. **Node B verifies on-chain** and processes the payment

### Scenario: Automated Payment Processing

For programmatic verification:

```typescript
import { StargateClient } from '@cosmjs/stargate';

async function verifyPayment(
  txHash: string,
  expectedFrom: string,
  expectedTo: string,
  expectedAmountMicro: string
): Promise<boolean> {
  const client = await StargateClient.connect('https://rpc2.neutaro.io');
  const tx = await client.getTx(txHash);
  
  if (!tx) return false;
  
  // Parse and verify the MsgSend
  const msg = tx.tx.body.messages[0];
  return (
    msg.fromAddress === expectedFrom &&
    msg.toAddress === expectedTo &&
    msg.amount[0].amount === expectedAmountMicro &&
    msg.amount[0].denom === 'uneutaro'
  );
}
```

---

## Allowlist as Trust Boundary

The allowlist serves as your wallet's trust boundary:

| Policy | Behavior |
|--------|----------|
| `blockUnknown: true` | Rejects sends to addresses not in allowlist |
| `blockUnknown: false` | Warns but allows sends anywhere |
| Per-address `maxAmount` | Caps how much can go to a specific address |
| `needsMemo: true` | Requires memo for specific destinations |

**Best practice**: Start with `blockUnknown: true` (enforce mode) and explicitly add trusted counterparties.

---

## Future Trust Enhancements

- [ ] **Multi-signature support** – Require N-of-M approvals for large transactions
- [ ] **Hardware wallet integration** – Ledger/Trezor support for key storage
- [ ] **Automated verification API** – REST endpoint for receipt validation
- [ ] **Incoming payment watcher** – Monitor and alert on received funds
- [ ] **Signed receipts** – Cryptographically sign receipts for non-repudiation

---

## Summary Checklist for Operators

- [ ] Use a strong, unique password for the keystore
- [ ] Back up the mnemonic immediately after wallet creation
- [ ] Verify keystore file has 0600 permissions
- [ ] Configure `maxSendAmount` appropriate to your risk tolerance
- [ ] Enable allowlist enforcement (`blockUnknown: true`)
- [ ] Add trusted counterparties to allowlist with per-address caps
- [ ] Back up `receipts.json` periodically for audit trail
- [ ] Monitor the Neutaro chain for incoming payments
