# Async — Keeping the One Event Loop Free

Mental model: each worker process runs a single event loop. Every `async def` endpoint, dependency, and middleware takes turns on it. A blocking call does not slow one request down — it stops all of them, including the health check, which is why "the whole service got slow" is almost always one line of code.

## Declaration Table

| Endpoint body | Declare | What runs where |
|---|---|---|
| Everything is awaited (asyncpg, httpx, aioredis) | `async def` | On the loop; thousands of concurrent requests are cheap |
| Any blocking library (psycopg2, requests, boto3, PIL, pandas) | `def` | Starlette moves it to the threadpool: 40 slots per worker (SKILL.md rule 2) |
| Mostly async, one blocking call | `async def` + `await run_in_threadpool(fn, arg)` | The one call leaves the loop, the rest stays async |
| Pure CPU over ~50 ms (hashing, encoding, parsing megabytes) | `def` is not enough — the GIL serializes it against every other thread | Process pool or a task queue |
| Unsure | `def` | Worst case it costs a threadpool slot; the async version's worst case is the whole worker |

Sync dependencies follow the same rule and consume the same 40 slots: an `async def` endpoint with three `def` dependencies still leaves the loop three times.

## Is The Loop Blocked? (the two-route test)

Run load against the suspect route while polling a trivial `/health` route:

- `/health` latency also degrades → the loop is blocked or the threadpool is full. Look for sync calls inside `async def`.
- Only the suspect route degrades → nothing is blocked; you are waiting on a downstream, a lock, or an exhausted connection pool.

Confirm from inside the process: run with asyncio debug mode (`PYTHONASYNCIODEBUG=1` or `uvicorn --loop asyncio` plus `loop.set_debug(True)`). It logs every callback that occupies the loop for longer than `slow_callback_duration`, default 0.1 s — the log line names the coroutine holding the loop hostage.

## The Blocking Offenders

Sync drivers (`psycopg2`, `PyMySQL`, `sqlite3`, `pymongo`), `requests`/`urllib3`, `boto3` and most cloud SDKs, `time.sleep`, `subprocess.run`, reading or writing large files, `pandas`/`numpy`/PIL work, password hashing (deliberately slow — costs in `auth.md`), template rendering of large pages, and `json.dumps` of multi-megabyte payloads.

Not blocking, despite the reputation: small `json.dumps`, `logging` to stdout, and pydantic validation of ordinary models — each is microseconds to low milliseconds, so they never appear in the slow-callback log.

## Getting Off The Loop

```python
from fastapi.concurrency import run_in_threadpool
result = await run_in_threadpool(legacy_client.fetch, item_id)   # shares the 40-slot limiter
```

- `asyncio.to_thread` also works but uses the interpreter's default executor, sized `min(32, cpu_count + 4)` — a second, separate ceiling that the AnyIO limiter does not govern. Prefer `run_in_threadpool` so one number bounds all blocking work.
- Raising the limit is a lifespan-time decision, not a per-call one:

```python
import anyio.to_thread
async def lifespan(app):
    anyio.to_thread.current_default_thread_limiter().total_tokens = 80
    yield
```

Each thread costs a stack plus GIL contention; raise it only for I/O-bound work you have measured, and never above what the downstream (database pool, upstream API) can absorb.

- CPU-bound work belongs in a `ProcessPoolExecutor` created at lifespan (`loop.run_in_executor(pool, fn, *args)`) or in a queue. Arguments and results are pickled, so passing a 200 MB DataFrame costs more than the computation; pass a path or a key instead.

## Fan-out, Deadlines, Cancellation

```python
async with asyncio.TaskGroup() as tg:            # python >=3.11
    a = tg.create_task(users.get(uid))
    b = tg.create_task(orders.list(uid))
profile, orders_ = a.result(), b.result()
```

- `TaskGroup` cancels siblings when one fails and never leaves a task running past the block. `asyncio.gather(..., return_exceptions=True)` keeps going but hands you exceptions as values — a silent failure if you do not inspect each result.
- Bare `asyncio.create_task(...)` with no reference kept can be garbage-collected mid-flight; hold the task in a set and discard it in a done callback, or use a TaskGroup.
- Bound every fan-out: `sem = asyncio.Semaphore(10)` around the per-item coroutine. Ten thousand items without a semaphore opens ten thousand sockets and the failure looks like the upstream being down.
- Deadlines: `async with asyncio.timeout(5):` (python >=3.11) or `anyio.fail_after(5)`. A timeout raises `CancelledError` inside the task — `except Exception` does not catch it in python >=3.8, and swallowing it breaks cancellation for everything above.
- Long loops should check `await request.is_disconnected()` and stop; otherwise a client that gave up still costs you the full computation.

## Startup, Shutdown, and uvloop

- Lifespan runs on the loop: a synchronous migration or a blocking warm-up there delays the port opening and every health probe. Wrap it in `run_in_threadpool` if it must stay sync.
- `uvicorn[standard]` installs uvloop and httptools; uvloop makes the loop itself faster and changes nothing about blocking — a blocked loop is blocked at any speed.
- Async generators as dependencies keep the connection open across the whole request; cleanup after `yield` runs at the end of the request (`dependencies.md`).

## When The Symptom Is Memory, Not Latency

Unbounded concurrency shows up as RAM before it shows up as time: every pending request holds its body, its ORM objects, and its response buffer. If RSS climbs with load and falls when load stops, add the semaphore and the queue limits before adding workers.
