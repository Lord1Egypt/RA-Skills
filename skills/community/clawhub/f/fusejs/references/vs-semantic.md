# Fuse.js vs Semantic Search Selection Guide

## Core Differences

| | Fuse.js | Semantic Search |
|---|---|---|
| Matching Method | Character similarity (fuzzy) | Semantic similarity (meaning) |
| Execution Location | Client-side (Browser/Node) | Server-side (API + Database) |
| Latency | < 10ms | 50-500ms |
| Cost | Free | Embedding API + Database hosting |
| Setup | `npm install fuse.js` | Model + Database + Indexing pipeline |
| Handles typos | ✅ Core capability | ❌ Embeddings are typo-sensitive |
| Understands semantics | ❌ | ✅ |
| Offline capable | ✅ | ❌ |
| Dataset size | Thousands ~ 100k | Millions+ |
| Dependencies | Zero dependencies | Embedding model, vector DB, backend |

## Choose Fuse.js When

Users are looking for known content — names, titles, settings, commands. This is the most common search interaction in applications.

**Good for:**
- Searching contacts, products, files, setting lists
- Command palettes and autocomplete
- Filtering tables or dropdowns by name
- Datasets < 100k items that fit in the browser
- Offline or privacy-sensitive scenarios

**Advantages:**
- Zero latency
- Zero cost
- Zero dependencies
- Privacy (data never leaves the device)
- ~5KB gzip, 5 lines of code to get started

## Choose Semantic Search When

Users describe needs in natural language, requiring understanding of meaning rather than character matching.

**Good for:**
- "Find articles about climate change" (even if those exact words aren't present)
- Semantic document retrieval for RAG pipelines
- Similar images / products / recommendations
- Cross-language search
- Million+ document scale

**Costs:**
- Embedding API calls
- Vector database hosting ($20-500+/month)
- Indexing pipeline complexity
- Network latency

## Common Misconception

❌ Using Embeddings for simple lookup:
```js
// Over-engineering — calling an API to search 200 items
const response = await fetch('/api/search', {
  method: 'POST',
  body: JSON.stringify({ query: userInput })
})
// Server: embed query → query Pinecone → return results
// Total latency: 300ms, cost: ~$0.001/request
```

✅ Correct approach:
```js
// Simple — in-browser search on 200 items <1ms
const fuse = new Fuse(items, { keys: ['name', 'description'] })
const results = fuse.search(userInput)
```

**Rule of thumb: Is the user searching "by meaning" or "by name"?** If the latter, you probably don't need Embeddings.

## Combining Both

The best AI applications often use both:

```js
// Layer 1: Instant search
const fuse = new Fuse(docs, { keys: ['title', 'headings', 'slug'], threshold: 0.3 })
function handleSearchInput(query) {
  return fuse.search(query).slice(0, 5) // Results appear as the user types
}

// Layer 2: Semantic search
async function handleQuestion(question) {
  const embedding = await embed(question)
  const chunks = await vectorDB.query({ vector: embedding, topK: 10 })
  return await llm.answer(question, chunks)
}
```

E-commerce example:
- Product search box → Fuse.js (instant, typo-tolerant filtering)
- "Find similar products" → Semantic Search (recommendations)
- Category browsing + filters → Fuse.js
- Natural language queries → Semantic Search

## Decision Checklist

**Choose Fuse.js:**
- [ ] Dataset fits in memory (< ~100k items)
- [ ] Users search by entering a name/title/known term
- [ ] Need <10ms zero-latency instant feedback
- [ ] Users frequently mistype search terms
- [ ] Offline or privacy-sensitive scenarios
- [ ] Zero backend infrastructure required

**Choose Semantic Search:**
- [ ] Users describe needs in natural language
- [ ] Need to find semantically similar content
- [ ] Dataset is too large for client-side search
- [ ] Building a RAG pipeline for an LLM
- [ ] Need cross-language search capabilities