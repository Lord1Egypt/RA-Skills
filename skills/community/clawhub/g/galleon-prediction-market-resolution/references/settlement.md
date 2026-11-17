# Versioned resolution and receipt evidence

Reviewed 2026-10-08. Primary sources: [resolution](https://docs.polymarket.com/concepts/resolution), [positions/tokens](https://docs.polymarket.com/concepts/positions-tokens), [onchain position data](https://docs.polymarket.com/resources/onchain-position-data), [deployed contracts](https://docs.polymarket.com/resources/contracts).

| Evidence | CTF v1 | Protocol V2 |
| --- | --- | --- |
| Outcome identity | Gamma outcome token ID; Conditional Tokens ledger | Gamma position ID; PositionManager ledger |
| Mapping | Condition/collection/collateral identity | Official mapping or native identifier helper; migration IDs must not be rehashed |
| Balance | ERC-1155 owner balance on Conditional Tokens | ERC-1155 owner balance on PositionManager |
| Final payout | `payoutNumerators` and nonzero `payoutDenominator` | Current PositionManager resolution and payout contract reads |
| Received funds | Successful redemption context, burn and collateral recipient delta | Version-specific redemption context, burn and collateral recipient delta |

The docs identify UMA and Chainlink TWAP resolution sources. The documented example timings/bonds are not universal contract guarantees. Use the market's request, module and oracle configuration. A 50/50 payout is possible for a binary market; a negative-risk market has its own one-winner rules. Current collateral documentation names pUSD; confirm chain/address/decimals for the actual market and deployment rather than assuming older USDC.e examples remain valid.

Canonical ledger transfers drive balances. Use `TransferSingle`/`TransferBatch` plus validated checkpoints; lifecycle and auto-redemption events add attribution. Do not add both a lifecycle event and its underlying transfer to portfolio balances. Read current V2 event and module definitions from the official source before interpreting them.

This skill collects evidence and explains uncertainty. Oracle proposals, disputes, orders and redemptions are external financial actions requiring the user's actual authorized workflow; installing the skill provides none of that authority.
