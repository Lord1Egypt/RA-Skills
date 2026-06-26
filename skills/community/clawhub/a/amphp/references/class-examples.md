# AMPHP Class Examples

## amphp/amp

### Future
```php
use Amp\Future;
use function Amp\async;
use function Amp\Future\{await, awaitAll, awaitAny, awaitFirst, awaitAnyN};

// Await a single future
$future = async(fn() => expensiveComputation());
$value = $future->await();

// await() — all must succeed, throws on first error, preserves keys
[$result1, $result2] = await([
    async(fn() => fetchData('url1')),
    async(fn() => fetchData('url2')),
]);

// awaitAll() — collects results AND errors, never throws
[$errors, $values] = awaitAll([$future1, $future2]);
foreach ($errors as $key => $exception) { /* handle */ }

// awaitAny() — first SUCCESSFULLY completed value (skips errors)
$first = awaitAny([$slow, $fast]);

// awaitFirst() — first completed, whether success or error (may throw)
$fastest = awaitFirst([$future1, $future2]);

// awaitAnyN() — first N successful results (verified in project FutureDemo.php)
$twoResults = awaitAnyN(2, [$f1, $f2, $f3, $f4]);

// Future static factories (no async work needed)
$future = Future::complete('cached_value');
$future = Future::error(new \RuntimeException('fail'));

// Chaining: map() transforms, catch() recovers, finally() always runs
$result = Future::complete('hello')
    ->map(fn(string $v) => strtoupper($v))
    ->catch(fn(\Throwable $e) => 'default')
    ->finally(fn() => cleanup())
    ->await();
```

### DeferredFuture
```php
use Amp\DeferredFuture;

$deferred = new DeferredFuture();
$future = $deferred->getFuture();

\Amp\async(function () use ($deferred) {
    \Amp\delay(1.0);
    $deferred->complete('done');
});

$value = $future->await(); // 'done'

// Signal failure
$deferred->error(new \RuntimeException('Failed'));
```

### TimeoutCancellation
```php
use Amp\TimeoutCancellation;
use Amp\Http\Client\HttpClientBuilder;
use Amp\Http\Client\Request;

$client = HttpClientBuilder::buildDefault();
$cancellation = new TimeoutCancellation(5.0); // 5-second deadline

try {
    $response = $client->request(new Request('https://example.com'), $cancellation);
    $body = $response->getBody()->buffer();
} catch (\Amp\CancelledException $e) {
    echo "Request timed out\n";
}
```

### DeferredCancellation
```php
use Amp\DeferredCancellation;

$deferredCancellation = new DeferredCancellation();
$cancellation = $deferredCancellation->getCancellation();

$future = \Amp\async(function () use ($cancellation) {
    while (true) {
        \Amp\delay(0.1, cancellation: $cancellation);
        // do work
    }
});

\Amp\delay(1.0);
$deferredCancellation->cancel(); // stop the loop
```

### CompositeCancellation
```php
use Amp\CompositeCancellation;
use Amp\TimeoutCancellation;
use Amp\DeferredCancellation;

$userAbort = new DeferredCancellation();
// Cancel if either the user aborts OR 30 s elapse
$cancellation = new CompositeCancellation(
    $userAbort->getCancellation(),
    new TimeoutCancellation(30.0),
);

$response = $httpClient->request($request, $cancellation);
```

### Interval
```php
use Amp\Interval;

// Constructor: new Interval(float $interval, \Closure $closure, bool $reference = true)
// $reference = false → same as calling unreference() immediately (loop may exit while Interval lives).
// The closure is called every $interval seconds until the Interval is GC'd or disabled.
$count = 0;
$interval = new Interval(0.5, function () use (&$count): void {
    echo "Tick #{$count}\n";
    $count++;
});

// Background heartbeat that does NOT keep the event loop alive:
$heartbeat = new Interval(5.0, fn() => ping(), reference: false);

// Interval fires automatically; disable/re-enable as needed
$interval->disable();  // pause
$interval->enable();   // resume (waits full timeout before next call)

// NOTE: Interval has NO iterate() method and NO cancel() method.
// It is automatically stopped when garbage collected.
// Use weakClosure() when the closure references $this to avoid circular GC issues:
// $interval = new Interval(1.0, weakClosure(fn() => $this->tick()));

// unreference(): let the event loop exit even while the Interval is still alive.
// Useful for background heartbeats that should not keep the process running.
$interval->unreference();
// reference(): re-register the Interval so the event loop waits for it again.
$interval->reference();
```

### async() / delay()
```php
use function Amp\async;
use function Amp\delay;
use Amp\Future;

// Fire-and-forget background task
async(function () {
    delay(2.0);
    echo "Background task done\n";
});

// Parallel fan-out
$futures = array_map(
    fn(string $url) => async(fn() => fetchUrl($url)),
    ['https://a.com', 'https://b.com', 'https://c.com'],
);
$results = Future\await($futures);
```

---

## amphp/byte-stream

### ReadableBuffer
```php
use Amp\ByteStream\ReadableBuffer;

$stream = new ReadableBuffer("Hello, World!");
$chunk  = $stream->read(); // "Hello, World!"
$eof    = $stream->read(); // null — stream exhausted
```

### WritableBuffer
```php
use Amp\ByteStream\WritableBuffer;

$buffer = new WritableBuffer();
$buffer->write("chunk1");
$buffer->write("chunk2");
$buffer->end();
$result = $buffer->buffer(); // "chunk1chunk2"
```

### ReadableResourceStream / WritableResourceStream
```php
use Amp\ByteStream\ReadableResourceStream;
use Amp\ByteStream\WritableResourceStream;
use Amp\ByteStream;

$resource = fopen('/path/to/file.txt', 'r');
stream_set_blocking($resource, false);
$readable = new ReadableResourceStream($resource);
$content  = ByteStream\buffer($readable);

$out = new WritableResourceStream(fopen('/tmp/out.txt', 'w'));
$out->write("line\n");
$out->end();
```

### CompressingWritableStream / DecompressingReadableStream
```php
use Amp\ByteStream\Compression\CompressingWritableStream;
use Amp\ByteStream\Compression\DecompressingReadableStream;
use Amp\ByteStream\WritableBuffer;
use Amp\ByteStream\ReadableBuffer;

// Compress on write — classes are in the Compression\ sub-namespace
$sink       = new WritableBuffer();
$compressor = new CompressingWritableStream($sink, \ZLIB_ENCODING_GZIP);
$compressor->write("some data");
$compressor->end();
$compressed = $sink->buffer();

// Decompress on read
$source       = new ReadableBuffer($compressed);
$decompressor = new DecompressingReadableStream($source, \ZLIB_ENCODING_GZIP);
$original     = \Amp\ByteStream\buffer($decompressor); // "some data"
```

### ReadableIterableStream
```php
use Amp\ByteStream\ReadableIterableStream;
use function Amp\ByteStream\buffer;

// Wraps an array/iterable of strings as a ReadableStream.
// Key difference from ReadableBuffer: does NOT close during read() —
// closes only after the iterator is exhausted. Required when the consumer
// calls isClosed() mid-stream (e.g. Base64DecodingReadableStream).
$chunks = ['Hello ', 'World', '!'];
$stream  = new ReadableIterableStream($chunks);
$content = buffer($stream); // 'Hello World!'

// Also works with a Generator
$stream = new ReadableIterableStream((function () {
    yield 'chunk1';
    yield 'chunk2';
})());
```

### Base64EncodingReadableStream / Base64DecodingReadableStream
```php
use Amp\ByteStream\Base64\Base64EncodingReadableStream;
use Amp\ByteStream\Base64\Base64DecodingReadableStream;
use Amp\ByteStream\ReadableBuffer;
use Amp\ByteStream\ReadableIterableStream;

// Encode to Base64
$encoded = \Amp\ByteStream\buffer(
    new Base64EncodingReadableStream(new ReadableBuffer("hello world"))
);

// Decode from Base64
// IMPORTANT: Use ReadableIterableStream (NOT ReadableBuffer) as the decoder source.
// ReadableBuffer closes itself inside read(), making isClosed()=true immediately,
// which causes Base64DecodingReadableStream to throw StreamException on the next read.
// ReadableIterableStream only closes after the iterator is exhausted, avoiding this bug.
$decoded = \Amp\ByteStream\buffer(
    new Base64DecodingReadableStream(new ReadableIterableStream([$encoded]))
);
```

### Payload
```php
use Amp\ByteStream\Payload;
use Amp\ByteStream\ReadableBuffer;

$payload = new Payload(new ReadableBuffer("binary data"));

// Full buffering
$bytes = $payload->buffer();

// Or stream chunk by chunk
while (null !== $chunk = $payload->read()) {
    processChunk($chunk);
}
```

### splitLines() — iterate a stream line by line
```php
use Amp\Socket;
use function Amp\async;
use function Amp\ByteStream\splitLines;

// splitLines(ReadableStream $stream): iterable<string>
// Reads the stream and yields each line without the trailing newline.
// Perfect for line-oriented protocols (TCP, UNIX sockets).
$server = Socket\listen('127.0.0.1:9000');

while ($socket = $server->accept()) {
    async(function () use ($socket): void {
        foreach (splitLines($socket) as $line) {
            $socket->write(strtoupper($line) . "\n"); // echo back uppercased
        }
        $socket->end();
    });
}
```

### pipe() / buffer()
```php
use Amp\ByteStream;
use Amp\ByteStream\ReadableBuffer;
use Amp\ByteStream\WritableBuffer;

$source = new ReadableBuffer("transfer me");
$sink   = new WritableBuffer();
ByteStream\pipe($source, $sink);
// IMPORTANT: pipe() does NOT call end() on the destination — caller must do it.
// WritableBuffer::buffer() blocks until end() is called.
$sink->end();
echo $sink->buffer(); // "transfer me"

// Shorthand: read entire stream into string
$text = ByteStream\buffer(new ReadableBuffer("hello"));
```

---

## amphp/cache

### LocalCache
```php
use Amp\Cache\LocalCache;

$cache = new LocalCache(sizeLimit: 1000, gcInterval: 5.0);

$cache->set('user:1', ['name' => 'Alice'], 60); // TTL 60 s
$value = $cache->get('user:1'); // ['name' => 'Alice'] or null

$cache->delete('user:1');

$count = $cache->count(); // number of items currently stored

// NOTE: LocalCache does NOT have getOrSet(). For atomic compute-if-absent, use AtomicCache.
```

### AtomicCache
```php
use Amp\Cache\AtomicCache;
use Amp\Cache\LocalCache;
use Amp\Sync\LocalKeyedMutex;

// AtomicCache is a separate wrapper class — NOT built into LocalCache.
// It requires a Cache backend and a KeyedMutex for per-key locking.
$base   = new LocalCache();
$atomic = new AtomicCache($base, new LocalKeyedMutex());

// computeIfAbsent: factory invoked only once per key, even under concurrency
$value = $atomic->computeIfAbsent('expensive-key', function (string $key): mixed {
    return doExpensiveWork($key);
});

// compute: always re-computes (mutex-protected read-modify-write)
$atomic->compute('counter', fn(string $key, ?int $v) => ($v ?? 0) + 1);
echo $atomic->get('counter'); // 1
```

### NullCache
```php
use Amp\Cache\NullCache;

// Use as a no-op drop-in during testing
$cache = new NullCache();
$cache->set('key', 'value'); // silently ignored
$result = $cache->get('key'); // always null
```

### PrefixCache
```php
use Amp\Cache\LocalCache;
use Amp\Cache\PrefixCache;

$base      = new LocalCache(500);
$userCache = new PrefixCache($base, 'user:');

$userCache->set('42', $userData);        // stored as 'user:42'
$val = $userCache->get('42');            // reads 'user:42'
$prefix = $userCache->getKeyPrefix();    // 'user:'
```

### SerializedCache
```php
use Amp\Cache\LocalCache;
use Amp\Cache\SerializedCache;
use Amp\Serialization\NativeSerializer;

$base   = new LocalCache(500);
$cache  = new SerializedCache($base, new NativeSerializer());

$cache->set('obj', new \stdClass());
$obj = $cache->get('obj'); // deserialized \stdClass
```

---

## amphp/cluster

### Cluster / ClusterWatcher
```php
use Amp\Cluster\Cluster;
use Amp\Cluster\ClusterWatcher;

// ---- worker.php ----
if (Cluster::isWorker()) {
    $socketFactory = Cluster::getServerSocketFactory();

    $server = \Amp\Http\Server\SocketHttpServer::createForBehindProxy($logger);
    $server->expose($socketFactory->listen('0.0.0.0:8080'));
    $server->start($requestHandler, $errorHandler);

    Cluster::awaitTermination(); // blocks until master sends SIGTERM
    $server->stop();
} else {
    // ---- master process ----
    $watcher = new ClusterWatcher(__FILE__, $logger);
    $watcher->start(workerCount: 4);

    \Amp\trapSignal([\SIGTERM, \SIGINT]);
    $watcher->stop();
}
```

---

## amphp/dns

### resolve() / query()
```php
use Amp\Dns;
use Amp\Dns\DnsRecord;

// Resolve A + AAAA records
$records = Dns\resolve('example.com');
foreach ($records as $record) {
    echo $record->getValue() . " (TTL {$record->getTtl()})\n";
}

// Restrict to IPv4
$ipv4 = Dns\resolve('example.com', DnsRecord::A);

// Arbitrary record type
$mxRecords = Dns\query('example.com', DnsRecord::MX);
foreach ($mxRecords as $mx) {
    echo "MX: " . $mx->getValue() . "\n";
}
```

### Rfc1035StubDnsResolver
```php
use Amp\Dns\Rfc1035StubDnsResolver;
use Amp\Dns\DnsRecord;
use Amp\Cache\LocalCache;

// Custom resolver with explicit cache
// Constructor: __construct(?Cache $cache = null, ?DnsConfigLoader $configLoader = null)
$resolver = new Rfc1035StubDnsResolver(cache: new LocalCache(256));
\Amp\Dns\dnsResolver($resolver); // set as global resolver — function is dnsResolver(), NOT resolver()

$records = $resolver->resolve('example.com', DnsRecord::AAAA);
```

---

## amphp/file

### File (openFile)
```php
use Amp\File;

// Stream a large file without loading it fully into memory
$file = File\openFile('/path/to/large.bin', 'r');
while (null !== $chunk = $file->read(length: 65536)) {
    processChunk($chunk);
}

// Write / append
$out = File\openFile('/tmp/output.log', 'a');
$out->write("[" . date('c') . "] event happened\n");
$out->end();
```

### Filesystem functions
```php
use Amp\File;

// One-shot read / write
$content = File\read('/etc/hostname');
File\write('/tmp/result.txt', strtoupper($content));

// Metadata
if (File\exists('/tmp/result.txt')) {
    $size  = File\getSize('/tmp/result.txt');
}

// Directory operations
File\createDirectoryRecursively('/tmp/a/b/c', 0755);

// IMPORTANT: listFiles() returns FILENAMES ONLY, not full paths.
// You must prepend the directory path yourself!
$names = File\listFiles('/tmp/a');   // ['file1.txt', 'file2.txt'] — NOT '/tmp/a/file1.txt'
foreach ($names as $name) {
    $fullPath = '/tmp/a/' . $name;   // must construct full path manually
    echo File\read($fullPath);
}

// File cleanup
File\deleteFile('/tmp/result.txt');
File\deleteDirectory('/tmp/a');      // remove an empty directory
```

---

## amphp/http-client

### ConnectionLimitingPool — limit concurrent connections per host
```php
use Amp\Http\Client\Connection\ConnectionLimitingPool;
use Amp\Http\Client\HttpClientBuilder;
use Amp\Http\Client\Request;
use Amp\Future;
use function Amp\async;

// Limit to N concurrent connections per authority (scheme+host+port).
// Constructor is private — use the static factory:
$pool = ConnectionLimitingPool::byAuthority(2); // max 2 conn per host

$client = (new HttpClientBuilder())
    ->usingPool($pool)
    ->followRedirects(0)
    ->build();

$futures = array_map(
    fn(string $url) => async(fn() => $client->request(new Request($url))->getBody()->buffer()),
    ['https://example.com/1', 'https://example.com/2', 'https://example.com/3'],
);

$bodies = Future\await($futures);
```

### HttpClientBuilder / HttpClient
```php
use Amp\Http\Client\HttpClientBuilder;
use Amp\Http\Client\Request;
use Amp\Http\Client\Interceptor\{DecompressResponse, FollowRedirects, RetryRequests};

$client = (new HttpClientBuilder())
    ->intercept(new DecompressResponse())
    ->intercept(new FollowRedirects(maxRedirects: 5))
    ->intercept(new RetryRequests(maxRetries: 2))
    ->build();

$response = $client->request(new Request('https://httpbin.org/get'));
$body     = $response->getBody()->buffer();
echo $response->getStatus(); // 200
```

### Request (POST with JSON)
```php
use Amp\Http\Client\Request;
use Amp\Http\Client\HttpClientBuilder;

$client  = HttpClientBuilder::buildDefault();
$request = new Request('https://api.example.com/users', 'POST');
$request->setHeader('Content-Type', 'application/json');
$request->setBody(json_encode(['name' => 'Alice']));

$response = $client->request($request);
$data     = json_decode($response->getBody()->buffer(), true);
```

### Parallel requests with TimeoutCancellation
```php
use Amp\Future;
use Amp\TimeoutCancellation;
use Amp\Http\Client\{HttpClientBuilder, Request};
use function Amp\async;

$client  = HttpClientBuilder::buildDefault();
$urls    = ['https://a.com', 'https://b.com', 'https://c.com'];

$futures = array_map(
    fn(string $url) => async(
        fn() => $client->request(new Request($url), new TimeoutCancellation(10.0))
    ),
    $urls
);

$responses = Future\await($futures);
```

---

## amphp/http-server

### SocketHttpServer / RequestHandler
```php
use Amp\Http\Server\{SocketHttpServer, Request, Response, RequestHandler, DefaultErrorHandler};
use Amp\Http\HttpStatus;
use Monolog\Logger;
use Monolog\Handler\StreamHandler;

$logger = new Logger('server');
$logger->pushHandler(new StreamHandler('php://stdout'));

$server = SocketHttpServer::createForDirectAccess($logger);
$server->expose('0.0.0.0:8080');

// Expose with BindContext to disable Nagle's algorithm (helps for small responses / benchmarks):
use Amp\Socket\BindContext;
$server->expose('0.0.0.0:8080', (new BindContext())->withTcpNoDelay());

$server->start(
    requestHandler: new class implements RequestHandler {
        public function handleRequest(Request $request): Response {
            return new Response(
                HttpStatus::OK,
                ['Content-Type' => 'text/plain'],
                'Hello, World!'
            );
        }
    },
    errorHandler: new DefaultErrorHandler(),
);

\Amp\trapSignal([\SIGTERM, \SIGINT]);
$server->stop();
```

### SocketHttpServer direct constructor (full control)
```php
use Amp\Http\Server\SocketHttpServer;
use Amp\Http\Server\DefaultErrorHandler;
use Amp\Http\Server\Driver\SocketClientFactory;
use Amp\Socket\ResourceServerSocketFactory;
use Amp\Socket\BindContext;
use Monolog\Logger;

// Use the direct constructor when you need custom socket factory, client factory,
// or fine-grained middleware (bypasses the connection-per-IP and concurrency limits
// built into createForDirectAccess()).
$server = new SocketHttpServer(
    logger:              $logger,
    serverSocketFactory: new ResourceServerSocketFactory(),
    clientFactory:       new SocketClientFactory($logger),
);

// Expose with TLS:
use Amp\Socket\{Certificate, ServerTlsContext};
$tlsContext = (new ServerTlsContext())
    ->withDefaultCertificate(new Certificate('/etc/ssl/cert.pem', '/etc/ssl/key.pem'));

$server->expose('0.0.0.0:443', (new BindContext())->withTlsContext($tlsContext));
$server->start($requestHandler, new DefaultErrorHandler());
```

### Middleware
```php
use Amp\Http\Server\{Request, Response, RequestHandler, Middleware};

$loggingMiddleware = new class implements Middleware {
    public function handleRequest(Request $request, RequestHandler $next): Response {
        $start    = microtime(true);
        $response = $next->handleRequest($request);
        $elapsed  = microtime(true) - $start;
        error_log(sprintf('%s %s %.3fms', $request->getMethod(), $request->getUri(), $elapsed * 1000));
        return $response;
    }
};

$handler = Middleware\stackMiddleware($appHandler, $loggingMiddleware);
$server->start($handler, $errorHandler);
```

---

## amphp/http-server-form-parser

### Form
```php
use Amp\Http\Server\FormParser\Form;
use Amp\Http\Server\{Request, Response, RequestHandler};
use Amp\Http\HttpStatus;

class UploadHandler implements RequestHandler
{
    public function handleRequest(Request $request): Response
    {
        $form     = Form::fromRequest($request);
        $username = $form->getValue('username');
        $file     = $form->getFile('avatar');

        if ($file !== null) {
            \Amp\File\write('/uploads/' . $file->getFilename(), $file->getContents());
        }

        return new Response(HttpStatus::OK, [], "Hello, $username");
    }
}
```

### StreamingFormParser
```php
use Amp\Http\Server\FormParser\{StreamingFormParser, FileField};
use Amp\Http\Server\{Request, Response, RequestHandler};
use Amp\Http\HttpStatus;
use Amp\ByteStream;
use Amp\File;

class StreamingUploadHandler implements RequestHandler
{
    public function handleRequest(Request $request): Response
    {
        $parser = new StreamingFormParser();
        $parser->parseForm($request, function (mixed $field) {
            if ($field instanceof FileField) {
                $dest = File\openFile('/uploads/' . $field->getFilename(), 'w');
                ByteStream\pipe($field->getStream(), $dest);
            }
        });

        return new Response(HttpStatus::OK, [], 'Uploaded');
    }
}
```

---

## amphp/http-server-router

### Router
```php
use Amp\Http\Server\Router;
use Amp\Http\Server\{Request, Response, RequestHandler};
use Amp\Http\HttpStatus;

$router = new Router($server, $logger, $errorHandler);

// Static routes
$router->addRoute('GET', '/', new HomeHandler());

// Route parameters (FastRoute syntax)
$router->addRoute('GET', '/users/{id:\d+}', new class implements RequestHandler {
    public function handleRequest(Request $request): Response {
        $args = $request->getAttribute(Router::class);
        $id   = $args['id'];
        return new Response(HttpStatus::OK, ['Content-Type' => 'application/json'],
            json_encode(['id' => (int) $id])
        );
    }
});

// POST with inline handler — class is ClosureRequestHandler (NOT CallableRequestHandler)
use Amp\Http\Server\RequestHandler\ClosureRequestHandler;
$router->addRoute('POST', '/api/users', new ClosureRequestHandler(
    function (Request $request): Response {
        $data = json_decode($request->getBody()->buffer(), true);
        return new Response(HttpStatus::CREATED, ['Content-Type' => 'application/json'],
            json_encode(['id' => 1, 'name' => $data['name']])
        );
    }
));

// 404 fallback
$router->setFallback(new class implements RequestHandler {
    public function handleRequest(Request $request): Response {
        return new Response(HttpStatus::NOT_FOUND, [], 'Not Found');
    }
});

$server->start($router, $errorHandler);
```

---

## amphp/http-server-session

### SessionMiddleware / Session
```php
use Amp\Http\Server\Session\{Session, SessionMiddleware, LocalSessionStorage, CookieAttributes};
use Amp\Http\Server\{Request, Response, RequestHandler, Middleware};
use Amp\Http\HttpStatus;

$sessionMiddleware = new SessionMiddleware(
    storage: new LocalSessionStorage(),
    cookieAttributes: CookieAttributes::default()
        ->withSecure()
        ->withHttpOnly()
        ->withSameSite(CookieAttributes::SAME_SITE_LAX)
        ->withMaxAge(3600),
);

$handler = Middleware\stackMiddleware(
    new class implements RequestHandler {
        public function handleRequest(Request $request): Response {
            /** @var Session $session */
            $session = $request->getAttribute(Session::class);

            $userId = $session->get('user_id');

            // Write requires an exclusive lock
            $session->lock();
            try {
                $session->set('user_id', 42);
                $session->commit();
            } finally {
                $session->unlock();
            }

            return new Response(HttpStatus::OK, [], "user=$userId");
        }
    },
    $sessionMiddleware,
);
```

---

## amphp/http-server-static-content

### DocumentRoot
```php
use Amp\Http\Server\StaticContent\DocumentRoot;

// Serve all files under /var/www/public
$documentRoot = new DocumentRoot($server, $errorHandler, '/var/www/public');

// Use as router fallback (SPA-friendly)
$router->setFallback($documentRoot);

// SPA index fallback
use Amp\Http\Server\StaticContent\StaticResource;
$documentRoot->setFallback(
    new StaticResource($server, $errorHandler, '/var/www/public/index.html')
);
```

### StaticResource
```php
use Amp\Http\Server\StaticContent\StaticResource;

// Single file — supports ETag, Range, If-None-Match automatically
$favicon = new StaticResource($server, $errorHandler, '/var/www/favicon.ico');
$router->addRoute('GET', '/favicon.ico', $favicon);
```

---

## amphp/http-tunnel

### Http1TunnelConnector
```php
use Amp\Http\Tunnel\Http1TunnelConnector;
use Amp\Http\Client\{HttpClientBuilder, Request};
use Amp\Http\Client\Connection\{DefaultConnectionFactory, UnlimitedConnectionPool};

$tunnelConnector = new Http1TunnelConnector(
    proxyAddress: '127.0.0.1:3128',
    proxyHeaders: [
        'Proxy-Authorization' => 'Basic ' . base64_encode('user:secret'),
    ],
);

$client = (new HttpClientBuilder())
    ->usingPool(new UnlimitedConnectionPool(
        new DefaultConnectionFactory($tunnelConnector)
    ))
    ->build();

$response = $client->request(new Request('https://example.com/api'));
$body     = $response->getBody()->buffer();
```

---

## amphp/mysql

### MysqlConnectionPool
```php
use Amp\Mysql\{MysqlConfig, MysqlConnectionPool};

$config = MysqlConfig::fromString(
    'host=127.0.0.1 port=3306 user=app password=secret db=myapp charset=utf8mb4'
);
$pool = new MysqlConnectionPool($config, maxConnections: 10);

// Simple query
$result = $pool->query('SELECT id, name FROM users WHERE active = 1');
foreach ($result as $row) {
    echo $row['name'] . "\n";
}
```

### MysqlStatement
```php
use Amp\Mysql\MysqlConnectionPool;

/** @var MysqlConnectionPool $pool */
$stmt   = $pool->prepare('SELECT * FROM users WHERE id = ? AND role = ?');
$result = $stmt->execute([42, 'admin']);
$row    = $result->fetchRow(); // associative array or null
```

### MysqlTransaction
```php
use Amp\Mysql\MysqlConnectionPool;

/** @var MysqlConnectionPool $pool */
$tx = $pool->beginTransaction();
try {
    $tx->execute('INSERT INTO orders (user_id, total) VALUES (?, ?)', [1, 99.99]);
    $orderId = $tx->getLastInsertId();
    $tx->execute('UPDATE inventory SET qty = qty - 1 WHERE product_id = ?', [5]);
    $tx->commit();
} catch (\Throwable $e) {
    $tx->rollback();
    throw $e;
}
```

---

## amphp/parallel

### Task / workerPool()
```php
use Amp\Parallel\Worker;
use Amp\Cancellation;
use Amp\Future;

class ResizeImageTask implements Worker\Task
{
    public function __construct(
        private string $src,
        private string $dst,
        private int    $width,
    ) {}

    public function run(\Amp\Sync\Channel $channel, Cancellation $cancellation): string
    {
        // Runs in a separate process/thread — blocking code is fine here
        $img = imagecreatefromjpeg($this->src);
        // ... resize logic ...
        imagejpeg($img, $this->dst, 85);
        return $this->dst;
    }
}

$pool = Worker\workerPool(); // global shared pool

$futures = array_map(
    fn(string $file) => $pool->submit(new ResizeImageTask($file, $file . '.resized.jpg', 800))->getFuture(),
    glob('/uploads/*.jpg'),
);

$outputs = Future\await($futures);
```

### Execution::getChannel() — Progress from Worker
```php
use Amp\Sync\ChannelException;
use function Amp\async;
use function Amp\Parallel\Worker\submit;

$execution = submit(new MyProgressTask());
$channel   = $execution->getChannel();

$progress = [];

// IMPORTANT: JobChannel::receive() throws ChannelException when the task closes its
// end of the channel (i.e. when the task finishes). It NEVER returns null.
// Must use async() fiber + try/catch(ChannelException):
$receiver = async(function () use ($channel, &$progress): void {
    try {
        while (true) {
            $progress[] = $channel->receive();
        }
    } catch (ChannelException) {
        // Task finished and channel was closed from the worker side — expected.
    }
});

$execution->getFuture()->await(); // wait for task to return
$receiver->await();              // wait for receiver fiber to finish

// $progress now contains all messages sent by the task via $channel->send(...)
```

### Context (long-lived child process)
```php
use Amp\Parallel\Context\DefaultContextFactory;

// DefaultContextFactory constructor: __construct(IpcHub $ipcHub = new LocalIpcHub())
// start(): __construct(string|array $script, ?Cancellation $cancellation = null): Context
$factory = new DefaultContextFactory();
$context = $factory->start('/path/to/worker-script.php');

$context->send(['type' => 'job', 'payload' => $data]);
$result = $context->receive();
$context->join();
```

---

## amphp/process

### Process — run shell commands asynchronously
```php
use Amp\Process\Process;
use Amp\ByteStream;

// Process::start() is a STATIC FACTORY — there is no __construct().
// Signature: start(string|array $command, ?string $workingDirectory = null,
//                  array $environment = [], array $options = [],
//                  ?Cancellation $cancellation = null): self
$process = Process::start('ls -la /tmp');

// Read stdout / stderr as async streams
$stdout = ByteStream\buffer($process->getStdout()); // entire stdout as string
$stderr = ByteStream\buffer($process->getStderr());

$exitCode = $process->join(); // wait for process to finish, returns exit code (int)

// Run a command with arguments as array (auto-escaped)
$process = Process::start(['git', 'log', '--oneline', '-5'], workingDirectory: '/var/www');
$output  = ByteStream\buffer($process->getStdout());
$process->join();

// Send input to stdin
$process = Process::start('cat');
$process->getStdin()->write("hello\n");
$process->getStdin()->end();             // close stdin so the process can finish
$result = ByteStream\buffer($process->getStdout());
$process->join();

// Stream output line by line using splitLines()
use function Amp\ByteStream\splitLines;
$process = Process::start('tail -f /var/log/syslog');
foreach (splitLines($process->getStdout()) as $line) {
    if (str_contains($line, 'error')) {
        $process->kill(); // terminate the process
        break;
    }
}
```

---

## amphp/phpunit-util

### AsyncTestCase
```php
use Amp\PHPUnit\AsyncTestCase;
use Amp\Http\Client\{HttpClientBuilder, Request};
use function Amp\async;
use function Amp\delay;
use Amp\Future;

class MyServiceTest extends AsyncTestCase
{
    public function testDelayedValue(): void
    {
        $deferred = new \Amp\DeferredFuture();
        async(function () use ($deferred) {
            delay(0.05);
            $deferred->complete(42);
        });
        $this->assertSame(42, $deferred->getFuture()->await());
    }

    public function testHttpRequest(): void
    {
        $client   = HttpClientBuilder::buildDefault();
        $response = $client->request(new Request('https://httpbin.org/get'));
        $this->assertSame(200, $response->getStatus());
    }

    public function testParallel(): void
    {
        $futures = [
            async(fn() => delay(0.02) ?? 'a'),
            async(fn() => delay(0.01) ?? 'b'),
        ];
        $this->assertCount(2, Future\await($futures));
    }
}
```

### Testing RequestHandlers — constructing Request manually
```php
use Amp\Http\Server\Driver\Client;
use Amp\Http\Server\Request;
use Amp\Http\Server\Response;
use Amp\PHPUnit\AsyncTestCase;
use League\Uri\Http;

// Request constructor: __construct(Client $client, string $method, PsrUri $uri, array $headers = [], ...)
// Use a mock Client when unit-testing RequestHandlers directly (no live server needed).
class ApiHandlerTest extends AsyncTestCase
{
    private Client $client;

    protected function setUp(): void
    {
        parent::setUp();
        $this->client = $this->createMock(Client::class);
    }

    private function makeRequest(string $method, string $path): Request
    {
        return new Request(
            $this->client,
            $method,
            Http::new('http://localhost:8080' . $path),
        );
    }

    public function testHandlerReturns200(): void
    {
        $handler  = new MyRequestHandler();
        $response = $handler->handleRequest($this->makeRequest('GET', '/api/status'));
        $this->assertSame(200, $response->getStatus());
    }
}
```

---

## amphp/pipeline

### Queue
```php
use Amp\Pipeline\Queue;
use function Amp\async;
use function Amp\delay;

$queue = new Queue(bufferSize: 10);

// Producer fiber — push() suspends current fiber until the consumer reads the value (back-pressure)
async(function () use ($queue) {
    for ($i = 1; $i <= 5; $i++) {
        $queue->push($i);   // blocking: suspends until consumer is ready
        delay(0.1);
    }
    $queue->complete();
});

// Consumer
foreach ($queue->iterate() as $value) {
    echo $value . "\n"; // 1 2 3 4 5
}

// pushAsync(): non-blocking alternative — returns a Future immediately.
// Useful when you don't want the producer to suspend (fire-and-forget style).
// The Future resolves when the consumer reads the value.
async(function () use ($queue): void {
    $futures = [];
    foreach ($items as $item) {
        $futures[] = $queue->pushAsync($item); // returns Future — does NOT suspend
    }
    $queue->complete();
    Future\await($futures); // wait for all items to be consumed if needed
});
```

### Pipeline (operators)
```php
use Amp\Pipeline\Pipeline;

// filter / map / take
$results = Pipeline::fromIterable(range(1, 20))
    ->filter(fn(int $n) => $n % 2 === 0) // even only
    ->map(fn(int $n) => $n ** 2)          // square
    ->take(4)                             // first 4
    ->toArray();                          // [4, 16, 36, 64]

// skip / takeWhile / sorted / skipWhile — verified in PipelineDemo.php
$result = Pipeline::fromIterable([1, 2, 3, 4, 5, 6, 7])
    ->skip(1)                             // skip first N
    ->takeWhile(fn(int $n) => $n < 6)     // take while predicate true: [2,3,4,5]
    ->sorted(fn(int $a, int $b) => $b <=> $a) // sort descending (buffers all)
    ->skipWhile(fn(int $n) => $n > 4)    // skip while true: [4, 3, 2]
    ->toArray();

// tap — side-effect without modifying values (e.g. logging)
$tapped = [];
$result = Pipeline::fromIterable([1, 2, 3])
    ->tap(function (int $v) use (&$tapped): void { $tapped[] = $v; })
    ->map(fn(int $v) => $v * 10)
    ->toArray(); // $tapped = [1,2,3], $result = [10,20,30]

// reduce — fold all items into one value
$sum = Pipeline::fromIterable([1, 2, 3, 4, 5])
    ->reduce(fn(int $carry, int $item) => $carry + $item, 0); // 15

// allMatch / anyMatch / noneMatch — boolean predicates
$all  = Pipeline::fromIterable([2, 4, 6])->allMatch(fn($n) => $n % 2 === 0); // true
$any  = Pipeline::fromIterable([1, 2, 3])->anyMatch(fn($n) => $n % 2 === 0); // true
$none = Pipeline::fromIterable([1, 3, 5])->noneMatch(fn($n) => $n % 2 === 0); // true

// count — total number of items
$n = Pipeline::fromIterable([1, 2, 3])->count(); // 3
```

### ConcurrentIterator (concurrent mapping)
```php
use Amp\Pipeline\Pipeline;
use Amp\Http\Client\{HttpClientBuilder, Request};

$client = HttpClientBuilder::buildDefault();

$pipeline = Pipeline::fromIterable($urls)
    ->concurrent(5)
    ->map(fn(string $url) => $client->request(new Request($url))->getBody()->buffer());

foreach ($pipeline as $body) {
    processBody($body);
}
```

---

## amphp/redis

### RedisClient
```php
use Amp\Redis\RedisConfig;
use function Amp\Redis\createRedisClient;
use Amp\Redis\Command\Option\SetOptions;

// IMPORTANT: RedisClient constructor takes RedisLink, NOT RedisConfig.
// Always create via the createRedisClient() factory function.
$client = createRedisClient('redis://127.0.0.1:6379/0');
// or:
$client = createRedisClient(RedisConfig::fromUri('redis://127.0.0.1:6379/0'));

// Basic key/value
$client->set('greeting', 'hello');
$value = $client->get('greeting'); // 'hello'

// With TTL — SetOptions has NO static expireIn(). Use withTtl() on an instance.
$client->set('session:abc', json_encode($payload), (new SetOptions())->withTtl(3600));

// Atomic counter — method is increment(), NOT incr()
$visits = $client->increment('page:views');
```

### Hash operations (RedisMap)
```php
use function Amp\Redis\createRedisClient;

// Redis HASH commands are accessed via getMap($key) — there are no direct hGet/hMSet methods
$client = createRedisClient('redis://127.0.0.1:6379');
$map = $client->getMap('user:1');

$map->setValues(['name' => 'Alice', 'email' => 'alice@example.com']); // HSET (multi)
$user  = $map->getAll();            // HGETALL → ['name' => 'Alice', 'email' => ...]
$email = $map->getValue('email');   // HGET → 'alice@example.com'
```

### Subscriber (pub/sub)
```php
use Amp\Redis\RedisSubscriber;
use function Amp\async;
use function Amp\Redis\createRedisClient;
use function Amp\Redis\createRedisConnector;

// RedisSubscriber is a separate class — RedisClient has NO createSubscriber() method.
$client     = createRedisClient('redis://127.0.0.1:6379');
$subscriber = new RedisSubscriber(createRedisConnector('redis://127.0.0.1:6379'));
$subscription = $subscriber->subscribe('notifications');

// RedisSubscription implements IteratorAggregate — iterate directly (no ->listen() method).
// Each message is a plain string (the message payload).
async(function () use ($subscription): void {
    foreach ($subscription as $message) {
        echo "Received: {$message}\n";
    }
});

// Publish from another fiber
$client->publish('notifications', json_encode(['event' => 'order_created']));
```

---

## amphp/socket

### connect() / Socket
```php
use Amp\ByteStream;
use Amp\Socket;

// Plain TCP
$socket = Socket\connect('tcp://example.com:80');
$socket->write("GET / HTTP/1.0\r\nHost: example.com\r\n\r\n");
$response = ByteStream\buffer($socket); // buffer() is in Amp\ByteStream, NOT Amp\Socket
$socket->end();
```

### connectTls() (TLS client)
```php
use Amp\Socket;
use Amp\Socket\{ConnectContext, ClientTlsContext};

$context = (new ConnectContext())
    ->withConnectTimeout(5.0)
    ->withTlsContext(
        (new ClientTlsContext('api.example.com'))
            ->withApplicationLayerProtocols(['http/1.1'])
    );

$socket = Socket\connect('tcp://api.example.com:443', $context);
$socket->setupTls();
$socket->write("GET /status HTTP/1.1\r\nHost: api.example.com\r\nConnection: close\r\n\r\n");
```

### SocketServer (TCP server)
```php
use Amp\Socket;
use function Amp\async;

$server = Socket\listen('tcp://0.0.0.0:9000');

while ($client = $server->accept()) {
    async(function () use ($client) {
        while (null !== $line = $client->read()) {
            $client->write(strtoupper($line)); // echo back uppercased
        }
        $client->end();
    });
}
```

### ServerTlsContext (TLS server)
```php
use Amp\Socket;
use Amp\Socket\{ServerTlsContext, Certificate, BindContext};

$tlsContext = (new ServerTlsContext())
    ->withDefaultCertificate(new Certificate('/etc/ssl/cert.pem', '/etc/ssl/key.pem'));

$server = Socket\listen(
    'tcp://0.0.0.0:443',
    (new BindContext())->withTlsContext($tlsContext),
);
```

---

## amphp/sync

### LocalMutex
```php
use Amp\Sync\LocalMutex;
use function Amp\Sync\synchronized;

$mutex = new LocalMutex();

// Recommended: synchronized() is a NAMESPACE FUNCTION — NOT a method on LocalMutex.
// import: use function Amp\Sync\synchronized;
$result = synchronized($mutex, function () use ($sharedMap) {
    $sharedMap['counter']++;
    return $sharedMap['counter'];
});

// Manual (always use try/finally)
$lock = $mutex->acquire();
try {
    $sharedResource->modify();
} finally {
    $lock->release();
}
```

### LocalSemaphore
```php
use Amp\Sync\LocalSemaphore;
use Amp\Future;
use function Amp\async;

$semaphore = new LocalSemaphore(5); // max 5 concurrent operations

$futures = array_map(function (string $url) use ($semaphore, $client) {
    return async(function () use ($semaphore, $url, $client) {
        $lock = $semaphore->acquire();
        try {
            return $client->request(new \Amp\Http\Client\Request($url))->getBody()->buffer();
        } finally {
            $lock->release();
        }
    });
}, $urls);

$bodies = Future\await($futures);
```

### LocalParcel
```php
use Amp\Sync\LocalParcel;
use Amp\Sync\LocalMutex;

// Constructor: new LocalParcel(Mutex $mutex, mixed $initialValue)
$parcel = new LocalParcel(new LocalMutex(), 0);

// Atomic read-modify-write — callback receives current value, return new value
$newValue = $parcel->synchronized(fn(int $current) => $current + 1);
echo $parcel->unwrap(); // 1
```

### Barrier
```php
use Amp\Sync\Barrier;
use function Amp\async;
use function Amp\Future\await;
use function Amp\delay;

// Synchronize N fibers at a rendezvous point
$barrier = new Barrier(3);
$log = [];

$futures = array_map(fn(int $i) => async(function () use ($barrier, &$log, $i): void {
    delay($i * 0.01);   // stagger arrivals
    $log[] = "arrived-$i";
    $barrier->arrive(); // non-blocking — just decrements counter
}), [1, 2, 3]);

$barrier->await(); // suspends until all 3 fibers have called arrive()
$log[] = 'all-arrived';
await($futures);
```

### RateLimitingSemaphore
```php
use Amp\Sync\LocalSemaphore;
use Amp\Sync\RateLimitingSemaphore;
use function Amp\async;
use function Amp\Future\await;

// RateLimitingSemaphore wraps another Semaphore and adds a lockPeriod:
// after a lock is released by the consumer, it does not become available again
// until $lockPeriod seconds have elapsed. Use to throttle operations over time.
//
// Constructor: new RateLimitingSemaphore(Semaphore $semaphore, float $lockPeriod)
// $lockPeriod must be > 0.
$inner = new LocalSemaphore(3);              // max 3 concurrent slots
$rateLimited = new RateLimitingSemaphore($inner, 1.0); // each slot reusable once per second

$futures = [];
for ($i = 1; $i <= 5; $i++) {
    $futures[] = async(function () use ($rateLimited, $i): int {
        $lock = $rateLimited->acquire();
        try {
            // at most 3 in parallel, and each slot held for ≥ 1 s after release
            return $i * 10;
        } finally {
            $lock->release();
        }
    });
}

$results = await($futures); // [10, 20, 30, 40, 50]
```

### LocalKeyedMutex
```php
use Amp\Sync\LocalKeyedMutex;
use function Amp\async;
use function Amp\Future\await;

// Per-key locking — different keys run concurrently, same key is serialized
$mutex = new LocalKeyedMutex();

$futures = [
    async(function () use ($mutex): void {
        $lock = $mutex->acquire('user:1');
        try { /* exclusive access for user:1 */ } finally { $lock->release(); }
    }),
    async(function () use ($mutex): void {
        $lock = $mutex->acquire('user:1'); // waits for the lock above
        try { /* runs after user:1 lock is released */ } finally { $lock->release(); }
    }),
    async(function () use ($mutex): void {
        $lock = $mutex->acquire('user:2'); // different key — runs immediately
        try { /* concurrent with user:1 */ } finally { $lock->release(); }
    }),
];

await($futures);
```

---

## amphp/websocket-client

### Rfc6455Connector / WebsocketConnection
```php
use Amp\Websocket\Client\{Rfc6455Connector, WebsocketHandshake};
use Amp\TimeoutCancellation;

$connector = new Rfc6455Connector();
$handshake = (new WebsocketHandshake('wss://echo.websocket.org'))
    ->withHeader('Authorization', 'Bearer ' . $token);

$connection = $connector->connect($handshake, new TimeoutCancellation(10.0));

$connection->sendText('Hello, Server!');

while ($message = $connection->receive()) {
    echo $message->buffer() . "\n";
    if ($message->buffer() === 'bye') {
        break;
    }
}

$connection->close();
```

### WebsocketMessage (streaming large messages)
```php
use Amp\Websocket\Client\{Rfc6455Connector, WebsocketHandshake};

$connector  = new Rfc6455Connector();
$connection = $connector->connect(new WebsocketHandshake('wss://stream.example.com'));

while ($message = $connection->receive()) {
    if ($message->isBinary()) {
        // Stream large binary payload without buffering all at once
        while (null !== $chunk = $message->read()) {
            processBinaryChunk($chunk);
        }
    } else {
        handleText($message->buffer());
    }
}
```

---

## amphp/websocket-server

### Websocket / WebsocketClientHandler
```php
use Amp\Http\Server\{SocketHttpServer, DefaultErrorHandler};
use Amp\Websocket\WebsocketClient;                           // amphp/websocket — NOT websocket-server!
use Amp\Websocket\Server\{Websocket, AllowOriginAcceptor, WebsocketClientHandler};
use Amp\Http\Server\{Request, Response};

$server = SocketHttpServer::createForDirectAccess($logger);
$server->expose('0.0.0.0:8080');

$websocket = new Websocket(
    httpServer: $server,
    logger:     $logger,
    acceptor:   new AllowOriginAcceptor(['https://example.com']),
    clientHandler: new class implements WebsocketClientHandler {
        public function handleClient(WebsocketClient $client, Request $request, Response $response): void {
            while ($message = $client->receive()) {
                $client->sendText('Echo: ' . $message->buffer());
            }
        }
    },
);

$router->addRoute('GET', '/ws', $websocket);
$server->start($router, new DefaultErrorHandler());
```

### WebsocketClientGateway (broadcast)
```php
use Amp\Websocket\WebsocketClient;
use Amp\Websocket\Server\{Websocket, AllowOriginAcceptor, WebsocketClientGateway, WebsocketClientHandler};
use Amp\Http\Server\{Request, Response};

$gateway = new WebsocketClientGateway();

$clientHandler = new class($gateway) implements WebsocketClientHandler {
    public function __construct(private WebsocketClientGateway $gateway) {}

    public function handleClient(WebsocketClient $client, Request $request, Response $response): void {
        // addClient() registers an onClose() callback internally — no removeClient() needed.
        // The client is automatically removed from the gateway when the connection closes.
        $this->gateway->addClient($client);

        while ($message = $client->receive()) {
            // Broadcast every incoming message to all connected clients
            $this->gateway->broadcastText($message->buffer());
        }
    }
};

// From anywhere: push a server-side event
$gateway->broadcastText(json_encode(['type' => 'update', 'data' => $payload]));
```
