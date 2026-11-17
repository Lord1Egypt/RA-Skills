# Authoritative state

Use the account or subaccount address whose state matters. The API wallet is a signer, not the account. Querying its address can return an empty account that looks flat.

## Core reads

| Question | Read |
|---|---|
| Account mode | `userAbstraction` |
| Perp positions and cross margin | `clearinghouseState`, with `dex` where needed |
| Spot balances and holds | `spotClearinghouseState` |
| Portfolio borrow and supply | `borrowLendUserState` plus current reserve states |
| Detailed resting orders | `frontendOpenOrders` or equivalent detailed stream |
| Order lifecycle | `orderStatus` by client order ID or order ID, `historicalOrders` |
| Fills | `userFillsByTime`, paginated and deduplicated by trade ID |
| Funding | `userFunding`, preserving account sign |
| Non-funding balance changes | `userNonFundingLedgerUpdates` |
| Effective fees | `userFees` |
| Action budget | `userRateLimit` |
| Market mark and metadata | `metaAndAssetCtxs`, `meta` |
| Per-market allowance | `activeAssetData` |

Time-ranged responses are bounded. Paginate from the last returned timestamp and deduplicate records that share the boundary.

## Account modes

Standard mode isolates spot and each perp DEX balance. Unified and portfolio modes use spot clearinghouse balances across products, so a single DEX state is incomplete. Portfolio mode also needs current borrow/lend state and its combined liquidation ratio.

Query every DEX with an open position or order. A default-DEX-only check can miss HIP-3 exposure. Report which scope each read covered: default-DEX perp equity is not unified-account value, and an account-value denominator observed today does not establish historical percentage returns.

## Reconciliation

For an order action, combine:

1. `orderStatus` for each client order ID or order ID.
2. Detailed open orders for resting, trigger, reduce-only, and grouping state.
3. Fills since the send time for executed size, price, fee, and trade ID.
4. Account positions and balances for net exposure.

No one source proves the whole outcome. If they disagree, report an incident state and keep every raw timestamp.

## Freshness

Each read carries network, request, server or payload time where available, local receive time, and maximum accepted age. Mixed-time snapshots disclose their skew. Do not compute a precise liquidation or open-risk verdict from states observed far apart.
