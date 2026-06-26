# Learning Store Layout

Use a stable on-disk layout so the pipeline can run repeatedly without turning into a junk drawer.

## Recommended structure

```text
.learnings/
|- inbox.jsonl        # raw captured items
|- scored.jsonl       # normalized and scored items
|- merge.json         # duplicate and merge groups
|- patches.json       # candidate patches for review
|- apply-report.json  # last apply report
`- archive/
   `- YYYY-MM-DD-inbox.jsonl
```

## File roles

### inbox.jsonl
Append-only raw capture store. Do not hand-edit unless you have to.

### scored.jsonl
Output of `score_learnings.py`. Same items, but with filled confidence, reuse, scope, and targets.

### merge.json
Output of `merge_candidates.py`. Use it to inspect likely duplicates before promotion.

### patches.json
Output of `draft_patches.py`. This is the review surface. Human approval happens here.

### apply-report.json
Output of `apply_approved_patches.py`. Use it as an audit trail.

### archive/
Move consumed inbox batches here once they are scored and reviewed.

## Recommended loop

1. capture into `inbox.jsonl`
2. score into `scored.jsonl`
3. review dedup with `merge.json`
4. generate `patches.json`
5. approve or reject with `review_patches.py`
6. apply approved patches
7. archive processed batch
