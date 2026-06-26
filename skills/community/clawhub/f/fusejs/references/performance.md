# Performance Guide

## Factors Affecting Performance

- **Indexing** — O(list size × number of keys × field length). Near-instant for 10k, tens of ms for 100k+
- **Search** — O(n×m), Bitap's 32-char limit provides a lower bound. Lower `threshold` enables earlier pruning.
- **Token search** — Runs Bitap independently for each token, overhead × number of tokens
- **Memory** — Only a few MB for <100k items in typical scenarios

## v7.4.0 Benchmarks

| List Size | Index | With Token Search | Recommendation |
|-----------|-------|-------------------|----------------|
| 1,000 | ~3ms | ~17ms | No optimization needed |
| 10,000 | ~28ms | ~182ms | OK |
| 50,000 | ~147ms | ~963ms | Pre-build index |
| 100,000 | ~299ms | ~2,061ms | FuseWorker |

## Pre-building the Index

```js
const index = Fuse.createIndex(keys, list)
const fuse = new Fuse(list, options, index)
```

## Local Benchmark Script

```js
import Fuse from 'fuse.js'
const SIZE = 10_000, KEYS = ['title', 'desc', 'cat', 'tags']

// Generate sample data
const w = 'alpha bravo charlie delta echo foxtrot golf hotel india juliet javascript typescript python rust'.split(' ')
const list = Array.from({ length: SIZE }, () => ({
  title: Array.from({length:4},()=>w[Math.random()*w.length|0]).join(' '),
  desc: Array.from({length:12},()=>w[Math.random()*w.length|0]).join(' '),
  cat: Array.from({length:2},()=>w[Math.random()*w.length|0]).join(' '),
  tags: Array.from({length:6},()=>w[Math.random()*w.length|0]).join(' '),
}))

const t0 = performance.now()
const fuse = new Fuse(list, { keys: KEYS, threshold: 0.4 })
console.log('Index:', (performance.now()-t0).toFixed(1), 'ms')

const t1 = performance.now()
for (let i=0;i<100;i++) fuse.search('javascript')
console.log('Search avg:', ((performance.now()-t1)/100).toFixed(2), 'ms')
```

Run: `node --input-type=module bench.mjs`

## Optimization Recommendations

- `fuse.search(q, { limit: 20 })` — Reduces sorting and return overhead
- `Fuse.createIndex(keys, items)` — Pre-build and reuse the index
- `FuseWorker` — For datasets larger than 10k
- Index only necessary fields, lower `threshold` to accelerate pruning