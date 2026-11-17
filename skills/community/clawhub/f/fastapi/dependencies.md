# Dependencies — The Injection Graph and Its Lifetimes

`Depends` is a per-request DAG: FastAPI resolves each node once per request, caches it, and passes the result down. Almost every dependency bug is a lifetime mistake — something built per request that should be per process, or the reverse.

## Lifetimes

| Scope | Built with | Use for |
|---|---|---|
| Per process | Lifespan handler → `app.state.x` | Engines, connection pools, HTTP clients, model weights, broker connections |
| Per process, lazy | `@lru_cache` on a no-argument factory | Settings, compiled regexes, static lookup tables |
| Per request | `Depends(get_x)` | Sessions, current user, request-scoped context, tenant resolution |
| Per call | `Depends(get_x, use_cache=False)` | A fresh transaction or a new token on each of several uses in one request |

Two dependencies asking for the same sub-dependency get the same object within one request: if A needs `get_db` and B needs `get_db`, `get_db` runs once and both share the session — the property the whole request-scoped-transaction pattern relies on.

## The Annotated Style

```python
DbSession = Annotated[AsyncSession, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]

@router.get("/orders")
async def list_orders(db: DbSession, user: CurrentUser, limit: int = 20): ...
```

`Annotated` (fastapi >=0.95) makes the dependency a reusable type, keeps default arguments working normally, and lets the same function be called directly from a test or a worker. The old `db: AsyncSession = Depends(get_db)` form still works but poisons parameter defaults: you cannot put a non-dependency default after it without ordering gymnastics.

## Dependencies With `yield`

```python
async def get_db() -> AsyncIterator[AsyncSession]:
    async with SessionLocal() as session:
        yield session          # everything after runs at request teardown
```

- The exit half runs after the response body is produced, in reverse dependency order, and runs even if the endpoint raised.
- `fastapi >=0.106`: resources from `yield` dependencies are **not** usable inside `BackgroundTasks` — the session is already closed when the task runs. Open a new one inside the task (`background.md`).
- Exceptions raised by the endpoint propagate into the `yield` dependency, so `try/except/finally` around the yield is how you roll back and always close.
- Never swallow the exception there: catching it and returning normally turns a 500 into a truncated 200.
- `yield` dependencies used at app or router level still run per request, so a global `yield` dependency doing I/O adds that I/O to every route, including health checks.

## Where To Attach

| Level | Syntax | Applies to |
|---|---|---|
| Path operation | parameter with `Depends` | That route only; the value is injected |
| Router | `APIRouter(dependencies=[Depends(auth)])` | Every route in the router; return value discarded |
| App | `FastAPI(dependencies=[...])` | Everything, including `/health`, `/metrics`, and `/docs` |

Router-level or app-level dependencies exist for their side effect (authorization, rate limiting, audit). When you need the value too, ask for it as a parameter as well — resolution is cached, so it does not run twice.

## Sub-Dependencies and Parameterization

- A dependency can declare its own dependencies, path params, query params, and headers; FastAPI hoists all of them into the OpenAPI schema for every route that uses it. A dependency that reads `x_tenant: Annotated[str, Header()]` documents that header on every route automatically.
- Parameterized dependencies need a callable class or a factory, because `Depends(f(arg))` calls `f` at import time:

```python
class RateLimit:
    def __init__(self, per_minute: int): self.per_minute = per_minute
    async def __call__(self, request: Request) -> None: ...

@router.post("/messages", dependencies=[Depends(RateLimit(per_minute=30))])
```

- `Security(get_user, scopes=["items:write"])` is `Depends` plus scope propagation; scopes accumulate down the graph and appear in the OpenAPI security requirements (`auth.md`).

## Overrides

```python
app.dependency_overrides[get_db] = lambda: test_session
```

- The key is the exact callable object referenced in `Depends`. Importing `get_db` from a different module path (or re-exporting it) produces a different key and the override silently does nothing — the number one reason "my override is ignored".
- Overrides replace the dependency everywhere in the app, including inside sub-dependencies.
- Always clear them (`app.dependency_overrides.clear()`) in a fixture teardown; leaked overrides make later tests pass for the wrong reason (`testing.md`).

## Sync vs Async Dependencies

A `def` dependency runs in the threadpool and consumes one of the 40 slots (SKILL.md rule 2), even when the endpoint is `async def`. Three sync dependencies on a hot route means three threadpool hops per request; convert them or make them trivial.

## Design Rules

1. A dependency returns a value or raises; it never returns a `Response`. Raise `HTTPException` for auth and validation failures so the handlers produce a consistent body.
2. No dependency does more than one round trip. `get_current_user` that also loads the user's organization, permissions, and feature flags turns every route into four queries; split them and let routes ask for what they need.
3. Anything expensive and stateless (settings, JWT public keys, tenant config) is cached at process level with an explicit refresh path, not fetched per request.
4. Dependencies are the right home for cross-cutting request logic that needs typed access to the request; middleware is the right home for logic that must wrap the response as well (`middleware.md`).
