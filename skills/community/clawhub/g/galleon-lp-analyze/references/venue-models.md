# Venue models

Resolve deployments from current official registries. Do not carry addresses between chains or versions.

| Venue | Position | Price coverage | Fee realization | Extra trust surface |
|---|---|---|---|---|
| Uniswap v2 | Fungible pair LP token | Full range | Fees compound into reserves and LP token value | Factory, pair, router, token behavior |
| Uniswap v3 | NFT | Chosen tick range | Fees accrue separately and require collection | Factory, pool, position manager, router |
| Uniswap v4 | Position managed against a singleton PoolManager | Chosen tick range | Depends on position manager and pool behavior | PoolKey, hook address and permissions, manager, unlock callback path |
| Uniswap v4 share-based hook | Fungible hook-issued share | Hook invariant, potentially across several currencies | Depends on internal reserves and fee split | Hook factory, reserve accounting, invariant, rate sources, admin controls |
| Aerodrome classic volatile | Fungible pair LP token | Full range | Verify whether the chosen staked or unstaked route owns fees | Factory, pair, router, gauge, voter model |
| Aerodrome classic stable | Fungible pair LP token | Full range around a stable invariant | Verify pool math and fee or gauge route | Same as classic volatile plus invariant assumptions |
| Aerodrome Slipstream | NFT | Chosen tick range | Unstaked fee rights and staked emission rights can be mutually exclusive | Factory, pool, NFT manager, gauge, epoch emissions |

## Uniswap v2

The position owns a share of reserves. There is no independent fee-claim balance in the ordinary pair model. Removing liquidity realizes the current reserve share. Measure return through LP value, not a fabricated collectable-fee field.

## Uniswap v3

Liquidity earns fees only while active at the traded price. The upper tick is exclusive: a position is active when `tickLower <= tickCurrent < tickUpper`. Decreasing liquidity and collecting tokens are distinct state changes. An NFT can be burned only after liquidity and owed tokens are zero.

## Uniswap v4

Pool identity is the complete PoolKey: ordered currencies, fee, tick spacing, and hook. A familiar pair and fee do not identify a pool. Decode the hook permission bits and inspect implementation, ownership, upgrade path, fee control, and delta-returning behavior. Do not assume v3 calldata, native token handling, or fee accounting.

If the hook issues fungible shares against its own reserve set, classify it separately. Do not apply concentrated range, NFT, active-liquidity, or per-PoolKey TVL assumptions to that share model.

## Aerodrome classic

Classify the pool as volatile or stable before using quotes or invariant assumptions. Map the LP token, gauge, reward token, voter-controlled fees, and any incentive contract. Staking can change who receives trading fees. Verify the deployed version rather than generalizing from the brand.

## Slipstream

Slipstream uses concentrated ticks and NFT positions with gauge accounting. A staked position may relinquish swap fees in exchange for emissions. Treat unstaked fees and staked emissions as separate seats until contract reads prove otherwise. Reward APR is epoch-dependent, range-dependent, and dilution-sensitive.
