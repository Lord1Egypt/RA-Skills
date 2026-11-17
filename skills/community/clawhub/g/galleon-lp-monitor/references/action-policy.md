# Action policy

Return `state unknown` when required evidence is incomplete, stale, or contradictory. With sufficient current evidence, recommend HOLD when no action clears its full cost and risk hurdle. Unknown state is not a healthy HOLD verdict.

## Collect

Collect only when claim value and operational need exceed gas, price impact, tax, approval, and reinvestment costs. A collect that leaves the intended position unchanged is different from a compound. Uniswap v2-style positions have no ordinary separate collect action.

## Recenter

Being near an edge or out of range is a trigger to evaluate, not an automatic order. Recenter only when:

- current state and quote are fresh
- token and pool gates still pass
- the new range has evidence tied to horizon and price distribution
- expected incremental fees or rewards clear unwind, swap, mint, stake, gas, slippage, MEV, and tax costs
- cooldown and churn limits pass
- the action does not violate spend, loss, inventory, or price-impact caps

Use hysteresis so small score or price changes do not flip the position repeatedly. Do not center blindly into a fast trend or a known gap event.

## Restake or unstake

Compare the actual fee seat with the actual reward seat using the current epoch, reward budget, dilution, lock or custody state, claim cost, and required management operations. A projected APR alone is insufficient.

## Reduce or exit

Exit or reduce when a hard gate fails, the position exceeds a user loss or inventory cap, the thesis is invalidated, the hook or admin surface changes materially, reward support expires, exit liquidity deteriorates, or a safer opportunity clears all switching costs.

Quote the full exit path at the user's size. If the exit is impaired, say so directly and separate recoverable actions from unavailable ones.
