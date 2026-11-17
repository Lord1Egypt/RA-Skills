# Product diligence from the underlying claims

Use this with [metric methodology](methodology.md) when comparing a vault, stablecoin, lending market or yield product. It supplies research questions, not a trading or signing procedure. Fetch the selected product's current primary documentation and relevant onchain configuration before asserting its mechanics.

## Trace the capital and yield

Identify what the user would hold: a token, redeemable claim, vault share, LP position or debt. Follow wrappers to the underlying assets and liabilities; identify custody, issuer obligations, leverage, counterparties and who takes losses first. Separate marketing names from enforceable redemption rights and actual collateral.

For each yield component record its payer, mechanism, capital basis, period and source date. Distinguish borrower interest, trading fees, staking income and external asset cash flows from token emissions or a subsidy funded by the same ecosystem. Separate cash distributions from accrued NAV and unrealized token appreciation. Identify who funds incentives, their expiry and conditions, then calculate after-fee proceeds under the same horizon. Do not add APR and APY or gross and already-net figures. Points and prospective airdrops are uncertain rewards, not realized yield.

Stress one assumption at a time: incentives end, funding reverses, utilization spikes, collateral depegs, or exit liquidity disappears. Show which cash flow or liability changes and who absorbs the shortfall. Do not assign scenario probabilities without a stated basis.

## Establish oracle and control risks

Record the actual valuation used by the contract: market feed, TWAP, redemption ratio, administrator NAV, fixed peg or a combination. Read the deployed feed identity, units, update timestamp and fallback logic. Identify the actors able to change collateral, caps, pricing, withdrawal rules or upgrades and the applicable delay.

Ask whether a market depeg can change this oracle and trigger liquidation before collateral becomes unexitable. A fresh accounting value can differ from a realizable market value. For Chainlink integrations check the feed's documented [timestamp and decimal fields](https://docs.chain.link/data-feeds/using-data-feeds), freshness policy and L2 sequencer handling when relevant. Apply the selected protocol's actual configuration; do not generalize one feed's heartbeat or chain's rules to another.

## Establish a realizable exit

Compare primary redemption with secondary-market sale. Record eligibility, request/claim stages, settlement delay, queues, gates, fees, caps, reserve liquidity and dependencies on an issuer or bridge. Check available depth at the research size and describe stress behavior. A transferable share, high TVL, successful read or redemption preview does not prove immediate withdrawal capacity. Confirm which asset is delivered and whether another conversion is required.

## Preserve chain evidence

Record chain ID, block number and block hash alongside contract state and the RPC's finality status. Reconcile related reads at the same block when supported. An included block can be reorganized; confirmation count alone is not universal finality. Apply the chain's documented rules, distinguishing L2 inclusion, L1 settlement and any withdrawal dispute period. [Ethereum's consensus documentation](https://ethereum.org/en/developers/docs/consensus-mechanisms/pos/) provides one chain-specific example.

If a canonical block hash changes or an indexer lags, invalidate the affected conclusion and reread its dependencies. Do not silently splice state from different forks or relabel old data as fresh. A transaction hash alone cannot establish a successful final state; verification of an existing receipt remains read-only.

## Deliver the decision-relevant evidence

Use a compact comparison with the claim held, dated yield breakdown, first-loss bearer, oracle/control risk, exit constraints and unresolved evidence. Distinguish a documented mechanism, an observed current state and a modeled stress outcome. If a critical assumption remains unverified, say which conclusion depends on it instead of replacing it with a safety label.
