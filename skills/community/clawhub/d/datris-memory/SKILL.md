---
name: datris-memory
description: Use the Datris Platform as a long-term semantic memory layer through the Datris MCP server. Local markdown memory files (MEMORY.md, memory/*.md) stay canonical; Datris is the retrieval index built from them. Use this skill any time the user mentions saving, recalling, ingesting, syncing, or searching memory through Datris — and any time they ask a memory-shaped question ("what did I note about X", "find anything related to Y", "summarize what I've written down about Z") even when they don't explicitly say "Datris." Trigger on any work involving long-term memory ingestion, retrieval, or sync.
---

# Datris memory layer

Datris is the long-term semantic memory layer. Local memory files are the source of truth. Datris is rebuilt from them — never the other way around.

## Rules

- Prefer Datris MCP tools over shell or CLI for memory operations.
- **One file in = one `upload_data` call.** Never concatenate, bundle, or consolidate multiple memory files into a single corpus upload. Each file's name is its provenance — it must round-trip cleanly into Datris and back out in retrieval results. Bundling looks like an optimization and is not one: it permanently breaks provenance, blocks per-file incremental sync, and makes resets harder.
- **Source filenames preserve the full relative path.** Use `MEMORY.md` and `memory/2026-05-06.md` as source filenames — the directory prefix is part of the provenance and must round-trip into retrieval results. Some Datris builds reject path separators at the temp-file staging layer; if uploads fail on slashes, encode the separator reversibly (e.g., `memory__2026-05-06.md`) and tell the user what encoding was applied. Never silently flatten to a basename — that strips the directory and creates ambiguity if two memory subdirectories ever contain files with the same name.
- Upload each file as-is. Let Datris chunk server-side. Do not pre-chunk. Do not use a document tap for local files. The only time to split a single file is when that one file genuinely exceeds the upload limit; in that case, split it with explicit provenance markers in the chunk filenames (e.g. `MEMORY.md.part1`, `MEMORY.md.part2`).
- **Run uploads concurrently across files.** Each `upload_data` call returns a job token immediately — collect all the tokens first, then poll. Use a bounded concurrency limit (8–16 parallel uploads is safe for most Datris builds) rather than unbounded fan-out. On bootstrap, where there are no pre-existing chunks to remove, this is straight parallelism.
- **Re-uploads are delete-then-upload, serialized per file.** When re-ingesting a file that already exists in the pipeline, delete its existing chunks first, wait for the delete to complete, then upload. Do not rely on upsert behavior — some Datris builds append duplicates rather than overwriting on filename collision, and a delete-then-upload pair is build-agnostic and idempotent. Within a single file, delete→upload is serial. Across files, multiple delete→upload pairs run concurrently up to the same bounded limit.
- Poll job status to completion before claiming any ingestion succeeded. Polling is for verification across the batch, not for gating cross-file uploads.
- Verify retrieval with a semantic search after every ingestion run.
- Memory pipelines must target a vector destination (pgvector, Qdrant, Weaviate, Milvus, or Chroma).
- The embedding model is pinned at pipeline-creation time. Vector dimensions cannot change after the fact. Confirm the embedder matches the pipeline before ingesting. Switching embedders means dropping and recreating the destination collection.
- **Place every created resource in the `openclaw` data catalog by default.** Pipelines, taps, secrets, destination collections — anything the agent creates in Datris on OpenClaw's behalf goes in the catalog named `openclaw` unless the user explicitly directs otherwise. This keeps OpenClaw's footprint cleanly separated from other Datris workloads on the same instance, makes cleanup and auditing trivial, and lets multiple OpenClaw users share an instance without colliding. If an existing resource the agent wants to reuse lives in a different catalog, do not migrate it silently — surface the mismatch to the user and ask before continuing.
- **Return to prescribed concurrency after debugging.** When isolating a failure — a Datris bug, a tool returning unexpected output, a transient error — it is reasonable to drop temporarily to single-file sequential operations to get a clean signal. Once the issue is identified and resolved, return to the concurrency model in the rules above before processing the rest of the batch. Do not carry a debug-mode sequential pattern into subsequent ingestion or sync runs. Note in the audit log when this happens, including the reason and what was done.

## First-run bootstrap

1. Read the Datris MCP resources and tool descriptions. Understand the pipeline, upload, job-status, and search workflows before acting.
2. Check service health.
3. Reuse an existing vector pipeline for memory in the `openclaw` catalog if one exists. Otherwise create one in the `openclaw` catalog — pgvector is fine. If a memory pipeline exists outside the `openclaw` catalog, surface that to the user before reusing or migrating it.
4. Ingest `MEMORY.md` and each `memory/*.md` file via its own `upload_data` call — one upload per file, no exceptions. Do not concatenate them into a single corpus document, even if the total set is small. Fire the uploads in parallel and collect all the job tokens before polling.
5. Poll all jobs concurrently until every one reports completion.
6. Verify with two or three representative semantic queries. Confirm both that (a) the expected content comes back, and (b) results show real source filenames (`MEMORY.md`, `memory/2026-05-06.md`, etc.) — not a consolidated corpus filename or any other synthetic name. The filename round-trip check is the early-warning signal that the one-file-per-upload rule is being followed; if results show a corpus filename, stop and apply the remediation workflow below.
7. Record the run in `memory/<today>.md`: pipeline used, files ingested, verification queries and results, any failures.
8. Propose an incremental sync strategy for future edits.

## Ongoing sync

Memory files change continuously — the agent writes to them during sessions, the user edits them in their editor between sessions, and new dated files appear over time. Sync is incremental and runs lazily, in three modes:

### When to sync

1. **Periodic background sync.** A timer-driven sweep runs every 30 minutes by default — diff memory files by `mtime` against the last sync record, upload anything stale. This runs out-of-band: it never blocks an agent response or a user query. Cadence is configurable: faster (5–10 min) for users actively editing memory between sessions, slower (hourly or more) for read-mostly use. The right value is whatever keeps the staleness window short enough that the user rarely needs to force a sync.

2. **End of any agent response that wrote to memory.** When the agent edits or creates a memory file during a turn, flush those uploads before the response is considered complete — including polling to completion. This puts the cost on the response that did the writing, not on later queries, and guarantees that a follow-up question in the same conversation can retrieve what the agent just wrote. Never let an agent-authored memory write wait for the next timer tick.

3. **On explicit user request.** Phrases like "sync memory," "save what we discussed," "update Datris with my recent notes" — full diff sweep across all memory files, immediate sync. This is the user's escape valve for the case where they just edited a file in their editor and want it queryable right now rather than waiting for the next timer tick.

### Staleness window — and why it's acceptable

Memory edits made outside of an agent session — for example, the user editing `MEMORY.md` in their editor between conversations — may be up to one timer interval behind in retrieval results. That is the explicit trade. Query latency stays predictable, ingestion is invisible, and the user has a one-line escape hatch ("sync memory") when freshness matters. Do not try to close the staleness window by syncing on every retrieval; that path puts ingestion cost on the user's wait time and is the design this skill replaces.

### Detecting what changed

Compare each memory file's filesystem `mtime` against the most recent sync timestamp recorded for that file in the `memory/<date>.md` audit logs. Three cases:

- **No sync record exists** → treat as a new file, ingest it.
- **`mtime` newer than last-sync timestamp** → re-upload.
- **`mtime` unchanged** → skip. Do not re-ingest unchanged files; the point of incremental sync is to do less work.

A content hash is more reliable than `mtime` if the user touches files without editing them (some editors do this on save), but `mtime` is sufficient as a default. Switch to hashing only if redundant uploads start showing up in the audit log.

### Sync workflow

Classify each changed file into one of four cases and act accordingly:

- **Edited file** → delete existing chunks for that source filename, wait for the delete to complete, then upload via `upload_data`. Per-file serial; multiple files' delete→upload pairs run concurrently.
- **New file** (no prior sync record) → upload via `upload_data` directly. No delete step needed since there are no existing chunks for this filename.
- **Renamed file** → delete chunks for the old filename, then upload the new file. Same per-file serialization as edits, same cross-file concurrency.
- **Deleted file** → delete its chunks from the destination collection. Do not leave orphans.

Then:

- Wait for all jobs to complete, polling concurrently.
- Verify with one or two semantic queries that touch the changed content. Confirm filenames in results reflect the post-sync state — no stale entries from before a rename or delete, no consolidated-corpus names, no duplicate chunks (same content under the same filename appearing more than once would indicate the delete step was skipped).
- Append a per-file entry to today's audit log: filename, change type (edit / new / rename / delete), timestamp, verification result.

## Inheriting a consolidated-corpus pipeline

If the existing memory pipeline was bootstrapped with a single consolidated upload (a `*-corpus-*.md` source file, or any upload whose filename doesn't match a real memory file), the pipeline has broken provenance and cannot be incrementally synced cleanly. Do not patch around it. Reset and re-ingest:

1. Confirm with the user before resetting — destination collections may contain manual edits.
2. Drop the destination collection (or recreate the pipeline with the same name).
3. Re-ingest each canonical memory file individually per the bootstrap workflow above.
4. Verify with semantic queries that retrieval results now show real source filenames (`MEMORY.md`, `memory/2026-05-06.md`, etc.) rather than a corpus filename.

## Retrieval

When the user asks a memory-shaped question, reach for `vector_search` (or `ai_answer` for synthesis) against the memory pipeline before grepping local files. Substring search on local markdown is a fallback, not the default.

## Reporting

After any bootstrap or sync, report:

- Pipeline used or created.
- Files ingested.
- Verification queries and whether they returned the expected content.
- Anything that failed and why.
