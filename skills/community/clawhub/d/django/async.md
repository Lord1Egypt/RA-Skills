# Async — Async Views, ASGI, Channels

Django's async support is real but partial: the request path and the view can be async, while the ORM, the cache backends and most third-party middleware are synchronous and get adapted with a thread hop. Adopt it where the work is outbound I/O; expect little where the work is queries.

## What Is Async And What Is Not

| Layer | State |
|---|---|
| Views | Async since Django >=3.1 — `async def` handlers, async CBVs since >=4.1 |
| ORM | Sync at its core; `a`-prefixed methods (`aget`, `acreate`, `asave`, `acount`, `aexists`, `async for`) exist since Django >=4.1 and wrap the sync path in a thread |
| Middleware | Either, declared with `async_capable` / `sync_capable`; Django adapts at each boundary |
| Templates | Sync rendering |
| Cache and sessions | Async cache methods added in recent versions; the backend still does sync I/O underneath |
| Signals | `asend()` exists; receivers may be either, and a sync receiver runs in a thread |
| Test client | `AsyncClient` for async views |

- Running under WSGI, an `async def` view still works: Django runs it in an event loop inside the worker thread. You get the code style, not the concurrency. Real concurrency needs an ASGI server (uvicorn, daphne, hypercorn).
- `runserver` is a WSGI development server. Testing ASGI-specific behavior means running the ASGI server locally.

## The ORM From Async Code

- `SynchronousOnlyOperation` means an ORM call reached an event loop. Three fixes, in order of preference:
  1. Use the async API: `order = await Order.objects.aget(pk=pk)`, `async for row in qs:`, `await qs.acount()`.
  2. Wrap a block: `await sync_to_async(self.do_the_queries)(pk)` — one thread hop for many queries beats one per query.
  3. In Channels consumers, `database_sync_to_async` — the same thing with connection cleanup wired in.
- `sync_to_async` defaults to `thread_sensitive=True`, which runs the function in a single shared executor thread so Django's thread-local connection state stays coherent. Passing `thread_sensitive=False` gets you a fresh thread and real parallelism — and a separate database connection per call, which breaks any surrounding transaction. Only use it for work that touches no ORM state.
- Lazy evaluation is a trap under async: `qs = Order.objects.filter(...)` is safe, `for o in qs` is not. The evaluation point is what must be awaited or wrapped.
- Attribute access on a related object triggers a query — so `order.customer.name` inside an async view raises `SynchronousOnlyOperation` unless the relation was already fetched with `select_related` in a wrapped block.
- Transactions do not span thread hops the way you expect: `atomic()` is bound to a connection, and each `sync_to_async(thread_sensitive=False)` call may see a different one. Keep a transaction inside a single sync function.

## Where Async Actually Pays

- Fan-out I/O: several outbound HTTP calls per request. `asyncio.gather` over an async HTTP client turns four 200 ms calls into one 200 ms wait; the same view in sync code waits 800 ms.
- Long-lived connections: server-sent events, WebSockets, streaming responses to many idle clients. A sync worker holds a whole thread per connection; an async worker holds a coroutine.
- It does **not** speed up CPU work (still one thread, still the GIL) and it does not speed up an ORM-bound view, because that path crosses back to a thread anyway.
- Async and sync views can coexist in one project. Choose per view; a project-wide migration is rarely justified by measurement.

## Mixed Sync/Async Chains

- Django adapts at every boundary: a sync middleware around an async view means the request crosses into a thread and back. The cost is context switches, not correctness — the claim that one sync middleware makes the whole request sync is wrong, but a chain that alternates sync/async/sync pays on each flip.
- Keep the middleware chain uniform where you can. A middleware declares support with `sync_capable = True` / `async_capable = True`; `django.utils.decorators.sync_and_async_middleware` marks a function-style one as both.
- Blocking calls inside an async view (a sync HTTP client, `time.sleep`, a sync database driver) block the entire event loop, and therefore every other request that worker is serving. This is the failure mode that looks like "the server froze" under low CPU.
- `asgiref.sync.async_to_sync` is the other direction: calling an async function from sync code. It creates or reuses an event loop, and calling it from inside a running loop raises.

## Channels And WebSockets

- Channels replaces the ASGI application with a protocol router: HTTP keeps going to Django, `websocket` goes to your consumers.
- A channel layer (Redis in production, `InMemoryChannelLayer` only for tests) is what lets one process broadcast to connections held by another. Without it, groups work only within a single process — which passes local testing and fails the moment you scale to two workers.
- Consumer lifecycle: `connect` (authenticate here and `accept()` or `close()`), `receive`, `disconnect`. Authentication comes from the scope (`scope["user"]`), which requires the auth middleware stack in the ASGI application.
- Every ORM call in a consumer goes through `database_sync_to_async`. Consumers are long-lived, so a connection leaked per message is a connection leak that grows all day.
- Blocking the consumer's coroutine blocks that connection only, but a shared executor thread pool is finite — heavy per-message work belongs in a task queue.
- Deployment differs from WSGI: sticky sessions are not required (the channel layer handles cross-process delivery), but connection counts, idle timeouts at the proxy, and per-connection memory become the limits.

## Testing Async Code

- `AsyncClient` for async views; `async def` test methods work under Django's test runner (or `pytest-asyncio` with pytest).
- `TestCase` wraps tests in a transaction bound to one connection, which fights async code that opens others. Async database tests generally need `TransactionTestCase`, at a real cost in speed.
- Channels ships `WebsocketCommunicator` for consumer tests — the only way to assert on the handshake and the message flow without a browser.
- A test that passes with `InMemoryChannelLayer` proves nothing about group delivery in production; run at least one integration test against the real layer.
