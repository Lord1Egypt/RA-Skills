# API Reference Template

Location: `/backend/docs/api.md`
For large backends: one file per subsystem, with an index in `/backend/docs/api.md`.

This file is the contract between backend and frontend (or any API consumer). It must be
kept in sync with actual controllers. When an endpoint changes, this file changes in the
same commit.

---

## File Structure Options

**Small backend (< ~20 endpoints):** Single `/backend/docs/api.md`.

**Large backend:** Split by subsystem:
```
/backend/docs/
  api.md              ← index only, links to subsystem files
  api-auth.md
  api-billing.md
  api-users.md
```

---

## Index Template (for split files)

```markdown
# API Reference

Base URL: `https://api.example.com/v1`
Auth: Bearer token in `Authorization` header. All endpoints require auth unless marked public.

| Subsystem | File | Endpoints |
|---|---|---|
| Auth | [api-auth.md](./api-auth.md) | POST /auth/login, POST /auth/logout, POST /auth/refresh |
| Users | [api-users.md](./api-users.md) | GET /users/:id, PATCH /users/:id, DELETE /users/:id |
| Billing | [api-billing.md](./api-billing.md) | GET /billing/plans, POST /billing/subscribe |
```

---

## Endpoint Template

Use this block for every endpoint. Do not abbreviate.

```markdown
---

### POST /auth/login
**[PUBLIC]** ← include this tag if no auth required

Authenticates a user and returns a signed JWT.

**Request**

| Location | Name | Type | Required | Description |
|---|---|---|---|---|
| Body | email | string | ✓ | User's email address |
| Body | password | string | ✓ | Plaintext password |

**Response — 200**
```json
{
  "token": "eyJhbGci...",
  "expiresIn": 900
}
```

**Status Codes**

| Code | Meaning |
|---|---|
| 200 | Login successful |
| 400 | Missing or malformed body |
| 401 | Invalid credentials |
| 429 | Rate limit exceeded |

**Source**
- Controller: `src/routes/auth.js → loginHandler`
- Services: `passwordService.compare`, `tokenService.issueToken`
```

---

## Instructions for AI agents

1. **Every externally callable endpoint gets a block.** No exceptions. "External" means any
   route that a browser, mobile app, webhook, or another service calls. Internal-only helper
   functions are not documented here.

2. **The Source section is mandatory.** Frontend and integration developers need to know
   exactly where to look when something breaks. Always include the controller file path and
   the service methods involved.

3. **Status codes must be exhaustive.** Document every status code the endpoint can actually
   return. If you're not sure, read the controller. Do not list codes it cannot return just
   because they're common.

4. **Request schema must match validation code.** Open the Zod schema (or equivalent) and
   copy fields from there, not from memory or assumption.

5. **Keep descriptions to one sentence.** The request/response schemas are self-documenting.
   The description is for "why does this endpoint exist and what does it do for the caller."

6. **Update this file in the same change as the code.** If an endpoint is added, modified,
   or removed — the API doc changes in that same PR. Never let them drift.

7. **Mark public endpoints clearly.** Any endpoint that doesn't require authentication must
   be tagged `[PUBLIC]` to prevent accidental over-permissioning on the frontend side.

---

## Common Mistakes to Avoid

| Mistake | Correct approach |
|---|---|
| Documenting what an endpoint *should* do | Document what it *actually does* — read the code |
| Listing only the happy-path status code | Document all realistic codes including 4xx |
| Omitting the Source mapping | Always include controller file + service methods |
| Copy-pasting endpoint docs without updating | Verify every field against live code |
| Documenting removed endpoints | Delete them — API doc is the live contract |
