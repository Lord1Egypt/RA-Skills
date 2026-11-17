# Incident response

Pause exposure-increasing actions when expected and observed state disagree.

## Unknown send

Follow the action state machine. Never resend to make sure.

## Rejection

Quote the exact action-level or order-level error. Re-read metadata and account state. Corrections require a new ticket. Do not edit and resend under the old approval.

## Unexpected or excess position

Read positions, fills, and detailed orders for the full window. Compute current exposure and liquidation buffer. Propose the smallest reduce-only containment action. It still requires an exact ticket and approval.

## Unprotected position

Report size, side, mark, liquidation buffer, and missing or invalid protection. Prepare a reduce-only trigger plan from live state. Do not create a stop from stale ticket size.

## Orphaned order

Prove the related position is flat. Cancel the specific client order ID or order ID. Never use account-wide cancel as a reflex.

## Blind or rate limited

Stop new sends. Existing exchange-resting orders may continue to work, but their current state is unknown until reads recover. Back off, preserve action budget, and reconcile before resuming.

## Suspected signer compromise

Tell the user to revoke the API wallet in the official Hyperliquid app immediately. Do not request the key or delay revocation for investigation. After revocation, reconstruct orders, fills, and exposure from the last known-good time. Any new signer must use a fresh address.

## Report

Record incident ID, start time, owner, observed state, unknowns, maximum exposure, containment intent, approvals, actions, reconciliation, end time, root cause if known, and one corrective action. Unknown root cause stays unknown.
