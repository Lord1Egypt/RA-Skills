# AMPHP v3 — Package Reference

All packages require **PHP >=8.1**, `revolt/event-loop ^1`, `amphp/amp ^3`.

---

## Foundation (always needed)

```bash
composer require revolt/event-loop   # event loop (install explicitly)
composer require amphp/amp           # Future, async(), delay(), Cancellation, Interval
```

---

## I/O and Networking

```bash
composer require amphp/socket        # TCP/UDP/TLS/Unix sockets
composer require amphp/dns           # async DNS resolution
composer require amphp/byte-stream   # ReadableStream, WritableStream, Payload, pipe()
composer require amphp/file          # async filesystem (read, write, openFile, listFiles)
composer require amphp/http-client   # async HTTP client
composer require amphp/http-tunnel   # HTTP CONNECT proxy (Http1TunnelConnector)
```

| Package | Key Classes |
|---------|-------------|
| `amphp/socket` | `Socket`, `SocketServer`, `ConnectContext`, `ClientTlsContext`, `ServerTlsContext`, `BindContext` |
| `amphp/dns` | `DnsResolver`, `Rfc1035StubDnsResolver`, `DnsRecord` |
| `amphp/byte-stream` | `ReadableStream`, `WritableStream`, `ReadableBuffer`, `WritableBuffer`, `ReadableIterableStream`, `Payload`, `CompressingWritableStream`, `DecompressingReadableStream` |
| `amphp/file` | functions: `read()`, `write()`, `openFile()`, `listFiles()`, `exists()`, `getSize()`, `deleteFile()`, `deleteDirectory()`, `createDirectoryRecursively()` |
| `amphp/http-client` | `HttpClientBuilder`, `HttpClient`, `Request`, `Response`, `ConnectionLimitingPool`, `UnlimitedConnectionPool`, `DefaultConnectionFactory` |
| `amphp/http-tunnel` | `Http1TunnelConnector` |

---

## HTTP Server

```bash
composer require amphp/http-server               # core: SocketHttpServer, RequestHandler, Middleware
composer require amphp/http-server-router        # FastRoute routing: Router
composer require amphp/http-server-form-parser   # forms / file upload: Form, StreamingFormParser
composer require amphp/http-server-session       # sessions: SessionMiddleware, LocalSessionStorage
composer require amphp/http-server-static-content # static files: DocumentRoot, StaticResource
```

| Package | Key Classes | When Needed |
|---------|-------------|-------------|
| `amphp/http-server` | `SocketHttpServer`, `RequestHandler`, `Middleware`, `Request`, `Response`, `DefaultErrorHandler`, `ClosureRequestHandler` | Always for servers |
| `amphp/http-server-router` | `Router` (`addRoute`, `setFallback`) | Multiple routes |
| `amphp/http-server-form-parser` | `Form::fromRequest()`, `StreamingFormParser` | HTML forms, uploads |
| `amphp/http-server-session` | `Session`, `SessionMiddleware`, `LocalSessionStorage`, `RedisSessionStorage` | User sessions |
| `amphp/http-server-static-content` | `DocumentRoot`, `StaticResource` | Serving HTML/CSS/JS files |

---

## WebSocket

```bash
composer require amphp/websocket-client   # WS client
composer require amphp/websocket-server   # WS server (on top of http-server)
# amphp/websocket is pulled in automatically (shared primitives)
```

| Package | Key Classes |
|---------|-------------|
| `amphp/websocket-client` | `Rfc6455Connector`, `WebsocketConnection`, `WebsocketHandshake`, `WebsocketMessage` |
| `amphp/websocket-server` | `Websocket` (RequestHandler), `AllowOriginAcceptor`, `WebsocketClientHandler`, `WebsocketClientGateway` |
| `amphp/websocket` | `WebsocketClient` — **NOTE: `WebsocketClient` lives here, NOT in websocket-server!** |

---

## Databases

```bash
composer require amphp/mysql      # async MySQL / MariaDB
composer require amphp/redis      # async Redis
composer require amphp/postgres   # async PostgreSQL
```

| Package | Key Classes |
|---------|-------------|
| `amphp/mysql` | `MysqlConfig`, `MysqlConnectionPool`, `MysqlStatement`, `MysqlResult` |
| `amphp/redis` | `RedisClient`, `RedisConfig`, `RedisSubscriber`, `RedisMap`; factory: `createRedisClient()` |
| `amphp/postgres` | `PostgresConfig`, `PostgresConnectionPool` |

---

## Concurrency and Data Flow

```bash
composer require amphp/sync       # Mutex, Semaphore, Parcel, Barrier
composer require amphp/pipeline   # Queue, Pipeline operators
composer require amphp/cache      # LocalCache, NullCache, AtomicCache, PrefixCache
composer require amphp/parallel   # Worker/Task, child processes
```

| Package | Key Classes |
|---------|-------------|
| `amphp/sync` | `LocalMutex`, `LocalSemaphore`, `LocalParcel`, `Barrier`, `LocalKeyedMutex`, `RateLimitingSemaphore`; function: `synchronized()` |
| `amphp/pipeline` | `Queue`, `Pipeline` |
| `amphp/cache` | `LocalCache`, `NullCache`, `PrefixCache`, `AtomicCache`, `SerializedCache` |
| `amphp/parallel` | `Worker\Task`, `Worker\Execution`; functions: `submit()`, `workerPool()`; `Context`, `DefaultContextFactory` |

---

## Multi-process Scaling

```bash
composer require amphp/cluster    # multiple processes sharing one port (requires ext-sockets)
```

`Cluster`, `ClusterWatcher`, `ServerSocketPipeProvider`

---

## Process & Logging

```bash
composer require amphp/process    # run shell commands asynchronously — Process::start() is a STATIC FACTORY
composer require amphp/log        # async-safe PSR-3 logging (StreamHandler for Amp)
```

---

## Testing

```bash
composer require --dev amphp/phpunit-util   # AsyncTestCase
```

`Amp\PHPUnit\AsyncTestCase` — runs each test inside the Revolt event loop automatically.
