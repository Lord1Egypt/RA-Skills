# Background Work — After The Response, And Beyond The Process

Three tiers, chosen by what happens when the process dies: `BackgroundTasks` (work is lost), an in-process scheduler (work is lost, and only one worker should run it), a real queue (work survives).

## `BackgroundTasks`

```python
@router.post("/orders", status_code=201)
async def create(order: OrderCreate, tasks: BackgroundTasks, db: DbSession):
    saved = await service.create(db, order)
    tasks.add_task(send_receipt, saved.id)     # runs after the response is sent
    return saved
```

- Runs in the same worker, after the response, sequentially in the order added. No parallelism, no retries, no visibility.
- A deploy, a crash, an OOM kill, or a scale-down between response and execution loses the task silently — the client already has its 201.
- `fastapi >=0.106`: resources from `yield` dependencies are closed before the task runs, so the request's DB session is unusable inside it. Open a new session in the task:

```python
async def send_receipt(order_id: UUID):
    async with SessionLocal() as db: ...
```

- A `def` task runs in the threadpool (one of the 40 slots, SKILL.md rule 2); an `async def` task runs on the loop and blocks it if it blocks (`async.md`).
- Exceptions inside a task never reach the client and, unhandled, only appear as a traceback in the log. Wrap the body in try/except and record the failure somewhere you actually watch.
- Fair uses: sending a fire-and-forget notification, writing an audit row, warming a cache. Not: payments, anything a user is told happened, anything that must be retried.

## The Queue Tier

| Tool | Fits |
|---|---|
| `arq` | Async-native, Redis, small surface — the natural fit for an async FastAPI app |
| `celery` | Mature, huge feature surface, sync workers; the default when the org already runs it |
| `dramatiq` / `rq` | Simpler than Celery, Redis-backed, sync workers |
| Cloud queue (SQS, Pub/Sub, Tasks) | No broker to operate, at-least-once delivery, provider retry semantics |

Rules that apply to all of them:

1. Enqueue a reference, never an object: the id and the minimum arguments, not a serialized ORM instance. The worker re-reads current state; a payload captured at enqueue time is already stale when it runs.
2. Enqueue *after* the transaction commits, or the worker can look up a row that was rolled back. Either commit first, then enqueue, or use a transactional outbox table that a relay drains.
3. Every task is idempotent, because every queue redelivers. Key the effect (a unique constraint on `payment_id`, a "sent" flag checked inside the transaction) rather than trusting once-only delivery.
4. Retries with exponential backoff plus jitter, a maximum attempt count, and a dead-letter destination. A task retrying forever on a poison message is an outage with no alert.
5. Tasks live in `services/`, importable by both the API and the worker; a task module that imports `main.py` drags the whole web app into the worker (`structure.md`).

## Reporting Progress

- Accept with 202 and return a job id plus a status URL; the client polls it or subscribes (`streaming.md`, `websockets.md`).
- Job state lives in the database or Redis with a TTL — `{status, progress, result_url, error}`. Reconstructing state from broker internals ties you to the broker.
- Return the final artifact by link, not inline: a completed export is a URL, not a base64 blob in a status response.

## Scheduled Work

- An in-process scheduler (APScheduler in lifespan) runs in **every** worker: 4 workers means the nightly job runs 4 times (SKILL.md rule 6). Either run exactly one scheduler process, or take a lock (a Redis key with a TTL, or `pg_advisory_lock`) at the start of each job.
- Container platforms have a cron primitive (Kubernetes CronJob, platform schedulers) — a separate one-shot process is simpler and observable, and it cannot slow the API down.
- Schedules need a timezone and a DST policy: a job at 02:30 local runs twice or never on the days the clock shifts. Schedule in UTC unless a human-facing time is the requirement.
- Every scheduled job needs a heartbeat check: silent non-execution is the failure mode nobody notices for a month.

## Long-Running Work Started By A Request

- `asyncio.create_task` for anything longer than the request is a trap: the task dies with the worker, keeps no reference by default (garbage collection can cancel it), and never retries (`async.md`).
- If it must run in-process, hold the task in a set, name it, log its exceptions with `add_done_callback`, and cancel it in the lifespan exit — and accept that a deploy kills it mid-flight.
- The honest question is whether losing the work is acceptable. "No" means a queue; there is no in-process arrangement that survives a SIGKILL.
