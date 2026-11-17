# Test matrix

## Identity and numbers

- mainnet and testnet metadata with different asset IDs
- default perps, spot, and multiple HIP-3 DEXs
- UI name remapping and reverse-map failure
- every supported size precision, price boundary, integer price, negative zero, trailing zeros, and scientific notation rejection
- size rounded down below minimum notional
- margin tier transition at exact lower bounds

## Orders

- action-level reject and per-leg error
- GTC resting, ALO crossing reject, IOC full and partial fill
- trigger wait, grouped parent wait, sibling cancel, and missing children after partial IOC
- cancel by order ID and client order ID
- fixed-size protection after add and reduce
- full versus partial close orphan handling
- scheduled cancel with and without an open position

## Delivery

- timeout before send, during send, and after server acceptance
- response lost but order found by client ID
- repeated negative reads before expiry remain unknown
- expiry then clean reconciliation permits a new ticket, never an automatic retry
- two processes contend for one signer nonce
- stale expiry and rate-limit exhaustion

## Account modes

- standard, unified, portfolio margin, legacy DEX abstraction, and unknown future value
- balances split across DEXs and spot
- portfolio borrow caps reached and fallback behavior
- coupled liquidation state and non-deterministic liquidation order

## Streams

- initial snapshot not emitted as new event
- duplicate fill, out-of-order update, silent disconnect, reconnect overlap, uncovered gap, and queue overflow
- open candle versus closed candle
- book invalid until fresh snapshot after gap

## Security

- forbidden action type, changed action after approval, mismatched network or account, signer no longer approved, leaked-secret detector, dependency audit, and malicious text in external metadata

Run unit and fixture tests offline. Any testnet integration write needs explicit authorization, a dedicated account, tight caps, unique client IDs, and complete cleanup proof. Ordinary CI never sends.
