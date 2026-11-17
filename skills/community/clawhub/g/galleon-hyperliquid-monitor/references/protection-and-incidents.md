# Protection and incidents

## Protected position

A perp position is protected only when current detailed order state shows a trigger on the closing side that is reduce-only and either:

- covers at least the live position size, or
- is explicitly position-tied and closes the current whole position.

Check that the trigger is on the intended loss side of current mark and that its execution limit leaves a deliberate fill bound. A local plan, chat promise, screenshot, or rejected order is not protection.

## Partial states

- Partial IOC entry: the remainder is canceled. Grouped children may not protect the filled part. Reconcile and flag any exposed size.
- Partial close: the position remains. Preserve a position-tied stop or replace a fixed-size stop before canceling it.
- Full close: prove the position is flat, then identify and cancel orphaned reduce-only triggers through a new action workflow.
- Add or reduce: fixed-size triggers do not resize automatically.

## Incident triggers

Declare `incident` when an action result is unknown, account exposure differs from the ticket, a position is unprotected, an unfamiliar order or fill appears, the feed is blind past its freshness bound, a scheduled cancel fired, or signer misuse is suspected.

## Read-only containment report

The monitor does not act. It reports:

```text
incident: <id and UTC>
state: <known exposure, orders, fills, liquidation buffer>
unknown: <missing or conflicting evidence>
smallest containment intent: <reduce, protect, or cancel one order>
urgency: <evidence-based deadline>
next owner: <user or execution workflow>
```

If signer compromise is suspected, tell the user to revoke the API wallet through the official app immediately. Investigation follows revocation. Never ask for the key.

## Scheduled cancel

The dead-man switch cancels all open orders in its account scope when it fires. That includes stops and take-profits. If a position remains, report it as unprotected. Do not automatically re-arm without a reviewed and authorized action.
