# AMPHP v3 — Verified Constructor Signatures

All signatures verified against vendor source files in an AMPHP v3 project (revolt/event-loop ^1, amphp/amp ^3).

---

## Core (amphp/amp)

```php
// Cancellation
new TimeoutCancellation(float $timeout, string $message = "Operation timed out")
new DeferredCancellation()
new CompositeCancellation(Cancellation ...$cancellations)  // variadic, NOT array
new NullCancellation()

// Future
new DeferredFuture()

// Timer
new Interval(float $interval, \Closure $closure, bool $reference = true)
// $reference = false: let the event loop exit even if the Interval is still alive
```

---

## Sync (amphp/sync)

```php
new LocalMutex()
new LocalSemaphore(int $maxLocks)        // param name: $maxLocks
new LocalParcel(Mutex $mutex, mixed $value)
new Barrier(int $count)
new LocalKeyedMutex()
new RateLimitingSemaphore(Semaphore $semaphore, float $lockPeriod)
// lockPeriod MUST be > 0
```

---

## Cache (amphp/cache)

```php
new LocalCache(?int $sizeLimit = null, float $gcInterval = 5)
// $sizeLimit = null → unlimited; $gcInterval = GC sweep interval in seconds
// Named arg: new LocalCache(sizeLimit: 100)

new AtomicCache(Cache $cache, KeyedMutex $mutex)
// Typical: new AtomicCache(new LocalCache(), new LocalKeyedMutex())

new PrefixCache(Cache $cache, string $keyPrefix)
// get key prefix: $cache->getKeyPrefix()

// NullCache: no constructor (uses default)
new NullCache()
```

---

## Pipeline (amphp/pipeline)

```php
new Queue(int $bufferSize = 0)
// bufferSize = 0 means no buffering; push() suspends until consumer reads
// bufferSize = N allows N items to be queued without suspension

// Pipeline: prefer static factories (constructor accepts ConcurrentIterator directly):
Pipeline::fromIterable(\Closure|iterable $iterable): Pipeline  // NOTE: accepts Closure too!
Pipeline::merge(array $pipelines): Pipeline
Pipeline::concat(array $pipelines): Pipeline
Pipeline::generate(\Closure $supplier): Pipeline
```

---

## ByteStream (amphp/byte-stream)

```php
new ReadableBuffer(?string $contents = null)
// contents = null → empty stream (EOF immediately)

new WritableBuffer()
// collect chunks: $buf->buffer() after $buf->end()

new ReadableIterableStream(iterable $iterable)
// wraps array or generator as ReadableStream
// Use instead of ReadableBuffer as source for Base64DecodingReadableStream

new Payload(ReadableStream $stream)
// buffer all: $payload->buffer()
// stream: $payload->read() → null on EOF
```

---

## HTTP Server (amphp/http-server)

```php
// Response
new Response(
    int $status = HttpStatus::OK,
    array $headers = [],
    ReadableStream|string $body = '',
    ?Trailers $trailers = null,
)

// Request (for testing — normal requests are created by the server)
new Request(
    Client $client,
    string $method,
    UriInterface $uri,          // use League\Uri\Http::new($url) in tests
    array $headers = [],
    ReadableStream|string $body = '',
    string $protocol = "1.1",
    ?Trailers $trailers = null,
)

// SocketHttpServer — direct constructor (for custom control)
new SocketHttpServer(
    PsrLogger $logger,
    ServerSocketFactory $serverSocketFactory,   // new ResourceServerSocketFactory()
    ClientFactory $clientFactory,               // new SocketClientFactory($logger)
    array $middleware = [],
    ?array $allowedMethods = AllowedMethodsMiddleware::DEFAULT_ALLOWED_METHODS,
    ?HttpDriverFactory $httpDriverFactory = null,
)

// SocketHttpServer — factory for direct access (most common)
SocketHttpServer::createForDirectAccess(
    PsrLogger $logger,
    bool $enableCompression = true,
    int $connectionLimit = 1000,
    int $connectionLimitPerIp = 10,
    ?int $concurrencyLimit = 1000,
    ?array $allowedMethods = AllowedMethodsMiddleware::DEFAULT_ALLOWED_METHODS,
    ?HttpDriverFactory $httpDriverFactory = null,
    ?ExceptionHandler $exceptionHandler = null,
): SocketHttpServer

// SocketHttpServer — factory for behind proxy
SocketHttpServer::createForBehindProxy(
    PsrLogger $logger,
    ForwardedHeaderType $headerType,            // ForwardedHeaderType::XForwardedFor etc.
    array $trustedProxies,                      // CIDR strings: ['10.0.0.0/8', ...]
    bool $enableCompression = true,
    ?int $concurrencyLimit = 1000,
    ?array $allowedMethods = AllowedMethodsMiddleware::DEFAULT_ALLOWED_METHODS,
    ?HttpDriverFactory $httpDriverFactory = null,
    ?ExceptionHandler $exceptionHandler = null,
): SocketHttpServer
```

---

## HTTP Client (amphp/http-client)

```php
// Request
new Request(string|UriInterface $uri, string $method = 'GET')

// HttpClientBuilder
HttpClientBuilder::buildDefault(): HttpClient  // static factory, no constructor
(new HttpClientBuilder())
    ->intercept(ApplicationInterceptor $interceptor): self
    ->usingPool(ConnectionPool $pool): self
    ->followRedirects(int $maxRedirects): self
    ->build(): HttpClient

// ConnectionLimitingPool — constructor is private, use static factory:
ConnectionLimitingPool::byAuthority(int $connectionLimit): self
// Example: ConnectionLimitingPool::byAuthority(2) — max 2 connections per host
```

---

## WebSocket Server (amphp/websocket-server)

```php
// Websocket — RequestHandler that upgrades HTTP to WebSocket
new Websocket(
    HttpServer $httpServer,                                     // positional or httpServer:
    PsrLogger $logger,                                         // logger:
    WebsocketAcceptor $acceptor,                               // acceptor:
    WebsocketClientHandler $clientHandler,                     // clientHandler:
    ?WebsocketCompressionContextFactory $compressionFactory = null,
    WebsocketClientFactory $clientFactory = new Rfc6455ClientFactory(),
)

// AllowOriginAcceptor
new AllowOriginAcceptor(
    array $allowOrigins,                                        // param name is $allowOrigins, NOT $allowedOrigins!
    ErrorHandler $errorHandler = new Internal\UpgradeErrorHandler(),
    WebsocketAcceptor $acceptor = new Rfc6455Acceptor(),
)
// Example: new AllowOriginAcceptor(['https://example.com', 'http://localhost:8080'])

// WebsocketClientGateway — no constructor args
new WebsocketClientGateway()
```

---

## Parallel (amphp/parallel)

```php
// Task — interface, not a class:
interface Task {
    public function run(Channel $channel, Cancellation $cancellation): mixed;
}

// Global functions:
submit(Task $task, ?Cancellation $cancellation = null): Execution  // uses global worker pool
workerPool(?WorkerPool $pool = null): WorkerPool                   // get/set global pool

// Execution methods:
$execution->getFuture(): Future<mixed>
$execution->getChannel(): Channel
```

---

## TLS / Socket (amphp/socket)

```php
new Certificate(string $certFile, ?string $keyFile = null, ?string $passphrase = null)

new ClientTlsContext(string $peerName = '')
    ->withDefaultCertificate(Certificate $certificate): self
    ->withPeerName(string $peerName): self
    ->withoutPeerNameVerification(): self

new ServerTlsContext()
    ->withDefaultCertificate(Certificate $certificate): self

new BindContext()
    ->withTlsContext(ServerTlsContext $tlsContext): self
    ->withTcpNoDelay(): self

// Listen / Connect (functions, not constructors):
Socket\listen(SocketAddress|string $address, ?BindContext $bindContext = null): ResourceServerSocket
Socket\connect(SocketAddress|string $uri, ?ConnectContext $context = null, ?Cancellation $cancellation = null): Socket

// ResourceServerSocketFactory — for SocketHttpServer direct constructor:
new ResourceServerSocketFactory(?int $chunkSize = null)

// SocketClientFactory — for SocketHttpServer direct constructor:
new SocketClientFactory(PsrLogger $logger, float $tlsHandshakeTimeout = 5)
```

---

## Router (amphp/http-server-router)

```php
new Router(
    HttpServer $httpServer,
    LoggerInterface $logger,
    ErrorHandler $errorHandler,
    int $cacheSize = Router::DEFAULT_CACHE_SIZE,  // DEFAULT_CACHE_SIZE = 512
)
// Add routes: $router->addRoute('GET', '/path', $handler)
// Fallback:   $router->setFallback($handler)
```

---

## DocumentRoot (amphp/http-server-static-content)

```php
new DocumentRoot(
    HttpServer $httpServer,
    ErrorHandler $errorHandler,
    string $root,               // absolute path to directory
    ?Filesystem $filesystem = null,
)
```

---

## Key naming rules

- `LocalSemaphore` param: `$maxLocks` (not `$locks`)
- `LocalCache` param: `$sizeLimit` nullable, default `null` (not `2000`)
- `Interval` param: `$closure` typed as `\Closure` (arrow functions are valid Closures)
- `CompositeCancellation` is variadic (`...$cancellations`), not `array`
- `ConnectionLimitingPool` constructor is **private** — always use `::byAuthority(int)`
- `SocketHttpServer` direct constructor needs `ResourceServerSocketFactory` + `SocketClientFactory($logger)`
- `AllowOriginAcceptor` param: `$allowOrigins` (NOT `$allowedOrigins`)
- `SerializedCache` first param is `StringCache` (not generic `Cache`)
- `Socket\listen()` param: `$bindContext` (not `$context`)
- `submit()` accepts optional `?Cancellation $cancellation = null` as second arg
- `Pipeline::fromIterable()` accepts `\Closure|iterable` (not just `iterable`)
- `Router` requires `HttpServer`, `LoggerInterface`, `ErrorHandler` — not zero-arg!
- `DocumentRoot` requires `HttpServer`, `ErrorHandler`, `string $root` — not zero-arg!
