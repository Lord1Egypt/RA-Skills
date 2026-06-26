# Workflow: CPU-bound Fan-out with Worker Pool + IPC Progress

This workflow runs many CPU-heavy tasks in parallel across worker processes, collecting progress updates via IPC channel while waiting for all results.

---

## Task class (worker side)

```php
<?php declare(strict_types=1);

// src/Worker/ProcessChunkTask.php
namespace App\Worker;

use Amp\Cancellation;
use Amp\Parallel\Worker\Task;
use Amp\Sync\Channel;

/**
 * Processes one chunk of data in an isolated worker process.
 *
 * Rules:
 * - Constructor args and return value must be PHP-serializable
 * - Class must be Composer-autoloadable (workers load it via autoloader)
 * - CPU-bound and blocking I/O are safe here — they run in a separate process
 */
final class ProcessChunkTask implements Task
{
    public function __construct(
        private readonly int   $chunkId,
        private readonly array $data,
    ) {}

    public function run(Channel $channel, Cancellation $cancellation): array
    {
        $total   = count($this->data);
        $results = [];

        foreach ($this->data as $i => $item) {
            $cancellation->throwIfRequested(); // cooperate with cancellation

            $results[] = $this->processItem($item);

            // Send progress update to parent
            $channel->send([
                'chunk'   => $this->chunkId,
                'step'    => $i + 1,
                'total'   => $total,
                'percent' => round(($i + 1) / $total * 100),
            ]);
        }

        return $results;
    }

    private function processItem(mixed $item): mixed
    {
        // CPU-heavy work here (hashing, compression, encoding, etc.)
        return hash('sha256', serialize($item));
    }
}
```

---

## Fan-out orchestrator (parent side)

```php
<?php declare(strict_types=1);

// src/Worker/ParallelProcessor.php
namespace App\Worker;

use Amp\Future;
use Amp\Parallel\Worker\Execution;
use Amp\Sync\ChannelException;
use function Amp\async;
use function Amp\Future\await;
use function Amp\Parallel\Worker\workerPool;

final class ParallelProcessor
{
    /**
     * Split $items into $chunkSize chunks, process each in a worker,
     * collect progress updates, and return all results merged.
     *
     * @param list<mixed>   $items
     * @param positive-int  $chunkSize
     * @param callable|null $onProgress  fn(array $progress): void
     * @return list<mixed>
     */
    public function process(array $items, int $chunkSize = 100, ?callable $onProgress = null): array
    {
        $pool   = workerPool();
        $chunks = array_chunk($items, $chunkSize);

        /** @var Execution[] $executions */
        $executions = [];
        foreach ($chunks as $id => $chunk) {
            $executions[$id] = $pool->submit(new ProcessChunkTask($id, $chunk));
        }

        // Spawn a progress receiver fiber for each execution
        $progressFibers = [];
        foreach ($executions as $id => $execution) {
            $channel = $execution->getChannel();
            $progressFibers[$id] = async(function () use ($channel, $onProgress): void {
                try {
                    while (true) {
                        $update = $channel->receive();
                        if ($onProgress !== null) {
                            ($onProgress)($update);
                        }
                    }
                } catch (ChannelException) {
                    // Worker finished and closed the channel — expected
                }
            });
        }

        // Collect all results
        $futures = array_map(fn(Execution $e) => $e->getFuture(), $executions);
        $chunkResults = await($futures); // indexed by $id

        // Wait for all progress drains to complete
        await($progressFibers);

        // Merge chunks back into a flat array (preserving original order)
        ksort($chunkResults);
        return array_merge(...array_values($chunkResults));
    }
}
```

---

## Usage

```php
<?php declare(strict_types=1);

use App\Worker\ParallelProcessor;
use Revolt\EventLoop;

require __DIR__ . '/vendor/autoload.php';

EventLoop::run(function (): void {
    $processor = new ParallelProcessor();

    $items = range(1, 500); // 500 items to process

    $results = $processor->process(
        items:      $items,
        chunkSize:  50,
        onProgress: function (array $p): void {
            printf("Chunk %d: %d/%d (%d%%)\n", $p['chunk'], $p['step'], $p['total'], $p['percent']);
        },
    );

    printf("Done: %d results\n", count($results));
});
```

---

## Key points

- **`ChannelException` signals completion** — `Channel::receive()` throws it when the remote end closes; it does NOT return null
- **Progress receivers run concurrently** — each gets its own `async()` fiber so all channels are drained in parallel
- **`await($futures)` then `await($progressFibers)`** — wait for results first, then drain remaining progress events
- **Serialization boundary** — `$chunkId` and `$data` in the constructor must be serializable; closures are not
- **`Cancellation::throwIfRequested()`** inside the task loop — cooperative cancellation support
- **`workerPool()`** returns the global pool; it reuses processes across calls — don't create a new pool per task
- Tasks must be in Composer's autoload map so workers can load them in their own PHP process

---

## Packages needed

```bash
composer require revolt/event-loop amphp/amp
composer require amphp/parallel
```
