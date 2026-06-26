# Fuse.js Complete Options Reference

## Constructor Options

```js
new Fuse(list, {
  // === Fuzzy Search ===
  isCaseSensitive: false,
  ignoreDiacritics: false,         // Ignore diacritics (é → e)
  includeScore: false,
  includeMatches: false,
  minMatchCharLength: 1,           // Minimum number of characters to match
  shouldSort: true,                // Sort results by score
  findAllMatches: false,           // Continue searching after finding a full match
  threshold: 0.6,                  // Fuzziness threshold (0.0=exact, 1.0=match anything)
  location: 0,                     // Expected location of the pattern
  distance: 100,                   // Distance of search window from expected location
  ignoreLocation: false,           // Ignore location penalty
  ignoreFieldNorm: false,          // Ignore field length normalization
  fieldNormWeight: 1,              // Field length normalization weight

  // === Key Configuration ===
  keys: ['title'],                 // Array of strings
  // Or keys with weights:
  // keys: [
  //   { name: 'title', weight: 2 },
  //   { name: 'description', weight: 0.5 }
  // ]

  // === Extended Search ===
  useExtendedSearch: false,        // Enable operator search

  // === Tokenized Search ===
  useTokenSearch: false,           // Enable multi-word tokenized search
  tokenMatch: 'any',               // 'any' = OR, 'all' = AND
  // tokenize: /[\w.+-]+/g          // Custom tokenization regex (function form for CJK)

  // === Sorting ===
  sortFn: undefined,               // Custom sort function
  // sortFn: (a, b) => a.score - b.score

  // === Custom Value Extraction ===
  getFn: undefined,                // Function to extract field value from a document
  // getFn: (obj, path) => { ... }

  // === Result Limit ===
  limit: undefined,                // Maximum number of results to return (-1 = all, heap selection)
  // Multi-key sorting:
  // useStrictSorting: false       // Default sorts by combined score; set to true for per-key sorting
})
```

## search() Method

```js
// String query
fuse.search('pattern')

// Logical query object
fuse.search({ $and: [...], $or: [...] })

// With runtime options
fuse.search('pattern', { limit: 5 })
```

## Result Format

```js
[{
  item: { ... },          // Original document
  refIndex: 0,            // Index in original array
  score: 0.25,            // 0-1 score (requires includeScore: true)
  matches: [{             // Match details (requires includeMatches: true)
    indices: [[0, 3]],    // Character index pairs of matches
    value: 'text',        // Matched field value
    key: 'title',         // Matched field name
    arrayIndex: 0         // Array element index (if applicable)
  }]
}]
```

## Static Methods

```js
// Single fuzzy match
Fuse.match(pattern, string, options?)
// → { isMatch: boolean, score: number, indices: readonly [number, number][] }

// Dynamically register extensions (for basic version)
Fuse.use(ExtendedSearch)

// Create an index for searching (internal use)
Fuse.createIndex(keys, docs, options?)
```

## Instance Methods

```js
// Add document (updates inverted index)
fuse.add(doc)

// Remove document (predicate function)
fuse.remove((doc) => doc.title === 'Old Book')

// Get the index
fuse.getIndex()
```

## FuseWorker Specific Options

```js
new FuseWorker(docs, options, workerOptions)

// workerOptions:
{
  numWorkers: 4,                              // Number of workers (default = hardwareConcurrency, max 8)
  workerUrl: '/static/fuse.worker.mjs'        // Path to worker script
}
```

All FuseWorker methods are asynchronous: `search()`, `add()`, `setCollection()`, `terminate()`.