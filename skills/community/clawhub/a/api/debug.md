# Debugging — Symptom to Cause

Work symptom-first. Chains are ordered by probability; every step is a check, not a guess.

## The Universal First Three

1. Reproduce with raw curl (`-v`) — you see headers both ways, the TLS handshake, and every redirect. If curl succeeds and your code fails, the bug is client-side (SKILL.md Core Rule 1).
2. Read the failure's response BODY, not just the status — most APIs put the real cause (`error.code`, `message`, a docs URL) in the body of a 4xx.
3. Capture the request ID header (`x-request-id`, `request-id`, `cf-ray`) from the failing response — it is the only thing provider support can act on, and it expires from their logs.

## Works in curl, Fails in the SDK

| Difference | Check |
|---|---|
| Base URL / API version pin | SDKs pin an API version and sometimes a regional or versioned base URL — print the SDK's effective config, don't assume it matches your curl |
| Proxy env vars | `HTTP_PROXY`/`HTTPS_PROXY`/`NO_PROXY` honored by one stack and not the other — unset them for one run and compare |
| Default timeout | The SDK's default read timeout may be shorter than the endpoint needs (report exports, LLM calls) — set it explicitly (→ `resilience.md`) |
| Stale SDK | An old SDK against a current API sends removed params or misses required ones — check the SDK changelog against the API's (→ `versioning.md`) |
| Request shape | Turn on the SDK's debug/verbose logging and diff the emitted request against your working curl byte by byte — the diff names the cause |

## Works Locally, Fails in CI/Prod

| Difference | Check |
|---|---|
| Egress IP not on the provider's allowlist | 403 only from the server — compare egress IPs, not code |
| Env var absent or empty in CI | Empty ≠ unset: an empty `API_KEY` sends `Authorization: Bearer ` and 401s with a valid-looking setup |
| Missing CA bundle in slim/alpine images | TLS verification fails only in the container — install the OS ca-certificates package |
| Clock skew | Signed requests and JWTs reject on drifted clocks (S3 returns `RequestTimeTooSkewed` beyond its 15-minute window) — check `date` on the failing host first |
| IPv6 route | Provider resolves AAAA but the network can't route it — force IPv4 for one test request to isolate |
| Different secrets per environment | The staging key against the prod base URL (or vice versa) — print the key PREFIX (`sk_test_`/`sk_live_`), never the key |

## Connection Errors Decoded

| Error | Meaning | First move |
|---|---|---|
| Connection refused | Nothing listening at that host:port | Wrong port, http vs https, or sandbox vs live base URL |
| Connect timeout | Packets silently dropped | Egress firewall or dead host — try from another network before blaming code |
| Read timeout | Server accepted, answer never finished | Endpoint slower than your timeout (→ `resilience.md` Timeouts), or a streaming response read as a normal one (→ `streaming.md`) |
| Connection reset | Peer or a middlebox closed mid-request | Oversized payload, or an idle pooled connection reused after the LB killed it — one retry on a fresh connection is legitimate here |
| TLS: unable to get issuer / verify | CA or intermediate cert missing locally | Update the CA bundle; behind a corporate MITM proxy, its root cert must be installed |
| TLS: certificate expired | Server cert expired — or YOUR clock is wrong | Check the local date before filing a report |
| TLS: hostname mismatch | Wrong base URL, or a proxy answering for the host | Confirm the URL; test with and without the proxy |

## Mysterious 400s

- Missing or wrong `Content-Type` — the top cause (SKILL.md Traps).
- Numbers sent as strings or strings as numbers where the API is strict (→ `data-formats.md`).
- Double-encoded JSON: the body is a JSON string containing JSON — comes from calling a serializer on an already-serialized string.
- Hand-built form bodies with unescaped `&`, `=`, or `+` inside values — URL-encode every value.
- A BOM or trailing newline in a body read from a file.

## Intermittent Failures

- Some requests 401, others fine → token expiring mid-run or a refresh race (→ `auth.md` OAuth).
- First request after idle fails, retry succeeds → stale pooled connection (→ `resilience.md` Connection Pooling).
- Failures only under load → rate limit reached, or per-connection limits at the provider (→ `resilience.md`).
- 5xx with an HTML body → the provider's edge (CDN/load balancer) answered, not the API — check `Content-Type` before JSON-parsing any error body, or the parse error masks the real status.
- Same request, different results → load-balanced instances mid-deploy, or eventual consistency after a recent write: read-your-writes is not guaranteed across API calls.

## When You Are Truly Stuck

Build the shortest curl that shows the bug, then re-add headers, params, and body fields one at a time — the addition that breaks it names the subsystem and the pattern file to open next.
