# Wallet Balances Concepts

## Lovelace

The smallest unit of ADA on Cardano. 1 ADA = 1,000,000 lovelace. Balances from the MCP server are always in lovelace — convert before displaying to the user.

## Native Assets

Cardano supports native multi-asset tokens without smart contracts. Each asset is identified by:

- **policyId** — 56-character hex string identifying the minting policy
- **nameHex** — hex-encoded asset name under that policy

Together, `policyId` + `nameHex` uniquely identify any native token.

## UTxO Model

Cardano uses an extended UTxO (eUTxO) model. Each unspent transaction output (UTxO) sits at an address and holds ADA plus optionally native assets. The wallet balance is the sum of all UTxO values.
