# AMPHP v3 — Parallel Processing (CPU-bound)

> Use `amphp/parallel` when you need true CPU parallelism. Tasks run in separate worker processes — they have no shared memory with the parent.

---

## Task class — runs in a worker process

```php
<?php declare(strict_types=1);

use Amp\Cancellation;
use Amp\Parallel\Worker\Task;
use Amp\Sync\Channel;

// Task must:
// 1. Implement Amp\Parallel\Worker\Task
// 2. Be autoloadable by Composer in the worker process
// 3. Have serializable constructor arguments and return value
final class SquareTask implements Task
{
    public function __construct(
        private readonly int $input,
    ) {}

    // Runs in the worker process — CPU-bound work and blocking I/O are safe here
    public function run(Channel $channel, Cancellation $cancellation): int
    {
        return $this->input ** 2;
    }
}
```

---

## Single task — submit() shortcut

```php
<?php declare(strict_types=1);

use function Amp\Parallel\Worker\submit;

// submit() sends to the global worker pool; equivalent to workerPool()->submit()
$result = submit(new SquareTask(7))->await(); // returns 49
```

---

## Fan-out — submit many tasks, await all results

```php
<?php declare(strict_types=1);

use Amp\Future;
use Amp\Parallel\Worker\Execution;
use function Amp\Parallel\Worker\workerPool;
use function Amp\Future\await;

$pool = workerPool(); // access the shared global pool

$inputs = [2, 3, 4, 5, 6];

/** @var Execution[] $executions */
$executions = array_map(
    fn(int $n) => $pool->submit(new SquareTask($n)),
    $inputs,
);

$futures = array_map(fn(Execution $e) => $e->getFuture(), $executions);

$results = await($futures); // [4, 9, 16, 25, 36]
```

---

## Task with progress via IPC Channel

```php
<?php declare(strict_types=1);

use Amp\Cancellation;
use Amp\Parallel\Worker\Task;
use Amp\Sync\Channel;
use function Amp\delay;

// Task sends progress messages back to the parent via Channel
final class ProgressTask implements Task
{
    public function __construct(
        private readonly int $steps,
    ) {}

    public function run(Channel $channel, Cancellation $cancellation): string
    {
        for ($i = 1; $i <= $this->steps; $i++) {
            delay(0.01); // simulate work
            $channel->send(['step' => $i, 'total' => $this->steps]);
        }
        return 'done';
    }
}
```

```php
<?php declare(strict_types=1);

use Amp\Sync\ChannelException;
use function Amp\async;
use function Amp\Parallel\Worker\submit;

$execution = submit(new ProgressTask(5));
$channel   = $execution->getChannel();
$progress  = [];

// IMPORTANT: Channel::receive() throws ChannelException when the task finishes —
// it does NOT return null. Use a try/catch loop, not a while (null !== ...) check.
$receiver = async(function () use ($channel, &$progress): void {
    try {
        while (true) {
            $progress[] = $channel->receive();
        }
    } catch (ChannelException) {
        // Task finished and closed its end of the channel — expected, not an error
    }
});

$result = $execution->getFuture()->await(); // wait for task return value
$receiver->await();                         // wait for progress drain to finish

echo $result; // "done"
// $progress === [['step'=>1,'total'=>5], ['step'=>2,'total'=>5], ...]
```

---

## Bidirectional Channel — parent sends to task

```php
<?php declare(strict_types=1);

use Amp\Cancellation;
use Amp\Parallel\Worker\Task;
use Amp\Sync\Channel;
use Amp\Sync\ChannelException;

// Task reads commands sent from the parent
final class InteractiveTask implements Task
{
    public function run(Channel $channel, Cancellation $cancellation): array
    {
        $results = [];
        try {
            while (true) {
                $command = $channel->receive(); // blocks until parent sends something
                $results[] = strtoupper($command);
                $channel->send("processed: $command");
            }
        } catch (ChannelException) {
            // Parent closed its end — we're done
        }
        return $results;
    }
}
```

```php
// Parent side
use function Amp\Parallel\Worker\submit;
use function Amp\async;

$execution = submit(new InteractiveTask());
$channel   = $execution->getChannel();

async(function () use ($channel): void {
    $channel->send('hello');
    $channel->send('world');
    // Close parent end to signal task to finish:
    // Destroying $channel or letting execution complete will close it
});

$result = $execution->getFuture()->await();
```

---

## Key Rules

- Tasks must be **serializable** — constructor args and return values go through PHP serialization
- Task classes must be **autoloadable by Composer** in the worker subprocess — no closures, no anonymous classes
- Use `workerPool()->submit()` for fan-out; `submit()` is a shorthand that uses the same global pool
- `Execution::getChannel()` returns the IPC channel; `Execution::getFuture()` returns the task result
- `Channel::receive()` throws `ChannelException` (not returns null) when the remote end closes — always use try/catch
- Worker processes share no memory with the parent — `Local*` sync primitives don't work across processes
- CPU-bound work and blocking I/O inside `Task::run()` are fine — they run in a separate process
