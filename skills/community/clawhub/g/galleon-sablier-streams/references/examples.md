# Sablier worked records

Synthetic observations only.

## Scale and funding

Intent: 1 USDC per day using a six-decimal USDC token, prefund 10 USDC. Token deposit is `10000000` base units. Flow rate is `floor(10^18 / 86400) = 11574074074074` UD21x18. Dividing six-decimal token base units by seconds would give a different incorrect rate scale. The floor represents slightly less than 1 USDC/day; report that rounding and the horizon difference rather than silently increasing the rate. Ten days is the approximate funding horizon, but an unpaused Flow continues accruing debt afterward.

## Debt is not receipt

At time T a Flow stream has total debt 100 USDC, funded/covered debt 20, uncovered debt 80, withdrawn zero. Report 100 earned/owed, 20 currently covered and up to the observed withdrawable cash, 80 uncovered, zero withdrawn. Do not call 100 paid or received. A later paused stream retains accrued debt; void is a separate permanent choice.

## Current NFT owner

Old indexer lists recipient A, while fresh NFT/state evidence shows recipient rights held by B. Refresh withdrawal recipient and caller permissions. A's historical address cannot authorize withdrawing B's entitlement. Do not sign against stale cached rights.

## Cancellation boundary

User requests pause of one Flow stream. Official cancellation example offers refund+void for all eligible streams. Prepare the requested pause only if the deployment supports it and the actual sender has rights. Explain the uncovered/covered debt after pausing. Do not expand scope to all streams or replace reversible pause with permanent void.

## Lockup funds

A prefunded 1,000-token Lockup has 300 vested, 100 withdrawn and 700 refundable unvested under its current cancellation policy. A permitted cancellation leaves 200 vested withdrawable for the current recipient and returns eligible 700 to the sender, subject to exact deployment rules. Report each obligation/receipt separately after state/receipt checks.
