---
name: cofferline
description: Manage an autonomous agent's on-chain treasury and prediction-market risk via Cofferline — keep a machine wallet funded, gassed, converted, spend-controlled, and accounted for, non-custodially over a REST API; for prediction-market agents (Polymarket) it also vaults trade-scoped credentials write-only, enforces hard risk policies (per-market caps, daily loss stops) server-side from the real books, routes policy-gated LIMIT orders, and journals fills. Use when an agent needs to hold/convert/spend crypto, trade prediction markets under risk limits, set a spending policy, grant scoped revocable signing authority, pay for services in USDC (x402), or produce an audit trail. Cofferline is non-custodial of your wallet and its keys (prepaid fee balances and optional venue credentials are enumerated exceptions in the authority/custody matrix).
---

# Cofferline — treasury for autonomous agents

Cofferline is the treasury + risk layer for a machine wallet: it keeps an
agent's balance funded, gassed, converted, controlled, and accounted for —
**non-custodially**. For prediction-market agents (Polymarket) it is
the back office: sealed trade-scoped credentials, hard risk policies enforced
server-side from your real books, order routing and fill journaling — one API.
It is **non-custodial of your wallet and its keys**: it never holds your
connected account's owner key, and execution authority comes from **scoped,
revocable on-chain session-key delegations** you grant, bounded by a **policy**
you set. Some surfaces are enumerated exceptions where the platform does hold
funds or authority — a prepaid fee balance is platform-held USDC, and optional
venue trade credentials are held sealed (a Polymarket signer owns your funder
wallet) — all laid out in the authority/custody matrix (\`{web}/docs/custody\`,
machine-readable at \`{web}/legal/custody.json\`). Identity is your wallet
(Sign-In-With-Ethereum) — no signup, email, or CAPTCHA.

Pricing is data, not doctrine: read the manifest's `pricing` object — it is
the source of truth and rates may change. Currently discovery, live venue
quotes, pre-flight checks, and reads are free; execution surfaces (conversion
intents, delegated execution, prediction-market orders) are metered at the
published rates, payable in USDC via x402 or prepaid balance — no cards.

## Discover first — never hardcode endpoints

Everything is driven by the machine-readable manifest. Fetch it and read
`capabilities` (the source of truth for what exists), `api.base`, `auth`,
`pricing`, and `tos`:

```
GET https://cofferline.com/.well-known/cofferline.json
```

The typed golden path is also machine-executable at `{web}/quickstart.json`, and
there is an MCP server at the manifest's `mcp.url` exposing the same API as
Model Context Protocol tools if your harness prefers that over raw HTTP. A
rendered API reference lives at `{web}/docs/api` (raw Markdown per section
at `{web}/docs/api/{section}.md`), generated from the same schemas that
validate requests.

## The operating procedure

Numbers map to `quickstart.json` steps; every URL comes from the manifest.

1. **Discover** — `GET {manifest}`; read capabilities, pricing, auth, ToS hash.
2. **Verify terms** — hash the served ToS prose and confirm it equals
   `manifest.tos.sha256`; the structured terms assert `non_custodial: true`
   (scoped to your wallet and its keys) and carry a `custody` object enumerating
   what the platform holds — full matrix at `{web}/legal/custody.json`.
3. **Evaluate** — `POST {api}/v1/quotes` (currently free, no auth): best
   full-size venue quote vs a sliced-execution estimate, all numbers from
   live venue APIs.
4. **Authenticate** — `POST {api}/v1/auth/challenge` with `{"address":"0x…"}`,
   sign the returned SIWE message with your own key (EOA, EIP-1271, or ERC-6492
   all verify), then `POST {api}/v1/auth/verify` → a `cl_sess_…` bearer token.
5. **Get a key** — `POST {api}/v1/keys` → a durable `cl_key_…` (returned once;
   scopes `read`/`write`/`admin`). Use it as the Bearer for everything below.
6. **Fund** — `POST {api}/v1/balance/topup` answers `402` with exact-scheme
   requirements. Pay via x402 (see below). Metered intents debit this balance.
   To never hit a mid-workflow 402, `PUT {api}/v1/balance/auto-topup`: a
   threshold plus pre-signed fixed-value EIP-3009 authorizations; when a fee
   debit crosses the threshold, Cofferline settles the next one and refills
   the balance. Each is cancellable on-chain by the payer at any time.
7. **Set a policy** — `PUT {api}/v1/policies`: float targets, execution bounds
   (slippage, slice size, venues), gas strategy, spend limits, and — for
   prediction markets — `prediction_markets` risk rules. Its hash travels
   into every intent and ledger row; nothing executes that the policy forbids.
8. **Delegate** — `POST {api}/v1/delegations/prepare` returns ONE EIP-712 digest;
   sign it with the account owner's key; `POST …/delegations/{id}/confirm`
   activates it. The permission {call allowlist, expiry, rate limit} installs
   on-chain with the first delegated execution. Revoke any time with `DELETE`
   — revocation is your own transaction and never requires Cofferline.
9. **Operate** — `POST {api}/v1/intents` for conversions and gas top-ups. The
   executor acts under your delegation; every fill is ledgered and aborts are
   typed and honest. Pre-check first with `POST {api}/v1/checks`.
10. **Account** — `GET {api}/v1/statements?wallet=0x…&period=YYYY-MM`:
    deterministic, content-addressed statements (JSON or CSV). Same period twice
    yields identical bytes — derived from real ledger rows, never invented.

## Prediction markets (Polymarket)

Cofferline routes venue orders with **your own trade-scoped credential** (BYO;
Cofferline mints nothing) and enforces the wallet's `prediction_markets`
policy rules — per-market cap, daily loss stop, resolution-exposure cap,
optional market allowlist — **server-side, floored by a ledger-derived
exposure figure** computed from journaled fills, not just your self-reported
state. Orders are LIMIT-only. Per-order metering is base + bps of notional at
the manifest's published rate; **cancels are free** — never hesitate to
reduce risk over a fee.

The flow (all URLs from the manifest; Bearer auth throughout):

1. **Store a credential** — `POST {api}/v1/pm/credentials`. Polymarket: the
   dedicated trade-signer key authorized for your proxy/funder wallet — never
   your funds key. The credential is verified live against the venue before it
   is stored, sealed AES-256-GCM at rest, and is **write-only**: no endpoint
   ever returns the material.
2. **Check trade-readiness** (Polymarket) — `GET {api}/v1/pm/onboarding/{address}`:
   live status of the six on-chain approvals order matching requires, plus
   owner-signable calldata for any that are missing. Your funds wallet signs
   and submits them itself — Cofferline never signs an approval.
3. **Set the risk policy** — `PUT {api}/v1/policies` with `prediction_markets`
   (`per_market_cap_usd`, `daily_loss_stop_usd`, `max_resolution_exposure_usd`,
   optional `market_allowlist`, optional `exposure_basis`: `"gross"` — the
   default — or `"net"`, under which YES and NO held in the same market offset
   against your caps; different markets still sum, resting orders always count
   gross, and a platform-imposed exposure ceiling stays gross regardless).
4. **Pre-flight** — `POST {api}/v1/checks/pm-order`: would this order pass the
   policy right now? Free, side-effect-free, and available even where
   execution is disabled. The response names the exposure basis used and shows
   both bases' figures, so a gross policy can see what `"net"` would change.
5. **Order** — `POST {api}/v1/pm/orders` (LIMIT). A forbidden order is refused
   with the violated rule and **never transmitted**. Cancel with
   `DELETE {api}/v1/pm/orders/{venue}/{order_id}` (free, its own generous rate
   budget). Recover your resting book any time with
   `GET {api}/v1/pm/orders?credential_id=…` (venue-authoritative), or flatten
   it in one call: `DELETE {api}/v1/pm/orders?credential_id=…[&market=…]`.
6. **Sync fills** — `POST {api}/v1/pm/fills/sync`: journals unseen venue fills
   (and settlements) into the wallet's double-entry ledger, idempotently — the
   venue fill id is the settlement identity, so calling after every order
   never double-books. This is what feeds the server-side exposure floor.
   Polymarket journals CLOB trades.

## Paying with x402

When an endpoint needs payment it returns `402` with exact-scheme requirements
(chain, USDC asset, amount, `payTo`). Construct an **EIP-3009
`transferWithAuthorization`** signed by your wallet — you need **zero ETH/gas**,
Cofferline submits the settlement for you — base64 it into the `X-PAYMENT`
header, and retry the same request. The retry answers `202`: the settlement is
on-chain and your balance is credited once the transfer reaches finality —
minutes on Base, not instant. The authorization nonce makes it exactly-once, so
retries and replays never double-credit. Poll `GET {api}/v1/balance` for it.

## Rules that always hold

- **Non-custodial of your wallet and its keys.** No code path stores or receives
  your wallet's private key; on-chain authority is a scoped, revocable session-key
  delegation enforced by your own ERC-4337 account. Enumerated exceptions (held
  by the platform): a prepaid fee balance is platform-held USDC service credit,
  auto-topup stores pre-signed USDC authorizations (API deletion is not on-chain
  revocation), and venue credentials are held sealed write-only (a Polymarket
  signer owns your funder wallet). See the authority/custody matrix
  (`{web}/docs/custody`).
- **Policy-bounded.** Requests may only _tighten_ the policy (slippage ≤ policy,
  venues ⊆ allowlist); anything beyond it is refused with `POLICY_VIOLATION`.
- **Fees are published, machine-readably.** Whatever the current rates, they
  are always in the manifest's `pricing` object and payable via 402 — read
  them there; never assume a number from prose.
- **Honest numbers.** Quotes are live venue prices; reports are computed from
  real fills; a report is `null` until fills exist — never synthetic.
- **Errors are typed** — `{code, message, remediation, docs_url, request_id}`.

## Reference

- Manifest: `{web}/.well-known/cofferline.json`
- Typed steps: `{web}/quickstart.json` · Prose: `{web}/docs/agent-quickstart`
- OpenAPI (generated from the validating schemas): `{api}/openapi.json` ·
  Rendered API reference: `{web}/docs/api` (`{api}/docs` 301s there)
- MCP tools: `{mcp}` (Bearer forwarded verbatim) · llms.txt: `{web}/llms.txt`
