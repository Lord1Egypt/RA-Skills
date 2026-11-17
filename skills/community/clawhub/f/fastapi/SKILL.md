---
name: fastapi
slug: fastapi
version: 1.0.1
changelog: "Full coverage pass: deeper guides, situation-named files, and per-user configuration"
description: >-
  Builds, debugs, and hardens FastAPI services: async endpoints, Pydantic models, dependency
  injection, auth, and deployment. Use when writing or reviewing a FastAPI app, router, or
  schema; when the API hangs or every route slows because a sync driver or CPU work blocks the
  event loop; when a request returns an unexpected 422, a POST becomes a 307, or a 500 arrives
  with no CORS headers; when migrating pydantic v1 to v2 (`model_dump`, `from_attributes`,
  `field_validator`); when `Depends` runs too often, `yield` cleanup misfires, or dependency
  overrides do not take; when SQLAlchemy raises `QueuePool limit` or `MissingGreenlet`, or
  connections leak across workers; when TestClient, httpx `AsyncClient`, or pytest-asyncio fail
  with a closed event loop; when uvicorn or gunicorn workers, graceful shutdown, `root_path`,
  or proxy headers need deciding; or when background tasks, WebSockets, SSE, uploads, or the
  OpenAPI docs misbehave. Not for Django, Flask, or general Python — `django`, `flask`, `py`.
homepage: https://clawic.com/skills/fastapi
metadata:
  clawdbot:
    emoji: ⚡
    requires:
      bins:
      - python3
    os:
    - linux
    - darwin
    - win32
    displayName: FastAPI
    configPaths:
    - ~/Clawic/data/fastapi/
---

User preferences live in `~/Clawic/data/fastapi/config.yaml` (see Configuration); nothing else is stored on the user's machine. If you have data at an old location (`~/fastapi/` or `~/clawic/fastapi/`), move it to `~/Clawic/data/fastapi/`.

## When To Use

- Writing or reviewing FastAPI code: routers, dependencies, request/response models, middleware
- Diagnosing latency and stalls: one blocking call, an exhausted pool, a saturated threadpool
- Modelling data at the edge: validation errors, serialization, ORM objects, pydantic v1 → v2
- Wiring auth, settings, database sessions, and background work into the dependency graph
- Getting a service to production: workers, proxies, shutdown, health checks, logging, limits
- Fixing tests that pass wrongly, hang, or die with a closed event loop
- Not for Django, Flask, or plain-Python problems — `django`, `flask`, `py` own those

## Quick Reference

| Situation | Play |
|-----------|------|
| Every route got slow at once, health check included | The loop is blocked: a sync call inside `async def`, or all threadpool slots busy → `async.md` |
| Choosing `def` vs `async def` for an endpoint | Any blocking call in the body → `def`; all-await → `async def` → `async.md` |
| CPU work, image processing, big parsing in a request | Off the loop and off the threadpool: process pool or queue → `async.md` |
| 422 on a request that looks correct | Read `loc` in the error body: alias, nesting, or a nullable field with no default → `pydantic.md` |
| `.dict()`, `parse_obj`, `@validator`, `orm_mode` no longer work | Pydantic v2 renames and behavior changes → `pydantic.md` |
| ORM instance will not serialize into the response | `from_attributes` plus a response model, or return the model you declared → `pydantic.md` |
| `Depends` runs more or fewer times than expected | Per-request cache, `use_cache=False`, singletons in lifespan → `dependencies.md` |
| Current user, scopes, tokens, password hashing | `auth.md` |
| `/users/me` hits the `{user_id}` route; 307 on POST; router prefixes | Declaration order and trailing slashes → `routing.md` |
| Where files go, circular imports, app factory, one app or many | `structure.md` |
| Env var ignored, secret in the wrong place, per-environment config | `settings.md` |
| Sessions, pools, transactions, N+1, migrations, async ORM errors | `database.md` |
| Error bodies inconsistent, custom handlers, validation error shape | `errors.md` |
| CORS headers missing, middleware order, request IDs, body read twice | `middleware.md` |
| Tests: dependency overrides, lifespan, async client, DB isolation | `testing.md` |
| Workers, gunicorn vs uvicorn, `root_path`, graceful shutdown, containers | `deployment.md` |
| Slow under load with the loop healthy: serialization, caching, pagination | `performance.md` |
| Large uploads or downloads, SSE, streaming JSON, client disconnects | `streaming.md` |
| WebSocket drops, broadcast across workers, authenticating a socket | `websockets.md` |
| Work after the response: `BackgroundTasks` vs a real queue, retries | `background.md` |
| Docs wrong or missing, generated clients, operation ids, examples | `openapi.md` |
| Logs with no request context, health vs readiness, metrics, tracing | `observability.md` |
| Ownership checks, mass assignment, SSRF, path traversal, security headers | `security.md` |
| Server-rendered HTML: Jinja2, forms, HTMX partials, static files | `templates.md` |
| Anything else | Reproduce in one file: one route, no middleware, no DB — then add back one layer at a time until it breaks |

Each file is one sub-job and self-contained: read SKILL.md by default, open exactly one guide when the situation matches.

## Core Rules

1. **`async def` obliges the whole chain to await.** One blocking call inside an async endpoint — `psycopg2`, `requests`, `time.sleep`, a large `open().read()` — freezes every concurrent request on that worker, not just its own. If any step blocks and cannot be replaced, declare the endpoint `def` and let Starlette move it to the threadpool.
2. **The threadpool has 40 slots per worker.** Every `def` endpoint and `def` dependency shares AnyIO's default limiter of 40 threads: ceiling = 40 concurrent blocking calls per worker process, the 41st waits with no error message. Concurrency budget = `40 × workers`; raise `total_tokens` in lifespan only after measuring.
3. **Dependencies cache per request, singletons live in lifespan.** `Depends(get_x)` used in three places runs once per request and again on the next one. Anything that must exist once per process — DB engine, HTTP client, cache client — is created in the lifespan handler and stored on `app.state`; `@lru_cache` on a factory is the escape hatch for cheap, argument-free objects like settings.
4. **Validate at the edge, exactly twice.** Request model in, response model out, plain objects in between. `response_model` re-validates everything you return, so a response is a second full validation pass — worth it as a contract, and skippable (`response_model=None` plus an explicit `Response`) only on a route you have profiled.
5. **Size the pool against the database, not the app.** SQLAlchemy defaults to `pool_size=5, max_overflow=10` = 15 connections per process, so total = `workers × 15`. Four workers = 60 of Postgres's default 100 `max_connections`; a second replica of the same service exhausts the server and every route starts failing on connect.
6. **One event loop and one memory space per worker.** Lifespan runs once per worker, so 4 workers means 4 pools, 4 in-process caches, and 4 disjoint sets of WebSocket clients. Any state two requests must share goes to Redis or the database — a module-level dict is a per-process cache with a 1-in-N hit rate.
7. **Every outbound call carries a timeout.** `httpx.AsyncClient(timeout=5.0)`, DB statement timeouts, lock acquisition bounds. Without one, a hung upstream converts into an unbounded queue of pending tasks and the worker dies holding requests it will never answer.
8. **Raise errors, never return them from helpers.** `raise HTTPException(404, ...)` travels through the exception handlers and produces the same body everywhere; a `JSONResponse` returned from a service function only works if the endpoint happens to pass it through, and it skips every handler and response-model check.
9. **Middleware order is the reverse of registration.** The last `add_middleware` call is the outermost layer. CORS registered first ends up innermost, so a 500 raised above it reaches the browser with no CORS headers and the real error is invisible in devtools — register CORS last, and add an exception handler so failures are returned rather than propagated.

## Version Floors

Behavior that changed with the framework, stated as the floor that gates it. Guides carry additional floors inline in the same form.

| Feature | Needs |
|---|---|
| Return-type annotation used as the response model | fastapi >=0.89 |
| `lifespan` context manager (replaces `@app.on_event`) | fastapi >=0.93 |
| `Annotated[X, Depends(...)]` dependency style | fastapi >=0.95 |
| Pydantic v2 models and `model_config` | fastapi >=0.100 |
| `yield` dependency resources no longer usable inside `BackgroundTasks` | fastapi >=0.106 |
| `fastapi dev` / `fastapi run` CLI (`fastapi[standard]`) | fastapi >=0.111 |
| `BaseSettings` moved to the separate `pydantic-settings` package | pydantic >=2.0 |
| `asyncio.TaskGroup` and `asyncio.timeout` for fan-out and deadlines | python >=3.11 |

## Error Signatures

| Signature | Cause | Go to |
|---|---|---|
| 422 with `"loc": ["body", ...]` | Body does not match the model: alias, nesting depth, or a nullable field that is required in pydantic v2 | `pydantic.md` |
| 307 Temporary Redirect on POST | Trailing-slash mismatch; method and body survive the redirect, but a proxy with wrong scheme headers sends the client to `http://` | `routing.md` |
| 500 in the browser with no CORS headers | Exception escaped above `CORSMiddleware` (rule 9) | `middleware.md` |
| `QueuePool limit of size 5 overflow 10 reached` | Sessions never closed, or the pool sized without counting workers (rule 5) | `database.md` |
| `MissingGreenlet` / `greenlet_spawn has not been called` | Lazy relationship access outside an await in async SQLAlchemy | `database.md` |
| `asyncpg ... another operation is in progress` | One connection or session shared by concurrent tasks | `database.md` |
| `RuntimeError: Event loop is closed` in tests | Session-scoped async fixture bound to a function-scoped loop | `testing.md` |
| `FastAPIError: Invalid args for response field` | A non-pydantic type used as `response_model` | `pydantic.md` |
| Endpoint hangs waiting for the body | Middleware consumed the request stream and passed the exhausted receive down | `middleware.md` |
| SSE or streamed response arrives only at the end | Proxy buffering the response | `streaming.md` |
| WebSocket closes with 1006, never 1000 | Abnormal close: proxy idle timeout or worker restart, not application logic | `websockets.md` |
| Everything returns 200 but clients time out | Worker saturated: blocked loop or full threadpool (rules 1-2) | `async.md` |

## Output Gates

Before delivering FastAPI code, verify:

- No blocking call inside an `async def` path; blocking work is in a `def` endpoint, `run_in_threadpool`, or a queue
- Every outbound HTTP, database, and lock call has an explicit timeout
- Request and response models declared; ORM objects only cross the boundary through a model with `from_attributes`
- `workers × (pool_size + max_overflow)` fits inside the database connection limit
- Configuration and secrets read through the settings object, never `os.getenv` scattered through handlers
- Auth applied at router level with health, readiness, and metrics endpoints excluded
- Every read and write filtered by owner or tenant inside the query, not in a separate `if`
- Errors raised as `HTTPException` with a consistent body; no stack trace, SQL, or upstream payload in `detail`
- Request body size and upload size bounded somewhere (proxy or middleware), not left unlimited
- Tests override dependencies instead of patching, and run inside the lifespan

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/fastapi/config.yaml`. Never interview the user — record a preference the moment it is stated.

| Variable | Type | Default | Effect |
|---|---|---|---|
| pydantic_version | 1 \| 2 | 2 | Which API names appear everywhere: `model_dump` vs `.dict()`, `field_validator` vs `validator`, settings package (`pydantic.md`) |
| db_stack | sqlalchemy-async \| sqlalchemy-sync \| sqlmodel \| tortoise \| none | sqlalchemy-async | Session and engine pattern, driver choice, and whether endpoints are emitted `def` or `async def` (`database.md`) |
| server_stack | uvicorn \| gunicorn-uvicorn \| hypercorn | uvicorn | Process model, worker flags, and shutdown settings (`deployment.md`) |
| auth_scheme | jwt \| session-cookie \| oauth2-provider \| api-key \| none | jwt | Which current-user dependency and token lifecycle `auth.md` emits |
| min_fastapi | text (version, e.g. 0.100) | 0.111 | Gates the Version Floors features; below the floor the fallback form is emitted instead |
| deploy_target | container \| vm \| serverless \| unknown | container | Worker model, health-check style, and shutdown guidance (`deployment.md`, `observability.md`) |
| error_envelope | bare \| enveloped | bare | Shape of every error body and the handlers generated in `errors.md` |
| task_backend | background-tasks \| celery \| arq \| rq \| dramatiq | background-tasks | Where after-response work goes and how failures are retried (`background.md`) |
| test_client | async-httpx \| testclient | async-httpx | Shape of emitted tests, fixtures, and the transport used (`testing.md`) |
| json_renderer | default \| orjson | default | Default response class and serialization advice (`performance.md`) |
| render_mode | json \| html-htmx \| both | json | Whether routes return JSON models or rendered templates, and which validation-error path is generated (`templates.md`) |

Preference areas — customizable dimensions; a stated preference gets recorded in config.yaml and applied:

- **Tooling**: package and env manager (pip, uv, poetry), linter and formatter, migration tool, load generator — affects every command block shown alongside code
- **Conventions**: router and module naming, schema suffixes (`Create`/`Read`/`Update`), URL casing, versioning scheme, docstring style — affects generated routers and models (`structure.md`)
- **Platform**: cloud, reverse proxy, Python version, CPU count, managed database — affects worker maths, proxy headers, and pool sizing (`deployment.md`)
- **Safety posture**: how loudly to flag missing auth, unbounded uploads, absent timeouts, `verify=False`, secrets in logs — affects review comments, never the correctness rules
- **Integrations**: cache, broker, and object store of choice (Redis, RabbitMQ, S3-compatible), auth provider, error tracker — affects which client patterns appear
- **Output format**: whole file vs minimal diff, how much explanation, whether tests and migrations accompany every change
- **Work order**: contract-first (OpenAPI or schema before handlers) vs code-first, migration before or after model change, review gates before edits — affects sequence, never correctness
- **Dependencies**: banned or mandated libraries (httpx vs requests, SQLModel vs SQLAlchemy, ORM vs raw SQL), tolerance for new transitive dependencies

## Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| `requests.get()` inside `async def` | Blocks the loop for the full round trip; under load the whole worker stalls (rule 1) | `httpx.AsyncClient` from lifespan, or make the endpoint `def` (`async.md`) |
| `@app.on_event("startup")` | Deprecated in favour of lifespan, and gives no way to hold a resource open across the app's life | `lifespan` async context manager (`structure.md`) |
| Module-level `cache = {}` as an application cache | One copy per worker: hit rate divided by the worker count, invalidation reaching only one process (rule 6) | Redis, or accept per-process caching explicitly (`performance.md`) |
| `app.include_router(..., dependencies=[Depends(auth)])` on everything | Health and metrics start returning 401, the orchestrator declares the pod dead and restarts it in a loop | Auth on business routers only; probes on an unauthenticated router (`observability.md`) |
| `items: list = []` "shared across requests" | Pydantic deep-copies mutable defaults per instance — this is not the bug; the real need for `default_factory` is a computed default (`uuid4`, `datetime.now`) | `Field(default_factory=...)` only when the value must be computed (`pydantic.md`) |
| `Optional[str]` and expecting it to be optional | In pydantic v2 that is required-and-nullable; the client must send `null` | Give it a default: `= None` (`pydantic.md`) |
| Reading `await request.body()` in middleware, then calling the endpoint | The receive channel is exhausted; the endpoint waits for a body that will never arrive | Pure ASGI middleware that replays the stream, or read the body only in the endpoint (`middleware.md`) |
| `BackgroundTasks` for anything that matters | Runs in the worker after the response; a deploy or crash loses it silently, and the client already got a 200 | Queue with retries and visibility (`background.md`) |
| `uvicorn --reload --workers 4` | `--reload` forces a single process; the worker count is silently ignored, so dev and prod differ in concurrency | Reload in dev, workers in prod, never both (`deployment.md`) |
| `TestClient` for testing async behavior | Drives the app through a sync portal — real concurrency bugs, cancellation, and loop blocking never show up | `httpx.AsyncClient` with `ASGITransport` (`testing.md`) |
| Returning the ORM object and hoping | Lazy attributes load during serialization, outside the session, after it closed | Load eagerly, convert with a response model (`database.md`) |
| Secrets in `HTTPException(detail=...)` | Whatever is in `detail` is JSON in the client's hands, including upstream error payloads | Generic message out, full context to the log with a correlation id (`errors.md`) |

## Where Experts Disagree

- **Async everywhere vs honest `def` endpoints.** One school makes every endpoint `async def` for uniformity; the other declares `def` whenever the body blocks. Boundary: an all-await stack (async driver, httpx, async cache) → `async def`; a single blocking library in the chain → `def` is strictly safer, because the threadpool bounds the damage to 40 slots instead of stopping the loop.
- **ORM vs raw SQL vs SQLModel.** SQLAlchemy gives migrations, identity map, and eager-loading control; raw SQL gives exact queries and no lazy-load surprises; SQLModel merges model and schema at the cost of coupling the table to the API contract. Boundary: one shape of data serving one API → SQLModel is fine; separate read and write shapes, or a schema older than the API → SQLAlchemy plus explicit response models.
- **Service layer or routers that talk to the database.** A repository/service layer pays off when the same operation is called from HTTP, a worker, and a CLI; below that it is indirection. Boundary: the second caller of the same logic, not the first.
- **Bare bodies vs an error envelope.** HTTP status plus a bare body is idiomatic and what generated clients expect; an envelope (`{"data": ..., "error": ...}`) survives clients that only read 200s. Boundary: public API or generated SDKs → bare with RFC 9457 problem details; a single front end with a legacy error contract → envelope, declared once in `error_envelope` and applied everywhere.

## Related Skills

More Clawic skills, get them at https://clawic.com/skills/fastapi (install if the user confirms):
- `py` — the Python language itself: packaging, typing, async primitives, tests
- `pg` — PostgreSQL behind the API: query plans, indexes, connection limits
- `auth` — authentication design across sessions, JWT, OAuth, MFA
- `api-design` — resource modelling, versioning, and the cost of breaking changes
- `docker` — containerizing and running the service

## Feedback

- If useful, star it: https://clawic.com/skills/fastapi
- Latest version: https://clawic.com/skills/fastapi

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/fastapi.
