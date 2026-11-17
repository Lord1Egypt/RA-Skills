# Speed Up & Cancel Pending Transactions

Manage pending (unconfirmed) transactions by speeding them up or cancelling them.

## Critical Constraint: Only the First Pending Transaction Can Be Acted On

> **Only the transaction with nonce = confirmedNonce + 1 (i.e., the first transaction in the pending list) can be sped up or cancelled.** You cannot skip ahead and act on a later pending transaction — EVM nonces must be processed sequentially.

If a user wants to cancel or speed up a transaction that is NOT the first in the pending queue, inform them:
- They must first resolve (speed up or cancel) all preceding pending transactions in nonce order.
- Example: if pending list shows nonce 5, 6, 7 and the user wants to cancel nonce 7, they must first handle nonce 5, then 6, then 7.

---

## `wallet cancel`

Cancel a pending transaction by submitting a replacement transaction (same nonce, higher gas) that sends 0 value to yourself.

### Syntax

```bash
baw wallet cancel <txHash> [--binanceChainId <binanceChainId>] --json
```

### Parameters

| Parameter          | Required | Default | Description                                                                           |
|--------------------|----------|---------|---------------------------------------------------------------------------------------|
| `<txHash>`         | Yes      | —       | The transaction hash of the pending transaction to cancel (0x-prefixed, 66 characters) |
| `--binanceChainId` | No       | —       | Binance chain ID. Auto-detected from the original transaction if omitted              |

### Example

```bash
# Cancel a pending transaction
baw wallet cancel 0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890 --json
```

### Response

```json
{
  "success": true,
  "data": {
    "orderId": "order_123456",
    "txHash": "0x9876543210abcdef9876543210abcdef9876543210abcdef9876543210abcdef",
    "status": "SUBMITTED"
  }
}
```

| Field       | Description                                                                 |
|-------------|-----------------------------------------------------------------------------|
| `orderId`   | Internal order ID for the cancel transaction                                |
| `txHash`    | The new replacement transaction hash (not the original)                     |
| `status`    | `SUBMITTED` (broadcast success) or `SUBMIT_FAIL` (broadcast failed)         |

### Important Notes

- The cancel transaction replaces the original by using the same nonce with higher gas.
- **Only the first pending transaction (confirmed nonce + 1) can be cancelled.** Attempting to cancel a later transaction will fail.
- A `SUBMITTED` status means the cancel tx was broadcast — it does **not** guarantee the original will be replaced. The replacement is confirmed only when the cancel tx is mined.
- After cancelling, use `wallet tx-history --type pending` to verify the original transaction status changes to `REPLACED`.
- **No second confirmation required** — cancel executes immediately without app approval.

---

## `wallet speed-up`

Speed up a pending transaction by resubmitting it with higher gas fees (same payload, same nonce).

### Syntax

```bash
baw wallet speed-up <txHash> [--level <level>] [--binanceChainId <binanceChainId>] --json
```

### Parameters

| Parameter          | Required | Default | Description                                                                           |
|--------------------|----------|---------|---------------------------------------------------------------------------------------|
| `<txHash>`         | Yes      | —       | The transaction hash of the pending transaction to speed up (0x-prefixed, 66 characters) |
| `--level`          | No       | `HIGH`  | Gas bump level: `LOW` (×1.1) or `HIGH` (×1.25)                                       |
| `--binanceChainId` | No       | —       | Binance chain ID. Auto-detected from the original transaction if omitted              |

### Example

```bash
# Speed up with default HIGH level (×1.25 gas bump)
baw wallet speed-up 0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890 --json

# Speed up with LOW level (×1.1 gas bump)
baw wallet speed-up 0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890 --level LOW --json
```

### Response

```json
{
  "success": true,
  "data": {
    "orderId": "order_789012",
    "txHash": "0xfedcba0987654321fedcba0987654321fedcba0987654321fedcba0987654321",
    "status": "SUBMITTED"
  }
}
```

| Field       | Description                                                                 |
|-------------|-----------------------------------------------------------------------------|
| `orderId`   | Internal order ID for the speed-up transaction                              |
| `txHash`    | The new replacement transaction hash with higher gas                        |
| `status`    | `SUBMITTED` (broadcast success) or `SUBMIT_FAIL` (broadcast failed)         |

### Important Notes

- The speed-up transaction reuses the original transaction's payload (to, value, data) but with bumped gas fees.
- **Only the first pending transaction (confirmed nonce + 1) can be sped up.** Attempting to speed up a later transaction will fail.
- Gas bump compares with the current network gas price and takes the higher value to ensure competitiveness.
- A `SUBMITTED` status means the speed-up tx was broadcast — confirmation depends on network conditions.
- After speeding up, use `wallet tx-history --type pending` to track both the original and replacement transactions.
- **No second confirmation required** — speed-up executes immediately without app approval.

---

## Querying Pending Transactions

To view pending transactions, use the existing `wallet tx-history` command with `--type pending`:

### Syntax

```bash
baw wallet tx-history --type pending [--binanceChainId <binanceChainId>] --json
```

### Example

```bash
# List all pending transactions
baw wallet tx-history --type pending --json

# List pending transactions on a specific chain
baw wallet tx-history --type pending --binanceChainId 56 --json
```

### Response

See [wallet-view.md](wallet-view.md) for the full `tx-history` response format.

---

## Error Handling

| Error Code | Name                    | Meaning                                                                 | Suggested Action                                                                                   |
|------------|-------------------------|-------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------|
| 351727     | TARGET_NOT_FOUND        | No pending transaction found matching the given txHash                  | Run `wallet tx-history --type pending` to check current pending transactions                       |
| 351728     | ALREADY_CONFIRMED       | The transaction has already been confirmed on-chain                     | No action needed — the transaction is already finalized                                            |
| 351729     | LEVEL_INVALID           | Invalid gas bump level provided                                         | Use `LOW` or `HIGH` only                                                                           |
| 351730     | LOCKED                  | Another transaction operation is in progress                            | Wait a moment and retry                                                                            |
| 351731     | NONCE_NOT_FIRST         | This transaction is not the first in the pending queue (nonce ≠ confirmedNonce + 1) | Run `wallet tx-history --type pending` to find the earliest pending transaction and speed up or cancel that one first |
| 351732     | TX_STATUS_UNSUPPORTED   | The transaction has already failed or been dropped                      | No action needed — check `wallet tx-history` to see the final status                              |
| 351733     | CHAIN_MISMATCH          | The provided `--binanceChainId` does not match the original transaction's chain | Omit `--binanceChainId` (auto-detected) or use the correct chain ID                         |

---

## Workflow: Helping Users with Pending Transactions

When a user asks about pending transactions, speeding up, or cancelling:

1. **First, list pending transactions:**
   ```bash
   baw wallet tx-history --type pending --json
   ```

2. **If no pending transactions found:** Inform the user they have no pending transactions.

3. **If pending transactions exist:** Display them in a table format showing:
   - Transaction hash
   - Nonce
   - Chain (binanceChainId)
   - Status
   - Time submitted

4. **Identify the actionable transaction:** Only the **first** pending transaction (lowest nonce = confirmed nonce + 1) can be sped up or cancelled. Highlight it clearly to the user. If the user asks to act on a different transaction, explain that pending transactions must be resolved in nonce order — they must handle the first one before they can act on later ones.

5. **Confirm the action** with the user (speed up or cancel the first pending transaction).

6. **Execute the action:**
   - Speed up: `baw wallet speed-up <txHash> --level HIGH --json`
   - Cancel: `baw wallet cancel <txHash> --json`

7. **Report the result:** Show the new txHash and status. Remind the user to check `wallet tx-history` for confirmation.

8. **If more pending transactions remain:** After the first is resolved, repeat from step 1 to handle the next one in sequence.
