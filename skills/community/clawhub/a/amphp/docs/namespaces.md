# AMPHP v3 — Namespace Cheat Sheet

All `use` import paths, verified against amphp project source files.

---

## Core (revolt + amphp/amp)

```php
use Revolt\EventLoop;
// Low-level EventLoop API (prefer Amp\delay() inside Fibers):
//   EventLoop::run(?callable): void           — start event loop
//   EventLoop::delay(float, callable): string — one-shot timer, returns ID
//   EventLoop::repeat(float, callable): string — recurring timer, returns ID
//   EventLoop::cancel(string $id): void       — cancel registered callback by ID

use function Amp\async;           // async(\Closure): Future — start a Fiber
use function Amp\delay;           // delay(float, bool $ref = true, ?Cancellation): void
use function Amp\trapSignal;      // trapSignal(int|array, bool $ref = true, ?Cancellation): int
use function Amp\weakClosure;     // weakClosure(\Closure): \Closure — weak $this reference

use Amp\Future;
use function Amp\Future\await;      // await(iterable<Future>): array — throws on first error
use function Amp\Future\awaitAll;   // awaitAll(iterable): [$errors, $values] — never throws
use function Amp\Future\awaitAny;   // awaitAny(iterable): mixed — first SUCCESS
use function Amp\Future\awaitFirst; // awaitFirst(iterable): mixed — first completion (may throw)
use function Amp\Future\awaitAnyN;  // awaitAnyN(int, iterable): array — first N successes

use Amp\DeferredFuture;             // low-level manually-resolved Future
use Amp\Interval;                   // repeating timer (auto-cancels on GC)
```

## Cancellation

```php
use Amp\Cancellation;               // interface: throwIfRequested(), subscribe(), unsubscribe()
use Amp\CancelledException;         // thrown when cancelled
use Amp\NullCancellation;           // no-op cancellation
use Amp\TimeoutCancellation;        // cancel after N seconds: new TimeoutCancellation(float $sec)
use Amp\DeferredCancellation;       // manual cancel: ->cancel(); ->getCancellation()
use Amp\CompositeCancellation;      // first-wins: new CompositeCancellation(...$cancellations)
```

## ByteStream

```php
use Amp\ByteStream;                                           // namespace for functions
use function Amp\ByteStream\buffer;                          // buffer(ReadableStream): string
use function Amp\ByteStream\pipe;                            // pipe(Readable, Writable): void — does NOT close sink
use function Amp\ByteStream\splitLines;                      // splitLines(ReadableStream): iterable<string>

use Amp\ByteStream\ReadableBuffer;                           // wrap string as ReadableStream
use Amp\ByteStream\WritableBuffer;                           // collect written chunks into string
use Amp\ByteStream\ReadableIterableStream;                   // wrap array/iterable as ReadableStream
use Amp\ByteStream\Payload;                                  // bufferable + streamable access

use Amp\ByteStream\Compression\CompressingWritableStream;   // GZIP compress on write
use Amp\ByteStream\Compression\DecompressingReadableStream; // GZIP decompress on read

use Amp\ByteStream\Base64\Base64EncodingReadableStream;     // Base64 encode
use Amp\ByteStream\Base64\Base64DecodingReadableStream;     // Base64 decode (use ReadableIterableStream as source!)
```

## Sync (amphp/sync)

```php
use Amp\Sync\LocalMutex;           // exclusive lock: acquire() → Lock → release()
use Amp\Sync\LocalSemaphore;       // N concurrent permits: new LocalSemaphore(int $permits)
use Amp\Sync\LocalParcel;          // mutex + value: new LocalParcel(Mutex, mixed $initial)
use Amp\Sync\Barrier;              // N-fiber rendezvous: new Barrier(int $count)
use Amp\Sync\LocalKeyedMutex;      // per-key locking: acquire(string $key) → Lock
use Amp\Sync\RateLimitingSemaphore; // throttle: new RateLimitingSemaphore(Semaphore, float $lockPeriod)
use Amp\Sync\ChannelException;     // thrown when Channel closes from remote end
use Amp\Sync\Channel;              // IPC channel: send(), receive() (throws ChannelException on EOF)
use function Amp\Sync\synchronized; // synchronized(Mutex, \Closure): mixed — NAMESPACE FUNCTION, not method!
```

## Pipeline (amphp/pipeline)

```php
use Amp\Pipeline\Queue;            // back-pressure queue: push(), complete(), error(), iterate()
use Amp\Pipeline\Pipeline;         // lazy operators: fromIterable(), filter(), map(), ...
```

## Cache (amphp/cache)

```php
use Amp\Cache\LocalCache;          // LRU in-memory: new LocalCache(?int $sizeLimit = null, float $gcInterval = 5)
use Amp\Cache\NullCache;           // no-op cache
use Amp\Cache\PrefixCache;         // key prefix decorator: new PrefixCache(Cache, string $prefix)
use Amp\Cache\AtomicCache;         // compute-if-absent: new AtomicCache(Cache, KeyedMutex)
use Amp\Cache\SerializedCache;     // serialize values: new SerializedCache(StringCache $cache, Serializer $serializer)
                                   // NOTE: first param is StringCache, not Cache!
```

## File (amphp/file)

```php
use Amp\File;
// Functions (all non-blocking):
// File\read(string $path): string
// File\write(string $path, string $data): void
// File\exists(string $path): bool
// File\getSize(string $path): int
// File\deleteFile(string $path): void
// File\deleteDirectory(string $path): void
// File\createDirectoryRecursively(string $path, int $mode = 0777): void
// File\listFiles(string $path): string[]   — FILENAMES ONLY, not full paths!
// File\openFile(string $path, string $mode): File\File   — streaming I/O
```

## Socket (amphp/socket)

```php
use Amp\Socket;
// Functions: Socket\connect(string $uri, ?ConnectContext): Socket
//            Socket\listen(string $uri, ?BindContext): SocketServer
use Amp\Socket\ConnectContext;
use Amp\Socket\BindContext;
use Amp\Socket\ClientTlsContext;
use Amp\Socket\ServerTlsContext;
use Amp\Socket\Certificate;
use Amp\Socket\ResourceServerSocketFactory;   // for SocketHttpServer direct constructor: new ResourceServerSocketFactory(?int $chunkSize = null)
use Amp\Http\Server\Driver\SocketClientFactory;    // for SocketHttpServer direct constructor: new SocketClientFactory(PsrLogger $logger)
```

## HTTP Client (amphp/http-client)

```php
// IMPORTANT: Amp\Http\Client\Request ≠ Amp\Http\Server\Request — alias one when both in scope!
use Amp\Http\Client\HttpClientBuilder;                          // factory: buildDefault() or custom
use Amp\Http\Client\Request as HttpRequest;                    // alias avoids conflict
use Amp\Http\Client\Response as HttpResponse;
use Amp\Http\Client\Connection\ConnectionLimitingPool;         // ::byAuthority(int $max): self
use Amp\Http\Client\Connection\UnlimitedConnectionPool;
use Amp\Http\Client\Connection\DefaultConnectionFactory;
use Amp\Http\Client\Interceptor\DecompressResponse;
use Amp\Http\Client\Interceptor\FollowRedirects;
use Amp\Http\Client\Interceptor\RetryRequests;
use Amp\Http\HttpStatus;                                        // shared constants: HttpStatus::OK, etc.
```

## HTTP Server (amphp/http-server)

```php
use Amp\Http\Server\SocketHttpServer;
use Amp\Http\Server\DefaultErrorHandler;
use Amp\Http\Server\RequestHandler;
use Amp\Http\Server\Request;                                    // server-side (≠ client-side!)
use Amp\Http\Server\Response;
use Amp\Http\Server\Middleware;
use Amp\Http\Server\Router;                                     // from amphp/http-server-router
use Amp\Http\Server\RequestHandler\ClosureRequestHandler;      // inline handler without a class
use Amp\Http\Server\Driver\SocketClientFactory;                // for SocketHttpServer direct constructor
use Amp\Http\Server\StaticContent\DocumentRoot;                // serve directory
use Amp\Http\Server\StaticContent\StaticResource;             // serve single file
use Amp\Http\Server\FormParser\Form;                           // from amphp/http-server-form-parser
use Amp\Http\Server\Session\{Session, SessionMiddleware, LocalSessionStorage, CookieAttributes};
use function Amp\Http\Server\Middleware\stackMiddleware;        // apply multiple middlewares
```

## WebSocket

```php
use Amp\Websocket\WebsocketClient;                              // from amphp/websocket — NOT websocket-server!
use Amp\Websocket\Server\Websocket;                            // RequestHandler wrapping WS logic
use Amp\Websocket\Server\AllowOriginAcceptor;
use Amp\Websocket\Server\WebsocketClientHandler;               // interface: handleClient()
use Amp\Websocket\Server\WebsocketClientGateway;               // broadcast to all clients

use Amp\Websocket\Client\Rfc6455Connector;                     // WS client connector
use Amp\Websocket\Client\WebsocketHandshake;
```

## MySQL / Redis

```php
use Amp\Mysql\MysqlConfig;
use Amp\Mysql\MysqlConnectionPool;

use Amp\Redis\RedisConfig;
use Amp\Redis\RedisSubscriber;
use function Amp\Redis\createRedisClient;   // FACTORY — do NOT use RedisClient constructor directly
use function Amp\Redis\createRedisConnector;
```

## Parallel (amphp/parallel)

```php
use Amp\Parallel\Worker\Task;            // interface: run(Channel, Cancellation): mixed
use Amp\Parallel\Worker\Execution;       // getChannel(), getFuture()
use function Amp\Parallel\Worker\submit; // submit(Task): Execution
use function Amp\Parallel\Worker\workerPool; // workerPool(): WorkerPool
use Amp\Parallel\Context\DefaultContextFactory; // long-lived child process
```

## Process (amphp/process)

```php
use Amp\Process\Process;
// Process::start() is a STATIC FACTORY — NOT a constructor!
// Process::start(string|array $command, ?string $cwd, array $env, ...): self
```

## DNS (amphp/dns)

```php
use Amp\Dns;
use Amp\Dns\DnsRecord;
use Amp\Dns\Rfc1035StubDnsResolver;
// Global resolver setter: Amp\Dns\dnsResolver(DnsResolver $resolver) — function is dnsResolver(), NOT resolver()
```

## Testing

```php
use Amp\PHPUnit\AsyncTestCase;           // base test class; runs each test inside Revolt event loop
```

---

> **Key rule**: `Amp\Http\Client\Request` and `Amp\Http\Server\Request` are **different classes**.
> In files that use both, alias the client one:
> ```php
> use Amp\Http\Client\Request as ClientRequest;
> use Amp\Http\Server\Request; // server-side keeps the plain name
> ```
