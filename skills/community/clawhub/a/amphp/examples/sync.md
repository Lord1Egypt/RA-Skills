# AMPHP v3 — Sync Primitives (Mutex, Semaphore, Barrier, Parcel)

Fibers share memory. Protect shared mutable state with sync primitives.

---

## LocalMutex — exclusive lock

```php
<?php declare(strict_types=1);

use Amp\Sync\LocalMutex;
use function Amp\async;
use function Amp\delay;
use function Amp\Future\await;

$mutex   = new LocalMutex();
$counter = 0;

$futures = [];
for ($i = 0; $i < 10; $i++) {
    $futures[] = async(function () use ($mutex, &$counter): void {
        $lock = $mutex->acquire();
        try {
            $current = $counter;
            delay(0); // yield — other fibers try to run, but they'll block on acquire()
            $counter = $current + 1;
        } finally {
            $lock->release(); // ALWAYS in finally
        }
    });
}

await($futures);
echo $counter; // 10 — consistent thanks to mutex
```

---

## synchronized() — cleaner alternative to try/finally

```php
<?php declare(strict_types=1);

use Amp\Sync\LocalMutex;
use function Amp\Sync\synchronized; // NAMESPACE FUNCTION — not a method!
use function Amp\async;
use function Amp\Future\await;

$mutex = new LocalMutex();
$log   = [];

$futures = array_map(fn(int $i) => async(
    fn() => synchronized($mutex, function () use (&$log, $i): void {
        $log[] = "enter-$i";
        $log[] = "exit-$i";
    })
), range(1, 3));

await($futures);
// $log entries are never interleaved
```

---

## LocalSemaphore — limit concurrency

```php
<?php declare(strict_types=1);

use Amp\Sync\LocalSemaphore;
use Amp\Future;
use function Amp\async;
use function Amp\Future\await;

$semaphore = new LocalSemaphore(3); // at most 3 concurrent tasks

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

$bodies = await($futures);
```

---

## LocalParcel — atomic read-modify-write

```php
<?php declare(strict_types=1);

use Amp\Sync\LocalParcel;
use Amp\Sync\LocalMutex;
use function Amp\async;
use function Amp\Future\await;

// Constructor: new LocalParcel(Mutex $mutex, mixed $initialValue)
$parcel = new LocalParcel(new LocalMutex(), 0);

$futures = array_map(
    fn() => async(fn() => $parcel->synchronized(fn(int $v) => $v + 1)),
    range(1, 10),
);

await($futures);
echo $parcel->unwrap(); // 10 — atomic, always consistent
```

> **Important**: the closure passed to `synchronized()` receives the **current value** and
> **must return the new value** to store it. Modifying in-place won't work.

---

## Barrier — rendezvous point for N fibers

```php
<?php declare(strict_types=1);

use Amp\Sync\Barrier;
use function Amp\async;
use function Amp\delay;
use function Amp\Future\await;

$barrier = new Barrier(3);
$log     = [];

$futures = array_map(fn(int $i) => async(function () use ($barrier, &$log, $i): void {
    delay($i * 0.01); // stagger
    $log[] = "arrived-$i";
    $barrier->arrive(); // non-blocking — decrements counter
}), [1, 2, 3]);

$barrier->await(); // suspends until all 3 have called arrive()
$log[] = 'all-arrived';

await($futures);
```

---

## LocalKeyedMutex — per-key locking

```php
<?php declare(strict_types=1);

use Amp\Sync\LocalKeyedMutex;
use function Amp\async;
use function Amp\delay;
use function Amp\Future\await;

$mutex = new LocalKeyedMutex();

$futures = [
    async(function () use ($mutex): void {
        $lock = $mutex->acquire('user:1');
        try { delay(0.02); } finally { $lock->release(); }
    }),
    async(function () use ($mutex): void {
        $lock = $mutex->acquire('user:1'); // same key — waits for the lock above
        try { /* runs after user:1 lock released */ } finally { $lock->release(); }
    }),
    async(function () use ($mutex): void {
        $lock = $mutex->acquire('user:2'); // different key — runs immediately
        try { /* concurrent with user:1 */ } finally { $lock->release(); }
    }),
];

await($futures);
```

---

## RateLimitingSemaphore — throttle over time

```php
<?php declare(strict_types=1);

use Amp\Sync\LocalSemaphore;
use Amp\Sync\RateLimitingSemaphore;
use function Amp\async;
use function Amp\Future\await;

// After a lock is released, that slot won't be available again for $lockPeriod seconds.
// Constructor: new RateLimitingSemaphore(Semaphore $semaphore, float $lockPeriod)
// $lockPeriod MUST be > 0.
$inner       = new LocalSemaphore(5);        // 5 concurrent slots
$rateLimited = new RateLimitingSemaphore($inner, 1.0); // each slot reusable once per second

$futures = [];
for ($i = 1; $i <= 10; $i++) {
    $futures[] = async(function () use ($rateLimited, $i): int {
        $lock = $rateLimited->acquire();
        try {
            return $i * 10;
        } finally {
            $lock->release();
        }
    });
}

$results = await($futures);
```
