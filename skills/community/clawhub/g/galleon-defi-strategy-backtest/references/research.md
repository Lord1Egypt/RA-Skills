# Data and research workflow

## Obtain compatible history

CoinGecko's [Demo market-chart contract](https://docs.coingecko.com/demo/reference/coins-id-market-chart), reviewed 2026-10-02, returns timestamp/price arrays and documents automatic daily samples at 00:00 UTC above 90 days, with Demo history limited to the last 365 days. Its documented Demo path requires the user's key. Public unauthenticated access is a separate bounded probe; a successful public response does not guarantee plan entitlement or future availability.

Use a resolved CoinGecko ID rather than a ticker. Query only the requested period, preserve the response and SHA-256, then select consecutive UTC-midnight observations and retain their timestamps. Exclude a trailing current partial-day observation explicitly. Do not rename hourly points as daily closes, interpolate missing days or silently shorten a requested period. Aggregate prices are not venue executions. Check the current official interface before depending on a plan, interval override or historical range.

For a venue dataset, record exchange, instrument, quote asset, candle convention, timezone, interval and source. Resolve splits, token migrations and delistings before comparing prices. USDT/USDC quotes are not automatically USD. Price feeds and corporate-action adjustment choices can change the result. This model is single-asset spot: leverage and funding require another engine.

The independently installed data pack's `galleon-defi-market-snapshot` helper can collect a compatible CoinGecko history and metadata. The strategy pack itself does not depend on it; prepare the [input contract](model.md) using existing official tools when unavailable.

## Write the thesis before reading the answer

Record the hypothesis, rule, parameter choices, budget, fees/slippage, data identity, evaluation dates, benchmark and invalidation criterion. Save exact input files and output together in the user's approved research location. Public market research can be shared; private holdings and account mappings need an appropriate private location.

A useful initial experiment changes one factor at a time. For example: test whether long/cash SMA timing reduces drawdown against buy-and-hold while preserving positive return on the same asset and date range, at declared costs. A rule tuned to maximize the full-history return has already consumed those observations.

## Compare a held-out period

Freeze the chosen rule before opening later observations. Keep reference and held-out date ranges distinct. Run the bundled `validate-strategy` command with an explicit zero-based split when dates are predetermined; it runs both periods and both cost assumptions without optimizing the rule. Its full [contract](model.md#frozen-rule-validation-contract) specifies sample minimums, costs and independent balances. A chronological partition labels an evaluation design; the runner cannot establish that the user had not already read the later prices.

The bundled engine starts each period with declared funded cash, no position or pending order and fresh indicator warmup. Only contributions dated within each subset enter it. This creates independent experiments, not a continuous strategy or automatic walk-forward test. State this startup convention. If continuity across the split matters, use an engine with explicit state carry and indicator prehistory rather than pretending a fresh run continued the previous position.

Report the number of observations, held-out dates, parameter variants attempted, both benchmark metrics and losses. A positive result on a short period or one surviving asset can reflect a regime or selection bias. Broad-market claims require an ex ante universe that includes delisted and unsuccessful assets, with available data and selection rules.

## Make costs visible

The validator reports baseline costs and a declared higher-cost scenario in each period; default stress is `max(2 × baseline, baseline + 10 bps)` capped at 1000 for each cost component. Both the rule and benchmark receive the same stress. Inspect dollar costs and the return/drawdown differences without inventing a pass threshold. You can repeat a small declared range of fees, adverse slippage and nearby SMA periods or DCA cadences separately. Describe the number of tested variants and avoid presenting the best one as a prior thesis. Fixed basis points are assumptions, not a measured liquidity curve. Confirm any future venue's fees, spread, depth, minimum order, funding, borrow, latency and gas independently.

The daily model cannot test intraday stops, limit-order queue position, partial fills or minute-level tactics. Its next observation prevents use of the signal mark as its own fill, but it does not prove that next aggregate price was tradeable. No Sharpe, Sortino, annualized return, win rate or profit factor is calculated; do not invent those metrics from this report.

## Decide the next step

Return one of: supported thesis for additional research, inconclusive due to data/sample/cost limitations, or thesis contradicted under the declared assumptions. Provide the report and concrete unresolved terms. Paper observation requires a real live-data loop and persisted simulated outcomes; a historical replay is not paper trading. Creating a recurring job or handing a specification to an execution venue uses the user's existing runtime and authority, not this pack.

Primary accounting reference: the [CFA Institute GIPS handbook](https://www.gipsstandards.org/standards/gips-standards-for-firms/gips-standards-handbook-for-firms/) explains valuing at external flows and geometrically linking subperiod returns. Our engine is a research implementation of that accounting principle; it makes no GIPS compliance claim.
