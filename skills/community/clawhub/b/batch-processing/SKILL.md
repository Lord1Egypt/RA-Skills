---
name: batch-processing
description: DataLoader pattern for batch processing to solve N+1 query problems. Reduces database/API calls from N+1 to 2 by batching and caching.
---

# Batch Processing with DataLoader

Solve N+1 query problems using the DataLoader pattern. This skill provides utilities for batching database queries, API calls, or any expensive operations.

## Problem: N+1 Query

```javascript
// BAD: N+1 queries (1 for list + N for each item)
const users = await db.query('SELECT * FROM users');
for (const user of users) {
  const posts = await db.query('SELECT * FROM posts WHERE user_id = ?', [user.id]);
  user.posts = posts;
}
// Total queries: 1 + N (where N = number of users)
```

## Solution: DataLoader Pattern

```javascript
// GOOD: 2 queries total using batching
const DataLoader = require('./batch-processing/dataloader.js');

const userLoader = new DataLoader(async (userIds) => {
  // Batch load all users in one query
  const users = await db.query('SELECT * FROM users WHERE id IN (?)', [userIds]);
  return userIds.map(id => users.find(u => u.id === id));
});

const postLoader = new DataLoader(async (userIdss) => {
  // Batch load posts for multiple users
  const allPosts = await db.query('SELECT * FROM posts WHERE user_id IN (?)', [userIdss.flat()]);
  return userIdss.map(ids => allPosts.filter(p => ids.includes(p.user_id)));
});

// Usage - automatically batches concurrent requests
const users = await Promise.all(userIds.map(id => userLoader.load(id)));
const posts = await Promise.all(userIds.map(id => postLoader.load(id)));
// Total queries: 2 (regardless of N)
```

## Core API

### DataLoader Constructor

```javascript
const loader = new DataLoader(batchLoadFn, options);
```

**batchLoadFn**: `async (keys) => values`
- Receives array of keys
- Must return array of values in same order
- Can return null/undefined for missing keys

**options** (optional):
- `maxBatchSize`: Maximum keys per batch (default: 100)
- `batchScheduleMs`: Delay to collect batch (default: 0, immediate)
- `cache`: Enable caching (default: true)
- `cacheKeyFn`: Custom cache key function

### Methods

- **`load(key)`**: Load a single key (returns Promise)
- **`loadMany(keys)`**: Load multiple keys (returns Promise<Array>)
- **`prime(key, value)`**: Manually prime cache
- **`clear(key)`**: Clear cache for key
- **`clearAll()`**: Clear entire cache

## Usage Examples

### Database Batching

```javascript
const userLoader = new DataLoader(async (ids) => {
  const rows = await db.query(
    'SELECT * FROM users WHERE id IN (?)',
    [ids]
  );
  return ids.map(id => rows.find(r => r.id === id) || null);
});

// Concurrent loads are automatically batched
const [user1, user2, user3] = await Promise.all([
  userLoader.load(1),
  userLoader.load(2),
  userLoader.load(3)
]);
```

### API Batching

```javascript
const apiLoader = new DataLoader(async (urls) => {
  const responses = await Promise.all(
    urls.map(url => fetch(url).then(r => r.json()))
  );
  return responses;
});

// Batch multiple API calls
const [data1, data2] = await Promise.all([
  apiLoader.load('https://api.example.com/users/1'),
  apiLoader.load('https://api.example.com/users/2')
]);
```

### Nested Batching (GraphQL-style)

```javascript
const postLoader = new DataLoader(async (userIds) => {
  const posts = await db.query(
    'SELECT * FROM posts WHERE user_id IN (?)',
    [userIds]
  );
  return userIds.map(id => posts.filter(p => p.user_id === id));
});

const commentLoader = new DataLoader(async (postIds) => {
  const comments = await db.query(
    'SELECT * FROM comments WHERE post_id IN (?)',
    [postIds.flat()]
  );
  return postIds.map(ids => comments.filter(c => ids.includes(c.post_id)));
});

// Resolve nested data efficiently
const users = await userLoader.loadMany(userIds);
for (const user of users) {
  user.posts = await postLoader.load(user.id);
  for (const post of user.posts) {
    post.comments = await commentLoader.load(post.id);
  }
}
```

## Performance Comparison

| Scenario | Without DataLoader | With DataLoader |
|----------|-------------------|-----------------|
| Load 100 users | 101 queries | 1 query |
| Load 100 users + posts | 201 queries | 2 queries |
| Load 100 users + posts + comments | 301 queries | 3 queries |

## Best Practices

1. **Create loaders per request**: Don't share loaders across requests to avoid cache pollution
2. **Batch size matters**: Tune `maxBatchSize` based on your database/API limits
3. **Handle errors gracefully**: Return null/undefined for missing keys, don't throw
4. **Use with Promise.all**: Concurrent loads trigger batching
5. **Clear cache when needed**: Use `clear()` for mutations that affect cached data

## Files

- `dataloader.js` - Core DataLoader implementation
- `examples/` - Usage examples for different scenarios
- `benchmarks/` - Performance comparison scripts

## Installation

This skill is self-contained. Import the DataLoader:

```javascript
const DataLoader = require('./batch-processing/dataloader.js');
```

## When to Use

✅ Multiple database queries in a loop
✅ Fetching related data for multiple items
✅ API calls that can be batched
✅ GraphQL resolvers
✅ Any N+1 query pattern

❌ Single queries
❌ Real-time streaming data
❌ When order matters and can't be preserved
