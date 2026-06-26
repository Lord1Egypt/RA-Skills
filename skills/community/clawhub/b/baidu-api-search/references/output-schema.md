# Output Schema

Use this reference before changing output files.

## Run Directory

Recommended web research shape:

```text
runs/<topic-or-run-id>/
├── query_plan.json
├── raw_results.jsonl
├── errors.jsonl
├── run_summary.json
├── deduped_sources.json
├── adaptive_trace.json
└── research_pack.md
```

Recommended lookup shape:

```text
runs/<topic-or-run-id>/
├── baike_candidates.json
├── baike_content.json
├── fallback_web_results.json
├── errors.jsonl
├── run_summary.json
└── lookup_pack.md
```

## query_plan.json

```json
{
  "topic": "新能源汽车 口碑",
  "mode": "normal",
  "profile": "product",
  "max_queries": 10,
  "queries": [
    {
      "query": "新能源汽车 口碑 评测",
      "intent": "review",
      "source": "template",
      "reason": "reviews and evaluations"
    }
  ]
}
```

## raw_results.jsonl

One search result reference per line:

```json
{
  "topic": "新能源汽车 口碑",
  "mode": "normal",
  "query": "新能源汽车 口碑 评测",
  "query_intent": "review",
  "query_source": "template",
  "rank": 1,
  "title": "...",
  "url": "...",
  "snippet": "...",
  "content": "...",
  "website": "...",
  "date": "...",
  "rerank_score": 0.0,
  "authority_score": 0.0,
  "key_id": "sha256-prefix"
}
```

Never write the full API key. `key_id` is a hash prefix only.

## deduped_sources.json

```json
{
  "summary": {
    "raw_count": 100,
    "deduped_count": 63,
    "duplicate_count": 37,
    "domain_count": 28
  },
  "sources": [
    {
      "source_id": "src_0001",
      "title": "...",
      "url": "...",
      "canonical_url": "...",
      "domain": "...",
      "snippet": "...",
      "best_rank": 1,
      "matched_queries": ["新能源汽车 口碑", "新能源汽车 口碑 评测"],
      "matched_intents": ["overview", "review"],
      "matched_stages": ["seed"],
      "matched_query_sources": ["template"],
      "duplicate_count": 2,
      "quality_flags": []
    }
  ],
  "duplicates": [
    {
      "kept_source_id": "src_0001",
      "reason": "duplicate_url",
      "query": "新能源汽车 口碑 评测",
      "rank": 3,
      "url": "..."
    }
  ]
}
```

## research_pack.md

A compact Markdown pack for downstream AI analysis. It should include:

```text
search coverage
coverage decision and recommended next steps
query plan
major domains
intent coverage
selected sources
duplicate note
limitations
```

Agents should cite `source_id` plus URL or domain for factual claims derived from selected sources. The pack is a source pack, not a license to make uncited assertions.

## adaptive_trace.json

Written by `adaptive_search.py`:

```json
{
  "summary": {
      "query_count": 3,
      "raw_result_count": 60,
      "deduped_count": 44,
      "error_count": 0,
      "cache_hit_count": 0,
      "cache_enabled": true,
      "cache_dir": "cache/web_search",
      "cache_ttl": 86400,
      "required_intents": ["official", "overview", "platform", "review"],
      "attempted_intents": ["official", "overview", "platform", "review"],
      "missing_required_intents": [],
      "stop_reason": "low_unique_yield"
  },
  "trace": [
    {
      "query": "新能源汽车 口碑 评测",
      "intent": "review",
      "stage": "seed",
      "reference_count": 20,
      "new_unique_count": 18,
      "unique_yield": 0.9,
      "cache_hit": false
    }
  ]
}
```

## lookup run_summary.json

Written by `lookup.py`:

```json
{
  "topic": "量子计算",
  "mode": "lookup",
  "candidate_count": 5,
  "content_count": 1,
  "fallback_search_used": false,
  "fallback_result_count": 0,
  "error_count": 0,
  "cache_hit_count": 0,
  "cache_enabled": true,
  "cache_dir": "cache/baike",
  "cache_ttl": 86400,
  "lookup_pack": "runs/.../lookup_pack.md"
}
```

## lookup_pack.md

A compact Markdown pack for entity lookup. It should include:

```text
summary
Baike candidates
Baike content
optional fallback web results
limitations
```

Agents should cite the Baike lemma URL or lemma ID for factual claims from lookup output.
