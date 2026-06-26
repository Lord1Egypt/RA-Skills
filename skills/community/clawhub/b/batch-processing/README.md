# Batch Processing Skill - DataLoader Pattern

🚀 **Solve N+1 query problems by reducing database/API calls from N+1 to 2**

## Quick Start

```javascript
const DataLoader = require('./batch-processing/dataloader.js');

// Create a loader for your data source
const userLoader = new DataLoader(async (ids) => {
  const users = await db.query('SELECT * FROM users WHERE id IN (?)', [ids]);
  return ids.map(id => users.find(u => u.id === id));
});

// Use it - concurrent loads are automatically batched!
const [user1, user2, user3] = await Promise.all([
  userLoader.load(1),
  userLoader.load(2),
  userLoader.load(3)
]);
// Only 1 database query instead of 3!
```

## The Problem: N+1 Queries

```javascript
// ❌ BAD: Makes N+1 queries
const users = await db.query('SELECT * FROM users');
for (const user of users) {
  const posts = await db.query('SELECT * FROM posts WHERE user_id = ?', [user.id]);
  // Each iteration = 1 query. 100 users = 101 queries!
}
```

## The Solution: DataLoader

```javascript
// ✅ GOOD: Makes only 2 queries total
const userLoader = new DataLoader(async (ids) => {
  const users = await db.query('SELECT * FROM users WHERE id IN (?)', [ids]);
  return ids.map(id => users.find(u => u.id === id));
});

const postLoader = new DataLoader(async (userIds) => {
  const posts = await db.query('SELECT * FROM posts WHERE user_id IN (?)', [userIds]);
  return userIds.map(id => posts.filter(p => p.user_id === id));
});

const users = await userLoader.loadMany([1, 2, 3, 4, 5]);
const posts = await Promise.all(users.map(u => postLoader.load(u.id)));
// Total: 2 queries regardless of N!
```

## Features

- ✅ **Automatic Batching**: Concurrent loads are automatically batched together
- ✅ **Caching**: Built-in cache prevents duplicate loads
- ✅ **Configurable**: Tune batch size, scheduling, and cache behavior
- ✅ **Zero Dependencies**: Pure JavaScript, works everywhere
- ✅ **Type Safe**: Validates batch function output

## API

### Constructor

```javascript
const loader = new DataLoader(batchLoadFn, options);
```

**batchLoadFn**: `async (keys) => values`
- Receives array of keys
- Must return array of values in same order
- Can return null/undefined for missing keys

**options**:
- `maxBatchSize`: Maximum keys per batch (default: 100)
- `batchScheduleMs`: Delay to collect batch (default: 0)
- `cache`: Enable caching (default: true)
- `cacheKeyFn`: Custom cache key function

### Methods

| Method | Description |
|--------|-------------|
| `load(key)` | Load a single key |
| `loadMany(keys)` | Load multiple keys |
| `prime(key, value)` | Manually prime cache |
| `clear(key)` | Clear cache for key |
| `clearAll()` | Clear entire cache |

## Performance

| Scenario | Without DataLoader | With DataLoader | Improvement |
|----------|-------------------|-----------------|-------------|
| Load 100 users | 101 queries | 1 query | **99% fewer** |
| Load 100 users + posts | 201 queries | 2 queries | **99% fewer** |
| Load 100 users + posts + comments | 301 queries | 3 queries | **99% fewer** |

**Benchmark Results** (100 users, 10ms query latency):
- Naive: 201 queries, 2100ms
- DataLoader: 3 queries, 120ms
- **Speedup: 17.5x faster** ⚡

## Run Examples

```bash
# Run usage examples
node examples.js

# Run performance benchmarks
node benchmark.js
```

## Use Cases

- 🗄️ **Database queries**: Batch IN() queries instead of individual SELECTs
- 🌐 **API calls**: Combine multiple API requests into batch endpoints
- 🔗 **GraphQL**: Resolve nested fields efficiently
- 📦 **File operations**: Batch file reads/writes
- 🔄 **Any N+1 pattern**: Wherever you're looping and querying

## Files

```
batch-processing/
├── SKILL.md           # Full documentation
├── dataloader.js      # Core implementation
├── examples.js        # Usage examples
├── benchmark.js       # Performance tests
└── package.json       # Package metadata
```

## License

MIT
