# AMPHP v3 — Common Mistakes and Gotchas

---

## Top Mistakes

### 1. Calling `await()` outside a Fiber
`await()` only works inside `async()`, `AsyncTestCase`, or `EventLoop::run()`.
Calling it at the top level of a script will throw.

```php
// WRONG — top level, no Fiber context:
$result = someAsyncFn()->await();

// CORRECT — wrap in EventLoop::run():
\Revolt\EventLoop::run(function (): void {
    $result = someAsyncFn()->await();
});
```

---

### 2. Blocking I/O inside the event loop

ANY standard PHP I/O blocks the **entire process** — not just the current fiber:

| Blocked | Async alternative |
|---------|-------------------|
| `sleep()` | `delay(float $seconds)` |
| `file_get_contents()` | `Amp\File\read()` |
| `file_put_contents()` | `Amp\File\write()` |
| `PDO`, `mysqli_query()` | `amphp/mysql`, `amphp/postgres` |
| `curl_exec()` | `amphp/http-client` |
| `dns_get_record()` | `amphp/dns` |
| CPU-heavy loops | `amphp/parallel` + `Worker\Task` |

---

### 3. Forgetting `lock->release()` in `finally`

```php
// WRONG — lock never released if exception thrown:
$lock = $mutex->acquire();
doRiskyWork();
$lock->release();

// CORRECT:
$lock = $mutex->acquire();
try {
    doRiskyWork();
} finally {
    $lock->release();
}
```

---

### 4. Not reading the HTTP response body

```php
// WRONG — leaves body unread, blocks connection reuse:
$response = $client->request($request);
// (body ignored)

// CORRECT:
$body = $response->getBody()->buffer();
// Or stream it:
while (null !== $chunk = $response->getBody()->read()) {
    process($chunk);
}
```

---

### 5. Sharing `Local*` primitives across processes

`LocalMutex`, `LocalSemaphore`, `LocalCache` etc. are **per-process only**.
For cross-process state, use Redis (`amphp/redis`).

---

### 6. Missing `-dzend.assertions=1` in tests

```bash
# WRONG — assert() checks in amphp libraries won't fire:
./vendor/bin/phpunit

# CORRECT:
php -dzend.assertions=1 -dassert.exception=1 ./vendor/bin/phpunit
```

---

### 7. `SIGTERM`/`SIGINT` undefined on Windows

These constants require the `pcntl` extension (Linux/macOS only). Always guard:

```php
if (\extension_loaded('pcntl')) {
    \Amp\trapSignal([\SIGTERM, \SIGINT]);
    $server->stop();
} else {
    \Revolt\EventLoop::run(); // Windows fallback
}
```

---

### 8. `delay()` — `cancellation:` is a named parameter

```php
use Amp\TimeoutCancellation;

// WRONG — second positional arg is bool $reference, not cancellation:
delay(5.0, $cancellation);

// CORRECT — use named parameter:
delay(5.0, cancellation: new TimeoutCancellation(5.0));
```

---

### 9. `File\listFiles()` returns filenames, not full paths

```php
// WRONG:
foreach (\Amp\File\listFiles('/tmp/data') as $path) {
    $content = \Amp\File\read($path); // FAILS — $path is just 'file.txt'
}

// CORRECT:
$dir = '/tmp/data';
foreach (\Amp\File\listFiles($dir) as $name) {
    $content = \Amp\File\read($dir . '/' . $name);
}
```

---

### 10. `Queue::complete()` is mandatory

```php
$queue = new \Amp\Pipeline\Queue();

async(function () use ($queue): void {
    foreach ($items as $item) {
        $queue->push($item);
    }
    $queue->complete(); // ← REQUIRED — omitting this hangs the consumer forever
});

foreach ($queue->iterate() as $value) { /* ... */ }
```

---

### 11. `Channel::receive()` throws, doesn't return null

```php
use Amp\Sync\ChannelException;

// WRONG — channel never returns null; throws ChannelException on EOF:
while ($msg = $channel->receive()) { process($msg); }

// CORRECT:
try {
    while (true) {
        $msg = $channel->receive();
        process($msg);
    }
} catch (ChannelException) {
    // Worker finished and closed its end of the channel — expected
}
```

---

### 12. `ReadableBuffer` closes itself on EOF — breaks Base64 decoder

```php
// WRONG — ReadableBuffer::isClosed() returns true after read(), breaking the decoder:
$decoded = \Amp\ByteStream\buffer(
    new Base64DecodingReadableStream(new ReadableBuffer($encoded))
);

// CORRECT — ReadableIterableStream stays open until iterator is exhausted:
use Amp\ByteStream\ReadableIterableStream;
$decoded = \Amp\ByteStream\buffer(
    new Base64DecodingReadableStream(new ReadableIterableStream([$encoded]))
);
```

---

### 13. `pipe()` does NOT close the destination stream

```php
use function Amp\ByteStream\pipe;

$source = new ReadableBuffer('data');
$sink   = new WritableBuffer();
pipe($source, $sink);
$sink->end(); // ← caller must close the sink manually
echo $sink->buffer();
```

---

### 14. `synchronized()` is a namespace function, not a method

```php
use function Amp\Sync\synchronized;
use Amp\Sync\LocalMutex;

// WRONG — LocalMutex has no synchronized() method:
$mutex->synchronized(fn() => $counter++);

// CORRECT:
$result = synchronized($mutex, fn() => $counter++);
```

---

### 15. Arrow functions don't capture by reference

```php
// WRONG — fn() captures $active by VALUE, not by reference:
$futures = array_map(fn(int $i) => async(fn() => $active++), range(1, 5));

// CORRECT — use foreach with explicit use (&$active):
$futures = [];
foreach (range(1, 5) as $i) {
    $futures[] = async(function () use (&$active): void { $active++; });
}
```

---

### 16. `createRedisClient()` is a factory function, not a class

```php
// WRONG — RedisClient constructor requires RedisLink, not RedisConfig:
$client = new \Amp\Redis\RedisClient($config);

// CORRECT — use the factory:
use function Amp\Redis\createRedisClient;
$client = createRedisClient('redis://127.0.0.1:6379');
// or:
$client = createRedisClient(\Amp\Redis\RedisConfig::fromUri('redis://127.0.0.1:6379'));
```

---

### 17. `Process::start()` is a static factory, not a constructor

```php
// WRONG:
$process = new \Amp\Process\Process('ls -la');

// CORRECT:
$process = \Amp\Process\Process::start('ls -la');
$exitCode = $process->join();
```

---

### 18. `WebSocket receive buffer deadlock`

When implementing a push-only WebSocket handler, **always drain incoming messages**:

```php
public function handleClient(WebsocketClient $client, Request $request, Response $response): void {
    $sender = async(function () use ($client): void {
        while (!$client->isClosed()) {
            $client->sendText(getData());
            delay(1.0);
        }
    });

    // REQUIRED — not draining incoming messages causes buffer overflow and deadlock:
    while ($client->receive() !== null) { /* ignore */ }

    $sender->ignore(); // fire-and-forget cleanup
}
```

---

### 19. `Future::ignore()` on fire-and-forget fibers

If you don't call `ignore()` on a background fiber, any unhandled exception will crash the process when the Future is garbage-collected:

```php
$sender = async(fn() => backgroundWork());
// ... main work ...
$sender->ignore(); // suppress errors from now-abandoned fiber
```
