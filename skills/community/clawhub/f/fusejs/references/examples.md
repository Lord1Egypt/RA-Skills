# Fuse.js Practical Patterns

## Search Box Filtering

```js
const fuse = new Fuse(items, { keys: ['name', 'description'], threshold: 0.3 })
const results = query ? fuse.search(query).map(r => r.item) : items
```

## Weighted Multi-field Search

```js
const fuse = new Fuse(products, {
  keys: [
    { name: 'name', weight: 3 },
    { name: 'brand', weight: 2 },
    { name: 'description', weight: 1 },
  ],
  threshold: 0.4,
})
```

## Search Highlighting

```js
const fuse = new Fuse(items, { keys: ['title', 'desc'], includeMatches: true })
// result.matches[].indices → [[start, end], ...]
// Iterate over indices and insert <mark> tags in reverse to avoid index shifting
```

## Prefix Search / Autocomplete

```js
// Method 1: Extended search operator
const fuse = new Fuse(countries, { keys: ['name'], useExtendedSearch: true })
fuse.search(`^${query}`).slice(0, 10)

// Method 2: Strict matching
const fuse = new Fuse(countries, { keys: ['name'], threshold: 0.0, ignoreLocation: true })
fuse.search(query, { limit: 10 })
```

## Long Text Search

```js
// Required! Default only searches the first ~60 characters
const fuse = new Fuse(articles, {
  keys: ['title', 'body'],
  ignoreLocation: true,
  threshold: 0.4,
})
```

## Tokenized Search (Multi-word Search Engine Experience)

```js
const fuse = new Fuse(docs, {
  useTokenSearch: true,
  keys: [{ name: 'title', weight: 2 }, { name: 'body', weight: 1 }],
  threshold: 0.3,
})
// "react state mgmt" → 3 words each fuzzy matched → IDF weighted ranking
```

## Extended Search + Logical Query Combination

```js
const fuse = new Fuse(items, { useExtendedSearch: true, keys: ['title', 'tags', 'status'] })

// Title starts with React AND (tags contain hooks OR status not deprecated)
fuse.search({
  $and: [
    { title: '^React' },
    { $or: [{ tags: "'hooks" }, { status: '!deprecated' }] },
  ],
})
```

## Scenario Quick Reference

| Scenario | Configuration Essentials |
|----------|--------------------------|
| Single field, short term | `threshold: 0.3` |
| Multi-field weighted | `keys: [{ name: 'x', weight: 2 }, ...]` |
| Long text | `ignoreLocation: true` |
| Multi-word search | `useTokenSearch: true` |
| Exact filtering | `useExtendedSearch: true` |
| Complex conditions | `{ $and: [...], $or: [...] }` |
| Large dataset >10K | `FuseWorker` |
| Highlighting | `includeMatches: true` |

## Dynamic Data

```js
const fuse = new Fuse([], { keys: ['name', 'email'], useTokenSearch: true })
items.forEach(item => fuse.add(item))
fuse.remove(doc => doc.name === 'Old')
```

For React integration, see [references/react.md](react.md).