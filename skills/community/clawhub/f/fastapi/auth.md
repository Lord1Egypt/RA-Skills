# Auth — Identity, Tokens, and Authorization in the Dependency Graph

FastAPI ships the *plumbing* for auth, not auth itself: `OAuth2PasswordBearer` extracts a header and documents a scheme — it never validates anything. Everything below the extraction is yours.

Reference patterns only: key names and settings fields below are placeholders for the reader to replace, and no example is meant to be executed as written.

## The Shape

```python
oauth2 = OAuth2PasswordBearer(tokenUrl="/v1/auth/token")

async def get_current_user(token: Annotated[str, Depends(oauth2)], db: DbSession) -> User:
    try:
        payload = jwt.decode(token, settings.jwt_public_key, algorithms=["RS256"],
                             audience=settings.audience, issuer=settings.issuer)
    except JWTError:
        raise HTTPException(401, "Not authenticated", headers={"WWW-Authenticate": "Bearer"})
    user = await db.get(User, payload["sub"])
    if user is None or not user.is_active:
        raise HTTPException(401, "Not authenticated", headers={"WWW-Authenticate": "Bearer"})
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]
```

- 401 means "no valid identity", 403 means "identity known, not allowed". Returning 403 for an expired token makes clients retry forever instead of refreshing.
- `WWW-Authenticate: Bearer` on the 401 is what tells a compliant client to re-authenticate.
- One dependency for authentication, separate ones for authorization: `CurrentUser` proves who; `require_role("admin")` decides what.

## Verifying a JWT Properly

Every one of these is a real bypass when skipped:

| Check | Why |
|---|---|
| `algorithms=[...]` explicitly | Without it, a library may honour the token's own `alg` — including `none`, or HS256 verified against a public key you published |
| `aud` and `iss` | A valid token from a different service or tenant is otherwise accepted |
| `exp` and `nbf` | Verified by default in most libraries; confirm your library does and that clock skew allowance is small (seconds, not hours) |
| Signature key source | Fetch JWKS once at startup or cache it with a TTL; fetching per request adds an upstream to every call and a new failure mode |
| `sub` shape | Treat it as an opaque string; casting to int breaks the day the provider issues UUIDs |

- Access tokens short (minutes), refresh tokens long and revocable. Revocation needs state — a deny list in Redis keyed by `jti`, or a `token_version` column compared on each request; a stateless JWT cannot be un-issued.
- Symmetric (HS256) is fine when the same service signs and verifies; asymmetric (RS256/EdDSA) once anything else must verify, so the private key never leaves the issuer.

## Passwords

- Hash with bcrypt, scrypt, or Argon2id. These are deliberately slow: bcrypt at the common cost factor 12 lands in the hundreds of milliseconds on server hardware — that is per login, by design.
- That cost is exactly why the login endpoint must not hash on the event loop. Declare the login route `def`, or `await run_in_threadpool(verify, ...)` from an async route (`async.md`).
- Compare with the library's `verify`, never `==`, and run the hash even when the user does not exist (compare against a dummy hash) so response time does not enumerate accounts.
- Rehash on login when the cost factor has been raised: verify with the stored hash, then store a fresh one.

## Sessions and Cookies (browser clients)

- Cookie flags are the security: `HttpOnly` (no JavaScript access), `Secure` (HTTPS only), `SameSite=Lax` as the default, `SameSite=None; Secure` only when a third-party context genuinely needs it.
- `SameSite=Lax` blocks the cookie on cross-site POSTs, which removes most CSRF exposure; anything looser needs a real CSRF token (double-submit or synchronizer) validated on every unsafe method.
- Server-side sessions (id in the cookie, state in Redis) give instant revocation and small cookies; JWT-in-cookie gives statelessness and no revocation. Pick per `auth_scheme`, and do not mix both for the same client.
- Never store a JWT in `localStorage` if the app renders any third-party script: XSS then equals full account takeover with no expiry.

## Authorization Patterns

```python
def require_scopes(*required: str):
    async def dep(user: CurrentUser) -> None:
        if not set(required) <= set(user.scopes):
            raise HTTPException(403, "Insufficient scope")
    return dep

@router.delete("/orders/{oid}", dependencies=[Depends(require_scopes("orders:write"))])
```

- `Security(get_current_user, scopes=["orders:write"])` does the same and propagates scopes into the OpenAPI security requirements, so generated clients and the docs show what each route needs.
- Object-level permission cannot live in a route-level dependency: "may this user delete *this* order" needs the object, so check it in the handler right after loading, and return 404 rather than 403 when even the existence of the object is private.
- Multi-tenancy: resolve the tenant in a dependency and *filter every query by it*. A route-level tenant check plus an unfiltered query is the classic cross-tenant leak.

## API Keys and Service-to-Service

- `APIKeyHeader(name="X-API-Key")` extracts; you compare with `secrets.compare_digest` against a stored hash, never the raw key, and never with `==` (timing).
- Keys need the same lifecycle as passwords: prefix for identification, hash at rest, created/last-used timestamps, revocation.
- Between your own services prefer short-lived mTLS or signed service tokens over a shared static key that appears in five deployment manifests.

## Rate Limiting and Lockout

- Limit by identity when authenticated and by IP before authentication; the login endpoint needs both, because per-IP alone lets a botnet grind one account and per-account alone lets one IP spray many accounts.
- Counters live in Redis, not in memory: per-process counters divide the real limit by the worker count (SKILL.md rule 6).
- Return 429 with `Retry-After`; a 401 for a locked account tells an attacker they found a real one.

## What Not To Leak

- Login failures: one generic message for wrong user and wrong password.
- Token errors: "Not authenticated" to the client, the decoded reason to the log with a correlation id (`errors.md`).
- Never log the token, the cookie, or the `Authorization` header — scrub them in the logging config (`observability.md`).
