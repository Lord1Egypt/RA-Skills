# Token Phases

The repo exposes token phase awareness through `bfun token-info`.

Current on-chain derivation:

- `curve` if `tradingStopped` is false
- `graduated` if `tradingStopped` is true and `sendingToPairForbidden` is true
- `dex` if `tradingStopped` is true and `sendingToPairForbidden` is false

The command also returns:

- `isGraduated`
- `isMigrated`

## `curve`

Meaning:

- bonding-curve trading is still active
- token supply and collateral reserves are still managed through the curve market

Agent behavior:

- safe to inspect with `token-info`, `token-get`, and quote commands
- normal buy/sell workflow is allowed after risk acknowledgement and explicit user confirmation

## `graduated`

Meaning:

- the bonding curve has stopped trading
- migration is pending or in progress
- the market is not yet ready for normal agent-executed trading

Agent behavior:

- do not run `buy` or `sell`
- explain that the token is between curve trading and DEX trading
- if the user wants to retry later, re-run `bfun token-info`

## `dex`

Meaning:

- liquidity migration has completed
- trades should route through the DEX-aware helper path

Agent behavior:

- use `quote-buy` or `quote-sell` first
- explain that execution should use the DEX route
- then use `buy` or `sell` after confirmation

## Operational note

The quote layer also distinguishes between curve and DEX-style routes based on API and market metadata. For user-facing safety, treat `bfun token-info` as the authoritative phase check before any write operation.

## Practical checklist

Before trading:

1. `bfun token-info <token>`
2. inspect `phase`
3. if `curve`, proceed to quote
4. if `graduated`, stop
5. if `dex`, quote and explain DEX routing
