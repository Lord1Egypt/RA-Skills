---
name: charge-my-users
description: Turn a deployed app into a product that bills ITS OWN end users per use — charge my users / end-user-pays / let users pay per use / bill app end users / usage-based billing / paywall / X-Settle-Payer / monetize an AI app that costs money per call. Use when the app makes paid platform calls (LLM, image/video, search, scraping) on a logged-in user's behalf and THEIR wallet should pay, with your markup on top — not the developer's wallet.
license: MIT
compatibility: "Requires the settlemesh CLI (npm i -g settlemesh) and a SETTLE_API_KEY; makes authenticated, metered calls to the SettleMesh platform over the network."
metadata:
  openclaw:
    requires:
      bins: ["settlemesh"]
      env: ["SETTLE_API_KEY"]
    primaryEnv: "SETTLE_API_KEY"
---

# charge-my-users — make end users pay per use

> **Session (auto — never dead-stop on auth):** before your first `settlemesh` call, run `settlemesh whoami`; if it errors and `SETTLE_API_KEY` is unset, run `settlemesh login` yourself — it opens the browser for a **one-time** human approval, polls until approved, and caches the session. Do NOT stop to ask the user to "log in manually" — drive it. Keep an explicit human confirmation only for spending / credential-lending actions (fail-closed).

Most "build an AI app" skills leave you holding the bill: every LLM call, image,
or search the app makes is charged to *you*, the developer. There is no account
model, no meter, and no payment rail to push that cost onto the person who
actually triggered it. **SettleMesh flips that with one HTTP header.** When your
app's server calls a platform capability on behalf of a logged-in user, add
`X-Settle-Payer: <that user's session>` and the platform charges the **user's**
Aev wallet `cost × m` — the markup `m−1` is your revenue.

A prompt-only skill cannot do this: it has no wallet ledger, no per-user session,
no metered capture. SettleMesh *is* the payment rail, the account model, and the
meter.

## Setup (once)

**End-user-pays only works AFTER deploy, from the app's own server.** The
`X-Settle-Payer` header is honored ONLY when the request's bearer is a
**deployed-app runtime key** (`SETTLEMESH_APP_API_KEY`, injected by
`settlemesh deploy --full-stack`). A normal CLI/user key returns
`403 payer_not_allowed`. So ship the app first (see the `ship-paid-app` skill),
then exercise the money path from the deployed backend — never locally.

The payer **value** must be a real logged-in user session — the `__settle_session`
cookie (durable, 7-day, preferred) or the `__settle_access` OAuth token — never an
API key. The auth gate passes those `__settle_*` cookies through to your server.

**Provision the charge first.** A paid endpoint must invoke a **published,
Approved, priced** capability or dynamic-service. Deploy injects the runtime key
but does NOT auto-create or price that charge — provision + price it first (see
the `sell-live-dataset` skill / `settlemesh provision`), or the first paid call
fails. Confirm the id exists and is callable:

```bash
settlemesh capabilities check <charge-id> --json
```

## Charge the user (server-side)

Your app's SERVER forwards the logged-in user's session so THEIR wallet pays:

```
POST {SETTLEMESH_BASE_URL}/v1/capabilities/<id>/invoke
Authorization: Bearer {SETTLEMESH_APP_API_KEY}          # the injected runtime key
X-Settle-Payer: {req.cookies.__settle_session}          # the user's session, NOT a key
```
No header ⇒ your own wallet pays (use that only for background jobs you fund).

## Quote before you charge

Read-only, no hold — show the user "≈ N Aev" before a costly action:

```bash
settlemesh quote <entrypoint-id> --input '{...}' --json
# HTTP: POST /v1/billing/quote  {"capability_id":"..."}   (or {"agent_id":"..."} / {"app_id":"...","endpoint_id":"..."})
# → { base_cost_credits, markup_bps, multiplier, total_credits, ... }
```

## Read the exact charge — and the user's balance

- The Aev actually billed is in the **`X-Settle-Charged-Aev`** response header
  (metered path also adds `X-Settle-Base-Cost-Aev` + `X-Settle-Markup-Aev`). Read
  that header; do NOT infer the charge from the provider's raw `usage.cost` in the
  body — that is the upstream cost, often a tiny number that rounds to "0.00".
- Show the user their own balance: `GET /v1/wallet/balance` with
  `X-Settle-Payer: <user session>` → `data.available_credits`. (Your OWN developer
  balance is `settlemesh aev balance`.)

## Preflight before real users

The app OWNER mints a short-lived self-test payer token and uses it exactly like a
user session — spends the owner's own wallet, so you can verify quote → capture →
ledger before onboarding anyone:

```
POST {SETTLEMESH_BASE_URL}/v1/apps/{app_id}/test-payer-token   → data.token
```
Send `data.token` in `X-Settle-Payer` alongside `Authorization: Bearer {SETTLEMESH_APP_API_KEY}`.
Rows are tagged `test_payer=true` (excluded from revenue views, but they still
count against daily spend caps). **Never ship this token as a user credential.**

## Billing errors to handle

- `app_allowance_required` (403) / `app_per_call_ceiling` (403) — user must set or
  raise the app allowance, or lower the call size.
- `app_allowance_exceeded` (402) — the app's per-user cap is hit.
- `insufficient_credits` (402) — user's balance is too low; the body carries a
  `topup_url` to hand them.
- `invalid_payer_token` (401) — the session expired; the user must re-log in.

Everything is billed in **Aev** (1 USD = 100 Aev). The markup you earn is credited
to your account; check it with `settlemesh aev balance`.
