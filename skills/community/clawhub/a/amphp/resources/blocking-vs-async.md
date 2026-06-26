# Blocking PHP vs AMPHP v3 Async Equivalents

Use this table when replacing standard PHP code with non-blocking AMPHP equivalents.

---

## I/O and networking

| Blocking PHP | AMPHP v3 equivalent | Package |
|---|---|---|
| `sleep(int $seconds)` | `delay(float $seconds)` | `amphp/amp` |
| `usleep(int $microseconds)` | `delay(float $seconds)` | `amphp/amp` |
| `file_get_contents($path)` | `File\read($path)` | `amphp/file` |
| `file_put_contents($path, $data)` | `File\write($path, $data)` | `amphp/file` |
| `fopen` / `fread` / `fwrite` / `fclose` | `File\openFile($path, $mode)` | `amphp/file` |
| `file_exists($path)` | `File\exists($path)` | `amphp/file` |
| `filesize($path)` | `File\getSize($path)` | `amphp/file` |
| `unlink($path)` | `File\deleteFile($path)` | `amphp/file` |
| `mkdir($path, recursive: true)` | `File\createDirectoryRecursively($path, 0755)` | `amphp/file` |
| `scandir($dir)` | `File\listFiles($dir)` | `amphp/file` (returns filenames only!) |
| `rmdir($path)` | `File\deleteDirectory($path)` | `amphp/file` |
| `curl_exec()` | `$client->request(new HttpRequest($url))` | `amphp/http-client` |
| `file_get_contents($url)` (HTTP) | `$client->request(new HttpRequest($url))->getBody()->buffer()` | `amphp/http-client` |
| `dns_get_record()` | `Dns\resolve($hostname)` | `amphp/dns` |
| `stream_socket_client()` | `Socket\connect($uri)` | `amphp/socket` |
| `stream_socket_server()` | `Socket\listen($uri)` | `amphp/socket` |

---

## Database

| Blocking PHP | AMPHP v3 equivalent | Package |
|---|---|---|
| `new PDO(...)` | `new MysqlConnectionPool(MysqlConfig::fromString(...))` | `amphp/mysql` |
| `$pdo->query($sql)` | `$pool->execute($sql, $params)` | `amphp/mysql` |
| `$pdo->beginTransaction()` | `$pool->beginTransaction()` | `amphp/mysql` |
| `$pdo->commit()` | `$transaction->commit()` | `amphp/mysql` |
| `$pdo->rollBack()` | `$transaction->rollback()` | `amphp/mysql` |
| `new Redis()` + `$r->connect()` | `createRedisClient(RedisConfig::fromUri(...))` | `amphp/redis` |
| `$redis->get($key)` | `$client->get($key)` | `amphp/redis` |
| `$redis->set($key, $val)` | `$client->set($key, $val)` | `amphp/redis` |

---

## Concurrency model

| Concept | Blocking PHP | AMPHP v3 |
|---|---|---|
| Run concurrent tasks | `pcntl_fork()` | `async(fn() => ...)` |
| Wait for all | `pcntl_waitpid()` | `Future\await([$f1, $f2])` |
| Wait for first | — | `Future\awaitAny([$f1, $f2])` |
| Cancel a task | `posix_kill()` | `$deferred->cancel()` / `TimeoutCancellation` |
| Mutex / locking | `flock()` | `LocalMutex` + `$lock->acquire()` |
| Limit concurrency | Process pool | `LocalSemaphore(N)` |
| Shared data (safe) | Shared memory / IPC | `LocalParcel` (same process only) |
| CPU-bound work | `pcntl_fork()` / `pthreads` | `Worker\submit(new Task(...))` |

---

## HTTP server

| Blocking PHP | AMPHP v3 |
|---|---|
| `nginx` + `php-fpm` | `SocketHttpServer::createForDirectAccess($logger)` |
| Apache VirtualHost | `$server->expose('0.0.0.0:8080')` |
| `$_GET`, `$_POST` | `$request->getQueryParameter($name)`, `$request->getBody()->buffer()` |
| `header(...)` | `new Response(headers: ['X-Foo' => 'bar'])` |
| `http_response_code(404)` | `new Response(HttpStatus::NOT_FOUND)` |
| `session_start()` / `$_SESSION` | `SessionMiddleware` + `$request->getAttribute(Session::class)` |
| Middleware (PSR-15) | `Middleware` interface + `stackMiddleware($handler, $m1, $m2)` |

---

## Event loop entry points

| Context | How to start the event loop |
|---|---|
| CLI script (top-level) | `EventLoop::run(fn() => ...)` or just call `async()` / `delay()` directly |
| PHPUnit test | Extend `Amp\PHPUnit\AsyncTestCase` |
| Long-running server | `$server->start(...)` + `trapSignal(...)` (or `EventLoop::run()` on Windows) |
| Background worker | Inside `Worker\Task::run()` — the worker already has its own event loop |

---

## Common gotchas summary

| Mistake | Correct approach |
|---|---|
| `sleep(1)` inside event loop | `delay(1.0)` |
| `file_get_contents()` inside handler | `File\read($path)` |
| `new PDO()` connection per request | `new MysqlConnectionPool(...)` once, shared |
| `curl_exec()` | `HttpClientBuilder::buildDefault()->request(...)` |
| Forgetting `$lock->release()` | Always use `finally { $lock->release(); }` |
| Not calling `$queue->complete()` | Consumer hangs forever |
| Leaving response body unread | Always call `->buffer()` or fully iterate |
| `new RedisClient(...)` | Use `createRedisClient()` factory function |
| `Process::__construct()` | Use `Process::start()` static factory |
