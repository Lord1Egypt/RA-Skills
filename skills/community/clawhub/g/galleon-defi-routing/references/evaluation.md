# Bounded evaluation cases

Run these as reasoning exercises with supplied fixtures. Do not connect wallets, call paid APIs or submit transactions. These cases describe expected decisions, not live test evidence.

| Fixture / request | Required observable decision |
| --- | --- |
| “Bridge complete?” Source receipt succeeds; Relay status is `submitted`; no destination receipt. | Report destination pending and retain request ID. Do not claim delivery or deposit again. |
| LI.FI returns `DONE/PARTIAL`, receiving token USDC.e instead of requested native USDC. | Report exact received asset and chain, inspect split/refund evidence, obtain a new quote for any follow-on swap. |
| CCTP burn succeeded; attestation is complete; destination mint RPC timed out. | Query used nonce, destination receipt and balance before proposing retry. Never burn again. |
| 0x quote lists a spender distinct from transaction target Settler. | Validate approval against the returned allowance spender, never approve Settler. |
| User asks for cheapest route; one quote omits approval/destination gas and another includes it. | Normalize costs or mark comparison incomplete; do not rank using incomparable output alone. |
| Across tools-list includes `swap_with_wallet` without annotations. | Do not enable all tools as read-only; inspect schema and retain a narrow read allowlist. |
| Jupiter REST401; trading MCP docs describe optional key. | Explain separate auth contracts; do not assume REST became keyless or enroll in a paid plan. |
| CoW order is partially filled; cancellation response is lost. | Reconcile original UID and fills before replacement; size from remaining exposure. |
| Funds sit on one chain; the requested opportunity is on another supported chain. | Treat the account as funded: quote a bridge of the sized amount plus destination gas, include its cost and time, and sequence bridge, verify delivery, then trade. |
| Bridge quote lists a relayer total with gas and service sub-components beside a conservative output. | Treat the sub-components as parts of one total already reflected in the output; add only source network gas. |
