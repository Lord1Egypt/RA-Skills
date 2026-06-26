# AMPHP v3 — Database Patterns

---

## MySQL — connection pool setup

```php
<?php declare(strict_types=1);

use Amp\Mysql\MysqlConfig;
use Amp\Mysql\MysqlConnectionPool;

// Pool is created once; reused across the application
$pool = new MysqlConnectionPool(
    MysqlConfig::fromString('host=127.0.0.1 user=root password=secret db=myapp')
);

// Alternatively, DSN-style named params:
$config = MysqlConfig::fromString('host=db.example.com port=3306 user=app password=s3cr3t db=prod charset=utf8mb4');
$pool   = new MysqlConnectionPool($config, maxConnections: 10);
```

---

## MySQL — query and iterate

```php
<?php declare(strict_types=1);

// Simple SELECT — parameterized (safe from SQL injection)
$result = $pool->execute('SELECT id, name FROM users WHERE active = ?', [1]);

foreach ($result as $row) {
    echo $row['id'] . ': ' . $row['name'] . "\n";
}

// Fetch all rows at once (buffered)
$rows = $pool->execute('SELECT * FROM products WHERE category_id = ?', [$categoryId]);
$data = [];
foreach ($rows as $row) {
    $data[] = $row;
}
```

---

## MySQL — transaction

```php
<?php declare(strict_types=1);

$transaction = $pool->beginTransaction();
try {
    $transaction->execute(
        'INSERT INTO orders (user_id, total) VALUES (?, ?)',
        [$userId, $total],
    );

    $result  = $transaction->execute('SELECT LAST_INSERT_ID() AS id');
    $orderId = $result->fetchRow()['id'];

    foreach ($items as $item) {
        $transaction->execute(
            'INSERT INTO order_items (order_id, product_id, qty) VALUES (?, ?, ?)',
            [$orderId, $item['product_id'], $item['qty']],
        );
    }

    $transaction->commit();
} catch (\Throwable $e) {
    $transaction->rollback();
    throw $e;
}
```

---

## MySQL — prepared statement (reuse for many rows)

```php
<?php declare(strict_types=1);

// Prepare once, execute many times — better performance for batch inserts
$statement = $pool->prepare('INSERT INTO events (type, payload, created_at) VALUES (?, ?, NOW())');

foreach ($events as $event) {
    $statement->execute([$event['type'], json_encode($event['data'], JSON_THROW_ON_ERROR)]);
}
```

---

## Redis — client setup

```php
<?php declare(strict_types=1);

use Amp\Redis\RedisConfig;
use function Amp\Redis\createRedisClient;

// createRedisClient() is a FACTORY FUNCTION — not a constructor!
// Always use it instead of new RedisClient(...)
$redis = createRedisClient(RedisConfig::fromUri('redis://127.0.0.1:6379'));

// With password:
$redis = createRedisClient(RedisConfig::fromUri('redis://:password@127.0.0.1:6379/0'));
```

---

## Redis — basic get/set/delete

```php
<?php declare(strict_types=1);

$redis->set('key', 'value');
$value = $redis->get('key');   // 'value'

// With TTL (seconds)
$redis->set('session:abc', $data, 3600);

$redis->delete('key');
$exists = $redis->exists('key'); // false
```

---

## Redis — hash operations

```php
<?php declare(strict_types=1);

$map = $redis->createHashMap('user:42');

$map->set('name', 'Alice');
$map->set('email', 'alice@example.com');

$name  = $map->get('name');       // 'Alice'
$all   = $map->getAll();          // ['name' => 'Alice', 'email' => 'alice@example.com']
$count = $map->count();           // 2

$map->delete('email');
```

---

## Redis — pub/sub

```php
<?php declare(strict_types=1);

use function Amp\Redis\createRedisClient;
use Amp\Redis\RedisConfig;

$publisher  = createRedisClient(RedisConfig::fromUri('redis://127.0.0.1:6379'));
$subscriber = createRedisClient(RedisConfig::fromUri('redis://127.0.0.1:6379'));

// Subscriber — blocks in a fiber, receiving messages as they arrive
$subscription = $subscriber->subscribe('events');

foreach ($subscription as $message) {
    echo $message->channel . ': ' . $message->payload . "\n";
    if ($message->payload === 'shutdown') {
        break;
    }
}

// Publisher (in a different fiber or file):
$publisher->publish('events', json_encode(['type' => 'order.created', 'id' => 99], JSON_THROW_ON_ERROR));
```

---

## Redis — cache wrapper (RedisCache)

```php
<?php declare(strict_types=1);

use Amp\Redis\Cache\RedisCache;
use function Amp\Redis\createRedisClient;
use Amp\Redis\RedisConfig;

$client = createRedisClient(RedisConfig::fromUri('redis://127.0.0.1:6379'));
$cache  = new RedisCache($client);

// Implements Amp\Cache\Cache interface — same API as LocalCache
$cache->set('config', serialize($data), ttl: 3600);
$value = $cache->get('config');
$cache->delete('config');
```

---

## Key Rules

- **MySQL**: always use parameterized queries — never interpolate user data into SQL strings
- **MySQL**: `MysqlConnectionPool` is thread-safe and reuses connections automatically; create it once
- **Redis**: use `createRedisClient()` factory function, not `new RedisClient()`
- **Redis**: each operation (get/set/subscribe) suspends the fiber and resumes when the server responds
- **Transactions**: always call `rollback()` in the catch block before re-throwing
- **Pub/sub**: the subscriber's `foreach` runs in a dedicated fiber — publish from a different fiber
- Both MySQL pool and Redis client are process-local — do not share across worker processes
