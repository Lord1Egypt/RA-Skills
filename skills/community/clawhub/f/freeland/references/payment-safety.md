# Payment Safety

Use this reference before entering card details on unfamiliar merchants, when a checkout keeps failing, or when OTP and retry boundaries matter.

## Core Rules

- Confirm the merchant domain, total amount, subscription terms, and currency before payment.
- Treat wallet balance and card balance as separate facts.
- Never invent billing details. Use the billing address returned by the sensitive card endpoint.
- Keep PAN, CVV, expiry, and OTP output scoped to the active checkout only.
- After any merchant error, inspect card transactions before retrying.

## Retry Boundaries

- Do not retry the same merchant checkout more than twice in one session without explicit user approval or clear pre-authorization.
- If a transaction is pending, declined, duplicated, or ambiguous, stop and inspect current state before another attempt.
- If OTP does not arrive, check inbox state first instead of resubmitting the checkout blindly.

## OTP and 3DS

- Use `GET /api/inbox/latest-otp` for the most recent code.
- Wait briefly for inbox lag before deciding the flow failed.
- If the merchant shows success but Freeland has no matching card transaction yet, inspect again before declaring failure.

## Billing and Net Amounts

- Wallet deposits credit the net amount that reaches the Freeland rail.
- External sender, exchange, and network fees may reduce the credited amount before Freeland receives it.
- Do not describe those reductions as a Freeland fee unless Freeland itself charged it.
