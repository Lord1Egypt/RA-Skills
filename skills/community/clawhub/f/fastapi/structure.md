# Project Structure — Layout, App Factory, and Circular Imports

The layout question is really a dependency-direction question: routers may import services, services may import models, and nothing imports back up. Every circular import in a FastAPI project is that arrow pointing the wrong way.

## Default Layout (grows to ~50 routes without reshaping)

```
src/app/
├── main.py            # create_app(), lifespan, middleware, include_router calls
├── settings.py        # Settings + get_settings (settings.md)
├── deps.py            # shared Annotated dependency aliases: DbSession, CurrentUser
├── db.py              # engine, session factory, Base
├── api/
│   ├── health.py      # unauthenticated probes
│   └── v1/
│       ├── users.py   # APIRouter: routes only, thin
│       └── orders.py
├── services/          # business operations, framework-free, callable from a worker
├── models/            # ORM tables
└── schemas/           # pydantic request/response models
tests/
alembic/
```

- Routers hold HTTP concerns: status codes, response models, dependency wiring. Anything you would also want to run from a CLI or a queue consumer belongs in `services/`.
- `models/` and `schemas/` stay separate even with SQLModel-style temptation: the day a column must not be exposed, or a response needs a computed field, one class serving both becomes two anyway.
- By-feature (`users/{router,service,models,schemas}.py`) beats by-layer past roughly a dozen features, because a change then touches one directory instead of four. Pick one and keep it: mixing the two is the layout that actually hurts.

## App Factory and Lifespan

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    app.state.engine = create_async_engine(settings.database_url, pool_size=5, max_overflow=10)
    app.state.http = httpx.AsyncClient(timeout=5.0)
    yield
    await app.state.http.aclose()
    await app.state.engine.dispose()

def create_app(settings: Settings | None = None) -> FastAPI:
    app = FastAPI(lifespan=lifespan, title="Orders API")
    app.include_router(health.router)
    app.include_router(v1_users.router, prefix="/v1")
    return app

app = create_app()
```

- A factory lets tests build an app with different settings without import-time side effects; a module-level `app = FastAPI()` plus decorators works until the first test needs two configurations.
- Everything opened in lifespan is closed after the `yield`, in reverse order. Missing `aclose()` on the HTTP client leaks sockets that only show up as file-descriptor exhaustion under load.
- Lifespan runs once per worker (SKILL.md rule 6) — never put "run migrations" or "seed data" there unless exactly one process may do it; use a release/init step instead.
- `@app.on_event("startup")` is the deprecated predecessor and cannot hold a resource open across the app's life, which is the whole point of lifespan.

## Breaking Circular Imports

Symptom: `ImportError: cannot import name 'X' from partially initialized module`.

| Cause | Fix |
|---|---|
| `main.py` imports a router, the router imports `app` from `main` | Routers never import the app; they define `APIRouter` and `main` includes them |
| Two services import each other's functions | Extract the shared piece into a third module, or pass the collaborator in as an argument |
| Models importing schemas for a type hint | `from __future__ import annotations` plus `if TYPE_CHECKING:` imports |
| Dependency functions living next to the routes that use them | One `deps.py` that imports downward only |

Rule of thumb: if module A needs something from module B and B needs something from A, the thing they share belongs in C.

## Where State Lives

| State | Home |
|---|---|
| Engine, pools, HTTP clients | `app.state`, created in lifespan |
| Settings | `@lru_cache` factory in `settings.py` |
| Per-request context (user, tenant, request id) | Dependencies, or a contextvar set by pure ASGI middleware (`middleware.md`) |
| Anything two workers must agree on | Redis or the database — never a module-level dict (SKILL.md rule 6) |

Accessing `app.state` from a route: `request.app.state.http`, or a dependency that returns it so the route stays testable.

## Import Cost and Startup Time

- Module-level work runs on import in every worker: a `create_engine` at import time opens pools before the app knows its configuration, and a model load costs seconds per worker at boot.
- Slow imports show up as failed readiness probes during rollout, not as request latency. Time it with `python -X importtime -c "import app.main"` and move the expensive part into lifespan.

## Multiple Services in One Repo

- Shared code goes in a package the services depend on, not in relative imports across service directories — the second service will otherwise pin the first's dependency versions forever.
- A worker process (queue consumer, scheduler) imports `services/` and `db.py`, never `main.py`; if it needs the FastAPI app to run, the business logic is in the wrong layer.
