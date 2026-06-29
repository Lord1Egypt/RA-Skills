# Semantic Memory Assurance

Use this checklist when validating dr-context-pipeline memory retrieval.

## Required Invariants
- Semantic memory search is the preferred persistent-memory retrieval path when prior memory is relevant.
- File/keyword retrieval is an allowed fallback, but it must be explicit in the normal-mode footer and debug/audit evidence.
- Embedding/vector/index health must be checked with machine-readable status before claiming semantic memory is healthy.
- Live alert delivery is a separate approval gate.

## Manual Check

```bash
python3 ./skills/dr-context-pipeline/scripts/memory_watchdog.py \
  --freshness-minutes 240 \
  --min-bytes 200 \
  --require-semantic \
  --probe-query "context pipeline embeddings semantic retrieval" \
  --min-search-results 1 \
  --emit-notification-payload
```

Expected healthy result:
- `status` is `OK`
- `semantic_required` is `true`
- semantic status shows embedding probe OK
- vector store and semantic vectors are available
- probe returns at least one result with `vectorScore`

## Failure Handling
- If status is `GAP`, do not claim the Context Pipeline is fully healthy.
- Continue with file fallback only when the user-facing task can be completed safely without semantic recall.
- In the footer, state `retrieval file_fallback` and include the reason when concise.
- For operational tasks, stop with `NOT EXECUTED: memory/embedding gap` if semantic memory is a prerequisite.

## Notification Gate
A scheduled checker may notify Daniel only after explicit approval of:
- schedule/frequency
- Discord DM target
- cooldown/suppression behavior
- exact message format
- whether failures should retry or only report once
