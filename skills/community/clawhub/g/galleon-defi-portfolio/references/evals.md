# Offline evaluation scenarios

Use the skill with these synthetic fixtures and no credentials or transaction tools. Assess the resulting ledger/report and whether it preserves uncertainty. These scenarios are acceptance criteria, not recorded live-provider results.

| Request / fixture | Required behavior |
| --- | --- |
| Report net worth: wallet has $100 USDC and a vault receipt marked $500; protocol reports that same receipt's $500 underlying. | Equity is $600, not $1,100; underlying exposure is a separate decomposition. |
| Lending item reports assets $1,000, debt $400 and net $600. Wallet holds $100. | Gross assets $1,100, debt $400, net $700; do not subtract the $400 twice. |
| Start equity $1,000, end $1,200, external contribution $300, no withdrawal. | Economic change is -$100; do not report $200 profit or a derived return without flow timing. |
| Borrowed $200 appears as a wallet inflow with equal new debt. | No $200 profit; show asset and liability increase. |
| Zerion default only_simple response has one token; separate evidence shows an Aave position. | Identify incomplete protocol coverage and request no_filter/appropriate protocol data; do not report full net worth. |
| Two chains each have a token called USDC; one is bridged, with missing price and delayed bridge receipt. | Keep distinct chain/contract identities and unpriced/pending status; do not assume peg or double-count in transit. |
| Account A transfers $100 to included account B, with $1 gas. | Internal movement is not external capital; reconcile gas as a portfolio cost. |
| A perpetual position has $10,000 notional and $1,000 account equity. | Report notional/exposure separately; do not add $10,000 to net worth. |
| Provider total is $2,000; underlying rows include missing pages and data timestamps one day apart. | Report partial/stale reconciliation instead of forcing totals to match. |
| User asks for a 50/50 allocation plan; one asset is queued for withdrawal and quotes have expired. | Present feasible dependencies, refreshed-quote requirements and costs; do not bridge, swap or create a recurring job. |
