# AMPHP v3 — Cancellation Patterns

Always accept `?Cancellation` in functions that do I/O. The caller decides the timeout policy.

---

## TimeoutCancellation

```php
<?php declare(strict_types=1);

use Amp\Cancellation;
use Amp\CancelledException;
use Amp\TimeoutCancellation;
use Amp\Http\Client\HttpClientBuilder;
use Amp\Http\Client\Request;

function fetchData(string $url, ?Cancellation $cancellation = null): string
{
    $client = HttpClientBuilder::buildDefault();
    try {
        $response = $client->request(new Request($url), $cancellation);
        return $response->getBody()->buffer();
    } catch (CancelledException $e) {
        throw $e; // let caller handle it
    }
}

// Caller passes the timeout policy:
$result = fetchData('https://api.example.com', new TimeoutCancellation(5.0));
```

---

## DeferredCancellation — manual cancel

```php
<?php declare(strict_types=1);

use Amp\DeferredCancellation;
use Amp\CancelledException;
use function Amp\async;
use function Amp\delay;

$dc = new DeferredCancellation();

$future = async(function () use ($dc): string {
    try {
        delay(10.0, cancellation: $dc->getCancellation());
        return 'completed';
    } catch (CancelledException) {
        return 'manually-cancelled';
    }
});

delay(0.1);      // let it start
$dc->cancel();   // cancel from another fiber

echo $future->await(); // 'manually-cancelled'
```

---

## CompositeCancellation — first wins

```php
<?php declare(strict_types=1);

use Amp\CompositeCancellation;
use Amp\DeferredCancellation;
use Amp\TimeoutCancellation;
use Amp\CancelledException;
use function Amp\delay;

$userAbort = new DeferredCancellation();

// Cancel if EITHER user aborts OR 30 s elapse — whichever is first:
$cancellation = new CompositeCancellation(
    $userAbort->getCancellation(),
    new TimeoutCancellation(30.0),
);

try {
    delay(100.0, cancellation: $cancellation);
} catch (CancelledException) {
    echo "Cancelled\n";
}
```

---

## Cooperative cancellation check in a loop

```php
<?php declare(strict_types=1);

use Amp\Cancellation;
use Amp\TimeoutCancellation;

function processItems(array $items, ?Cancellation $cancellation = null): array
{
    $results = [];
    foreach ($items as $item) {
        $cancellation?->throwIfRequested(); // check before each item
        $results[] = process($item);
    }
    return $results;
}

$result = processItems($bigList, new TimeoutCancellation(2.0));
```

---

## Subscribing to cancellation for cleanup

```php
<?php declare(strict_types=1);

use Amp\DeferredCancellation;
use Amp\CancelledException;
use function Amp\async;
use function Amp\delay;

$dc = new DeferredCancellation();
$cancellation = $dc->getCancellation();

// Register cleanup callback
$id = $cancellation->subscribe(function (): void {
    releaseResource(); // runs when cancelled
});

$future = async(function () use ($cancellation): void {
    try {
        delay(10.0, cancellation: $cancellation);
    } catch (CancelledException) {
        // cleanup subscription is triggered automatically
    }
});

delay(0.01);
$dc->cancel();
$future->await();

$cancellation->unsubscribe($id); // deregister when no longer needed
```

---

## Key Facts

- `TimeoutCancellation(float $seconds)` — cancel after N seconds
- `DeferredCancellation` — cancel manually via `->cancel()`; get token via `->getCancellation()`
- `CompositeCancellation(...$cancellations)` — cancelled when **any** source fires
- `NullCancellation` — no-op, useful as default `?Cancellation` argument
- Cancellation is **advisory** — operations may complete anyway (e.g. nearly-finished HTTP request)
- Always let `CancelledException` propagate unless you specifically need to suppress it
- `delay()` uses a **named** `cancellation:` parameter: `delay(5.0, cancellation: $token)`
