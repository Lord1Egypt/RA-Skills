# Review Report

> READ-ONLY ANALYSIS ONLY
> DirStat_Skill never changes files automatically. It only explains what a human should review.

- root: `examples/sample-data`
- total_findings: 3
- configured_dominant_percent: `0.8`

## How To Read This

- Start from `dominant space` to see where the volume is concentrated.
- Use `path safety` and `protected huge hotspots` to understand sensitive areas.
- Treat `probable duplicates` as a strong suspicion, not as byte-level proof.
- Treat `nearby references` as contextual evidence, not as certainty of active use.

## Dominant Space

Shows the paths that explain most space under the configured dominant-space threshold.

- none

## Path Safety

Shows paths whose location changes their risk posture even before deeper inspection.

- none

## Nearby References

Shows paths with local evidence pointing to nearby configs, manifests, or workflow references.

- none

## Signature Heuristics

Shows paths matched by obvious signatures such as cache, temp, trash, or incomplete-download patterns.

### `examples/sample-data/downloads/pack.bin.part`

- size_bytes: `901120`
- size_human: `880.0 KB`
- attention_level: `review first`
- review_reason: incomplete download pattern surfaced by the dominant-space walk
- evidence: matched partial-download suffix
- confidence: `high`
- selection_source: `dominant_leaf`

## Probable Duplicates

Shows large assets that look duplicated by basename, size, and extension across different directories.

### `examples/sample-data/backup/models/model.gguf`

- size_bytes: `102400`
- size_human: `100.0 KB`
- attention_level: `review carefully`
- review_reason: large asset appears structurally duplicated across different directories
- evidence: same basename and same size across 2 directories
- confidence: `medium`
- group_key: `duplicate:model.gguf:102400`
- selection_source: `duplicate_cluster`

### `examples/sample-data/models/model.gguf`

- size_bytes: `102400`
- size_human: `100.0 KB`
- attention_level: `review carefully`
- review_reason: large asset appears structurally duplicated across different directories
- evidence: same basename and same size across 2 directories
- confidence: `medium`
- group_key: `duplicate:model.gguf:102400`
- selection_source: `duplicate_cluster`

## Protected Huge Hotspots

Shows very large protected areas that matter for visibility but should stay handled carefully.

- none

## Limits

- `probable duplicates` uses fast structural signals by default, not full-content hashing.
- `protected huge hotspots` are visibility findings, not an invitation to act blindly.
- low-confidence findings still need human judgment.
