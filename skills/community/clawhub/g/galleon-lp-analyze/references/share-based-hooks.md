# Share-based v4 hooks

A Uniswap v4 label does not prove concentrated-liquidity NFT accounting. A hook can maintain its own reserves, invariant, fee logic, and fungible share token while using v4 for settlement.

## Bind the model

Identify:

- every supported currency, canonical order, decimals, scaler, wrapper, and rate source
- the hook, factory, PoolManager, pairwise PoolKeys, and fungible share token
- invariant, amplification state, fee model, and admin controls
- internal reserves, actual token balances, total share supply, and locked minimum liquidity
- proportional deposit and withdrawal rules
- quote, minimum-amount, minimum-share, refund, and native-currency behavior

Do not use tick ranges, active liquidity, NFT ownership, or fee-growth accounting unless the deployed hook actually uses them. Do not sum TVL from multiple pairwise PoolKeys when they settle against one shared reserve set.

## Token and oracle gate

Check the implementation's decimal bounds and transfer assumptions. Internal reserve accounting can break when tokens rebase, charge transfer fees, deflate, invoke callbacks, or deliver less than the requested amount.

For each rate source, verify units, scaling, heartbeat, stale-data handling, L2 sequencer handling, zero or negative answers, fallback behavior, upgrade authority, and what happens when the call reverts. A valid ABI return can still be economically wrong.

## Invariant and admin gate

Test balanced and imbalanced reserves, small amounts, rounding boundaries, maximum values, fee changes, amplification changes, and rate changes. Determine whether:

- amplification changes immediately or ramps over time
- an admin can make swaps or deposits uneconomic or unavailable
- the invariant solver can stop converging in reachable states
- deposits, swaps, and withdrawals fail independently
- a full proportional withdrawal remains possible in adverse state

Treat a pool that still permits withdrawal but rejects swaps or deposits as degraded, not healthy.

## Return and exit

Separate LP fees retained in reserves from hook and protocol fee shares. Quote a full share redemption into every currency, including minima, price impact, wrappers, loose balances, and any conversion needed after withdrawal.

Report the position model explicitly as `share-based hook`, not `v4 concentrated`.
