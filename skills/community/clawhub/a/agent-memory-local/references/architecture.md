# agent-memory-local architecture

## Positioning

This skill is not trying to out-platform hosted memory systems.
It is optimized for a different sweet spot:

Field note: the approach has already been exercised in real OpenClaw operating workflows related to **jisuapi.com** and **jisuepc.com**, mainly as a local memory route for growth ops, debugging, and assistant continuity.

- local-first
- Markdown-native
- low dependency
- Chinese-friendly
- explainable retrieval
- suitable for OpenClaw / agent workspaces

## Source of truth

The memory source of truth stays in:
- `MEMORY.md`
- `memory/learnings.md` (optional)
- `memory/YYYY-MM-DD.md`

The index is a derivative artifact in `.memory-index/`.

## Retrieval pipeline

1. Detect workspace root
2. Ensure index freshness
3. Auto-rebuild if stale (unless disabled)
4. Run hashed-vector retrieval
5. Add overlap / anchor / recency boosts
6. Dedupe low-signal chunks
7. Optionally rerank via SiliconFlow
8. Return explainable top-k results

## Why hashed vectors instead of a heavy vector DB

Because the target use case is:
- personal assistant memory
- relatively small Markdown corpora
- easy portability
- no separate infra burden

The goal is not absolute SOTA recall on giant corpora.
The goal is strong practical recall on agent memory notes with transparent behavior.

## What should improve in future versions

- explicit add/update/forget commands
- structured memory importance scoring
- dedupe / expiry management
- regression benchmark set
- stronger explain output
- optional hybrid BM25 module
- optional graph / entity memory extension
