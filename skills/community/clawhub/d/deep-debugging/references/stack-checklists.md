# Stack Checklists

Load only the relevant checklist for the current hypothesis.

## Generic API chain

```text
Client action → request construction → network → proxy/CORS → middleware → auth/guard → controller/route → service/domain → DB/cache/external API → response serialization → client handling
```

Split the chain and prove which half contains the failure.

## Auth / JWT / session

```text
□ Login endpoint returns expected status?
□ Token/session/cookie created? presence only, no raw token.
□ Client stores/sends credential correctly? header/cookie name only.
□ Server extracts credential from expected location?
□ Validation config matches signing config? key source names only.
□ Expiry/clock/skew/audience/issuer mismatch?
□ Role/permission/tenant guard failing after authentication?
□ Browser cookie rules: SameSite, Secure, domain, path, credentials mode?
```

Common root causes:
- token generated but not sent on follow-up request
- signing and validation read different env keys
- cross-site cookie blocked
- `401` auth failure confused with `403` authorization failure
- tenant/role guard throws after valid auth

## Frontend / React / Next.js

```text
□ Event handler runs?
□ State update happens and component re-renders as expected?
□ useEffect dependencies correct? no stale closure/infinite loop?
□ Network request payload correct?
□ Response handled correctly, including error path?
□ SSR/client boundary issue? window/localStorage/date/random mismatch?
□ Hooks called before any early return?
□ Cache/revalidation/stale data involved?
```

## Database / ORM

```text
□ Runtime schema matches migrations/generated client?
□ Query returns null/empty unexpectedly?
□ Relation/include/join missing?
□ Transaction boundary correct?
□ Unique constraint or FK error hidden by generic 500?
□ Connection pool exhausted or leaked?
□ Slow query has index? use EXPLAIN/ANALYZE safely.
□ Migration is backward-compatible with deployed code?
```

## External API / webhook

```text
□ Provider request built as docs require?
□ Auth header/key present by name only?
□ Status code and response body category captured redacted?
□ Rate limit, quota, or plan restriction?
□ Pagination/filter/timezone issue?
□ Signature verification and timestamp tolerance?
□ Retry/idempotency behavior prevents duplicates?
□ Provider SDK version changed?
```

## Deploy / CI / runtime

```text
□ CI failure is install, lint/typecheck, test, build, or deploy step?
□ Lockfile/package manager mismatch?
□ Node/Python/runtime version mismatch?
□ Env key present in target environment? names only.
□ Build-time vs runtime env confusion?
□ Port/host/healthcheck route mismatch?
□ Native dependency or binary unavailable in target image?
□ Cache artifact stale?
```

## Performance / memory

```text
□ Repro has baseline timing/memory/CPU evidence?
□ N+1 queries or looped network calls?
□ Missing DB index or inefficient query plan?
□ Large bundle or expensive hydration?
□ Unbounded queue, recursion, pagination, or stream buffering?
□ Event listener/interval/subscription cleanup missing?
□ Cache miss storm or retry storm?
```
