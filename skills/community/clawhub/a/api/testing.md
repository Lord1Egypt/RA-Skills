# Testing Integrations — Sandbox, Mocks, Drift

## Sandbox First

- How sandbox is selected differs per provider: separate keys (Stripe `sk_test_`), separate base URL (PayPal sandbox host), or a separate account/tenant — the service section states which; `credentials.md` names the variables.
- Magic test values exist to test FAILURE, not just success: Stripe's `4242 4242 4242 4242` succeeds, and its other documented test cards produce specific declines — a suite that only uses the success value ships untested decline handling.
- Sandbox ≠ production: latency is lower, rate limits differ, emails/SMS don't actually deliver, and some features are stubbed — passing sandbox proves the request shape, not the production behavior. Sandbox events still fire webhooks: point them at your dev tunnel (→ `webhooks.md` Development).
- A test suite pointed at live keys is an incident, not a test run. Gate before the suite starts: assert the key prefix or base URL is the sandbox one.

## Record and Replay

- Record real sandbox responses (VCR-style cassettes) and replay them in CI: fast, deterministic, zero rate-limit spend.
- Scrub before commit: cassettes capture auth headers, cookies, and account IDs — a committed cassette is a leaked credential.
- Re-record on every API version bump (→ `versioning.md` Migration Procedure): stale cassettes make tests pass against an API that no longer behaves that way.

## Mock Discipline

- A mock written from the docs encodes your misreading of the docs; seed mocks from recorded real responses.
- Mock the failures providers won't produce on demand: 429 with `Retry-After`, 500, timeout, malformed JSON, an HTML error page from the edge (→ `debug.md`) — retry and fallback code is exactly the code that otherwise ships untested.
- Contract smoke in CI: one real sandbox call per critical endpoint, daily or on deploy — catches expired keys, version drift, and provider-side changes that mocks by definition cannot.

## Webhook Testing

- Provider CLI forwarders (Stripe CLI `listen`) beat re-registering tunnel URLs every session; keep captured raw deliveries as replay fixtures (→ `webhooks.md` Development).
- Test signature verification with a wrong-secret payload — a handler that accepts it has failed security review, not just a test.
