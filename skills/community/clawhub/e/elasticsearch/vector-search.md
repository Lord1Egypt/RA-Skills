# Vector Search — kNN, Hybrid Retrieval, and What It Costs

Vector search in Elasticsearch is approximate nearest-neighbour over HNSW graphs held in memory-mapped Lucene segments. It complements BM25; it replaces it only in narrow cases.

## Mapping a Vector Field

```json
"embedding": { "type": "dense_vector", "dims": 768, "index": true,
               "similarity": "cosine",
               "index_options": {"type": "int8_hnsw", "m": 16, "ef_construction": 100} }
```

- `dims` must match the model exactly and cannot be changed later — a model swap is a reindex (SKILL.md Core Rules 3). `elasticsearch >=8.11` raises the cap to 4096.
- `similarity`: `cosine` for normalised text embeddings (the usual case), `dot_product` when vectors are already unit-length (same ranking, less work per comparison), `l2_norm` for spatial or image features. Choosing `dot_product` with un-normalised vectors returns confidently wrong neighbours.
- `index: false` stores the vector without a graph: no `knn` search, only `script_score` brute force. Correct for small collections where exactness matters more than latency.
- `element_type: byte` for models that emit int8 directly; quarter of the storage.

## HNSW Parameters

| Parameter | Default | Raising it |
|---|---|---|
| `m` | 16 | More graph edges: better recall, more memory, slower indexing. 32 is the usual step up for high-recall needs |
| `ef_construction` | 100 | Better graph quality at build time: slower indexing, no query-time cost |
| `num_candidates` (per query) | — | More nodes explored per shard: better recall, more latency. Must be ≥ `k` and ≤ 10,000 |

`num_candidates` is the one to tune first, because it is per-request and needs no reindex. Sweep it against a recall measurement: `k: 10` with `num_candidates: 100` is a reasonable start, and the recall curve usually flattens well before 500.

## Querying

```json
{ "knn": { "field": "embedding", "query_vector": [...], "k": 10, "num_candidates": 100,
           "filter": {"term": {"tenant_id": "acme"}} },
  "_source": ["title"] }
```

- The `filter` inside `knn` is applied **during** graph traversal, so `k` results come back post-filter. A `bool.filter` outside the knn clause filters after retrieval and can return fewer than `k` — or zero — results.
- Highly selective filters degrade HNSW: the graph walk keeps hitting excluded nodes. Past roughly a 5% selectivity, Elasticsearch may fall back to brute force, which is correct but slower. For a tenant filter that always cuts to 0.1% of the index, per-tenant routing beats a filter.
- `knn` as a query clause (`elasticsearch >=8.12`) can sit inside `bool` alongside text clauses; the top-level `knn` option is the older, simpler form.
- Multiple `knn` clauses in one request are allowed and their scores sum — useful for multi-vector documents (title vector + body vector).

## Quantization

- `int8_hnsw` cuts memory to roughly a quarter of `float` with a small recall loss, and is the default for float vectors on recent versions. `bbq_hnsw` (binary quantization, `elasticsearch >=8.16`) goes far further and needs oversampling plus rescoring to recover precision.
- Quantized graphs keep the full-precision vectors on disk for rescoring; memory savings apply to the graph, which is the part that must stay resident.
- **The sizing rule that matters**: the HNSW graph should fit in off-heap memory (the OS page cache), not in the JVM heap. Rough estimate for float32: `num_vectors × dims × 4 bytes × 1.1`. One million 768-dim vectors ≈ 3.4 GB unquantized, ≈ 0.9 GB with int8. Once the graph spills to disk, query latency goes from milliseconds to hundreds of milliseconds.

## Hybrid Retrieval with RRF

Reciprocal rank fusion combines rankings without needing comparable scores:

`rrf_score(d) = Σ over retrievers of 1 / (rank_constant + rank(d))`

with `rank_constant` default 60. Because it uses **ranks**, not scores, it sidesteps the fact that BM25 scores and cosine similarities live on incomparable scales.

```json
{ "retriever": { "rrf": {
    "retrievers": [
      { "standard": { "query": { "multi_match": { "query": "wireless router", "fields": ["title^3","body"] } } } },
      { "knn": { "field": "embedding", "query_vector": [...], "k": 50, "num_candidates": 200 } } ],
    "rank_window_size": 100, "rank_constant": 60 } } }
```

- Retriever syntax is `elasticsearch >=8.14`; the earlier `rank: {rrf: {...}}` form works from 8.8.
- `rank_window_size` must be ≥ the final `size`; a document outside every retriever's window cannot be fused in.
- Lowering `rank_constant` sharpens the preference for top-ranked results from each retriever; raising it flattens the contribution across the window.
- Alternative to RRF: linear combination of normalised scores. It gives finer control and requires you to maintain the normalisation as either side's score distribution drifts. RRF is the lower-maintenance default.

## When Vectors Lose

- **Exact identifiers**: part numbers, SKUs, error codes, names. Embeddings smear them into semantic neighbourhoods, so `ERR-4471` retrieves other error codes. BM25 gets these right by construction.
- **Rare terms**: a word appearing three times in the corpus has no reliable embedding neighbourhood; IDF handles it perfectly.
- **Negation and numbers**: "not waterproof", "under 200g". Embeddings encode both sides of a negation similarly.
- **Freshness and filtering-heavy workloads**: the filter does most of the work and the vector adds latency for little gain.

Hence the default: hybrid, and drop BM25 only when an offline evaluation on real queries says it contributes nothing (an offline `_rank_eval` run against a judgement set).

## Semantic Fields and Managed Inference

- `semantic_text` (`elasticsearch >=8.15`) handles chunking, inference at index time, and query embedding automatically against a configured inference endpoint. Far less plumbing; less control over chunk boundaries and no way to reuse embeddings you already computed elsewhere.
- ELSER is a learned **sparse** model: it expands text into weighted term-like features stored in a `sparse_vector` field, queried with `text_expansion`/`sparse_vector`. It behaves like BM25 on steroids — good on exact terms, no embedding pipeline to run, and it is a licensed feature (`license_tier`).
- Both bind the index to a specific model. Record which model produced which field in the index metadata, because "why did recall drop" three months later is almost always an undocumented model change.

## Chunking (the part that decides quality)

- One vector per document fails on long documents: averaging a 5,000-word article into 768 dimensions retrieves nothing precisely. Chunk to roughly 200-500 tokens with 10-20% overlap, index chunks as `nested` sub-documents or as separate documents carrying a parent ID.
- With `nested` chunks, `inner_hits` returns the matching chunk, which is what a RAG pipeline needs to cite. Nested vectors are supported and score with `score_mode`.
- Chunk boundaries at semantic edges (headings, paragraphs) beat fixed-width windows measurably. Detailed chunking strategy belongs to the retrieval pipeline rather than the index — see the Clawic `rag-chunking` skill.

## Vector Gates

- Does `dims` match the deployed model, and is the model version recorded somewhere queryable?
- Is the filter inside the `knn` clause rather than wrapped around it?
- Does the estimated graph size fit in off-heap memory on the nodes that hold it?
- Is `num_candidates` tuned against a measured recall number rather than left at `k`?
- For hybrid: is `rank_window_size` at least the requested `size`?
- Is there a BM25 leg for exact identifiers, or a documented evaluation showing there does not need to be?
