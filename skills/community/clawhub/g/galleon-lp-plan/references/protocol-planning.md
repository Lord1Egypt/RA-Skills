# Protocol planning

Resolve every target and capability from current official deployments and verified code.

## Uniswap v2

Plan token pairing or one-sided preparation, exact token approvals, add-liquidity constraints, LP recipient, and refund behavior. The position is full range. Fees live in the reserve share; do not schedule a collect transaction. Exit planning removes LP liquidity and may require a separate conversion.

## Uniswap v3

Plan fee tier, onchain tick spacing, lower and upper ticks, desired amounts, minimum amounts, recipient, deadline, and optional native wrapping. Mint creates an NFT. Increasing liquidity targets its token ID. Decreasing liquidity creates owed balances; collecting transfers them. Burn is valid only after liquidity and owed balances are zero.

## Uniswap v4

Bind the full PoolKey and inspect hook permissions before planning. Read pool state through the current StateView deployment. Verify the current PositionManager action model, currency settlement, native token behavior, Permit2 path, unlock callback, and hook-specific data. Position discovery can depend on indexed events, so recheck the selected position onchain. Reject a plan that treats the pool as v3 with a different address.

If the hook issues fungible shares against internal reserves, do not use concentrated range or NFT planning. Bind every supported currency, reserve, rate source, invariant control, expected shares, minimum shares, actual token amounts, per-token minima, refunds, and proportional exit quote.

## Aerodrome classic

Classify stable versus volatile invariant. Plan add liquidity, LP receipt, optional gauge approval and deposit, reward claim, gauge withdrawal, and removal as separate states. Verify who receives trading fees in the selected route and how rewards accrue.

## Slipstream

Plan the concentrated NFT first. Then choose one route based on verified contracts:

- keep the NFT unstaked and retain its fee rights
- stake or deposit it into the gauge and earn emissions under current epoch rules

Do not project fees plus emissions when staking forfeits fees. Check whether a position must be unstaked before increasing, decreasing, collecting, transferring, or burning. Reward claims and fee collection are distinct actions.
