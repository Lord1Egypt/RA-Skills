# Security — The API Attack Surface Beyond Login

Reference patterns only: every credential below is a placeholder name for the reader to replace, and no example here is meant to be executed as written. Identity and tokens are `auth.md`; this file is everything an authenticated attacker can still do.

## Object-Level Authorization (the top API vulnerability)

- `GET /orders/{id}` that loads by id and returns it lets any authenticated user read every order. Route-level auth answers "is this a user", not "is this *their* order".
- The fix is in the query, not in an `if`: `select(Order).where(Order.id == oid, Order.owner_id == user.id)` — one statement that cannot be forgotten halfway down a handler.
- Multi-tenant systems scope every query by tenant, resolved once in a dependency (`dependencies.md`). A single unscoped query is a cross-tenant leak.
- Return 404 rather than 403 when the existence of the object is itself private; 403 confirms the id is real.
- Sequential integer ids make enumeration trivial. UUIDv4 or a random public id removes the easy sweep — it is defense in depth, never a substitute for the ownership filter.

## Mass Assignment

- A request model that accepts every column lets a client send `{"role": "admin", "credit": 9999}`. Use a `Create`/`Update` model containing only client-settable fields (`pydantic.md`).
- `model_config = ConfigDict(extra="forbid")` turns a smuggled field into a 422 instead of a silent ignore — and catches your own typos.
- Never `Model(**payload.model_dump())` straight into an ORM object without an explicit allowlist; the allowlist is the response to "we added a column and it became writable".

## Input That Reaches Something Dangerous

| Sink | Rule |
|---|---|
| SQL | Bound parameters only; `text("... WHERE name = :n")` with parameters, never f-strings. Table and column names cannot be parameterized — map user input through a dict of allowed names |
| Shell | No user input in a shell string; argument list, no `shell=True` |
| Filesystem | Never join user input into a path: generate your own key, or resolve and verify the result is inside the base directory (`..%2f` survives naive checks) |
| Archives | Zip entries can contain `../` paths and symlinks; validate every member before extracting |
| Deserialization | JSON only; `pickle` of client data executes code |
| URLs you fetch (SSRF) | Allowlist hosts, resolve the DNS name and reject private ranges and `169.254.169.254`, disable redirects or re-validate after each hop |
| HTML rendering | Autoescaping on; never `\| safe` on user content (`templates.md`) |
| Regex on user input | A catastrophic pattern turns one request into 100% CPU; bound input length and avoid nested quantifiers |

## Limits Are Security Controls

- Body size, upload size, and multipart part count: unbounded means one request can exhaust memory or disk (`streaming.md`).
- Pagination `limit` capped server-side; an uncapped `?limit=1000000` is a denial-of-service parameter (`performance.md`).
- Timeouts on every outbound call, and a bound on fan-out concurrency (SKILL.md rule 7).
- Rate limits on authentication, password reset, and anything that sends email or SMS — those spend money as well as CPU (`auth.md`).
- Recursion depth in nested pydantic models: deeply nested JSON is a cheap way to burn validation CPU; cap nesting where the shape allows.

## Response Headers

| Header | Value | Stops |
|---|---|---|
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` | Downgrade to http after the first visit |
| `X-Content-Type-Options` | `nosniff` | Browsers guessing a JSON response is HTML |
| `Content-Security-Policy` | Tight for any HTML you serve | Injected scripts (`templates.md`) |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | Leaking URLs with ids to third parties |
| `Cache-Control` | `no-store` on authenticated responses | Private data cached by a shared proxy |

A pure JSON API needs `nosniff` and HSTS at minimum; the rest matter as soon as the app renders any HTML. Set them at the proxy or in a small pure-ASGI middleware (`middleware.md`).

## Data Exposure

- The response model is the filter: what is not declared is not sent, which is how hashes, internal flags, and other users' fields stay out of a payload (`pydantic.md`).
- Errors leak more than payloads do: upstream bodies, SQL fragments, and file paths inside `detail` all reach the client (`errors.md`).
- Debug mode and the interactive docs expose route inventory and model shapes — disable them for internal APIs (`openapi.md`, `settings.md`).
- Logs are an exfiltration path too: redact tokens, cookies, and request bodies from auth routes (`observability.md`).

## Dependencies And Supply Chain

- Pin with a lockfile and rebuild regularly: a base image or wheel pinned for six months carries six months of known CVEs.
- Audit in CI (`pip-audit` or equivalent) and again at the registry, because CVEs are published after your build.
- Weigh a new dependency by what it can reach: anything imported into the API process runs with the API's credentials and network access.

## Pre-Ship Checks

- Every read and write filtered by ownership or tenant, in the query
- Request models limited to client-settable fields; `extra="forbid"` where the client is your own front end
- Body, upload, and pagination limits set; every outbound call has a timeout
- No user input reaching SQL, shell, a path, a template's raw filter, or a fetched URL without containment
- Security headers set; docs and debug disabled where the API is internal
- Secrets typed `SecretStr`, absent from logs, errors, and the OpenAPI schema
