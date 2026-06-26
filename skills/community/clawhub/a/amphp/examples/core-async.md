# AMPHP v3 — Core Async / Future Patterns

AMPHP uses **PHP 8.1 Fibers** (not generators). One Fiber runs at a time; others suspend cooperatively on I/O. The entry point is the Revolt event loop.

---

## Starting the Event Loop

```php
<?php declare(strict_types=1);

use Revolt\EventLoop;
use function Amp\async;
use function Amp\delay;
use Amp\Future;

// Option 1: wrap in EventLoop::run()
EventLoop::run(function (): void {
    $future1 = async(fn() => fetchSomething());
    $future2 = async(fn() => fetchSomethingElse());
    [$result1, $result2] = Future\await([$future1, $future2]);
});

// Option 2 (server, Linux/macOS): start server, then block on OS signal
$server->start($handler, $errorHandler);
if (\extension_loaded('pcntl')) {
    \Amp\trapSignal([\SIGTERM, \SIGINT]);
    $server->stop();
} else {
    EventLoop::run(); // Windows fallback
}
```

---

## async() and delay()

```php
<?php declare(strict_types=1);

use function Amp\async;
use function Amp\delay;
use Amp\Future;

// Start a Fiber (returns immediately with a Future)
$future = async(function (): string {
    delay(1.0); // suspends THIS fiber for 1s; others keep running
    return 'done';
});

$result = $future->await(); // 'done'

// Parallel fan-out — all three run concurrently
$futures = array_map(
    fn(string $url) => async(fn() => fetchUrl($url)),
    ['https://a.com', 'https://b.com', 'https://c.com'],
);
$results = Future\await($futures); // ['result-a', 'result-b', 'result-c']
```

---

## Future Combinators

```php
<?php declare(strict_types=1);

use Amp\Future;
use function Amp\async;
use function Amp\Future\{await, awaitAll, awaitAny, awaitFirst, awaitAnyN};

$f1 = async(fn() => 'a');
$f2 = async(fn() => 'b');
$f3 = async(fn() => throw new \RuntimeException('oops'));

// await() — ALL must succeed; throws on first error; preserves keys
[$r1, $r2] = await([$f1, $f2]);

// awaitAll() — collects results AND errors; never throws
[$errors, $values] = awaitAll([$f1, $f2, $f3]);
foreach ($errors as $key => $exception) { /* handle */ }

// awaitAny() — first SUCCESSFULLY completed value (skips errors)
$first = awaitAny([$f1, $f2, $f3]);

// awaitFirst() — first completed, success OR error (may throw)
$fastest = awaitFirst([$f1, $f2]);

// awaitAnyN() — first N successful results
$twoResults = awaitAnyN(2, [$f1, $f2, $f3]);
```

---

## DeferredFuture — manually resolved Future

```php
<?php declare(strict_types=1);

use Amp\DeferredFuture;
use function Amp\async;
use function Amp\delay;

$deferred = new DeferredFuture();

// Another fiber completes it later
async(function () use ($deferred): void {
    delay(0.1);
    $deferred->complete('result');
    // Or on failure: $deferred->error(new \RuntimeException('failed'));
});

$value = $deferred->getFuture()->await(); // 'result'
```

---

## Future Static Factories and Chaining

```php
<?php declare(strict_types=1);

use Amp\Future;

// Already-resolved Future (no async work needed)
$future = Future::complete('cached_value');
$future = Future::error(new \RuntimeException('fail'));

// Chaining: map() transforms, catch() recovers, finally() always runs
$result = Future::complete('hello')
    ->map(fn(string $v) => strtoupper($v))   // 'HELLO'
    ->catch(fn(\Throwable $e) => 'default')  // recovery
    ->finally(fn() => cleanup())             // always runs, no args
    ->await();                               // 'HELLO'

// Recovering from error
$result = Future::error(new \RuntimeException('boom'))
    ->catch(fn(\Throwable $e) => 'recovered:' . $e->getMessage())
    ->await(); // 'recovered:boom'
```

---

## Future::ignore() — fire-and-forget fibers

```php
<?php declare(strict_types=1);

use function Amp\async;
use function Amp\delay;

// Background fiber whose result we don't need
$bg = async(function (): void {
    while (true) {
        sendHeartbeat();
        delay(5.0);
    }
});

// Main work...

// When done, suppress any errors from the abandoned fiber:
$bg->ignore(); // prevents unhandled-exception crash on GC
```

---

## Key Rules

- `delay(float $seconds, cancellation: $token)` — `cancellation:` is a **named** parameter (second positional arg is `bool $reference`)
- `await()` / `delay()` only work inside a Fiber — wrap top-level scripts in `EventLoop::run()`
- Fibers are cooperative: a CPU-heavy loop without any `delay()` / I/O will block all other fibers
