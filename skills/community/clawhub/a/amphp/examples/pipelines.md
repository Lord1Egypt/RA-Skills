# AMPHP v3 — Pipeline & Queue Patterns

---

## Queue — producer/consumer with back-pressure

```php
<?php declare(strict_types=1);

use Amp\Pipeline\Queue;
use function Amp\async;

$queue = new Queue();

// Producer fiber — MUST call complete() or error(), otherwise consumer hangs forever
async(function () use ($queue): void {
    foreach (['a', 'b', 'c'] as $item) {
        $queue->push($item); // suspends if consumer is slow (back-pressure)
    }
    $queue->complete();
    // On error: $queue->error(new \RuntimeException('source failed'));
});

// Consumer — iterates in current fiber
$results = [];
foreach ($queue->iterate() as $value) {
    $results[] = $value;
}
// $results === ['a', 'b', 'c']
```

---

## Queue error propagation

```php
<?php declare(strict_types=1);

use Amp\Pipeline\Queue;
use function Amp\async;

$queue = new Queue();

async(function () use ($queue): void {
    $queue->push(1);
    $queue->error(new \RuntimeException('source failed'));
});

try {
    foreach ($queue->iterate() as $value) {
        // consume values
    }
} catch (\RuntimeException $e) {
    echo $e->getMessage(); // "source failed"
}
```

---

## Pipeline::fromIterable() — filter, map, take

```php
<?php declare(strict_types=1);

use Amp\Pipeline\Pipeline;

$result = Pipeline::fromIterable([1, 2, 3, 4, 5, 6])
    ->filter(fn(int $x) => $x % 2 === 0)  // keep even: 2, 4, 6
    ->map(fn(int $x) => $x ** 2)            // square: 4, 16, 36
    ->take(2)                                // first 2: 4, 16
    ->toArray();
// $result === [4, 16]
```

---

## skip, takeWhile, skipWhile, sorted

```php
<?php declare(strict_types=1);

use Amp\Pipeline\Pipeline;

$result = Pipeline::fromIterable([1, 2, 3, 7, 8, 9])
    ->skip(1)                               // skip 1: [2, 3, 7, 8, 9]
    ->takeWhile(fn(int $x) => $x < 8)      // take while < 8: [2, 3, 7]
    ->sorted(fn(int $a, int $b) => $b <=> $a) // sort descending: [7, 3, 2]
    ->toArray();
// sorted() buffers ALL items — only use on bounded pipelines

// skipWhile: skip until predicate is false
$result = Pipeline::fromIterable([1, 2, 3, 4, 5])
    ->skipWhile(fn(int $x) => $x < 3)     // skip 1, 2 → [3, 4, 5]
    ->toArray();
```

---

## tap() — side effects without modifying values

```php
<?php declare(strict_types=1);

use Amp\Pipeline\Pipeline;

$logged = [];

$result = Pipeline::fromIterable([10, 20, 30])
    ->tap(function (int $v) use (&$logged): void {
        $logged[] = "saw: $v"; // log/debug without affecting the stream
    })
    ->map(fn(int $v) => $v * 2)
    ->toArray();
// $result === [20, 40, 60]
// $logged === ['saw: 10', 'saw: 20', 'saw: 30']
```

---

## reduce, count, allMatch, anyMatch, noneMatch

```php
<?php declare(strict_types=1);

use Amp\Pipeline\Pipeline;

$numbers = [2, 4, 6, 8];

$sum = Pipeline::fromIterable($numbers)
    ->reduce(fn(int $carry, int $item) => $carry + $item, 0);
// $sum === 20

$count = Pipeline::fromIterable($numbers)->count();
// $count === 4

$allEven  = Pipeline::fromIterable($numbers)->allMatch(fn(int $x) => $x % 2 === 0); // true
$anyOver5 = Pipeline::fromIterable($numbers)->anyMatch(fn(int $x) => $x > 5);       // true
$noneOdd  = Pipeline::fromIterable($numbers)->noneMatch(fn(int $x) => $x % 2 !== 0); // true
```

---

## concurrent() — parallel item processing

```php
<?php declare(strict_types=1);

use Amp\Pipeline\Pipeline;
use Amp\Http\Client\HttpClientBuilder;
use Amp\Http\Client\Request as HttpRequest;

$client = HttpClientBuilder::buildDefault();

$bodies = Pipeline::fromIterable($urls)
    ->concurrent(5)   // process up to 5 items simultaneously
    ->map(fn(string $url) => $client->request(new HttpRequest($url))->getBody()->buffer())
    ->toArray();

// Add ->unordered() after ->concurrent() for higher throughput when order doesn't matter:
// ->concurrent(5)->unordered()->map(...)
```

---

## Pipeline::merge() and Pipeline::concat()

```php
<?php declare(strict_types=1);

use Amp\Pipeline\Pipeline;

$a = Pipeline::fromIterable([1, 2, 3]);
$b = Pipeline::fromIterable([4, 5, 6]);

// merge(): interleaves — items arrive as they become available (unordered)
$merged = Pipeline::merge([$a, $b])->toArray();
// order not guaranteed; contains all 6 values

// concat(): sequential — fully drains first pipeline, then second
$a2 = Pipeline::fromIterable([1, 2, 3]);
$b2 = Pipeline::fromIterable([4, 5, 6]);
$sequential = Pipeline::concat([$a2, $b2])->toArray();
// $sequential === [1, 2, 3, 4, 5, 6] (order guaranteed)
```

---

## Queue + Pipeline chained

```php
<?php declare(strict_types=1);

use Amp\Pipeline\Queue;
use Amp\Pipeline\Pipeline;
use function Amp\async;

$queue = new Queue();

async(function () use ($queue): void {
    foreach (range(1, 10) as $n) {
        $queue->push($n);
    }
    $queue->complete();
});

$results = Pipeline::fromIterable($queue->iterate())
    ->filter(fn(int $n) => $n % 2 === 0)
    ->map(fn(int $n) => $n * 10)
    ->toArray();
// $results === [20, 40, 60, 80, 100]
```

---

## Key Rules

- `Queue::complete()` or `Queue::error()` **must** always be called — otherwise consumers hang forever
- `sorted()` buffers all items into memory — avoid on infinite or very large pipelines
- `concurrent()` preserves order by default; add `->unordered()` after it for maximum throughput when order doesn't matter
- `Pipeline::merge()` interleaves (items arrive as ready); `Pipeline::concat()` is strictly sequential
- `Pipeline::fromIterable()` accepts arrays, generators, and any `Queue::iterate()` result
