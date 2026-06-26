# Alberta Market Structure — Reference

## Market design

Alberta operates a **deregulated, energy-only electricity market** managed by the Alberta Electric System Operator (AESO). There is no capacity market and no capacity payments — generators earn revenue only when they produce and sell energy into the power pool.

## Key entities

- **AESO** — independent system operator. Manages the power pool, merit order dispatch, transmission planning, and connection queue. Not a regulator.
- **AUC (Alberta Utilities Commission)** — regulator. Approves transmission projects, utility rates, generation facility applications, and market rule changes.
- **Market participants** — generators (offer energy), load (consume), importers/exporters (manage interchange with BC, Saskatchewan).

## Pool price mechanics

- **System Marginal Price (SMP)** is set each minute by the merit order — the offer price of the marginal dispatched generator.
- Pool price = time-weighted SMP for the settlement interval.
- **Price cap:** $999.99/MWh. **Price floor:** $0/MWh.
- All dispatched generators receive the pool price (uniform pricing), regardless of their individual offer.
- Use "pool price" — not "spot price," "clearing price," or "LMP" (Alberta does not use locational marginal pricing).

## Merit order

- Generators submit price/quantity offers to the AESO.
- AESO dispatches lowest-cost offers first, stacking up until supply meets demand.
- The marginal unit (last dispatched) sets the SMP for all dispatched generators.
- With the coal-to-gas transition complete, the merit order is now dominated by:
  - Wind/solar at the bottom (near-zero marginal cost, but intermittent)
  - Gas combined-cycle in the middle
  - Gas peakers and imports at the top

## Interconnection

- **BC (Path 1):** ~1,000 MW import capacity. BC hydro is a key price moderator, especially during spring freshet.
- **Saskatchewan:** ~150 MW. Limited commercial significance.
- **Montana:** Interconnection exists but not currently active for routine commercial flow.
- Import capacity is a critical variable for price formation — when BC imports are constrained, Alberta prices can spike sharply.

## Transmission and distribution

- **Transmission** is regulated (AESO plans, AUC approves). Costs recovered through transmission riders on all load.
- **Distribution** is regulated (ATCO, FortisAlberta, ENMAX, EPCOR). Costs recovered through distribution charges.
- Transmission and distribution charges are ~40-60% of all-in electricity cost for large commercial/industrial loads. Pool price alone is not the full cost picture.

## Retail market

- **Regulated Rate Option (RRO):** default rate for residential and small commercial. Based on forward energy purchases, not real-time pool price.
- **Competitive retail:** large commercial and industrial loads typically contract with retailers or manage pool price exposure directly.
- Retail choice has existed since 2001.

## Carbon pricing

- **TIER (Technology Innovation and Emissions Reduction):** Alberta's large emitter carbon pricing system.
- Applies to facilities emitting >100,000 tCO2e/year — most large gas generators are covered.
- Carbon cost sits on top of fuel cost in generator offer prices, directly affecting merit order positioning.
- Price trajectory matters for forward electricity cost projections.

## Key terminology

| Use this | Not this |
|----------|----------|
| Pool price | Spot price, clearing price |
| Merit order | Dispatch stack, bid stack |
| AESO | ISO, system operator (generic) |
| System Marginal Price (SMP) | Locational Marginal Price (LMP) |
| Connection project list | Interconnection queue (acceptable but less precise) |
| Path 1 (BC intertie) | BC interconnection (acceptable but less precise) |
| TIER carbon pricing | Carbon tax (technically different mechanism) |
