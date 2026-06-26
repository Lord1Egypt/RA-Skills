# BOB Score — Proof Submission

Agents submit historical on-chain transaction proofs. BOB verifies each tx on the public ledger and awards credit. Both the sender and recipient of a transaction can submit the same proof for dual-sided credit.

## Proof types

| Type | Flag(s) | Confidence | What it proves |
|---|---|---|---|
| `btc_onchain_tx` | `--proof-type btc_onchain_tx --proof-ref <txid>` | **provisional→strong** | BTC on-chain tx confirmed (upgrades as confirmations accumulate) |
| `eth_onchain_tx` | `--proof-type eth_onchain_tx --proof-ref <txhash>` | **provisional→strong** | Ethereum mainnet on-chain tx |
| `base_onchain_tx` | `--proof-type base_onchain_tx --proof-ref <txhash>` | **provisional→strong** | Base L2 on-chain tx |
| `sol_onchain_tx` | `--proof-type sol_onchain_tx --proof-ref <txsig>` | **provisional→strong** | Solana on-chain tx |

**Confidence tiers:**
- `strong` — on-chain tx confirmed with sufficient confirmations, OR both counterparties submitted the same proof
- `medium` — single-sided proof with on-chain verification
- `provisional` — on-chain tx detected, awaiting confirmations

## Dual-sided proof submission

Both the sender and recipient of a transaction can independently submit a proof for the same on-chain tx. Each side earns credit:

- **Outbound** (`--direction outbound`, default): You sent the payment. Requires `--sender-address` for EVM proofs. The address is verified against the on-chain sender — a mismatch fails with `sender_address_mismatch`. Recommended for all chains.
- **Inbound** (`--direction inbound`): You received the payment. Requires `--recipient-address` for EVM proofs (must match a bound wallet).

When both counterparties submit the same transaction, confidence is automatically boosted from `medium` to `strong`.

Use `--counterparty-ref` to identify the other party in the transaction.

## Import historical on-chain proofs (primary flow)

Submit on-chain transactions you sent or received. BOB verifies them on the public ledger and awards credit.

```bash
# Outbound BTC — you sent the payment
bob agent credit-import <agent-id> \
  --proof-type btc_onchain_tx \
  --proof-ref <txid> \
  --rail onchain \
  --currency BTC \
  --amount <sats> \
  --direction outbound

# Inbound ETH — you received the payment
bob agent credit-import <agent-id> \
  --proof-type eth_onchain_tx \
  --proof-ref <0x...txhash> \
  --rail onchain \
  --currency ETH \
  --amount <wei> \
  --direction inbound \
  --recipient-address <your-bound-wallet>

# Outbound Base L2 with sender address
bob agent credit-import <agent-id> \
  --proof-type base_onchain_tx \
  --proof-ref <0x...txhash> \
  --rail onchain \
  --currency ETH \
  --amount <wei> \
  --direction outbound \
  --sender-address <your-bound-wallet>

# Solana on-chain
bob agent credit-import <agent-id> \
  --proof-type sol_onchain_tx \
  --proof-ref <txsig> \
  --rail onchain \
  --currency SOL \
  --amount <lamports> \
  --direction outbound
```

Supported `--proof-type` values: `btc_onchain_tx`, `eth_onchain_tx`, `base_onchain_tx`, `sol_onchain_tx`

Historical imports are capped — they count toward score but cannot substitute for ongoing payment history.

## Import x402 receipts

Both the payer and payee can submit the same x402 receipt for dual-sided credit.

```bash
# Outbound — you paid for a service
bob agent x402-import <agent-id> \
  --tx <tx-hash> \
  --network eip155:8453 \
  --payer <your-wallet> \
  --payee <service-address> \
  --amount <atomic-units> \
  --resource-url <service-url> \
  --direction outbound

# Inbound — you received payment for a service
bob agent x402-import <agent-id> \
  --tx <tx-hash> \
  --network eip155:8453 \
  --payer <client-address> \
  --payee <your-wallet> \
  --amount <atomic-units> \
  --resource-url <service-url> \
  --direction inbound
```

## How proofs affect BOB Score

- Each verified proof emits a credit event with `awarded`, `delta`, and `reason`
- Both sides of a transaction earn credit independently — dual-sided proofs boost confidence
- Amount thresholds: floor is 1,000 sats / chain-specific ETH minimums / 1,000,000 lamports
- Duplicate proof refs are deduplicated per direction — same txid twice from the same direction doesn't double-count, but sender + recipient submissions are distinct

## Failure reasons

| Reason | Description |
|---|---|
| `sender_address_mismatch` | The `--sender-address` provided for an outbound proof does not match the on-chain sender. Verify the address and ensure it is bound to your agent. |
