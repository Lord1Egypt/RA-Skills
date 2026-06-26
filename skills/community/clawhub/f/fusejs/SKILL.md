---
name: fusejs
description: Implement fuzzy search in JavaScript/TypeScript projects using Fuse.js. Use when users need client-side search, fuzzy matching, search highlighting, multi-field weighted search, tokenized search, or Web Worker parallel search.
---

# Fuse.js Fuzzy Search

A zero-dependency TypeScript library based on the Bitap algorithm. Works in browsers, Node.js, and Deno.

## Installation

```bash
npm install fuse.js           # Full version
npm install fuse.js@beta      # Includes FuseWorker
```

```js
import Fuse from 'fuse.js'          // ESM full version
import Fuse from 'fuse.js/basic'    // Basic version (fuzzy search only)
```

## Minimal Example

```js
const fuse = new Fuse(list, {
  keys: ['title', 'author'],
  includeScore: true,         // Returns score 0-1
  threshold: 0.4,             // 0=exact match, 1=any match (0.3-0.4 recommended for search-as-you-type)
})
fuse.search('jon')            // → [{ item, score, refIndex }]
```

## Usage by Scenario

### Fuzzy Search (Basic)

```js
new Fuse(list, {
  keys: ['name'],
  threshold: 0.4,
  ignoreLocation: true,       // MUST enable for long text, otherwise only searches ~first 60 chars
  includeMatches: true,       // For highlighting
  includeScore: true,
  minMatchCharLength: 2,      // Ignores single-character matches
})
```

### Multi-field Weighted Search

```js
keys: [
  { name: 'title', weight: 2 },
  { name: 'description', weight: 1 },
]
```
Dot notation: `'author.firstName'`. Set `ignoreFieldNorm` to disable the short-field bonus.

### Extended Search (Operators)

```js
{ useExtendedSearch: true }

fuse.search('^java =exact')    // space=AND, |=OR
fuse.search("!deprecated | 'active")
```

Operators: no prefix=fuzzy, `=`=exact, `'`=contains, `!`=exclude, `^`=prefix, `.$`=suffix. Requires `Fuse.use(ExtendedSearch)` for the basic version.

### Tokenized Search

```js
{
  useTokenSearch: true,
  tokenMatch: 'any'           // 'any'(OR, default) | 'all'(AND filtering)
}
```

Multi-word queries are split into independent tokens for fuzzy matching + IDF weighting. Word order is irrelevant, and there is no 32-character length limit. Use the `tokenize` function + `Intl.Segmenter` for CJK tokenization. Full version only.

### Logical Queries

```js
fuse.search({
  $and: [{ title: 'js' }, { $or: [{ author: 'a' }, { author: 'b' }] }]
})
```

### Highlighting

`includeMatches: true` → `result.matches[].indices` → `[[start, end], ...]`. Note: `end` is inclusive.

### Dynamic Add/Remove & Single Matching

```js
fuse.add(doc)
fuse.remove(doc => doc.id === 'x')
Fuse.match('patern', 'pattern matching')  // → { isMatch, score, indices }
```

### Web Worker (Large Datasets)

```js
import { FuseWorker } from 'fuse.js/worker'
const fuse = new FuseWorker(docs, { keys: ['title'] })
const r = await fuse.search('q')
fuse.terminate()    // Must clean up
```
With 4 workers + 100K documents: approximately 3.3x speedup. Browser only. Does not support `sortFn`/`getFn`/`useTokenSearch`.

## Reference Documentation

Load as needed:
- **[options](references/options.md)** — Complete options API
- **[examples](references/examples.md)** — Practical patterns and scenario quick reference
- **[react](references/react.md)** — React components: debouncing, highlighting, virtualization
- **[performance](references/performance.md)** — Benchmark data and optimization guide
- **[vs-semantic](references/vs-semantic.md)** — Comparison with semantic search and selection guide

## Important Notes

- Default search only looks at the first ~60 characters of a field → Use `ignoreLocation: true` for long text.
- Bitap has a single-pattern limit of 32 characters → Use `useTokenSearch` for long queries.
- FuseWorker is browser only. The `search()` method returns a Promise. Does not support function options.
- Score: 0 = perfect match, 1 = no match.
- The basic version does not include extended search or tokenized search.