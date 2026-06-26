# Fuse.js React Integration

## Basic Search Component

```jsx
import { useMemo, useState } from 'react'
import Fuse from 'fuse.js'

function SearchList({ items }) {
  const [query, setQuery] = useState('')
  const fuse = useMemo(() => new Fuse(items, {
    keys: ['title', 'author'], threshold: 0.4
  }), [items])

  const results = query ? fuse.search(query).map(r => r.item) : items

  return <>
    <input value={query} onChange={e => setQuery(e.target.value)} />
    {results.map(item => <div key={item.id}>{item.title}</div>)}
  </>
}
```

**Key points**: Wrap Fuse in `useMemo` to avoid rebuilding on every render; `threshold: 0.3-0.4` is suitable for search-as-you-type.

## Debouncing (200ms)

```jsx
function useDebounce(value, delay = 200) {
  const [v, setV] = useState(value)
  useEffect(() => { const t = setTimeout(() => setV(value), delay); return () => clearTimeout(t) }, [value])
  return v
}
// Usage: const q = useDebounce(query); fuse.search(q)
```

## Match Highlighting

```jsx
function highlight(text, indices = []) {
  if (!indices.length) return text
  const parts = []; let last = 0
  for (const [s, e] of indices) {
    if (s > last) parts.push(text.slice(last, s))
    parts.push(<mark key={s}>{text.slice(s, e + 1)}</mark>)
    last = e + 1
  }
  if (last < text.length) parts.push(text.slice(last))
  return parts
}
```

Enable `includeMatches: true`, retrieve match intervals from `result.matches[].indices` (note: `end` is inclusive).

## Large Dataset Optimization

```jsx
// Limit results
fuse.search(q, { limit: 20 })

// Pre-build index
const idx = Fuse.createIndex(keys, items)
const fuse = new Fuse(items, { keys }, idx)

// Virtualization (react-window)
import { FixedSizeList } from 'react-window'
<FixedSizeList height={400} itemCount={results.length} itemSize={40}>
  {({ index, style }) => <div style={style}>{results[index].item.title}</div>}
</FixedSizeList>
```

## Complete Generic Component

```jsx
function FuzzySearch({ items, keys, itemKey, placeholder = 'Search...' }) {
  const [query, setQuery] = useState('')
  const q = useDebounce(query, 200)
  const fuse = useMemo(() => new Fuse(items, { keys, includeMatches: true, threshold: 0.4 }), [items, keys])
  const results = q ? fuse.search(q, { limit: 50 }) : []

  return <>
    <input value={query} onChange={e => setQuery(e.target.value)} placeholder={placeholder} />
    {(results.length ? results.map(({ item, matches }) => (
      <div key={item[itemKey]}>
        {keys.map(k => highlight(item[k], matches?.find(m => m.key === k)?.indices))}
      </div>
    )) : items.slice(0, 50).map(i => <div key={i[itemKey]}>{keys.map(k => i[k])}</div>))}
  </>
}
```

## Tips

- Nested keys: `keys: ['address.city']`
- Weighting: `keys: [{ name: 'title', weight: 2 }, ...]`
- Enable `includeScore` only in development, remove in production
- When data doesn't change, use `useMemo(() => ..., [])` instead of `[items]`