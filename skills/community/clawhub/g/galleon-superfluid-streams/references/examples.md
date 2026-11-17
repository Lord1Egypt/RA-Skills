# Superfluid worked records

Synthetic observations only; no contract or account access is implied.

## Incoming flow dependency

Sender has 900 tokens of observed real-time spendable funding after any locked buffer. Outgoing aggregate flow is 90/day; incoming is 60/day. With incoming unchanged, net spend is 30/day and the indicative horizon is 30 days. If incoming stops, it is 10 days. Use the conservative 10-day case for an obligation that cannot rely on that payer; show both assumptions. Do not subtract the locked buffer again from already-spendable 900.

## Rate scale

For an 18-decimal Super Token, 1 token/day floor rate is `11574074074074` base units/second. That superficially matches Flow's UD21x18 example only because this token has 18 decimals; the models are different. A six-decimal token rate uses its actual interface's scale, not a universal 1e18 rule. Discover decimals and documented representation before constructing a call.

## Scheduler not executed

A stop schedule exists at T, but no execution receipt exists and the current CFA flow remains positive after T. Report schedule-configured/stop-not-executed and current ongoing obligation. Read actual automation permissions/status. Do not report subscription stopped from the stored deadline alone.

## Operator versus approval

ERC20 allowance to a wrapper exists, but CFA operator has no create/update permission. The wrap may succeed; the flow operation remains blocked until an explicitly requested compatible operator authorization or direct sender path exists. Do not add unlimited flow permission to fix the test.

## Changed macro

Typed message names recipient A while decoded nested calls route a flow to B or approve a different operator. Return a mismatch and preserve unsigned evidence. A clear-signing label and successful simulation do not establish intent match.
