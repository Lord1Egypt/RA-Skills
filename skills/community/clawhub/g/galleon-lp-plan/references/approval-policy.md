# Approval policy

An approval is a separate asset-risk decision.

## Bind it

For every approval state:

- chain ID
- owner wallet
- token address and verified behavior
- spender address and verified role
- exact amount or justified cap
- expiration or cleanup condition
- direct ERC-20, NFT approval, Permit2 allowance, or signature transfer

Prefer exact or bounded amounts and short expiries. An unlimited approval needs a specific reason and separate risk disclosure. Never infer a spender from a frontend label.

## Permit2

Distinguish the token's approval to Permit2 from a Permit2 authorization to an application. A one-time signature transfer and a time-bounded allowance are different mechanisms. Bind chain, spender, token, amount, nonce, and deadline. Reject replayable or cross-context signatures.

## Special token behavior

Some tokens require allowance reset before a new nonzero approval, charge transfer fees, rebase, block recipients, or return nonstandard values. Detect behavior from current verified code and simulation. Do not generalize from the symbol.

## Native value

State whether each leg uses the chain's native currency or a wrapped token. Bind `msg.value`, wrapping, refunds, and dust handling. Never treat native and wrapped balances as interchangeable without an explicit step.
