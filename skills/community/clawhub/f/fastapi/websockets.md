# WebSockets — Connections That Outlive The Request

A WebSocket is a long-lived connection pinned to one worker process. Everything hard about it follows from that: state is per worker, restarts are disconnections, and broadcast needs something outside the process.

## The Endpoint

```python
@router.websocket("/ws/{room}")
async def ws(websocket: WebSocket, room: str, user: Annotated[User, Depends(ws_user)]):
    await websocket.accept()
    try:
        while True:
            msg = await websocket.receive_json()
            await handle(room, user, msg)
    except WebSocketDisconnect:
        pass
    finally:
        await registry.remove(room, websocket)
```

- `accept()` must come before any send or receive; without it the client sees the handshake fail with no explanation.
- `WebSocketDisconnect` is raised by `receive_*` when the peer goes away — it is control flow, not an error, and it must always be caught or every disconnect logs a traceback.
- Cleanup belongs in `finally`: a registry that keeps dead sockets grows until sends start failing en masse.
- Dependencies work in WebSocket routes, but `HTTPException` does not: after the handshake there is no status code to send. Reject with `await websocket.close(code=1008)` (policy violation) or by not accepting at all.

## Close Codes Worth Knowing

| Code | Meaning | Typical cause |
|---|---|---|
| 1000 | Normal closure | Either side finished deliberately |
| 1001 | Going away | Server shutting down, browser navigating |
| 1006 | Abnormal, no close frame | Proxy idle timeout, worker killed, network drop — never sent by an application |
| 1008 | Policy violation | Your auth or validation rejection |
| 1011 | Internal error | Unhandled exception in the handler |
| 4000-4999 | Application-defined | Your own reasons, readable by the client |

Seeing only 1006 in the logs means the connection is being cut below the application: check proxy `proxy_read_timeout`, load-balancer idle timeouts, and whether workers are being recycled.

## Authentication

Browsers cannot set headers on a WebSocket handshake, so `Authorization: Bearer` is unavailable to browser clients. Options, in order of preference:

1. Cookie set by the normal login flow — sent automatically on the handshake, `HttpOnly`, and validated in a dependency (`auth.md`).
2. Short-lived ticket: the client calls an authenticated HTTP endpoint for a one-time token valid for seconds, then connects with `?ticket=...`. Query strings land in access logs, so a long-lived token there is a leak; a single-use ticket is not.
3. First-message authentication: accept, wait for an auth frame with a deadline (`asyncio.timeout`), close 1008 if it does not arrive. Costs an accepted connection per attacker.

Also validate `Origin` on the handshake: browsers do not apply CORS to WebSockets, so any site can open one against your endpoint with the user's cookies attached.

## Broadcast Across Workers

An in-process registry (`dict[room, set[WebSocket]]`) only reaches the clients connected to *that* worker (SKILL.md rule 6). With 4 workers, three quarters of a room miss every message.

- Redis pub/sub is the standard fix: each worker subscribes to the channels its clients care about and fans out locally; publishers publish once. Delivery is at-most-once and messages sent while a worker is down are lost.
- Durability changes the tool: Redis Streams, NATS JetStream, or Kafka when a client must be able to resume after a gap. Design the message with a monotonic id so a reconnecting client can ask for "everything after N".
- Sticky sessions only make a single connection stable; they do not make broadcast work. Both are needed at scale.

## Backpressure and Slow Clients

- `await websocket.send_json(...)` to a client that is not reading eventually blocks on the socket buffer. One slow client can stall the coroutine that fans out to a room.
- Give each connection its own send queue with a bounded size; when the queue is full, drop the client (close 1013 or an application code) instead of degrading everyone.
- Never fan out with a bare `for` loop over sockets awaiting each send — one slow peer delays all the rest. Use `asyncio.gather` over per-connection send tasks with `return_exceptions=True`, and remove the ones that failed.
- Cap connections per user and per IP; a WebSocket costs a file descriptor and a coroutine, and nothing rate-limits handshakes by default.

## Keepalive

- The protocol has ping/pong frames; uvicorn sends pings on an interval and drops the connection when pongs stop. Application-level heartbeats are still useful because they also prove the *handler* is alive, not just the socket.
- Every hop has an idle timeout (proxy, load balancer, corporate middlebox). Heartbeat below the smallest of them or connections die silently at that interval — a "drops after exactly 60 seconds" report is always this.
- Clients need exponential backoff with jitter on reconnect; without jitter, a worker restart brings the entire client population back simultaneously.

## Shutdown

Graceful shutdown drains HTTP requests but cuts WebSockets (`deployment.md`). Close them deliberately on the lifespan's exit path with code 1001 so clients treat it as "reconnect", and keep the client's reconnect logic tested — a rolling deploy exercises it every time.

## When Not To Use One

| Need | Better tool |
|---|---|
| Server → client updates only | SSE: plain HTTP, automatic reconnect, no upgrade issues (`streaming.md`) |
| Updates every few minutes | Polling with `ETag`; a connection per client for that rate is waste |
| Job progress until completion | 202 plus a status endpoint (`background.md`) |
| Guaranteed delivery to offline clients | A queue plus push notifications; a socket only reaches who is connected |
