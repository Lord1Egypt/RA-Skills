---
name: debug-openreceive-payment
description: >
  Diagnose a failing OpenReceive integration. Use when an OpenReceive-powered
  checkout misbehaves: the server refuses to boot, checkout routes return 403,
  404, 409, or 5xx, a paid invoice never settles, a swap refund seems
  unreachable, or the checkout UI renders nothing.
license: MIT
---

# Debug an OpenReceive payment

Work top-down: configuration, then the request, then settlement. Every guide
URL below is raw markdown — fetch it when the step needs it.

## 1. Run the doctor first

```sh
npx openreceive doctor                     # Node version, NWC_URI, swap config, wallet probe
npx openreceive doctor --db <db>           # + are openreceive_payments/openreceive_meta migrated?
npx openreceive doctor --url http://localhost:3000   # + are the routes actually mounted?
npx openreceive doctor --scan-build <dir>  # alone, after a production build: did a code reach it?
bin/rails openreceive:doctor               # Rails
manage.py openreceive_doctor               # Django
openreceive doctor --app main:app           # FastAPI
php artisan openreceive:doctor             # Laravel
wp openreceive doctor                      # WordPress
php bin/doctor                             # plain PHP: host script calling $engine->doctor()
```

Each failing line states its own fix. `npx openreceive debug-report` prints the
same diagnostics redacted, always exit 0 — safe to share.

## 2. Boot failures

| Symptom | Cause and fix |
| --- | --- |
| `MISSING_NWC` / "needs a receive-only NWC code" | `NWC_URI` is not in the server process env. A `.env` file alone is not enough — something must load it (`dotenv/config`, Next auto-load). Get a code: https://openreceive.org/get_a_nwc_code_to_receive_payments |
| `INVALID_NWC` / "not a valid NWC code" | The value is malformed (must be `nostr+walletconnect://` with 64-hex pubkey and secret, ≥1 `wss` relay). Re-copy it from the wallet. |
| "NOT receive-only" / spend methods advertised | The wallet minted a spend-capable code; OpenReceive fails closed because a leak would drain the wallet. Mint a receive-only code. Overriding (`allowSpendCapableWallet` / `OPENRECEIVE_ALLOW_SPEND_CAPABLE_NWC`) is a last resort. |
| Wallet preflight failed (methods/encryption) | The wallet must advertise `make_invoice` + `list_transactions` and NIP-04 or NIP-44 v2. Use a compatible wallet. |
| "The openreceive_meta table does not exist" / raw `no such table: openreceive_payments` | The migration was never applied. Node: `npx openreceive scaffold payments --orm <yours>`, then run the emitted migration through the app's normal workflow. Rails: `bin/rails generate openreceive:install`, then `bin/rails db:migrate`. Django: `manage.py openreceive_install <app> && manage.py migrate`. FastAPI: `openreceive scaffold payments --alembic --dialect <db>` (or `--sql`), then apply through the host workflow. Laravel: `php artisan openreceive:install && php artisan migrate`. Plain PHP: apply `OpenReceive\Storage\PaymentsSchema::statements($dialect)` through the host workflow. WordPress: check plugin activation/upgrades applied the tables. https://openreceive.org/guides/storage.md |
| "requires amountFor / onPaid / authorize / host" | The factory is missing a required hook — see the host contract in https://openreceive.org/guides/api-reference.md |

## 3. Request-time errors from the routes

| Status | Meaning | Where to look |
| --- | --- | --- |
| 403 FORBIDDEN | Your own `authorize` hook denied it, or the request looked cross-site. Check the session/cookie actually reaches the checkout routes. https://openreceive.org/guides/authorization.md |
| Never 403s — any visitor can mint, poll, or refund for any reference | The opposite failure: on Rails the generated `config.authorize = OpenReceive::ALLOW_ALL_AUTHORIZE` placeholder is still installed (the engine warns at boot; `bin/rails openreceive:doctor` reports it). Replace it with the app's real ownership check. https://openreceive.org/guides/authorization.md |
| 404 NOT_FOUND | `amountFor` returned `null` (unknown reference), or the `payment_hash` does not belong to that reference. |
| 409 CONFLICT | **Normal state, not a bug**: the reference already settled, or an unpaid checkout for that method is already live. Show it as order state; never retry-loop. |
| 503 retryable | The host hook failed while persisting the attempt (instructions withheld), or the wallet is unavailable. Read the server log for the underlying error. |
| Framework 404 / HTML error page | The router is not mounted, or mounted at a different prefix than the UI's `prefix` prop. `doctor --url` distinguishes these. |

## 4. Paid but never settles

- Settlement is opportunistic: any OpenReceive request runs one reconcile pass
  through a durable gate (min 3s between wallet scans, stretched by invoice
  age). A quiet server settles on the next request — or run the optional
  notifications worker: Rails `bin/rails openreceive:notifications`, Django
  `manage.py openreceive_notifications`, FastAPI
  `openreceive notifications --app main:app`, Laravel
  `php artisan openreceive:notifications`, WordPress `wp openreceive notifications`,
  or plain PHP's host script `php bin/notifications`. Node hosts run their
  separate worker using the notifications API. No web-process timer is missing.
- An unpaid attempt closes only after a successful wallet scan at/after expiry
  plus a 900s grace constant — a local clock alone never closes one. `expired`
  arriving "late" is correct.
- `onPaid` runs once per reference, first settled attempt only, inside the
  settlement transaction. If your fulfillment did not run, check whether the
  guarded `UPDATE … WHERE` matched zero rows (already transitioned).
  https://openreceive.org/guides/storage.md

## 5. Swaps and refunds

- A deposit that arrives short or late becomes `refund_required`; the payer
  claims it on a second visit. That needs a per-order URL you serve
  (`/checkout/:reference`, `syncUrl` on the drop-ins). Keep the
  `payment_hash`: `POST /swaps/status` reopens the attempt with no expiry
  window, while re-picking the coin mints a new deposit after ~30 minutes.
- Refunds exist only for swap deposits from `refund_required`. There is **no
  Lightning refund** — the wallet cannot spend. Do not chase one.
  https://openreceive.org/guides/swap-refunds.md
- "Payer reports two different amounts on a stablecoin checkout" (50.05 or
  50.03?): the deposit amount is a token quantity, `fee.pay_in_fiat` is its
  fiat valuation. Only `swap.deposit_amount` is an instruction. From 0.4.10 the
  packaged checkout renders a USD stablecoin's breakdown in the token and never
  shows `pay_in_fiat`; on an older bundle, upgrade `@openreceive/*`. To verify,
  read the row's `deposit_amount` and `fee` and confirm the UI shows only the
  deposit amount. A custom UI must call `createSwapFeeBreakdown(fee, swap)`
  with the swap, not the fee alone.

## 6. Checkout UI shows nothing

- The components require `prefix` — the exact base path the routes are mounted
  at (`"/openreceive"` unless you changed it).
- Import `@openreceive/react/styles.css` or `@openreceive/elements/styles.css`
  alongside the component registration. For standalone Django/Laravel/PHP,
  serve both `openreceive-checkout.js` (as a module) and
  `openreceive-checkout.css`. Django serves them from `static/openreceive/`
  via `collectstatic`; Laravel/PHP serve the unpacked standalone assets from
  the public directory. Check that both requests succeed and the custom
  element is registered. Do not process the compiled stylesheet with Tailwind.
- "invoice must not be an NWC connection string" means a server secret leaked
  into a browser payload — stop and fix the server response; never render it.
  https://openreceive.org/guides/frontend-checkout.md

## Still stuck

The full route/option/error reference:
https://openreceive.org/guides/api-reference.md · machine-readable contract:
https://openreceive.org/openapi.yaml · library bug reports:
https://openreceive.org/contact
