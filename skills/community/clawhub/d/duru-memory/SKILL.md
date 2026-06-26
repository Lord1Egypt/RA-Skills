---
name: duru-memory
description: Markdown-based memory continuity system for agents using local Markdown files as the primary memory source. Use when building or operating local Markdown memory files (daily logs, project memory, handoff notes), maintaining current-state records, running session start/close memory protocols, and pairing a structured Markdown workflow with OpenClaw's built-in memory tools.
---

# Duru Memory

Use this skill to run a high-traceability memory system based on plain Markdown files.

This skill is complementary to OpenClaw's built-in memory stack:
- `duru-memory` manages the Markdown files, conventions, and maintenance workflow
- built-in `memory_search` and `memory_get` are the primary recall/read tools during normal assistant operation
- `memory-core` indexes and retrieves from the same Markdown tree
- `active-memory` is an optional pre-reply recall layer for eligible interactive sessions, not a guaranteed default for every deployment

Treat the Markdown files as the source of truth, and OpenClaw's built-in memory stack as the main retrieval and recall layer.

## Core workflow

1. Load `memory/CORE/hard-rules.md` and `memory/CORE/current-state.md`.
2. Load recent daily logs from `memory/daily/` (default: last 2 days).
3. Before answering context-dependent questions, prefer built-in `memory_search` first.
4. Use `scripts/memory-search.sh "<query>"` when you want explicit file-level control, debugging, maintenance, or a second opinion against built-in recall.
5. Update `current-state.md` when project/task state changes.
6. Append a state diff entry in `state-changelog.md` for every meaningful state update.
7. At session close, run `scripts/session-close.sh`.

## Directory contract

```text
memory/
  CORE/
    hard-rules.md
    current-state.md
    state-changelog.md
  daily/
  projects/
  people/
  concepts/
  handoff/
  archive/raw/
  INDEX.md
```

## Memory admission rules

Record only high-value memory:

- decisions
- commitments
- deadlines
- preferences
- blockers
- postmortem conclusions

Add attributes when possible:
- `status: active | superseded | invalid`
- `polarity: positive | negative`
- `confidence: high | medium | low`
- `avoid_reason: ...` (required for negative/pitfall entries)

Avoid logging casual chat unless it impacts future execution.

## Retrieval policy (built-in first, local deterministic second, optional semantic third)

For normal assistant recall, built-in `memory_search` is the default path. It integrates with `memory-core`, can include indexed session transcripts, and follows the configured OpenClaw memory backend.

Use this skill's local retrieval scripts when you want explicit file-level control, debugging, maintenance, reproducible inspections, or a second opinion against built-in recall.

Local deterministic retrieval uses weighted matching:

- exact keyword / phrase in headings
- tags and fields (`decision`, `todo`, `blocker`, `preference`)
- recency boost for recent daily logs
- path boost for likely directories (`projects`, `people`, `CORE`)

Optional local semantic retrieval is an experimental supplement, not the primary OpenClaw memory path. When local Ollama embedding is available, it can be added as a second pass after deterministic retrieval (default embedding model in `config.yaml`: `qwen3-embedding:0.6b`). This local semantic layer can coexist with built-in retrieval, but it does not replace OpenClaw's built-in `memory_search` contract.

This skill's semantic mode uses a local SQLite + sqlite-vec path with incremental indexing:
- DB path: `memory/.semantic-index.db`
- Vector extension: `sqlite-vec` (loaded via APSW)
- Incremental policy: file mtime/size/hash detection + chunk-level embedding cache
- Consistency keys: fixed `model`, embedding `dimension`, and `pipeline_version`
- Threshold: `SEMANTIC_MIN_SCORE` (default `0.48`)
- Fusion rerank mode: `FUSION_MODE=rrf|linear` (default `rrf`)
- RRF parameter: `RRF_K` (default `60`)
- Keyword boost in RRF mode: `KEYWORD_BOOST` (default `0.006`)
- Linear fallback weights: `FUSION_SEM_WEIGHT` + `FUSION_KEY_WEIGHT` (defaults `0.65/0.35`)
- Daily warmup: `session-start.sh` runs `memory-semantic-search.py --build-only` once per day
- Negative memory handling: entries with `polarity=negative` or `status in {invalid,superseded}` are excluded from positive ranking and surfaced in a dedicated `⚠ Avoided Pitfalls` warning block

## Failure and degraded mode guidance

Do not assume semantic retrieval is available.

If built-in vector search, sqlite-vec, Ollama embeddings, or the skill's local semantic service is unavailable, fall back to built-in `memory_search` in its degraded lexical mode or to this skill's deterministic local retrieval. In degraded mode:

- prefer exact facts from `MEMORY.md`, `memory/CORE/current-state.md`, and recent daily logs
- treat semantic hits as optional enrichment, not a dependency
- explicitly report uncertainty when no strong hit exists
- avoid presenting local semantic indexing behavior as part of OpenClaw's guaranteed built-in memory contract

## Coexistence guidance

Recommended division of labor:
- Write and maintain long-term notes in `MEMORY.md` and `memory/*.md`
- Keep `memory/CORE/current-state.md` as the execution truth for active work
- Let OpenClaw `memory-core` index the same tree
- Treat built-in `memory_search` and `memory_get` as the default runtime recall path
- Consider `active-memory` optional and deployment-dependent, especially if pre-reply recall causes latency or timeout issues
- Use local scripts for maintenance, audits, tagging, and deterministic investigations

Avoid creating separate parallel memory trees for built-in memory and Markdown memory. One shared Markdown tree is the cleanest setup.

## Scripts

- `scripts/session-start.sh`: startup checklist + quick context load hints
- `scripts/memory-search.sh`: hybrid retrieval entry (keyword first, semantic optional)
- `config.yaml`: centralized model/runtime tuning (`ollama.base_url`, `models.*`, `semantic.*`, `fusion.*`)
- `scripts/memory-semantic-search.py`: semantic recall via Ollama `/api/embeddings`
- `scripts/memory-auto-tag.py`: local-model auto-tagger (model from `config.yaml`, default `gemma4:e4b`) for incremental memory changes (`--mode tag|review`, `--files`, `--force`)
- `scripts/memory-write-tag.sh`: write/append helper that immediately tags the target file
- `scripts/memory-compact.py`: weekly compaction (daily -> summaries, mark stale, re-sync vectors)
- `scripts/memory-forget.py`: monthly forgetting (archive old stale daily logs, keep negative pitfalls)
- `scripts/session-close.sh`: runs auto-tagger in `--mode review` first, then daily log append + state freshness check
- `scripts/auto-commit.sh`: optional git safety-net commit

## References

- `references/templates.md`: canonical templates for state/daily/project/handoff files
