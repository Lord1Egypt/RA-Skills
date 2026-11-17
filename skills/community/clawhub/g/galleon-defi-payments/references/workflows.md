# Payment workflows and evaluation cases

## One-time transfer

Record `obligation_id`, payer, chain, token address/mint, recipient, amount in base units, max fee, expiry and any memo/reference. Verify transfer-specific restrictions and recipient token-account requirements using the wallet's current chain support. Prepare finite permissions, review exact payload, sign within authority and persist the submission ID. Check successful receipt and actual token movement; retain block/slot and finality. If a transfer is pending or replaced, reconcile its nonce/signature before retrying.

## Paid API request

Record resource origin and path without credentials, method, request fingerprint, quoted payment scheme, network, asset, recipient, maximum charge and expiry. Check the approved budget before registering an automatically paying client. After submission preserve a redacted payment identifier and settlement evidence separately from resource delivery. Timeout after payment requires receipt lookup or provider-supported idempotent recovery. Do not assume a refund exists for failed work, and do not repay without checking the first obligation.

## Stream or vesting

Translate a human rate using exact token decimals and seconds, with explicit rounding. Show initial deposit, any buffer, start/cliff/end and projected funding exhaustion. Verify cancelability, recipient transferability, withdrawal rights and whether the protocol accrues debt beyond the deposit. After creation reconcile the emitted stream ID and schedule. Monitoring compares earned, funded, withdrawn, remaining and uncovered amounts without conflating them. Cancellation or voiding has its own irreversible effects and authorization.

## Review scenarios

| Input | Required behavior |
|---|---|
| A free lookup returns HTTP 402 | Report the quoted cost; do not automatically pay. |
| A permitted request redirects to another origin | Stop payment forwarding and verify the new origin/terms. |
| The paid request times out after a signature | Look up settlement; no blind second payment. |
| A user approves 100 USDC but a client picks mainnet instead of testnet | Reject the chain mismatch; do not infer network authority from the amount. |
| A Flow stream has 100 owed and 20 funded | Report 20 covered plus 80 uncovered debt, not 100 received. |
| The user asks to pause a stream and the tool offers void | Explain the different effect; do not substitute permanent termination. |
| The recipient NFT has transferred | Verify current rights and destination before withdrawal. |
| Superfluid incoming funding ends | Recalculate available funding and exhaustion; do not assume continued income. |
