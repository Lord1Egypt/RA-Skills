# Errors — One Contract, Raised Not Returned

Every failure a client can see should have the same shape, come from the same place, and carry an id that appears in your logs. FastAPI gives three entry points: `HTTPException`, exception handlers, and the validation error hook.

## The Default Bodies

| Failure | Status | Body |
|---|---|---|
| `raise HTTPException(404, "Order not found")` | 404 | `{"detail": "Order not found"}` |
| Request validation fails | 422 | `{"detail": [{"type","loc","msg","input"}, ...]}` |
| Response model validation fails | 500 | Generic error; the real message is in your logs only |
| Unhandled exception | 500 | `{"detail": "Internal Server Error"}` (plus a traceback in the server log) |

`detail` accepts any JSON-serializable value, so `HTTPException(409, {"code": "duplicate_email", "field": "email"})` is a structured error without any custom handler.

## Raise, Never Return

A `JSONResponse` returned from a service function only becomes the response if every caller passes it through untouched — and it skips exception handlers, response-model filtering, and your error logging. Raising travels the same path from any depth (SKILL.md rule 8).

Define domain exceptions once and map them at the edge:

```python
class DomainError(Exception):
    status = 400; code = "domain_error"
class OrderNotFound(DomainError):
    status = 404; code = "order_not_found"

@app.exception_handler(DomainError)
async def handle_domain(request: Request, exc: DomainError):
    return JSONResponse(status_code=exc.status,
                        content={"code": exc.code, "message": str(exc),
                                 "request_id": request.state.request_id})
```

Services raise `OrderNotFound`; the HTTP mapping lives in one file; the same service called from a worker raises the same exception and nobody imports `fastapi` outside the API layer.

## Handler Rules

- Handlers are registered per exception class and matched by inheritance, most specific first. A handler for `Exception` catches everything *except* what a more specific handler claims.
- `HTTPException` has its own built-in handler; a handler for `Exception` does not catch it. To restyle 404s and 401s, override `HTTPException` explicitly:

```python
@app.exception_handler(StarletteHTTPException)
async def handle_http(request, exc): ...
```

- Override validation errors with `RequestValidationError` when the client needs your envelope instead of pydantic's list. Keep `loc` and `type` in the payload — they are what makes a 422 debuggable (`pydantic.md`).
- Handlers run inside the middleware stack, so their responses get CORS headers; an exception that escapes to `ServerErrorMiddleware` does not (SKILL.md rule 9).
- A handler that raises is a 500 with a confusing traceback: keep handlers free of I/O and of anything that can fail.
- `raise HTTPException(...) from exc` preserves the cause in the log while the client sees only `detail`.

## Status Code Choices That Clients Care About

| Situation | Status |
|---|---|
| Body failed validation | 422 (FastAPI default) or 400 — choose one for the whole API |
| Authenticated but not allowed | 403; use 404 when existence itself is private |
| Conflicting write (duplicate key, version mismatch) | 409, with the conflicting field named |
| Client should slow down | 429 with `Retry-After` |
| Upstream failed or timed out | 502 for a bad upstream response, 504 for a timeout — never 500, which says the bug is yours |
| Accepted, still processing | 202 with a status URL (`background.md`) |

422 vs 400 is the one real argument: 422 is FastAPI's default and distinguishes "well-formed but invalid" from "malformed"; teams standardizing on 400 must convert with a `RequestValidationError` handler, not with per-route code.

## Logging the Real Cause

- Log at the boundary, once. Logging in the service *and* the handler produces duplicate stack traces and doubles the noise during an incident.
- `logger.exception(...)` inside the generic handler captures the traceback; the client gets a generic message plus the request id that ties the two together (`observability.md`).
- Never put upstream response bodies, SQL, or environment values in `detail` — they reach the client verbatim.
- 4xx are the client's problem: log them at `INFO` or `WARNING` with the route and code, not with a stack trace. Only 5xx deserve `ERROR`.

## Errors In Special Contexts

- Background tasks: raising there does nothing to the response, which already left. Catch, log, and record the failure yourself (`background.md`).
- Dependencies with `yield`: exceptions from the endpoint pass through the exit half, so the teardown must rollback and re-raise, never swallow (`dependencies.md`).
- WebSockets: `HTTPException` is meaningless after the handshake; close with a code (`websockets.md`).
- Streaming responses: once the first byte is sent, the status is already committed — an error mid-stream can only truncate the body or emit an in-band error event (`streaming.md`).

## Client-Facing Contract

Document errors in the schema so generated clients can handle them: `responses={404: {"model": ErrorBody}, 409: {"model": ErrorBody}}` on the route, or `responses=` on the router for the shared set (`openapi.md`). RFC 9457 `application/problem+json` (`type`, `title`, `status`, `detail`, `instance`) is the standard shape when the API is public; a house envelope is fine when the only consumer is your own front end, as long as it is the same everywhere.
