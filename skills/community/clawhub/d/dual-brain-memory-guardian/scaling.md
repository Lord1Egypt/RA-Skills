# Scaling Patterns (Dual-Brain)

## Volume Thresholds

| Scale | Rule Entries in Markdown | Episodic Events in Pinecone | Strategy |
|-------|--------------------------|-----------------------------|----------|
| Small | <100 | <10k | Keep HOT/WARM compact, basic DEEP recall |
| Medium | 100-500 | 10k-500k | Add strict namespace hygiene and metadata filters |
| Large | 500-2000 | 500k-10M | Strong digest pipeline, selective Markdown promotion |
| Massive | >2000 | >10M | Import-based ingestion and aggressive summary-only HOT |

## Tier Split

- HOT (Markdown): global contracts only.
- WARM (Markdown): project/domain constraints.
- DEEP (Pinecone): full correction/reflection/episodic history.

## When to Split Markdown Namespaces

Create or split namespace files when:

- Single file exceeds 200 lines.
- One topic has 10+ distinct confirmed rules.
- User explicitly separates contexts (work/project/client).

## Pinecone Data Growth Strategy

- Keep one namespace per tenant (`dualbrain-<tenant>`).
- Use structured IDs for traceability (`tenant#event#timestamp#id`).
- Keep metadata filterable and compact.
- Avoid high-cardinality ID-list filters.

## Ingestion Strategy by Size

- Day-to-day events: `upsertRecords` with text.
- Large historical backfill: `startImport` with Parquet vectors.
- Prefer import for very large datasets to control cost and throughput.

## Markdown Compaction Rules

- Do not delete confirmed rules.
- Merge semantically duplicate rules.
- Replace verbose narratives with concise contracts.
- Keep one clear rule per bullet when possible.

## DEEP Digest Rules

- Raw vector episodes are not destructively compacted.
- Heartbeat performs periodic digest from DEEP memory.
- Promote only repeated and validated findings to HOT/WARM Markdown.

## Conflict Detection

When loading context:

1. Build Markdown inheritance chain: global -> domain -> project.
2. Resolve conflicts in Markdown first (most specific wins).
3. Use Pinecone as advisory context only.

## Recovery Patterns

### Context Lost

1. Reload HOT (`memory.md`).
2. Reload relevant WARM files from index.
3. Re-run DEEP semantic recall for current task.

### Rule Corruption

1. Rebuild local rule candidates from recent DEEP digest.
2. Ask user to reconfirm critical contracts.
3. Restore with minimal edits and clear timestamps.

## Performance Notes

- Keep Top-K low for online execution (3-5).
- Increase Top-K only during weekly digest or audits.
- Avoid unnecessary fields in search response to reduce latency.
