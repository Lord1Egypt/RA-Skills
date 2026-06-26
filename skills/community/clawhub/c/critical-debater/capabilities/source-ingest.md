# Capability: Source Ingest

## Purpose

Search the web for evidence related to a debate topic, normalize results to EvidenceItem format, and populate the evidence store.

## Inputs

| Parameter | Required | Default | Description |
|---|---|---|---|
| workspace_dir | Yes | - | Path to debate workspace |
| topic | Yes | - | Debate topic text |
| mode | No | broad | broad (initial) / focused (per-round) |
| round | No | 0 | Current round number |
| search_focus | No | null | Judge-driven focus areas (for focused mode) |
| depth | No | standard | Controls number of queries: quick=3, standard=5, deep=8 |

## Execution Steps

### 1. Generate Search Queries

Use LLM to generate diverse search queries based on:
- **Broad mode (round=0)**: Cover multiple angles of the topic — supporting, opposing, neutral, historical, statistical
- **Focused mode (round>0)**: Target gaps identified by judge — mandatory_response_points, contested claims, weak evidence areas

Query diversity requirements:
- At least 1 query per major perspective (pro, con, neutral)
- Include domain-specific sources where relevant
- Include temporal queries for time-sensitive topics ("latest", "2026", "recent")

### 2. Execute Searches

For each query:
1. `search(query)` → collect result URLs and snippets
2. For top results: `fetch(url)` → extract full content
3. If fetch fails on JS-heavy page: retry once, then skip with `fetch_skipped` note

### 3. Normalize to EvidenceItem

For each source found, construct an EvidenceItem:
1. Generate `evidence_id`: "evi_" + first 8 chars of SHA-256 hash of snippet
   - Use `scripts/hash-snippet.sh` for hashing
   - Fallback: first 8 chars of URL if hash fails
2. Classify `source_type`: web / twitter / academic / government / other
3. Assign `credibility_tier` using LLM judgment:
   - tier1_authoritative: Government, central banks, AP, Reuters
   - tier2_reputable: Major newspapers, research institutions, peer-reviewed
   - tier3_general: Blogs, smaller publications, industry reports
   - tier4_social: Twitter/X, Reddit, forums
4. Set `evidence_track` using LLM:
   - "fact": Concrete data, current-state claims, statistics
   - "reasoning": Mechanisms, causal explanations, historical patterns
5. For Twitter sources: set `social_credibility_flag` via LLM pre-screening for fake news patterns
   - `verification_priority`: likely_unreliable → high, needs_verification → medium, otherwise low
6. Tag discovery metadata:
   - `discovered_by`: "orchestrator" (this capability) or "pro"/"con" (when called from debate-turn)
   - `discovered_at_round`: current round number
   - `search_context`: "initial_broad" or "judge_feedback_round_N" or "pro_supplement"/"con_supplement"

### 4. Deduplicate

Before adding to evidence_store:
- Check existing entries by `url` + `hash`
- Skip exact duplicates
- If same URL but different snippet: keep both (different excerpts from same source)

### 5. Write Evidence Store

Append new items to `evidence/evidence_store.json`.

### 6. Audit Log

Log via `scripts/append-audit.sh`:
```json
{"timestamp":"...","action":"evidence_added","details":{"round":0,"mode":"broad","items_added":N,"total_items":M}}
```

## Completion Marker

Output `DONE:source_ingest` when complete.
