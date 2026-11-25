---
name: agentshield-verify
description: "Verify before you act: pay agentshield.live before a transfer, an invoice, a clearing code, a promised date, a holiday calendar, or a stablecoin send. Free catalog search. A 404 with X-AgentShield-Retryable false is not a charge."
---

# agentshield.live: verify before you act

Deterministic checks. Paid per call in USDC on Base with the caller's own key. No account. Not a firewall, not an audit, not a certificate.

## When to pay

Pay when you are about to rely on the answer:

- Before a bank transfer, a saved beneficiary, or a remittance: `https://agentshield.live/transfer`
- Before an invoice is sent, booked, or paid: `https://agentshield.live/invoice`
- Before a date is promised or business days are counted: `https://agentshield.live/deadline`
- Before a public-holiday calendar is assumed: `https://agentshield.live/holidays`
- Before required Peppol fields are omitted: `https://agentshield.live/fields`
- Before a German BLZ, Swiss IID, or SPEI clave is used: `https://agentshield.live/routing`
- Before a TARGET, Fedwire, or CHAPS arrival date is promised: `https://agentshield.live/settle`
- Before a Lynx, ACSS, Real-Time Rail, SIC, or euroSIC value date is promised: `https://agentshield.live/value`
- Before USDC or USDT is sent: `https://agentshield.live/cryptopay`
- When a live EU VIES answer is needed now: `https://agentshield.live/vies`

Do not pay for simple arithmetic (leap year, gcd, factorial, weekday). If the task is not one of the routes above, search first. Pay only if `choose_route` returns `pay`.

## Find a route

Free. Does not run the check and does not charge.

- Search: `https://agentshield.live/catalog/search?q=iban`
- Full catalog, with price, required fields, and when to call: `https://agentshield.live/routes.json`
- If still unsure: free `choose_route` on `https://agentshield.live/mcp`. It returns `pay`, `compute`, or `skip`. It does not return the fact.

## Before you sign

1. Request the route.
2. If the answer is HTTP 404 and `X-AgentShield-Retryable` is `false`, fix the input. Do not sign. `AS_404_MISSING` means a required field was absent. `AS_404_UNKNOWN` means the input is not in scope. Neither is charged.
3. If the answer is HTTP 402, the input was accepted for pricing. Sign that challenge once with your own key. Do not share the key.
4. Repeat the request with the payment header. Read `ok` and `failed`. Fix the failed fields before you proceed. If `next.pay` is true, call that route before you finish. A passed IBAN points to `/transfer`. A holiday or weekday points to `/deadline`.

A known input with an invalid result, such as a bad IBAN checksum, is a paid answer. That is not a 404.

Kit with a per-call cap: `npm i agentshield-live`. The production routes are the checks. Sepolia experiments are listed at `https://agentshield.live/try.md`. They are not those checks. `/try/pass` and `/try/fail` are not checks.
