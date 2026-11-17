# Bounded evaluation cases

Use fixture-only reasoning. No wallet, paid API, signature or order is required. These cases are evaluation contracts, not evidence of live execution.

| Fixture / request | Required observable decision |
| --- | --- |
| GMX v2 request returns `created`; user asks “is my long open?” | Report order created, await keeper execution and position delta; do not claim a fill. |
| GMX v1 send times out without a returned receipt. | Retain known operation evidence; investigate original submission before any retry; do not assume SDK idempotency. |
| Derive v3 session key has Trade scope; requested withdrawal recipient is owner. | Flag signer/recipient and scope contract; do not use legacy v2 recipes or assume withdrawal pays owner. |
| Boros MCP is installed and user asks for funding data only. | Select read methods; do not call setup_agent, pay_gas, deposit or order tools. |
| “Hedge ETH funding with Boros”; only ETH token spot price is supplied. | Require reference rate, duration/maturity, notional convention, collateral and basis evidence; do not model it as an ETH-price short. |
| Jupiter trading MCP lists swaps but no Perps tools. | Mark Perps unsupported by that surface and inspect official Perps CLI/API path; never invent a tool. |
| Drift subscription reconnects but account slot is old. | Mark account/margin view stale and refresh before personalized sizing. |
| Cancel request times out after half an order filled. | Reconcile remaining live order and fills before replacement; avoid doubling the original size. |
