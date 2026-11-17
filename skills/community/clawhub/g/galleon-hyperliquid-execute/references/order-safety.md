# Order safety

## Construction

Use a maintained SDK for signing and current official types for payloads. Keep signing outside the skill and repository. Preserve numeric wire fields as decimal strings.

- `Gtc`: may rest.
- `Alo`: must rest or reject.
- `Ioc`: fills inside the approved limit and cancels the remainder.
- Trigger: mark-price condition plus a separate executable limit.
- Close, stop, and take-profit: reduce-only.

Never change time in force or widen a price bound after approval.

## Order identity

Persist a unique client order ID for every leg before sending. Record the request digest, signer address, user account, network, nonce, and `expiresAfter` without recording a key or signature material that creates replay risk.

## Grouped protection

Grouped entry children do not make every partial state safe. After any partial IOC or parent cancellation, read fills and current detailed orders. Place a separately approved stop for exposed size if no valid child rests.

Fixed-size protection becomes stale after an add or reduce. Replacement order:

1. Read live position size.
2. Place new reduce-only trigger.
3. Prove the new trigger is resting and correctly sized.
4. Cancel the old trigger.
5. Prove the old trigger is absent.

## Close

Read size seconds before submission. Send a reduce-only IOC inside the approved bound. Re-read the position:

- Flat: identify orphaned protection and cancel it through its own authorized step.
- Smaller: preserve position-tied protection or resize fixed protection before any cancel.
- Unchanged or larger: incident. Do not resend.

## Scheduled cancel

Use only when the user explicitly approved its scope and time. It cancels protective triggers as well as maker orders. If it fires with exposure open, the account is unprotected.
