# Middleware — Order, CORS, and Why `BaseHTTPMiddleware` Bites

Middleware wraps the entire request/response cycle, including routes that do not exist and requests that never reach a handler. That reach is the point — and the reason a bad middleware breaks everything at once.

## Order Is Reverse Registration

```python
app.add_middleware(GZipMiddleware)          # registered first  → innermost
app.add_middleware(RequestIDMiddleware)
app.add_middleware(CORSMiddleware, ...)     # registered last   → outermost
```

Request flows outermost → innermost; the response returns innermost → outermost (SKILL.md rule 9).

- CORS outermost means even an error produced above your handlers still carries the headers. CORS registered first is the classic cause of "the browser shows a CORS error but the server logged a 500" — the 500 is real, the CORS message is the symptom.
- GZip innermost, so it compresses the final body and nothing after it rewrites the payload without fixing `Content-Length`.
- Authentication as middleware applies to `/health`, `/docs`, and `/openapi.json` too; auth belongs in dependencies where it can be scoped (`dependencies.md`).

## CORS That Actually Works

```python
app.add_middleware(CORSMiddleware,
    allow_origins=settings.cors_origins,        # explicit list
    allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"], max_age=600)
```

- `allow_origins=["*"]` together with `allow_credentials=True` is rejected by browsers: with credentials the response must echo one concrete origin. The middleware will not warn; the request just fails.
- Preflight is an `OPTIONS` request the middleware answers itself — if it never arrives, the problem is upstream (proxy blocking OPTIONS), not FastAPI.
- Custom response headers the browser must read need `expose_headers=["X-Request-ID", ...]`; only a short safelist is visible otherwise.
- `max_age` caps how long a browser caches preflight (browsers enforce their own ceiling); raising it removes an extra round trip per unique route+method.

## `BaseHTTPMiddleware` vs Pure ASGI

`BaseHTTPMiddleware` (the `@app.middleware("http")` decorator) is convenient and has three real costs:

1. It runs the downstream app in a separate task, so a `contextvar` set by the endpoint is not visible to the middleware after `call_next`. Set context *before* calling down, never expect to read it back.
2. Streaming responses lose backpressure: the body passes through an internal queue, so a large `StreamingResponse` can be buffered in memory instead of flowing to the client (`streaming.md`).
3. Exceptions and cancellation cross a task boundary, which produces confusing tracebacks and makes client-disconnect handling unreliable.

Pure ASGI middleware avoids all three and is barely longer:

```python
class RequestIDMiddleware:
    def __init__(self, app): self.app = app
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        rid = dict(scope["headers"]).get(b"x-request-id", b"").decode() or str(uuid4())
        request_id_var.set(rid)
        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                message["headers"].append((b"x-request-id", rid.encode()))
            await send(message)
        await self.app(scope, receive, send_wrapper)
```

Use `BaseHTTPMiddleware` for quick, non-streaming, low-traffic concerns; use pure ASGI for request ids, timing, tracing, and anything on every request.

## Never Consume The Body

`await request.body()` inside middleware drains the receive channel; the endpoint then waits for a body that will never arrive and the request hangs. If middleware must see the body (signature verification, audit), read it and replay it:

```python
body = b"".join([chunk async for chunk in request.stream()])
async def receive(): return {"type": "http.request", "body": body, "more_body": False}
await self.app(scope, receive, send)
```

Replaying buffers the whole body in memory — cap it, and skip the middleware for upload routes.

## What Belongs Where

| Concern | Middleware | Dependency |
|---|---|---|
| Request id, access log, timing | Yes (pure ASGI) | No — must wrap the response |
| CORS, GZip, HTTPS redirect, trusted hosts | Yes (built-in) | No |
| Authentication, authorization | No | Yes — scoped, typed, testable |
| Tenant resolution used by queries | Only to set a contextvar | Yes, when handlers need the value |
| Response envelope rewriting | Last resort | Better: one response model |

## Built-Ins Worth Adding

- `TrustedHostMiddleware(allowed_hosts=[...])` rejects Host-header attacks that turn into poisoned absolute URLs and password-reset links.
- `HTTPSRedirectMiddleware` only works if the app knows the real scheme — behind a proxy that means correct forwarded headers first (`deployment.md`), otherwise it redirects forever.
- `GZipMiddleware(minimum_size=500)` compresses responses above 500 bytes; below that the header overhead exceeds the saving. Never compress already-compressed payloads (images, video).
- `SessionMiddleware` signs a cookie but does not encrypt it: the contents are readable by the client.

## Debugging Middleware

Symptom-first: comment out the whole stack, confirm the route works bare, then re-add one middleware at a time. A hang points at a consumed body or a `call_next` that is never awaited; a missing header points at order; a 500 with an empty log points at an exception inside the middleware itself, which never reaches your handlers.
