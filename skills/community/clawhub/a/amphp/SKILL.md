---
name: amphp
description: >
  Writing non-blocking, async PHP code using the AMPHP framework — revolt/event-loop,
  amphp/amp ^3, and the full amphp/* ecosystem (http-server, http-client, websocket,
  mysql, redis, parallel, socket, pipeline, file, cache, sync, dns, process).
  Always use this skill when PHP code involves: amphp/* packages, the Revolt event loop,
  Amp\Future, Amp\async(), Amp\delay(), PHP Fibers for async I/O, DeferredFuture,
  TimeoutCancellation, SocketHttpServer, WebsocketClientHandler, or Worker\Task.
  Also use when the user wants to replace blocking PHP (curl_exec, file_get_contents,
  PDO, sleep) with AMPHP async equivalents, build a non-blocking PHP HTTP or WebSocket
  server, run concurrent PHP I/O without pcntl, or debug Revolt event-loop behavior —
  even if they don't say "amphp" explicitly but the context clearly points to this ecosystem.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Agent
---

# AMPHP v3 Skill

## Version

This skill covers **AMPHP v3 only** — `amphp/amp ^3`, `revolt/event-loop ^1`, PHP 8.1+.

If you see v2 patterns (`yield $promise`, `Amp\Loop::run()`, `Promise`, `Coroutine`), treat them as wrong and rewrite using v3 equivalents. See [`docs/v2-v3.md`](docs/v2-v3.md) for the full migration table.

---

## Non-Negotiable Rules

These apply to every file you write or modify in an AMPHP project:

- Always add `declare(strict_types=1)` at the top of every PHP file.
- Always pass `JSON_THROW_ON_ERROR` to every `json_encode` / `json_decode` call.
- Never use blocking I/O (`file_get_contents`, `PDO`, `curl_exec`, `sleep`) inside the event loop — use async equivalents from `amphp/file`, `amphp/mysql`, `amphp/http-client`, `Amp\delay()`.
- Always release mutex/semaphore locks in a `finally` block — exceptions skip cleanup otherwise.
- Always `buffer()` or fully iterate HTTP response bodies — unread bodies block connection reuse.

For the full list of 19+ documented gotchas (buffer deadlocks, channel EOF, arrow function capture, Redis factory vs constructor, etc.), read [`docs/common-mistakes.md`](docs/common-mistakes.md) before writing async code.

---

## Reference Files

Load only the file(s) relevant to the task. Do not load all files at once.

### Docs

| File | When to load |
|------|-------------|
| [`docs/constructors.md`](docs/constructors.md) | Instantiating any AMPHP class — verified constructor signatures, param names, defaults, and factory methods |
| [`docs/namespaces.md`](docs/namespaces.md) | Writing `use` imports — complete namespace paths for every class, function, and enum |
| [`docs/packages.md`](docs/packages.md) | Starting a new project or adding a dependency — `composer require` commands and package overview |
| [`docs/common-mistakes.md`](docs/common-mistakes.md) | Before writing any async code — 19+ real bugs with wrong/correct examples |
| [`docs/v2-v3.md`](docs/v2-v3.md) | Migrating from AMPHP v2 or encountering `yield`/`Promise`/`Coroutine` patterns |

### Examples

| File | When to load |
|------|-------------|
| [`examples/core-async.md`](examples/core-async.md) | EventLoop bootstrap, `async()`, `delay()`, Future combinators (`await`, `awaitAll`, `awaitAny`), `DeferredFuture` |
| [`examples/cancellation.md`](examples/cancellation.md) | `TimeoutCancellation`, `DeferredCancellation`, `CompositeCancellation`, propagating cancellation |
| [`examples/sync.md`](examples/sync.md) | `LocalMutex`, `LocalSemaphore`, `LocalParcel`, `Barrier`, `LocalKeyedMutex`, `RateLimitingSemaphore`, `synchronized()` |
| [`examples/http-server.md`](examples/http-server.md) | Minimal server, Router with route params, Middleware stack, TLS, Sessions, Static files, proxy setup |
| [`examples/http-client.md`](examples/http-client.md) | GET/POST, parallel requests, `ConnectionLimitingPool`, interceptors, proxy, streaming response body |
| [`examples/websocket.md`](examples/websocket.md) | Echo server, push-only with drain pattern, broadcast gateway, WS client, streaming binary messages |
| [`examples/byte-stream.md`](examples/byte-stream.md) | `ReadableBuffer`, `pipe()`, GZIP compress/decompress, Base64 encode/decode, `splitLines()` |
| [`examples/pipelines.md`](examples/pipelines.md) | `Queue` back-pressure, `Pipeline` operators (`map`, `filter`, `tap`), `concurrent()`, `merge()`, `concat()` |
| [`examples/parallel.md`](examples/parallel.md) | `Task` interface, fan-out with worker pool, IPC Channel progress reporting, `ChannelException` handling |
| [`examples/database.md`](examples/database.md) | MySQL connection pool, transactions, prepared statements; Redis get/set/hash/pubsub/cache |
| [`examples/file-io.md`](examples/file-io.md) | `File\read/write/exists/getSize/openFile/listFiles/deleteDirectory/createDirectoryRecursively` |
| [`examples/cache.md`](examples/cache.md) | `LocalCache` (LRU + TTL), `AtomicCache` (compute-if-absent), `PrefixCache`, `NullCache` |
| [`examples/interval.md`](examples/interval.md) | `Interval` repeating timer, `enable/disable`, `weakClosure()` to prevent GC cycles, `EventLoop::delay/repeat/cancel` |
| [`examples/testing.md`](examples/testing.md) | `AsyncTestCase`, constructing mock `Request` objects, `League\Uri\Http::new()`, phpunit CLI flags |

### Workflows

| File | When to load |
|------|-------------|
| [`workflows/http-server-full.md`](workflows/http-server-full.md) | Building a complete HTTP server from scratch: Router + Middleware + Static files + WebSocket + graceful shutdown |
| [`workflows/parallel-fan-out.md`](workflows/parallel-fan-out.md) | CPU-bound workload split across multiple worker processes with IPC progress reporting |
| [`workflows/tcp-server.md`](workflows/tcp-server.md) | Raw TCP server: echo, custom binary protocol, TLS mutual auth, graceful shutdown |

### Templates

| File | When to load |
|------|-------------|
| [`templates/http-server.php`](templates/http-server.php) | Copy-paste boilerplate for a full HTTP server (Router + Middleware + Static files + graceful shutdown) |
| [`templates/websocket-handler.php`](templates/websocket-handler.php) | Copy-paste boilerplate for WebSocket handlers: echo, push-only, broadcast gateway |
| [`templates/parallel-task.php`](templates/parallel-task.php) | Copy-paste boilerplate for a worker `Task` class with IPC progress + fan-out orchestration |

### Scripts

| File | Usage |
|------|-------|
| [`scripts/server-demo.php`](scripts/server-demo.php) | `php scripts/server-demo.php [--port=N]` — run a minimal HTTP server to verify setup |
| [`scripts/http-client-demo.php`](scripts/http-client-demo.php) | `php scripts/http-client-demo.php [url]` — demo GET, parallel requests, ConnectionLimitingPool |

### Resources

| File | When to load |
|------|-------------|
| [`resources/blocking-vs-async.md`](resources/blocking-vs-async.md) | Quick lookup: mapping every common blocking PHP function to its AMPHP v3 async replacement |

### Legacy

| File | Contents |
|------|----------|
| [`references/advanced-patterns.md`](references/advanced-patterns.md) | Deep dives: fiber model internals, all Future combinators, Queue back-pressure mechanics, Pipeline concurrency, Cancellation semantics, EventLoop timer details |
| [`references/class-examples.md`](references/class-examples.md) | One minimal usage example per key AMPHP class, organized by package |
