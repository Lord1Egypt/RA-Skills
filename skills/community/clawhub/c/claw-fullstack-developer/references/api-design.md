# API Design

Guidance for designing REST and GraphQL APIs that age well.

## REST vs. GraphQL — how to choose

**Default to REST.** It's simpler, better-cached, easier to debug, and matches HTTP semantics. Most apps need REST.

Pick GraphQL when:
- Multiple clients (web, iOS, Android) have genuinely different data needs from the same backend
- The app has deeply nested data and REST endpoints are proliferating into N+M mess
- A team has strong GraphQL experience already

Don't pick GraphQL for:
- A public API (the resolver N+1 problem and caching story are hard)
- A small app with one frontend (overkill — REST is faster to build)

tRPC is a third option for monorepos where frontend and backend share types. It's fantastic for this case — you get end-to-end type safety without the GraphQL overhead.

## REST design

### URL structure
- Resources are **nouns, plural**: `/users`, `/orders`, not `/getUsers` or `/user`.
- Use HTTP methods correctly: `GET` (read, idempotent, cacheable), `POST` (create), `PUT` (full replace), `PATCH` (partial update), `DELETE` (remove).
- Nest when there's a true parent-child: `/orders/{id}/items`. Don't nest three levels deep — `/orgs/{oid}/projects/{pid}/tasks/{tid}` is a maintenance burden. Prefer `/tasks/{tid}` with scope enforced by auth.

### Path patterns
```
GET    /users                 # list (with query params for filtering/pagination)
POST   /users                 # create
GET    /users/{id}            # read one
PATCH  /users/{id}            # partial update
DELETE /users/{id}            # delete

GET    /users/{id}/orders     # sub-resource list
```

### Status codes — use them correctly
- **200** OK — successful read or update with body returned
- **201** Created — successful creation; include the new resource in the body and a `Location` header
- **204** No Content — successful operation with no body (e.g., DELETE)
- **400** Bad Request — malformed request or validation failure
- **401** Unauthorized — not authenticated
- **403** Forbidden — authenticated but not allowed
- **404** Not Found — resource doesn't exist (or authed user can't see it — don't leak existence)
- **409** Conflict — state conflict (duplicate email, version mismatch)
- **422** Unprocessable Entity — validation failure (some APIs prefer this over 400)
- **429** Too Many Requests — rate limited
- **500** Internal Server Error — server bug (log it, page oncall)
- **503** Service Unavailable — temporarily down

Don't return 200 with `{"error": "..."}`. Use the HTTP status. Clients rely on it for retry logic and error handling.

### Error response shape
Pick one shape and stick to it across every endpoint:
```json
{
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "Human-readable message.",
    "details": [
      { "field": "email", "issue": "already_taken" }
    ]
  }
}
```

The `code` is machine-readable (clients switch on it). The `message` is for humans/logs. `details` is optional structured info.

### Pagination
Two styles, pick one:

**Cursor-based (recommended)** — handles inserts mid-stream, scales well:
```
GET /posts?limit=20&cursor=eyJpZCI6MTIzfQ==
Response:
{
  "data": [...],
  "next_cursor": "eyJpZCI6MTQzfQ==",
  "has_more": true
}
```

**Offset-based** — simpler, fine for small datasets or stable-ordered results:
```
GET /posts?page=2&page_size=20
Response:
{
  "data": [...],
  "page": 2,
  "page_size": 20,
  "total": 847
}
```

Never return unbounded lists. A default `limit` (50–100) protects the DB and the client.

### Filtering, sorting, searching
- Filtering: `?status=active&role=admin`
- Sorting: `?sort=created_at` (default asc), `?sort=-created_at` (desc). Or separate `sort_by` and `order` params.
- Searching: `?q=search+terms` for simple search. For complex, a dedicated endpoint (`POST /search`) with a body.

### Versioning
- **URL version** (`/v1/users`) — most common, easy to understand, easy to route differently.
- **Header version** (`Accept: application/vnd.company.v1+json`) — cleaner URLs, harder to test.

Pick one, document it. Prefer URL versioning for public APIs.

Avoid version proliferation: it's easier to keep v1 stable and add optional fields than to ship v2, v3, v4. Only bump major version for breaking changes.

### Authentication patterns
- **Bearer tokens** (JWT or opaque): `Authorization: Bearer <token>`
- **API keys** (machine-to-machine): `Authorization: Bearer <key>` or `X-API-Key: <key>`
- **Session cookies** (same-site web apps): HTTP-only, Secure, SameSite=Lax

See `references/authentication.md` for the auth system design.

### Idempotency
Clients retry on network errors. If the user hits "Pay Now" and the browser disconnects, the request may or may not have happened. Idempotency keys solve this:

```
POST /payments
Idempotency-Key: user-session-abc-attempt-1
Body: { amount: 100, ... }
```

The server checks: have I seen this key before? If yes, return the stored response. If no, process and store. Stripe, AWS, and other serious APIs all do this.

Apply to: payment creation, sending emails, creating external resources, anything costly or visible.

### Rate limiting
Set limits on every endpoint. Signal them with:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 47
X-RateLimit-Reset: 1712345678
Retry-After: 30
```

Return 429 when exceeded. Tighter limits on auth endpoints (login, signup, password reset) — these are brute-force targets.

### OpenAPI / docs
Generate OpenAPI specs automatically. FastAPI does this for free; Fastify has a plugin; NestJS too. Publish at `/docs` (or `/api-docs`). Up-to-date, auto-generated docs beat a hand-written `API.md` that's out of date.

## GraphQL design

### Schema design
- **Nodes and edges.** Define clear types; relationships are edges between types.
- **Keep mutations narrow.** A `createUser` mutation takes user fields, not an omnibus "doEverything" input.
- **Consistent naming.** Types in `PascalCase`, fields in `camelCase`, enums in `SCREAMING_CASE`.
- **Nullability matters.** Be deliberate — `User.email: String!` (always present) vs `User.phone: String` (optional). Don't make everything non-null by default.
- **Relay-style connections** for paginated lists: `posts(first: 10, after: "cursor"): PostConnection`.

### Resolver pitfalls
- **N+1 queries.** A naïve resolver fetches the parent list, then per-item fetches children → N+1 DB calls. Use DataLoader to batch and cache.
- **Depth limits / complexity limits.** Public APIs need these; a malicious client can construct a query that asks for 1M items via deeply nested fields. Use `graphql-depth-limit` and query complexity analysis.
- **Auth at every resolver,** not just the entry point. A user who can query `user(id)` may still be able to reach `user.privateField` unless the field-level auth says otherwise.

### Tooling
- **Server**: Apollo Server, GraphQL Yoga, or Pothos (TypeScript-first, code-first).
- **Client**: Apollo Client, Relay, or urql. Apollo is the most common default.
- **Codegen**: `graphql-codegen` generates TypeScript types from the schema. Use it.

## tRPC (TypeScript monorepo)

If both backend and frontend are TypeScript in one repo, tRPC gives you end-to-end type safety with near-zero config:

```ts
// server
export const appRouter = router({
  getUser: procedure
    .input(z.object({ id: z.string() }))
    .query(({ input }) => db.user.findUnique({ where: { id: input.id } })),
});
export type AppRouter = typeof appRouter;

// client
const user = await trpc.getUser.query({ id: "123" }); // fully typed
```

Use tRPC when: monorepo, TypeScript, no non-TS clients. Avoid when: public API, mobile clients, polyglot stacks.

## Webhooks

When your app needs to notify external systems of events:

- **Sign every payload.** Include a signature header (HMAC-SHA256 of the body with a secret). The receiver verifies it.
- **Timestamp the payload** and include it in the signature. Reject requests older than 5 minutes to prevent replay.
- **Retry with exponential backoff** on 5xx / timeout. Give up after a reasonable limit (24h, 48h).
- **Idempotency**: include an event ID. Receivers dedupe on it.
- **Endpoint format**: `POST` with JSON body. Respond 2xx fast; queue the actual work.

When your app receives webhooks (Stripe, GitHub, etc.):
- Verify the signature before processing anything.
- Respond 2xx immediately; do the work async via a job queue.
- Store events by their ID; dedupe on retries.

## API design — what to avoid

- **RPC-style names in REST**: `/getUserById`, `/deleteOrder`. Use resource URLs + HTTP methods.
- **Inconsistent response shapes.** If `GET /users` returns `{data: [...]}` but `GET /orders` returns a bare array, clients suffer. Pick a shape; stick to it.
- **Returning nothing useful on POST.** Creating a resource without returning it forces the client to do a second GET. Return the created object.
- **Allowing `DELETE` without a 2xx idempotent contract.** A second `DELETE` on a deleted resource should return 204 or 404 — both are fine, just be consistent. Don't return 500.
- **Unbounded result sets.** Always paginate.
- **Exposing internal IDs** (database auto-increments) in URLs. Use UUIDs.
- **Mixing plural/singular.** `/user/{id}` and `/orders`. Pick plural for everything.
