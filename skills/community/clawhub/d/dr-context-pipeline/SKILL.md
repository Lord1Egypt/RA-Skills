---
name: dr-context-pipeline
description: "Deterministic memory/context pipeline with semantic retrieval checks, compression/lint, safe fallback, and memory watchdog."
---

# DR Context Pipeline

Use this skill to standardize how an agent loads memory into its prompt for correctness.

## Prerequisites
- A file-based memory layout with `memory/always_on.md` and topic files under `memory/topics/`.
- Recommended: install `dr-memory-foundation` or an equivalent memory layout.
- For semantic retrieval assurance, OpenClaw memory search should be configured and visible through `openclaw memory status --deep --json`.

## Quick Install
These commands work from anywhere because they set `WORKSPACE`:

```bash
export WORKSPACE=${WORKSPACE:-~/.openclaw/workspace}
cd "$WORKSPACE"
clawhub install dr-context-pipeline --version 2.1.1 --dir skills --force
python3 ./skills/dr-context-pipeline/scripts/install_pipeline.py --target "$WORKSPACE/context_pipeline"
ls -1 "$WORKSPACE/context_pipeline"
git -C "$WORKSPACE" diff -U20 AGENTS.md | cat
python3 ./skills/dr-context-pipeline/scripts/validate_pipeline.py --context-root "$WORKSPACE/context_pipeline"
python3 ./skills/dr-context-pipeline/scripts/memory_watchdog.py --freshness-minutes 240 --min-bytes 200 --require-semantic --probe-query "context pipeline embeddings semantic retrieval" --min-search-results 1
git -C "$WORKSPACE" status -sb context_pipeline AGENTS.md
echo "CONTEXT PIPELINE APPLY COMPLETE"
```

Paste every command's output. If any step fails or the watchdog reports `GAP`, stop and reply `NOT EXECUTED: <reason>`.

## Apply To This Workspace
When the user asks to apply this skill, follow this order:

1. Lay down the files:
   `python3 ./skills/dr-context-pipeline/scripts/install_pipeline.py --target context_pipeline`
2. Show the tree:
   `ls -1 context_pipeline`
3. Patch `AGENTS.md` with the Context Pipeline instructions, preserving unrelated content.
4. Validate:
   `python3 ./skills/dr-context-pipeline/scripts/validate_pipeline.py --context-root context_pipeline`
5. Run the semantic memory watchdog:
   `python3 ./skills/dr-context-pipeline/scripts/memory_watchdog.py --freshness-minutes 240 --min-bytes 200 --require-semantic --probe-query "context pipeline embeddings semantic retrieval" --min-search-results 1`
6. Show final state:
   `git status -sb context_pipeline AGENTS.md`
7. Print the success banner:
   `echo "CONTEXT PIPELINE APPLY COMPLETE"`

This flow must be idempotent. If validation or the watchdog fails, stop with `NOT EXECUTED` and quote the issue.

## Memory Commit / Continue Workflow
- When Daniel says "memorize this" or similar, run `references/MEMORY_COMMIT.md`.
- When he says "let's continue" after a reset, reload `memory/now.md`, `memory/open-loops.md`, and the relevant topic files before acting.

## Trigger Gate

Every task loads the small always-on policy. The **full** context pipeline is
required only when one or more of these are true:

- persistent memory or a prior decision is materially relevant;
- the work is complex, risky, production-facing, or otherwise depends on
  historical context for correctness;
- the user explicitly asks for debug, audit, tracing, receipts, or an evidence
  dump.

For a routine, self-contained task where persistent memory is not needed:

- record retrieval mode as `not_needed`;
- answer or act directly;
- do not require a Retrieval Bundle, Context Pack, lint, artifact persistence,
  or a pipeline-specific footer;
- do not block the task because memory tooling is unavailable.

If the agent is unsure whether history materially affects the result, retrieve
the smallest relevant context. If needed history is unavailable, use fresh
read-only evidence or ask one targeted question. Stop the affected action only
when its correctness genuinely depends on that missing historical state.

## Runtime Modes
Apply `references/RUNTIME_CHECKLIST.md` when the full pipeline is triggered.

Modes:
- `normal` - compact day-to-day operation
- `debug` - full Retrieval Bundle and Context Pack artifacts
- `audit` - debug artifacts plus Receipt Ledger

Default to `normal` unless the user explicitly asks for debug, audit, tracing, receipts, or a full evidence dump.

## Semantic Memory Contract
When persistent memory is relevant, semantic or hybrid memory search is the preferred retrieval source.

The agent must record retrieval mode internally as one of:
- `semantic`
- `hybrid`
- `file_fallback`
- `not_needed`

If semantic memory is unavailable, not attempted, or degraded to file/keyword retrieval:
- use file/keyword fallback when it is sufficient;
- in normal mode, mention the limitation only when it materially affects the result;
- in debug/audit mode, include the reason;
- stop only an operational check whose correctness specifically depends on
  semantic recall, with `NOT EXECUTED: memory/embedding gap`.

Normal footer shape:

```text
Context: task type <type>; snippets <ids>; retrieval <semantic|hybrid|file_fallback|not_needed>; compression <succeeded|fallback>.
```

## Notification Safety
The watchdog can emit a dry-run notification payload on `GAP`, but this skill must not enable live delivery by itself.

Live memory/embedding alerts require a separate approval gate covering:
- schedule/frequency
- Discord DM target
- cooldown/suppression behavior
- exact message format
- retry behavior

Until approved, the watchdog prints JSON only.

## Operating Procedure
1. Load `memory/always_on.md`.
2. Apply the Trigger Gate.
3. For `not_needed` work, answer or act directly within the always-on
   safety and authority rules.
4. For triggered work, route the message deterministically using
   `references/router.yml`.
5. Retrieve relevant snippets; prefer semantic/hybrid memory search when
   persistent memory is relevant.
6. Build a Retrieval Bundle that records retrieval mode.
7. Compress to a Context Pack and lint it. If lint fails, fall back to raw
   retrieved snippets.
8. Call the main reasoning model with always-on policy + Context Pack + user
   message.
9. For `debug` and `audit`, persist artifacts described in
   `references/RUNTIME_ARTIFACTS.md`.
10. Emit evidence according to the active runtime mode.

## What To Read / Use
- Router + caps: `references/router.yml`
- Compressor prompt: `references/compressor_prompt.txt`
- Retrieval Bundle schema: `references/schemas/retrieval_bundle.schema.json`
- Context Pack schema: `references/schemas/context_pack.schema.json`
- Receipt Ledger schema: `references/schemas/receipt_ledger.schema.json`
- Runtime artifact layout: `references/RUNTIME_ARTIFACTS.md`
- Runtime checklist: `references/RUNTIME_CHECKLIST.md`
- Semantic memory checklist: `references/SEMANTIC_MEMORY_ASSURANCE.md`
- Starter example file: `references/tests/golden.json`
- Positive-path harness fixtures: `references/tests/harness_cases.json`
- Anti-fabrication fixtures: `references/tests/anti_fabrication_cases.json`
- Installer/validator/watchdog scripts: `scripts/install_pipeline.py`, `scripts/validate_pipeline.py`, `scripts/memory_watchdog.py`
- Behavioral test runner: `scripts/run_pipeline_tests.py`

## Notes
- Keep `memory/always_on.md` tiny; put detail behind retrieval.
- Use snippet IDs only (`S1`, `S2`, etc.) in Context Pack `sources`.
- Follow `references/deterministic_ids.md` when deterministic snippet IDs matter.
- Run `scripts/run_pipeline_tests.py` after changing routing, retrieval caps, snippet IDs, runtime artifacts, derived queries, daily-log triggers, or transcript evidence.
- Run `scripts/memory_watchdog.py --require-semantic` before claiming semantic memory is healthy.
