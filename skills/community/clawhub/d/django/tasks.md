# Tasks — Background Jobs, on_commit, Retries, Email

A background job is a second process reading your database. Everything below follows from that: it does not share your transaction, it does not share your memory, and it may run twice.

## The Transaction Rule

```python
def create_order(...):
    with transaction.atomic():
        order = Order.objects.create(...)
        transaction.on_commit(lambda: send_receipt.delay(order.pk))   # after COMMIT
    return order
```

- A task queued inside `atomic()` is visible to the broker immediately, while the row is not yet visible to anyone else. A worker can pick it up and fail with `DoesNotExist` — then succeed on retry, which is exactly the symptom that makes this bug take a day to find (SKILL.md Core Rules 5).
- `transaction.on_commit(callback)` runs after COMMIT, and runs immediately when no transaction is active, so the same function works inside and outside a transaction.
- The same rule covers every outbound side effect: emails, webhooks, cache invalidation, search index updates, payment captures.
- With `ATOMIC_REQUESTS = True` the *whole view* is a transaction, so every naive `.delay()` in the codebase is subject to this — one more reason to prefer explicit `atomic()` blocks.
- `TestCase` never commits, so `on_commit` callbacks never fire in tests unless you use `captureOnCommitCallbacks`.

## Task Design

- **Pass identifiers, never objects.** A serialized model instance carries the field values from the moment of dispatch; by the time the worker runs, the row has changed. `task.delay(order.pk)` and re-fetch inside the task.
- **Assume at-least-once delivery.** Brokers redeliver after a worker dies, and retries re-run the body. Make the task idempotent: check state first (`if order.receipt_sent: return`), or use a unique constraint that turns the second run into a no-op.
- **Keep tasks small and single-purpose.** A task that does five things fails on the third and re-runs the first two on retry.
- **Pass primitives.** Arguments are serialized (JSON by default in Celery); datetimes, Decimals and model instances either fail or arrive with a different type than you sent.
- **Set a time limit on every task.** A task with no limit and a hung HTTP call occupies a worker slot forever; the queue then looks broken for reasons unrelated to the queue.
- **Route by shape, not by feature.** Fast tasks and slow tasks in one queue means the fast ones wait behind a video transcode. Two queues and two worker pools is the whole fix.

## Retries And Failure

```python
@shared_task(bind=True, autoretry_for=(RequestException,), retry_backoff=True,
             retry_jitter=True, max_retries=5, acks_late=True)
def sync_invoice(self, invoice_id): ...
```

- Retry only what is transient: network errors, 429s, 5xx from a provider, lock timeouts. Retrying a `ValidationError` or a 400 just burns the queue five more times.
- Exponential backoff with jitter, or a provider outage turns your retries into a synchronized thundering herd against it.
- `acks_late=True` re-queues a task if the worker dies mid-execution — correct only if the task is idempotent, because "died mid-execution" includes "died after the side effect".
- A dead-letter path matters more than the retry policy: after the last retry, the task must land somewhere a human sees, with its arguments.
- Log the task id and the object id in every task. Without them, a failure in the worker log cannot be tied to the request that queued it.
- Retries with a delay do not hold a database connection — but a task that opens a transaction and then calls an external service does. Do the external call outside the `atomic()` block, in the worker as much as in the view.

## Scheduling

- A periodic task needs a single scheduler process (Celery beat or the platform's scheduler). Two schedulers means every job runs twice.
- Cron-style scheduling of a management command is simpler than a beat process, and easier to run manually when it fails.
- Scheduled jobs must be reentrant: the run at 02:00 may still be going at 03:00. Guard with a database advisory lock or a cache key with a TTL, not a boolean flag that a crash leaves set forever.
- Anything that walks a whole table on a schedule needs batching and a resume key, or its runtime grows with your data until it overlaps itself.
- Recurring cleanups worth having from day one: `clearsessions`, expired tokens, orphaned uploads, old exports.

## Worker Operations

- Workers are separate processes with their own database connections, so they add a **second tier** on top of the web tier rather than replacing it: `peak_connections = (instances × workers_per_instance × threads_per_worker) + (task_workers × concurrency)`. Budget both against the same server limit, or the queue drains the connections the site needs.
- Workers hold long-lived connections. Enable `CONN_HEALTH_CHECKS` (Django >=4.1) or a broken connection after an idle period fails the next task instead of reconnecting.
- Deploys must update workers too. A worker running old code with a new message signature fails on arguments it does not understand — add parameters with defaults, and remove tasks only after the queue is drained.
- Prefetching: a worker that reserves many messages at once leaves them invisible to other workers while it processes one slowly. Lower it for long tasks.
- Monitor queue depth and oldest-message age, not just worker CPU. A queue that is always empty is over-provisioned; one whose age keeps climbing is under-provisioned, and the difference is invisible in CPU graphs.

## Without A Broker

- `transaction.on_commit(lambda: do_work())` runs the work inline after commit. For fast, non-critical work it is the right amount of machinery, and it is not durable: a crash between commit and callback loses it.
- A database-backed queue table with `select_for_update(skip_locked=True)` gives durability and transactional enqueue with no broker, at the cost of writing the worker loop yourself.
- Django's own background task interface exists in recent versions and standardizes the enqueue API; the operational concerns above do not change with the tool.
- Choose deliberately: a broker adds an availability dependency, and a database queue adds load to the database you are already trying to protect.

## Email

- `send_mail` is synchronous: an SMTP call inside a request holds a worker for the round trip and fails the request when the provider is slow. Queue it.
- Backends: SMTP in production, `console` in development, `locmem` in tests (`django.core.mail.outbox` is then the assertion target).
- `EmailMultiAlternatives` for HTML plus a plain-text part; a single HTML body lands in spam more often and is unreadable in text clients.
- Build absolute URLs from a configured site domain, not from `request.get_host()` — a host-header attack otherwise rewrites password-reset links.
- Email is a side effect: `transaction.on_commit`, always. Sending inside the transaction means users receive receipts for orders that rolled back.
