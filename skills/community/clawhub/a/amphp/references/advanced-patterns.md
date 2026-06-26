# AMPHP Advanced Patterns & Gotchas

This file covers the top 10 most important non-obvious knowledge pieces about AMPHP v3,
plus gotchas that cause real bugs in production. Read when the code involves complex
concurrency, pipelines, parallel work, or cancellation.

---

## Top 10 Critical Knowledge Pieces

### 1. Fibers are Cooperative, Not Preemptive

Only ONE fiber runs at any given time. Others are suspended waiting for I/O.
Fibers yield control **voluntarily** — only when they call an async function
(`delay()`, `->await()`, socket reads, DB queries, etc.). This means:

- A CPU-heavy loop blocks ALL other requests/fibers until it finishes
- "Concurrent" means interleaved, not parallel (use `amphp/parallel` for true parallelism)
- There is no race condition from interruption mid-operation (unless you yield mid-operation)

```php
// This is fine — yields to event loop between iterations
foreach ($urls as $url) {
    $results[] = $client->request(new Request($url))->getBody()->buffer(); // yields here
}

// This is NOT fine — no yield point, locks event loop for entire loop
foreach ($bigArray as $item) {
    expensiveComputation($item); // never yields → blocks all other requests
}
```

### 2. Blocking I/O Kills Concurrency

ANY standard PHP I/O function blocks the **entire process** — not just the current fiber.
This is the #1 cause of AMPHP performance problems:

| Blocked | Use instead |
|---------|-------------|
| `sleep()` | `delay(float $seconds)` |
| `file_get_contents()` | `Amp\File\read()` |
| `file_put_contents()` | `Amp\File\write()` |
| `PDO`, `mysqli_query()` | `amphp/mysql`, `amphp/postgres` |
| `curl_exec()` | `amphp/http-client` |
| `dns_get_record()` | `amphp/dns` |
| CPU-heavy work | `amphp/parallel` + `Worker\Task` |

### 3. Future States and `map/catch/finally` Chaining

A `Future` has exactly three states: **pending** → **completed** or **errored**.

```php
// Completed immediately (no async work needed):
$future = Future::complete('cached_value');
$future = Future::error(new \RuntimeException('fail'));

// Chaining (alternative to await + try/catch):
$result = $future
    ->map(fn($val) => strtoupper($val))        // transform on success
    ->catch(fn($e) => 'default')               // recover from error
    ->finally(fn() => $this->cleanup())        // always runs
    ->await();
```

> `DeferredFuture` is a low-level primitive — prefer `async()` in application code.
> Never pass `DeferredFuture` to other classes; it's internal state of the operation.

### 4. Future Combinators — Know All Five

```php
// await() — all must succeed, throws on first error, preserves keys
$results = Future\await([$future1, $future2, $future3]);

// awaitAll() — collects both results AND errors, never throws
[$errors, $values] = Future\awaitAll([$future1, $future2]);
foreach ($errors as $key => $exception) { /* handle */ }

// awaitAny() — returns first SUCCESSFULLY completed value (skips errors)
$first = Future\awaitAny([$slow, $fast]);

// awaitFirst() — returns first completed, whether success or error
$fastest = Future\awaitFirst([$future1, $future2]); // may throw

// awaitAnyN() — returns first N successful results
$twoResults = Future\awaitAnyN(2, [$f1, $f2, $f3, $f4]);
```

### 5. Queue Back-Pressure and DisposedException

`Queue::push()` **suspends the producer** until the consumer has consumed the value.
This is the back-pressure mechanism — producers can't outrun consumers.

```php
$queue = new Queue();

// Producer: MUST call complete() or consumer hangs forever
async(function () use ($queue): void {
    foreach ($items as $item) {
        $queue->push($item);    // suspends here until consumer reads it
    }
    $queue->complete();          // ← critical! without this, consumer loops forever
    // Or on error: $queue->error(new \RuntimeException('failed'));
});

// If consumer is destroyed before queue is complete, push() throws DisposedException
// Catch it if you want to stop gracefully, ignore it if that's fine
try {
    $queue->push($item);
} catch (DisposedException) {
    break; // consumer is gone, stop producing
}
```

### 6. Pipeline Concurrency and Ordering Control

Pipelines are lazy — nothing runs until iterated. Use `.concurrent()` to process multiple
items simultaneously, `.unordered()` to allow out-of-order results for better throughput:

```php
$pipeline = Pipeline::fromIterable($urls)
    ->concurrent(10)        // process up to 10 items at once (uses LocalSemaphore internally)
    ->unordered()           // results may arrive out of order — more throughput
    ->map(fn($url) => $client->request(new Request($url))->getBody()->buffer())
    ->filter(fn($body) => strlen($body) > 0);

foreach ($pipeline as $body) {
    // process results as they arrive
}

// Alternative: Pipeline::generate() for infinite sequences
// IMPORTANT: must use a full function (not arrow fn) to use static local variables
Pipeline::generate(static function(): int { static $i = 0; return ++$i; })
    ->take(100)
    ->concurrent(5)
    ->delay(0.1)       // Pipeline::delay(float $seconds) — async pause between items
    ->forEach(fn($v) => process($v)); // forEach() iterates the pipeline, calling $fn for each item
```

### 7. Task::run() Signature and Autoloading Requirement

Worker `Task` implementations must use the v3 signature with **both** `Channel` and `Cancellation`:

```php
use Amp\Cancellation;
use Amp\Parallel\Worker\Task;
use Amp\Sync\Channel;

class MyTask implements Task
{
    public function __construct(private readonly array $data) {}

    // run() is called in a SEPARATE PROCESS — no shared memory with parent
    // Channel allows bidirectional communication with parent while running
    public function run(Channel $channel, Cancellation $cancellation): mixed
    {
        // $channel->send() / $channel->receive() for progress/intermediate data
        $channel->send(['progress' => 50]);
        return expensiveComputation($this->data); // blocking code is OK here!
    }
}

// Task + data are serialized — everything must be serializable
// The class must be autoloadable by Composer in the worker process
$execution = Worker\submit(new MyTask($data));
$result = $execution->await();

// Or with progress tracking:
$execution = Worker\submit(new MyTask($data));
$channel = $execution->getChannel();
async(fn() => $channel->send(['command' => 'pause'])); // send to worker
$progress = $channel->receive(); // receive from worker
```

### 8. Cancellation is Advisory — Not Guaranteed

Cancellation is a **request**, not a command. The operation may complete anyway
(e.g., a nearly-finished HTTP request may continue to reuse the connection).

```php
// Implement cancellation in custom async functions:
function processItems(array $items, ?Cancellation $cancellation = null): array
{
    $results = [];
    foreach ($items as $item) {
        $cancellation?->throwIfRequested(); // check before each item
        $results[] = process($item);
    }
    return $results;
}

// Or subscribe to cancellation for cleanup:
$id = $cancellation?->subscribe(function () use ($resource): void {
    $resource->close(); // run when cancelled
});
// Unsubscribe when done:
$cancellation?->unsubscribe($id);

// CompositeCancellation — cancelled when ANY source cancels:
$cancellation = new CompositeCancellation(
    new TimeoutCancellation(30.0),
    $deferredCancellation->getCancellation(),
);
```

### 9. HTTP Server Request Handler Details

Each request runs in its **own Fiber** automatically — no manual `async()` needed.
Multiple requests ARE processed concurrently through cooperative scheduling.

```php
// createForDirectAccess vs createForBehindProxy
$server = SocketHttpServer::createForDirectAccess($logger);
// Limits: 10 conn/IP, 1000 total conn, 1000 concurrent requests (adjustable)

$server = SocketHttpServer::createForBehindProxy(
    $logger,
    ForwardedHeaderType::XForwardedFor,
    ['10.0.0.0/8', '172.16.0.0/12'],   // trusted proxy IPs
);

// ClosureRequestHandler for quick inline handlers (no class needed):
// Class name is ClosureRequestHandler (NOT CallableRequestHandler)
use Amp\Http\Server\RequestHandler\ClosureRequestHandler;
$handler = new ClosureRequestHandler(function (Request $request): Response {
    return new Response(HttpStatus::OK, body: 'Hello');
});

// Middleware: handleRequest signature requires BOTH request AND next handler
class AuthMiddleware implements Middleware {
    public function handleRequest(Request $request, RequestHandler $next): Response {
        if (!$this->isAuthorized($request)) {
            return new Response(HttpStatus::UNAUTHORIZED);
        }
        return $next->handleRequest($request);
    }
}

// Stack multiple middlewares (applied left to right — first listed = outermost):
$handler = Middleware\stackMiddleware($router, new LogMiddleware(), new AuthMiddleware());
```

### 10. weakClosure() and Interval for Repeating Timers

Closures captured via `$this` create circular references that prevent garbage collection.
Use `weakClosure()` when a class holds a callback that references itself:

```php
use function Amp\weakClosure;

class Server {
    private Interval $heartbeat;

    public function __construct() {
        // Without weakClosure: $this is strongly held → Server never GC'd
        $this->heartbeat = new Interval(5.0, weakClosure(function (): void {
            $this->sendHeartbeat(); // safe — weak reference, throws Error if $this is destroyed
        }));
    }
}

// Interval: runs callback every N seconds until disabled or object destroyed
$interval = new Interval(0.5, function (): void {
    $this->checkStatus();
});
$interval->disable();      // pause
$interval->enable();       // resume (waits full timeout before next call)
$interval->unreference();  // let event loop exit even if Interval is alive (background heartbeats)
$interval->reference();    // re-register so event loop waits for it
// Interval is automatically cancelled when garbage collected
```

---

## Additional Important Gotchas

### Future::ignore() — Suppress Errors on Fire-and-Forget Fibers

When you spawn a background fiber with `async()` and don't need its result, any unhandled exception
will crash the process. Call `->ignore()` to explicitly mark the Future as intentionally discarded:

```php
// Without ignore(): if the fiber throws, the exception is rethrown when the Future is GC'd
$sender = async(function () use ($client): void {
    while (!$client->isClosed()) {
        $client->sendText(getData());
        delay(1.0);
    }
});

// Main fiber finishes (client disconnected) — cancel the background sender
$sender->ignore(); // suppress any error from the now-abandoned fiber

// Contrast: if you DO care about errors, use ->await() or Future\await()
```

> Use `ignore()` for background push fibers in WebSocket handlers, heartbeat loops, and similar
> "fire-and-forget" tasks where the fiber lifetime is tied to an external condition (client disconnect,
> server shutdown) rather than a specific return value.

### Strict Types Affects Closures in async()

All library files declare `strict_types=1`. Closures passed to `async()` run in
strict-types context. Scalar type coercion that would work in non-strict mode will fail:

```php
// This may fail if the function expects int but receives '42' (string):
async(fn() => myFunction('42')); // strict_types=1 context!
```

### synchronized() Helper — Cleaner than Manual Acquire/Release

`synchronized()` is a **namespace function** `Amp\Sync\synchronized(Semaphore, Closure)`.
It is NOT a method on `LocalMutex`. Always import with `use function Amp\Sync\synchronized;`.

```php
use function Amp\Sync\synchronized;
use Amp\Sync\LocalMutex;
use Amp\Sync\LocalParcel;

// Instead of try/finally with manual acquire/release:
$result = synchronized($mutex, fn() => expensiveOperation());

// LocalParcel — mutex + value in one unit.
// Constructor: new LocalParcel(Mutex $mutex, mixed $initialValue)
$parcel = new LocalParcel(new LocalMutex(), []);
$parcel->synchronized(function (array $value): array {
    $value[] = 'new item';
    return $value; // return modified value to update parcel's stored value
});
echo $parcel->unwrap(); // ['new item']
```

### Arrow Functions Do NOT Capture by Reference

PHP arrow functions (`fn()`) always capture outer variables **by value**, even if the outer
variable was declared with `&`. If you need an inner closure to capture `&$ref` from the outer
scope, use a full `function()` with explicit `use (&$ref)` — do NOT use arrow functions:

```php
// WRONG — $active inside the async closure captures a COPY of $active,
// not the original variable:
$futures = array_map(fn(int $i) => async(function () use (&$active): void {
    $active++; // modifies the arrow function's copy, NOT outer $active
}), range(1, 5));

// CORRECT — use a foreach loop so the closure captures &$active directly:
$futures = [];
foreach (range(1, 5) as $i) {
    $futures[] = async(function () use (&$active): void {
        $active++; // modifies outer $active correctly
    });
}
```

### EventLoop::delay() vs Amp\delay() — Two Different Things

`Amp\delay(float $seconds)` **suspends the current fiber** until the timeout elapses.
It can only be called inside a fiber (`async()`, `AsyncTestCase`, or `EventLoop::run()`).

`Revolt\EventLoop::delay(float $seconds, callable $callback): string` is a **raw event loop
primitive** — it registers a callback to be invoked after a delay WITHOUT suspending any fiber.
It returns a string ID that can be cancelled. Used in low-level timer code when you need to
schedule a callback from a context that cannot suspend (e.g. inside an Interval callback).

```php
use Revolt\EventLoop;

// Register a one-shot callback after $delay seconds (non-suspending)
$id = EventLoop::delay(2.5, function (): void {
    // runs in a new context — can use delay() and await() here
    echo "Fired after 2.5 s\n";
});

// Cancel before it fires
EventLoop::cancel($id);

// Repeat a callback every N seconds (raw, low-level alternative to Interval):
$id = EventLoop::repeat(1.0, function () use (&$id): void {
    doWork();
    if (shouldStop()) {
        EventLoop::cancel($id); // cancel the repeat timer
    }
});
```

Real-world use (from IntervalDemo.php) — re-enabling an Interval from within its own callback
via a delayed raw callback (you can't call `$interval->enable()` directly from inside the same
callback because the Interval's own tick context is still active):

```php
use Revolt\EventLoop;
use Amp\Interval;

$interval = new Interval(0.5, function () use (&$interval): void {
    $interval->disable();
    // Schedule re-enable after 2× the period via raw EventLoop:
    EventLoop::delay(1.0, function () use (&$interval): void {
        $interval?->enable();
    });
});
```

### EventLoop::run() is Rarely Needed in v3

In v3, `await()` and `delay()` automatically start the event loop if not already running
(via Revolt's `Suspension` API). Explicit `EventLoop::run()` is mainly needed for:
- Top-level scripts that don't call any async functions explicitly
- Tests that need to run the event loop to completion

### Nagle's Algorithm Affects Benchmarks

For benchmark scenarios, disable Nagle's algorithm to reduce latency:

```php
use Amp\Socket\BindContext;
$server->expose('0.0.0.0:8080', (new BindContext())->withTcpNoDelay());
```

### Transitive Dependencies Must Be Declared

If you use a class from `amphp/socket` (e.g., `BindContext`) but only required
`amphp/http-server` (which depends on socket internally), declare socket explicitly:

```bash
composer require amphp/socket  # even if http-server already pulls it in
```

### Request Body Must Always Be Consumed

HTTP client responses: always call `buffer()` or fully iterate the body.
Leaving it unread prevents connection reuse and may block:

```php
$response = $client->request($request);
// WRONG: ignoring body
// RIGHT:
$body = $response->getBody()->buffer();
// Or if streaming:
while (null !== $chunk = $response->getBody()->read()) {
    process($chunk);
}
```
