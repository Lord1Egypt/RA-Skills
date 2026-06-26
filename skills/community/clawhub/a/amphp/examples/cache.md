# AMPHP v3 — Cache Patterns

---

## LocalCache — in-memory LRU cache

```php
<?php declare(strict_types=1);

use Amp\Cache\LocalCache;

// Default constructor: no size limit, no TTL
$cache = new LocalCache();

// Optional: $sizeLimit caps the number of entries (LRU eviction)
$cache = new LocalCache(sizeLimit: 100);

$cache->set('key', 'value');
$value = $cache->get('key');   // 'value'
$cache->delete('key');         // returns true if key existed
$cache->get('key');            // null — key was deleted
```

---

## LocalCache with TTL

```php
<?php declare(strict_types=1);

use Amp\Cache\LocalCache;

$cache = new LocalCache();

// set(key, value, ttl) — ttl is in seconds; null = no expiry
$cache->set('session', $data, ttl: 3600); // expires in 1 hour

$value = $cache->get('session'); // returns value within TTL window
```

---

## LocalCache LRU eviction

```php
<?php declare(strict_types=1);

use Amp\Cache\LocalCache;

$cache = new LocalCache(sizeLimit: 3); // max 3 entries

$cache->set('a', 1);
$cache->set('b', 2);
$cache->set('c', 3);

$cache->get('a'); // access 'a' → makes it recently used

$cache->set('d', 4); // evicts least-recently-used (which is now 'b')

echo $cache->get('a'); // 1 — still present
echo $cache->get('b'); // null — evicted
echo $cache->get('d'); // 4 — present
echo $cache->count();  // 3 (within limit)
```

---

## NullCache — no-op (useful in tests / disabling cache)

```php
<?php declare(strict_types=1);

use Amp\Cache\NullCache;

$cache = new NullCache();

$cache->set('key', 'value'); // silently discarded

echo $cache->get('key');    // always null
echo $cache->delete('key'); // always null (key never existed)
```

---

## PrefixCache — namespace keys with a prefix

```php
<?php declare(strict_types=1);

use Amp\Cache\LocalCache;
use Amp\Cache\PrefixCache;

$base   = new LocalCache();
$users  = new PrefixCache($base, 'user:');
$orders = new PrefixCache($base, 'order:');

$users->set('42', $userData);      // stored as 'user:42' in $base
$orders->set('99', $orderData);    // stored as 'order:99' in $base

$users->get('42');                 // fetches 'user:42'
$users->getKeyPrefix();            // 'user:'
$base->get('user:42');             // same underlying value
```

---

## AtomicCache — compute-if-absent

```php
<?php declare(strict_types=1);

use Amp\Cache\AtomicCache;
use Amp\Cache\LocalCache;
use Amp\Sync\LocalKeyedMutex;

$base   = new LocalCache();
$atomic = new AtomicCache($base, new LocalKeyedMutex());

// computeIfAbsent: factory is called only once even under concurrent requests for the same key
$value = $atomic->computeIfAbsent('config', function (string $key): array {
    return loadExpensiveConfig(); // called once, then cached
});

// Second call for the same key — factory is NOT called again
$sameValue = $atomic->computeIfAbsent('config', fn(string $k) => expensiveCall());
```

---

## AtomicCache::compute() — always re-computes (mutex-protected update)

```php
<?php declare(strict_types=1);

use Amp\Cache\AtomicCache;
use Amp\Cache\LocalCache;
use Amp\Sync\LocalKeyedMutex;

$base   = new LocalCache();
$atomic = new AtomicCache($base, new LocalKeyedMutex());

// compute(key, closure(key, ?currentValue) => newValue)
// Closure receives the current value (null if absent) and MUST return the new value to store
for ($i = 0; $i < 3; $i++) {
    $atomic->compute('counter', fn(string $k, ?int $v) => ($v ?? 0) + 1);
}

echo (int) $atomic->get('counter', 0); // 3

// IMPORTANT: get(key, default) — second arg is the default when key is absent
$value = $atomic->get('missing', 42); // returns 42 if 'missing' not found
```

---

## Cache as a dependency (type hint on interface)

```php
<?php declare(strict_types=1);

use Amp\Cache\Cache;        // interface for get/set/delete
use Amp\Cache\LocalCache;

class UserRepository
{
    public function __construct(
        private readonly Cache $cache,
    ) {}

    public function find(int $id): ?array
    {
        $cached = $this->cache->get("user:$id");
        if ($cached !== null) {
            return $cached;
        }

        $user = $this->loadFromDatabase($id);
        $this->cache->set("user:$id", $user, ttl: 300);
        return $user;
    }
}

// Production: real cache
$repo = new UserRepository(new LocalCache(1000));

// Test: no-op cache (no need to mock)
use Amp\Cache\NullCache;
$repo = new UserRepository(new NullCache());
```

---

## Key Rules

- `LocalCache` is single-process only — do not share across worker processes
- `AtomicCache::computeIfAbsent()` prevents stampedes (only one fiber runs the factory)
- `AtomicCache::compute()` closure signature: `fn(string $key, ?CurrentType $current): NewType` — must return the new value
- `AtomicCache::get($key, $default)` — second param is the default value when key is absent
- `LocalCache(sizeLimit: N)` uses LRU eviction; accessing a key counts as "recently used"
- `NullCache::delete()` returns `null` (key never existed) — useful to know in tests
- For cross-process cache, use `amphp/redis` (`RedisCache`) instead of `LocalCache`
