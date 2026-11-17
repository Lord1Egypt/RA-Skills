# Deployment — Servers, Workers, Static and Media, Release Sequence

Django does not serve itself. Production is an application server running your WSGI or ASGI callable, a web server or CDN in front for static assets and TLS, and a release procedure that applies migrations in a safe order.

## WSGI Or ASGI

| Choose | When |
|---|---|
| gunicorn + `wsgi.py` (sync workers) | The default. Ordinary request/response apps, ORM-bound work |
| gunicorn + `gthread` workers | Many slow outbound calls per request and you are not ready for async |
| uvicorn/hypercorn + `asgi.py` | Async views, WebSockets, SSE, long-lived connections |
| gunicorn with the uvicorn worker class | ASGI with gunicorn's process management |
| A PaaS build pack | It picks one of the above; know which, or the tuning advice will not apply |

- `runserver` is a development server: single-process by default, auto-reloading, and explicitly not hardened. It is never the production answer.
- Async views run under WSGI too, in an event loop inside the worker — correct, but with no concurrency benefit.

## Worker And Connection Math

- Sync workers: gunicorn's own documentation recommends `(2 × cores) + 1` as a starting point. It is a starting point, not a law: measure with your real latency profile.
- Each sync worker serves exactly one request at a time. Throughput ≈ `workers / mean_request_seconds`. Eight workers at 200 ms mean serve about 40 requests per second — if that is short of your peak, more workers or faster requests, nothing else.
- Memory ceiling: `workers × RSS_per_worker` must still leave room for the page cache and for the request-time peak, so size it from RSS measured under load rather than from an idle worker. Django workers commonly sit in the hundreds of megabytes; overcommit and the OOM killer removes a worker mid-request.
- **Database connections (canonical formula): `peak_connections = instances × workers_per_instance × threads_per_worker`**, and every one of them is held for `CONN_MAX_AGE` seconds after the request. Against PostgreSQL's documented default `max_connections` of 100, two instances of sixteen sync workers already claim 32 — a third of the server before any other client connects. Either keep `CONN_MAX_AGE = 0`, or put a pooler in front.
- Set a worker timeout above your slowest legitimate request and below the proxy's timeout, or the proxy returns 504 while the worker keeps burning resources on a request nobody will read.
- `--max-requests` with `--max-requests-jitter` recycles workers periodically: a blunt but effective answer to slow memory growth, and it hides the leak rather than fixing it.
- Preload (`--preload`) shares memory across workers via copy-on-write and disables graceful code reload; it also means anything opened at import (a database connection, a Redis client) is inherited by every worker, which is usually a bug.

## Static Files

```
collectstatic → STATIC_ROOT → served by whitenoise, the web server, or a CDN
```

- `STATICFILES_DIRS` is where your source assets live; `STATIC_ROOT` is the output directory `collectstatic` writes. They must be different directories, or `collectstatic` copies its own output.
- Nothing serves `STATIC_ROOT` automatically. `runserver` serves static files only when `DEBUG = True`. In production it is whitenoise inside the app, the web server, or object storage plus CDN.
- `ManifestStaticFilesStorage` appends a content hash to every filename and writes a manifest. Cache headers can then be immutable and long. It also raises at render time for a file that was never collected — strict on purpose, and the reason a deploy fails loudly instead of 404ing quietly.
- The `STORAGES` setting (Django >=4.2) replaces `STATICFILES_STORAGE` and `DEFAULT_FILE_STORAGE`, which were removed in >=5.1:

```python
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}
```

- Run `collectstatic --noinput` at build time (into the image), not at boot. Doing it at boot multiplies the work by the number of instances and delays every restart.

## Media Files

- User uploads are not static files: they are written at runtime, they must survive deploys, and they must be shared across instances. A local `MEDIA_ROOT` on ephemeral container storage loses them on every deploy.
- Object storage (S3-compatible) with a storage backend is the default answer at more than one instance. Serve private files with time-limited signed URLs, not through a Django view — a view streaming a large file occupies a worker for the whole download.
- Serve user content from a separate domain, or force `Content-Disposition: attachment` and `X-Content-Type-Options: nosniff`.

## Behind A Proxy

- TLS terminates at the proxy, so Django sees plain HTTP. Without `SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")`, `request.is_secure()` is False and `SECURE_SSL_REDIRECT` produces an infinite redirect loop.
- Only set that header when the proxy strips and rewrites it. If a client can send `X-Forwarded-Proto` directly, you have handed it the ability to claim a secure connection.
- `USE_X_FORWARDED_HOST` for host-header-derived URLs; `ALLOWED_HOSTS` still validates the result.
- The client IP is `X-Forwarded-For` — the leftmost value your infrastructure did not add. Getting this wrong makes every rate limit and every audit log point at the proxy.
- Configure the proxy's body size, header size, and read timeout in step with Django's `DATA_UPLOAD_MAX_MEMORY_SIZE` and the worker timeout, or the two layers reject different requests for different reasons.

## Release Sequence

Ordered for a rolling deploy where old and new code run at once:

1. **Build** — install dependencies, `collectstatic`, produce an immutable artifact.
2. **Check** — `manage.py check --deploy` and `makemigrations --check --dry-run` against production settings; both belong in CI, before anything ships.
3. **Migrate** — run once, from one process, before or alongside the new code depending on the change. Only backward-compatible migrations may run *before* the new code; anything destructive waits for the contract deploy.
4. **Roll** — start new instances, let the health check pass, drain the old ones.
5. **Verify** — error rate, latency, and a smoke request on a path that touches the database.

- Migrations must not run from every instance at once: two concurrent `migrate` processes race on the same tables. Use a release phase, a job, or an advisory lock.
- Rollback of code is easy; rollback of a migration is often not. That asymmetry is the reason for expand/contract — it keeps the previous version of the code runnable.
- Health checks should be cheap and honest: a view that returns 200 without touching the database tells you the process is up; one that runs `SELECT 1` tells you it can serve. Pick per endpoint and know which is which.

## Operating It

- Log to stdout, structured, at INFO. The blank-500 failure mode is a logging configuration, not a Django bug.
- Watch: error rate, p95 latency, worker saturation (queued requests), database connection count, and 4xx/5xx split. A rising 499/504 count with flat CPU means workers blocked on I/O.
- An error tracker with `@sensitive_variables` scrubbing beats `ADMINS` email for anything with real traffic.
- Scheduled work belongs in the platform's scheduler running management commands, not in a cron that shells into a random container: `clearsessions`, session and token cleanup, expired-file pruning, backfills.
- Verify the deployment matches the checklist before calling it done: `DEBUG` off, `ALLOWED_HOSTS` set, `SECRET_KEY` from the environment, static files served by something other than Django, media on shared storage, migrations applied once, `check --deploy` clean.
