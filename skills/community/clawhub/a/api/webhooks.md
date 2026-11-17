# Webhook Traps

## Handler Order (the only correct one)

1. Capture the **raw** request body (bytes, before any JSON middleware)
2. Verify HMAC signature over the raw body, constant-time comparison
3. Check the signed timestamp is recent (Stripe's default tolerance: 5 minutes; Slack recommends the same window) — signature alone doesn't stop replays
4. Dedupe by event ID against a store you keep at least as long as the provider retries (Stripe retries for up to 3 days)
5. Enqueue durably, return 2xx immediately — target well under the provider's timeout
6. Process async from the queue

Steps out of order are the root cause of most webhook bugs below.

## Delivery

- Provider timeouts are short (5-30s); processing inline = timeout = retry = duplicates. Ack fast, work async (Handler Order §5)
- Provider retry = same event multiple times; handler MUST be idempotent — dedupe by event ID, not by payload hash (payloads can legitimately repeat)
- Delivery order not guaranteed: `updated` can arrive before `created`. Never build state from event sequence; on receipt, fetch current state from the API and treat the event as a "something changed" ping
- Provider IPs change; an IP allowlist breaks silently on their next migration — signature verification is the durable control

## Verification

- HMAC comparison with `==` = timing attack; use the constant-time compare every crypto stdlib ships
- Signature header names are non-standard (`Stripe-Signature`, `X-Hub-Signature-256`, `X-Twilio-Signature`) and so are the schemes — check the provider's section, don't pattern-match from another service
- Body parsed/re-serialized by middleware before verification = signature never matches: JSON key order and whitespace changed. This is the #1 "signature invalid but secret is right" cause
- Verifying but skipping the timestamp = replayable forever with one captured request

## Processing

- Returning 200 before durable enqueue = crash after ack loses the event and the provider won't resend
- Returning 500 after partial side effects = provider retries = the completed part runs twice; make side effects idempotent or ack first and retry internally
- Removed/renamed payload fields your code expects = undefined/null crashes; treat webhook payloads as untyped input, validate before use
- New unknown fields must not fail parsing — providers add fields without notice; strict schemas break on their schedule, not yours

## Development

- Localhost isn't reachable by the provider; you need a tunnel (ngrok or similar), and the URL changes each session — re-register the endpoint or use the provider's CLI forwarder (Stripe CLI `listen` avoids re-registering)
- Provider webhook logs expire quickly; when debugging, capture and store raw deliveries on your side from the first test
- Some providers have no manual "resend" button — trigger a real event to test, or keep captured payloads to replay locally

## Security

- Public endpoint without verification = anyone can forge events ("payment succeeded" from an attacker)
- Same signing secret across environments = staging deliveries accepted by production; one secret per environment
- Handler that fetches URLs from the payload = SSRF vector; never follow payload-supplied URLs to internal hosts
- Detailed error bodies in webhook responses leak internals to whoever probes the endpoint; return status codes, log details server-side
