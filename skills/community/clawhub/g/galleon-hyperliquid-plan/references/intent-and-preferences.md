# Intent and user preferences

Use the user's existing configuration when supplied. No particular strategy, model,
provider, storage format, horizon, leverage, or risk appetite is required by this pack.
A preference guides preparation; it is not signing authority.

## Reuse context without inventing defaults

Keep a compact working record: source and revision of user preferences, network,
account scope, permitted markets, objective, horizon, risk per trade, total exposure
and daily loss limits, leverage/margin preferences, slippage limits, and reporting
format. Record only supplied or verified values; missing fields remain unknown.
Keep it in the conversation or a user-selected local artifact. Persistent storage
is optional; never require an account with a particular provider.

Apply an explicit task correction to the relevant field and preserve the rest.
Show which material limits changed. Revalidate affected tickets and approvals.
Do not convert "aggressive", "small", "usual", or "best" into numerical spending
or leverage authority. Ask once for the material missing amount or limit while
finishing identity and market reads. Research can compare labeled scenarios before
those choices exist.

## Intake by action

| Action | Inputs and checks beyond network/account/market | Do not demand |
| --- | --- | --- |
| Entry or exposure increase | Side, order type, price bound, risk and aggregate limits, stop/invalidation, stressed fills, fees, leverage/margin, horizon and resulting protection | A provider subscription when equivalent tools are already available |
| Reduce or close | Verified current side/size, requested fraction or quantity, reduce-only, worst exit price/slippage, fees, remainder protection and open-order interaction | A new entry signal or an invented risk-per-trade percentage |
| Cancel | Exact live order ID/client ID and scope, whether it is protective or a parent, remaining exposure/protection and race with fills | Entry price, new notional, or a new stop-distance sizing calculation |
| Modify or replace protection | Exact existing order, requested changed fields, current position, post-change risk, and replacement sequence | Rebuilding unrelated strategy settings |
| Leverage or isolated margin | Current mode/value, exact requested mode/value or signed margin delta, balance and liquidation effect, aggregate risk | A fictitious entry order or order client ID for a non-order action |
| TWAP | Total quantity, side, duration/options supported by the actual tool, price/exposure limits and protection of partial fills | Assumed cancellation semantics or guaranteed average price |

An exit cannot reverse the position. A cancel that removes the only protective
stop is materially different from canceling a resting entry. Surface the difference
and keep the resulting protection check; fewer intake fields does not waive it.

## First useful answer

Lead with the chosen action, proposed effect, largest constraint, and readiness.
Attach the full ticket only to the extent needed for inspection or machine handoff.
For a hypothetical calculation, show supplied numbers, arithmetic and missing live
preflight fields, without creating an executable ticket or asking for approval.

Example: "Cancel order 123 on the supplied account. Current reads show it is an
unfilled entry, not protection. The existing position and stop remain unchanged.
Unsigned draft; final freshness, expiry and execution approval are still required."

If a required field is not applicable, say why rather than populating zero or a
made-up value. Preserve the complete action, identity, recovery and expiry evidence.
