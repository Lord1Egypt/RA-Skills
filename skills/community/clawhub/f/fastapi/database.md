# Database — Sessions, Pools, Transactions, Migrations

Three decisions drive everything else: one session per request, one pool per process, and where the transaction boundary sits. Get those right and the exotic errors stop appearing.

## Session Per Request

```python
engine = create_async_engine(url, pool_size=5, max_overflow=10, pool_pre_ping=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_db() -> AsyncIterator[AsyncSession]:
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

- Commit-at-the-end makes the request the transaction: either the whole handler's writes land or none do. The alternative — committing inside services — means a later failure leaves half the operation persisted.
- `expire_on_commit=False` keeps attributes readable after the commit; the default expires every instance, so serializing the object after committing triggers a refresh query per attribute, or fails once the session is gone.
- One session must never be shared by concurrent tasks. `asyncio.gather` over two coroutines using the same session raises `asyncpg ... another operation is in progress` or corrupts state; give each task its own session from the factory.
- The session from a `yield` dependency is closed before background tasks run (fastapi >=0.106): open a fresh one inside the task (`background.md`).

## Pool Sizing

Formula: total connections = `workers × (pool_size + max_overflow)`. SQLAlchemy defaults to `pool_size=5, max_overflow=10` = 15 per process (SKILL.md rule 5).

| Situation | Setting |
|---|---|
| 4 uvicorn workers, Postgres default 100 `max_connections` | 60 used; leaves room for one replica and psql, not for three replicas |
| Managed Postgres with a low connection cap | Lower `pool_size`, or put PgBouncer in front and set `poolclass=NullPool` in the app |
| PgBouncer in transaction mode | Disable statement caching (`prepared_statement_cache_size=0` for asyncpg) or prepared statements collide across pooled sessions |
| Serverless or per-request containers | `NullPool`; a pool that outlives the request is wasted and holds server slots |

- `pool_pre_ping=True` costs one round trip per checkout and eliminates the "server closed the connection unexpectedly" class after a database failover or an idle timeout.
- `pool_recycle` shorter than the database's or proxy's idle timeout (`wait_timeout` on MySQL, `idle_in_transaction_session_timeout` on Postgres) prevents handing out dead connections.
- `QueuePool limit of size 5 overflow 10 reached` means sessions are not being returned: a `yield` dependency without the `async with`, a session stored on `app.state`, or a long-running task holding one across an await on something slow.

## Async ORM Traps

- `MissingGreenlet` / `greenlet_spawn has not been called` = a lazy attribute was touched outside async context — usually during response serialization, after the endpoint returned. Load relationships explicitly: `selectinload(User.orders)` in the query, or declare `lazy="raise"` on relationships so the mistake fails at development time instead of in production.
- `selectinload` issues a second query with an `IN` clause (safe for large parents); `joinedload` does one query with a join (rows multiply for one-to-many). Default to `selectinload` for collections, `joinedload` for many-to-one.
- N+1 signature: a request whose query count scales with the number of returned rows. Count queries per request in development by logging with `echo=True` or an event listener; a list endpoint should be a fixed small number of queries regardless of page size.
- `await session.execute(select(...))` then `.scalars().all()`; `session.query(...)` is the removed 1.x API.
- `run_sync` bridges sync-only ORM features into the async session: `await session.run_sync(lambda s: s.refresh(obj, ["orders"]))`.

## Sync Stack Without Async

A sync driver is a legitimate choice — it just changes the endpoint declaration:

```python
def get_db() -> Iterator[Session]:
    with SessionLocal() as s: yield s

@router.get("/users")
def list_users(db: Annotated[Session, Depends(get_db)]):   # def, not async def
    return db.execute(select(User).limit(20)).scalars().all()
```

Both the endpoint and the dependency become `def`, so they run in the threadpool and never touch the loop (SKILL.md rules 1-2). Concurrency ceiling becomes the smaller of the 40 threadpool slots and the pool size — matching those two numbers avoids threads queueing on connections.

## Transactions Beyond One Request

- Nested logical units: `async with session.begin_nested():` (SAVEPOINT) rolls back part of a request without losing the rest.
- Idempotency for retried POSTs: unique constraint on a client-supplied key, catch `IntegrityError`, return the existing resource. Application-level "check then insert" races under concurrency; the constraint does not.
- Locking: `select(...).with_for_update()` for read-modify-write on a row; keep the lock inside a single request and never across an external HTTP call, or one slow upstream blocks a table row for its timeout.
- Long transactions are the hidden cost of a request-scoped commit: a handler that calls a payment API mid-transaction holds a connection open for the whole call. Commit before the external call, or move the write after it.

## Migrations

- Alembic autogenerate detects table and column changes; it does not detect renames (drops and recreates, losing data), check constraints, or changes inside enum types. Read every generated migration.
- Enum changes on Postgres need explicit `ALTER TYPE ... ADD VALUE` outside a transaction block; autogenerate produces nothing.
- Zero-downtime column removal is three deploys: stop writing it, stop reading it, then drop. A single deploy that drops a column breaks every old process still serving traffic during the rollout.
- Adding a NOT NULL column with a default rewrites the table on older Postgres versions; add nullable, backfill in batches, then set NOT NULL.
- Run migrations as a release step (a job, an init container, a manual command), never in lifespan — with N workers, N processes race the same migration (`structure.md`).
- Index creation on a live table: `CREATE INDEX CONCURRENTLY`, which Alembic must run with `autocommit_block()`.

## Testing Against a Real Database

Use the real engine, not SQLite-in-memory: SQLite accepts SQL Postgres rejects, lacks the types you use, and hides constraint behavior. Isolation and fixture patterns: `testing.md`.
