# Testing — Real Async, Real Database, Overridden Dependencies

Two failure modes dominate: tests that pass because the app under test is not the real one, and async tests that break on event-loop plumbing. Both are fixed by fixture design, not by more mocks.

## Client Choice

| Client | Runs | Use for |
|---|---|---|
| `TestClient(app)` | Sync, drives the ASGI app through a portal | Quick route checks, sync codebases |
| `httpx.AsyncClient(transport=ASGITransport(app=app), base_url="http://test")` | On the test's own loop, in-process | Everything async: concurrency, cancellation, real await behavior |
| `httpx.AsyncClient(base_url=live_url)` | Over a real socket to a running server | Smoke tests against a deployed instance, proxy and header behavior |

`TestClient` never exposes a blocked event loop, a missing await, or a race — the very bugs async code has (`async.md`). Use it for coverage, not for confidence in concurrency.

## Lifespan In Tests

- `with TestClient(app) as client:` runs the lifespan; the bare `TestClient(app)` does not, so `app.state.engine` is missing and the first request raises `AttributeError`.
- With `ASGITransport`, lifespan does **not** run at all. Drive it explicitly:

```python
@pytest_asyncio.fixture
async def client():
    async with LifespanManager(app):                      # asgi-lifespan
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as c:
            yield c
```

Or skip lifespan deliberately and inject the resources you need through overrides — but then say so, because the test no longer proves startup works.

## Event Loop Plumbing

- `pytest-asyncio` with `asyncio_mode = auto` in the config removes a decorator from every test and is the setting most projects want.
- `RuntimeError: Event loop is closed` or `attached to a different loop` = a session-scoped async fixture (engine, client) used by function-scoped tests. Either make the loop session-scoped too, or make the fixture function-scoped. The two scopes must match.
- `anyio` projects: mark with `pytest.mark.anyio` and a `anyio_backend` fixture pinned to `asyncio`, or every test runs twice (asyncio and trio) and the trio run fails on asyncio-only code.

## Dependency Overrides

```python
app.dependency_overrides[get_db] = lambda: session
...
app.dependency_overrides.clear()      # always, in teardown
```

- The key is the exact function object referenced in `Depends`; a re-import from a different module path is a different key and the override does nothing (`dependencies.md`).
- Override the *dependency*, not the internals: replacing `get_settings` beats monkeypatching `os.environ`, because it also proves the injection wiring works.
- Overriding auth (`get_current_user` → a fixed user) is the standard way to test protected routes; add at least one test that exercises the real dependency with a real token, or a broken auth chain never fails a test.
- Leaked overrides make later tests pass for the wrong reason — clear them in a fixture, not at the end of each test function.

## Database Isolation

Rollback-per-test, one real database, no truncation between tests:

```python
@pytest_asyncio.fixture
async def session(engine):
    conn = await engine.connect()
    trans = await conn.begin()
    s = AsyncSession(bind=conn, expire_on_commit=False)
    yield s
    await s.close(); await trans.rollback(); await conn.close()
```

- The app's `get_db` is overridden to yield this session, so the endpoint's commit lands inside the outer transaction and disappears on rollback.
- Code under test that commits and then expects a *new* session to see the data needs `begin_nested` (SAVEPOINT) plus a `after_transaction_end` listener, or a truncate-based strategy. Choose one and document it — mixing them produces tests that pass alone and fail in a suite.
- Test against the real engine, not SQLite: dialect differences (JSONB, arrays, `ON CONFLICT`, enum types, case sensitivity) hide real failures until production (`database.md`).
- Parallel test workers (`pytest-xdist`) need one schema or one database per worker; sharing one gives flaky unique-constraint failures.

## What To Test At Each Level

| Level | Test | Do not test |
|---|---|---|
| Model | Validators, computed fields, serialization of edge values | Pydantic itself |
| Service | Business rules against a real session | HTTP status codes |
| Route | Status, response shape, auth enforcement, validation failures | Business logic branches already covered below |
| Contract | The OpenAPI schema does not change unexpectedly (snapshot it) | Every field's description |

At least one test per route asserting the 401/403 path: a missing `dependencies=[...]` is invisible to every happy-path test.

## Mocking The Outside World

- `respx` (for httpx) or a fake client injected through a dependency; both beat patching `httpx.AsyncClient` globally, which also intercepts the test client itself.
- Assert on the request you sent (URL, headers, body), not just on your handling of the canned response — half of integration bugs are a wrong outbound payload.
- Time: inject a `now()` dependency or freeze with a library; `datetime.now()` scattered through services cannot be tested at a boundary.

## Speed

- Build the app once per session and override per test; recreating the app for every test re-imports and re-validates every model.
- Reuse one database container for the whole run and roll back per test — schema creation per test is usually the slowest thing in a FastAPI suite.
- Password hashing is deliberately slow (`auth.md`): drop the cost factor in the test settings, or a hundred login tests add minutes.
