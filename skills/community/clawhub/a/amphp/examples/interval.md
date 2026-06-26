# AMPHP v3 — Interval & EventLoop Timers

---

## Interval — repeating timer (fiber-friendly)

```php
<?php declare(strict_types=1);

use Amp\DeferredFuture;
use Amp\Interval;

$ticks   = 0;
$deferred = new DeferredFuture();

$interval = new Interval(1.0, function () use (&$ticks, &$interval, $deferred): void {
    $ticks++;
    if ($ticks >= 3) {
        $interval = null; // nulling the reference calls __destruct, which cancels the timer
        $deferred->complete(null);
    }
});

$deferred->getFuture()->await();
echo $ticks; // 3
```

> `Interval` fires the closure every N seconds. When the `$interval` variable goes out of scope (or is set to `null`), the timer is automatically cancelled via `__destruct`.

---

## disable() and enable() — pause and resume

```php
<?php declare(strict_types=1);

use Amp\DeferredFuture;
use Amp\Interval;

$tickCount = 0;
$deferred  = new DeferredFuture();

$interval = new Interval(0.1, function () use (&$tickCount, &$interval, $deferred): void {
    $tickCount++;

    if ($tickCount === 1) {
        $interval->disable(); // pause the timer

        // Resume after 0.3s using EventLoop::delay (raw callback, not fiber-suspending)
        \Revolt\EventLoop::delay(0.3, function () use (&$interval): void {
            $interval->enable(); // resume
        });
    } elseif ($tickCount === 2) {
        $deferred->complete(null);
    }
});

$deferred->getFuture()->await();
$interval = null;

echo $tickCount; // 2 (tick 1, pause, resume, tick 2)
```

---

## weakClosure() — avoid circular reference

```php
<?php declare(strict_types=1);

use Amp\DeferredFuture;
use Amp\Interval;
use function Amp\weakClosure;

class Reporter
{
    private DeferredFuture $done;
    private ?Interval $interval = null;
    private int $count = 0;

    public function __construct()
    {
        $this->done = new DeferredFuture();

        // weakClosure prevents $this from being strongly held by the closure.
        // Without weakClosure, the Interval keeps the Reporter alive indefinitely
        // because: Reporter → Interval → closure → Reporter (circular reference).
        $this->interval = new Interval(0.1, weakClosure(function (): void {
            $this->count++;
            if ($this->count >= 3) {
                $this->interval = null;         // cancel timer
                $this->done->complete(null);
            }
        }));
    }

    public function run(): int
    {
        $this->done->getFuture()->await();
        return $this->count;
    }
}

$reporter = new Reporter();
echo $reporter->run(); // 3
```

---

## EventLoop::delay() — one-shot raw callback timer

```php
<?php declare(strict_types=1);

use Revolt\EventLoop;

// One-shot: execute callback once after $seconds
// Returns a callback ID (string) that can be cancelled
$id = EventLoop::delay(2.0, function (): void {
    echo "fired after 2 seconds\n";
});

// Cancel before it fires (e.g., if some condition is met first):
EventLoop::cancel($id);
```

> **`EventLoop::delay()` vs `Amp\delay()`**:
> - `Amp\delay(float)` — fiber-suspending: suspends the current fiber and resumes it after N seconds. Used inside `async()` or `AsyncTestCase`.
> - `EventLoop::delay(float, callable)` — raw callback: registers a timer callback, does NOT suspend any fiber. Used when you need a timer from outside a fiber or when the callback must be a plain closure (e.g., inside an `Interval` handler to schedule a future event).

---

## EventLoop::repeat() — recurring raw callback timer

```php
<?php declare(strict_types=1);

use Revolt\EventLoop;

$count = 0;

$id = EventLoop::repeat(0.5, function () use (&$count, &$id): void {
    $count++;
    echo "tick $count\n";

    if ($count >= 3) {
        EventLoop::cancel($id); // stop repeating
    }
});

// EventLoop::run() needed to actually run this if not already in an event loop
EventLoop::run();
```

---

## Interval vs EventLoop::repeat() — when to use which

| | `Interval` | `EventLoop::repeat()` |
|---|---|---|
| Usage | Inside fibers / OOP | Low-level / outside fibers |
| Cancellation | Set reference to `null` | `EventLoop::cancel($id)` |
| Fiber-safe | Yes | Callback only, no suspension |
| Weak reference support | Via `weakClosure()` | No built-in support |
| Typical use | Recurring tasks in app code | Low-level event loop integration |

---

## Key Rules

- `Interval` is cancelled automatically when the object is destroyed (set to `null` or goes out of scope)
- `disable()` / `enable()` toggle the timer without destroying it — useful for pause/resume patterns
- Use `weakClosure()` when a class stores an `Interval` as a property to avoid a circular reference that prevents garbage collection
- `EventLoop::delay(float, callable)` does **not** suspend the current fiber — it only schedules a callback
- `EventLoop::repeat()` returns a callback ID; cancel with `EventLoop::cancel($id)` when done
- Prefer `Amp\delay()` inside fibers for pauses; use `EventLoop::delay()` only when you need a callback-based timer
