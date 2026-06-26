# Tag Taxonomy

Use this reference when assigning tags or revising the taxonomy after every 50 papers.

## Starter taxonomy

Start with a compact reusable set. Expand only after repeated demand.

### `tags_topic`

- `llm`
- `multimodal`
- `agent`
- `retrieval`
- `alignment`
- `reasoning`
- `evaluation`
- `efficiency`
- `data`
- `security`

### `tags_method`

- `rag`
- `finetuning`
- `rl`
- `distillation`
- `pretraining`
- `synthetic-data`
- `moe`
- `benchmark`
- `tool-use`
- `search`

### `tags_task`

- `qa`
- `code-gen`
- `summarization`
- `translation`
- `information-extraction`
- `math`
- `planning`
- `classification`
- `generation`
- `grounding`

### `tags_domain`

- `general`
- `biology`
- `medicine`
- `finance`
- `education`
- `legal`
- `robotics`
- `software-engineering`

### `tags_stage`

- `reading`
- `important`
- `worth-reproducing`
- `survey-only`
- `to-discuss`

## Tag assignment rules

Assign at most:

- 2 topic tags
- 3 method tags
- 2 task tags
- 2 domain tags
- 2 stage tags

Fewer tags are better than noisy tags.

## Synonym policy

Map synonyms to a canonical visible tag.

Examples:

- `instruction-tuning` -> `finetuning`
- `retrieval-augmented-generation` -> `rag`
- `eval` -> `evaluation`
- `coding` -> `code-gen`

Store synonym mappings in code or configuration, but keep only canonical labels in the table.

## 50-row review checklist

Run this when total rows hit `50`, `100`, `150`, and so on.

1. Count tag frequency by dimension.
2. Mark tags with fewer than 3 uses as sparse candidates.
3. Detect synonyms and spelling variants.
4. Detect overloaded tags that mean multiple things.
5. Merge or rename low-value tags.
6. Split overloaded tags only when the split will improve actual retrieval.
7. Publish a new taxonomy version.
8. Backfill old rows with the new mapping.

## Taxonomy revision heuristics

Prefer merges when:

- two tags are frequently co-assigned
- users would search them as the same concept
- one tag is just a longer spelling of another

Prefer splits when:

- one tag spans clearly different retrieval intents
- the tag appears on more than 20 percent of rows
- the split aligns with an actual browsing workflow

## Change log format

When a taxonomy review runs, produce a short change log like:

| Change type | Before | After | Reason |
| --- | --- | --- | --- |
| merge | `instruction-tuning` | `finetuning` | synonym consolidation |
| split | `evaluation` | `benchmark`, `safety-eval` | overloaded tag |
| rename | `coding` | `code-gen` | canonical naming |
