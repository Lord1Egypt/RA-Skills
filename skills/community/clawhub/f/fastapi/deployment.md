# Deployment — Workers, Proxies, Shutdown, Containers

An ASGI app in production is three decisions: how many processes, what sits in front, and how it stops. Each has a default that is wrong for someone.

## Process Model

| Setup | Command | When |
|---|---|---|
| Single process | `uvicorn app.main:app --host 0.0.0.0 --port 8000` | One container per process, orchestrator does the scaling |
| Uvicorn multi-worker | `uvicorn app.main:app --workers 4` | One VM or one fat container, no orchestrator |
| Gunicorn + uvicorn workers | `gunicorn app.main:app -k uvicorn.workers.UvicornWorker -w 4` | You want gunicorn's supervision, `--max-requests` recycling, and preload behavior |
| Dev | `fastapi dev` (fastapi >=0.111) or `uvicorn --reload` | Local only |

- Start at 1 worker per CPU core for async workloads and measure; the `(2 × cores) + 1` rule comes from *sync* gunicorn workers, where each process handles one request at a time, and it over-provisions an async app that already multiplexes.
- Every worker multiplies memory and connections: pool per worker (SKILL.md rule 5), cache per worker, WebSocket clients per worker (rule 6).
- `--reload` forces a single process and silently ignores `--workers`; never run reload in production, where it also watches the filesystem forever.
- Under an orchestrator, prefer one worker per container: restarts, limits, and metrics all become per-process instead of averaged.
- `--limit-max-requests N` (gunicorn `--max-requests`) recycles a worker after N requests — a legitimate patch for a leak you have not found yet, not a substitute for finding it.

## Behind A Proxy

```bash
uvicorn app.main:app --proxy-headers --forwarded-allow-ips="10.0.0.0/8"
```

- Without `--proxy-headers`, every client IP in your logs is the proxy and every generated URL is `http://`. `--forwarded-allow-ips` defaults to `127.0.0.1`, so a proxy on another host has its headers ignored — the most common cause of "we enabled proxy headers and nothing changed".
- Never trust `X-Forwarded-For` from the internet: only accept it from the proxy's address range, and read the correct position in the chain.
- Serving under a path prefix (`/api`) that the proxy strips: set `root_path="/api"` on the app (or `--root-path`). It fixes the docs, `openapi.json`, and `url_for`; it does not change route matching.
- Proxy timeouts must exceed your slowest legitimate response, and the proxy's body-size limit is the real upload cap — nginx's `client_max_body_size` defaults to 1 MB and returns 413 before FastAPI sees a byte (`streaming.md`).
- Buffering proxies break streaming and SSE; disable per-route (`streaming.md`).

## Timeouts You Must Set

| Setting | Default | Meaning |
|---|---|---|
| uvicorn `--timeout-keep-alive` | 5 s | How long an idle keep-alive connection is held; raise only to match a load balancer that reuses connections longer |
| gunicorn `--timeout` | 30 s | Kills a worker that stops heartbeating. Uvicorn workers heartbeat during long requests, so this does **not** cut a slow request — you still need per-request deadlines (`async.md`) |
| gunicorn `--graceful-timeout` | 30 s | Time given to finish in-flight requests on shutdown before SIGKILL |
| Client/upstream timeouts | none | `httpx.AsyncClient(timeout=5.0)`; without it a hung upstream ties up the worker (SKILL.md rule 7) |

## Graceful Shutdown

On SIGTERM, uvicorn stops accepting new connections and waits for in-flight requests. What breaks that:

- Being PID 1 in a container without signal handling: run the server as the container's actual entrypoint (exec form), or the signal never arrives and the platform SIGKILLs after its grace period.
- The load balancer still routing to a pod that already stopped accepting: add a small pre-stop delay (a few seconds) so endpoints are deregistered before shutdown starts.
- Lifespan teardown that hangs (a pool that will not drain, a queue consumer with no cancel path) — the platform kills the process mid-request instead.
- Long-lived connections: WebSockets are not "in-flight requests" and are cut at shutdown; tell clients to reconnect (`websockets.md`).
- Readiness must flip to failing *before* shutdown work begins, liveness must stay passing during it (`observability.md`).

## Containers

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt   # layer before source
COPY src/ .
USER 10001
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

- Bind `0.0.0.0`; the default `127.0.0.1` is unreachable from outside the container no matter what you publish.
- Exec-form `CMD` so SIGTERM reaches uvicorn.
- Install dependencies in a layer above the source copy, or every code edit reinstalls everything.
- Alpine plus compiled wheels (asyncpg, pydantic-core, cryptography) means building from source on musl: `-slim` is the safer default.
- Set memory limits and check them against worker count: 4 workers × the app's resident size, plus the page cache the kernel counts against the container.

## Serverless And PaaS

- A per-request container means no warm pool: use `NullPool` and an external connection pooler, or the first burst exhausts the database (`database.md`).
- Lifespan may run per invocation; anything expensive at startup becomes per-request latency. Move model loading and JWKS fetching behind a lazy cache.
- Long-running WebSockets and background tasks do not survive the response — use the platform's queue (`background.md`).

## Release Checklist

- Migrations as a separate release step, never in lifespan (`database.md`)
- `--proxy-headers` plus a correct `--forwarded-allow-ips`, and `root_path` if the prefix is stripped
- Docs disabled or protected if the API is internal (`openapi.md`)
- Health and readiness endpoints unauthenticated and cheap (`observability.md`)
- Worker count, pool size, and the database connection limit reconciled with the formula in SKILL.md rule 5
- Structured logs to stdout with a request id; no secrets in the log or the environment dump
