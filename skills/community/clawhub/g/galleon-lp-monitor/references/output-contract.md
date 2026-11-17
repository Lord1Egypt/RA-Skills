# Monitor output

## Verdict

One line: hold, collect, recenter, restake, reduce, exit, or state unknown. Include the condition that would change it.

## Bound position

Chain ID, wallet, protocol, pool, position ID or LP balance, staking state, token order, observation block, and evidence class.

## State

For concentrated positions show current tick, range, active state, distance to each edge, liquidity, claimable fees, and claimable rewards. For ordinary full-range positions show reserve share and gauge state. For hook-issued shares show all currencies, internal reserves, actual balances, share supply, attributable shares, rate sources, invariant controls, and proportional exit amounts.

## Accounting

Show original quantities or `unknown`, current inventory, HOLD value, claimable and realized income, loose residue, costs, divergence, and net result versus HOLD. Label every estimate and window.

## Action economics

Show full action cost, expected incremental benefit, break-even assumption, invalidation, and skipped gates. If current evidence is sufficient and no action clears the hurdle, say HOLD. If required state or cost evidence is missing, say state unknown for the affected decision and identify the missing read.

## Next read

State the next block, time, price, range, reward epoch, or security event that warrants another check. Do not include calldata.
