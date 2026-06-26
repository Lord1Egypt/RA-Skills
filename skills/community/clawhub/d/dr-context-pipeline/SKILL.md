---
name: dr-context-pipeline
description: "Deterministic memory/context pipeline for agents: route a user message, retrieve relevant memory snippets, compress into a cited Context Pack (sources are snippet IDs), lint, and fall back safely. Prerequisite: a file-based memory layout with memory/always_on.md + topic files (works out-of-the-box with dr-memory-foundation). Use when building or standardizing agent memory, reducing prompt bloat, implementing retrieval+compression, creating a context pack, designing a memory pipeline, adding lint gates, or setting up golden regression tests for agent context. After install, users can simply say: Apply dr-context-pipeline as default behavior." 
---

# DR Context Pipeline (retrieval + compression + lint)

Use this skill to standardize how an agent loads memory into its prompt **for correctness**.

## Prerequisites
- A file-based memory layout that includes `memory/always_on.md` (policy header + topic catalog) and topic files under `memory/topics/`.
- Recommended: install **dr-memory-foundation** (or implement an equivalent structure).

## Quick install commands (copy/paste)
These commands work from anywhere because they set `$WORKSPACE` (defaults to `~/.openclaw/workspace`). Rerun them whenever you need to re-apply the pipeline:
```bash
export WORKSPACE=${WORKSPACE:-~/.openclaw/workspace}
cd "$WORKSPACE"
clawhub install dr-context-pipeline --version X.Y.Z --dir skills
python3 ./skills/dr-context-pipeline/scripts/install_pipeline.py --target "$WORKSPACE/context_pipeline"
ls -1 "$WORKSPACE/context_pipeline"
git -C "$WORKSPACE" diff -U20 AGENTS.md | cat
python3 ./skills/dr-context-pipeline/scripts/validate_pipeline.py --context-root "$WORKSPACE/context_pipeline"
python3 ./skills/dr-context-pipeline/scripts/memory_watchdog.py --freshness-minutes 240 --min-bytes 200
git -C "$WORKSPACE" status -sb context_pipeline AGENTS.md
echo "CONTEXT PIPELINE APPLY COMPLETE"
```
Paste every command’s output. If any step fails or the watchdog reports a gap, stop and reply `NOT EXECUTED: <reason>`.


## Apply to this workspace
When the user asks to **apply** this skill (for example: `Apply dr-context-pipeline as default behavior`), follow this exact order and paste the evidence for every step:
All commands assume you’ve set `WORKSPACE=${WORKSPACE:-~/.openclaw/workspace}` and are running from that directory.
1. **Lay down the files** — run `python3 ./skills/dr-context-pipeline/scripts/install_pipeline.py --target context_pipeline` (adds/updates the workspace copy from `assets/context_pipeline/`). Keep the script output in the transcript (hash summary + file count).
2. **Show the tree** — `ls -1 context_pipeline` so the user sees which files are now present.
3. **Patch `AGENTS.md`** — read the file, insert/refresh the “Context Pipeline” instructions, and include a `git diff -U20 AGENTS.md` (or equivalent) snippet in your reply. Preserve everything else.
4. **Validate** — run `python3 ./skills/dr-context-pipeline/scripts/validate_pipeline.py --context-root context_pipeline` and paste the PASS/FAIL summary. If it fails, stop and report `NOT EXECUTED` with the error.
5. **Run the memory watchdog** — `python3 ./skills/dr-context-pipeline/scripts/memory_watchdog.py --freshness-minutes 240 --min-bytes 200` (tune as needed). Paste the JSON output; if status ≠ OK, stop and reply `NOT EXECUTED: memory gap` after quoting the issues.
6. **Final state** — show `git status -sb context_pipeline AGENTS.md` (or `git status -sb` if cleaner) so the user can see what changed.
7. **Success banner** — `echo "CONTEXT PIPELINE APPLY COMPLETE"` so the transcript clearly shows the run finished cleanly.

This apply flow must be idempotent: if the files already match and `AGENTS.md` already contains the section, the diff should be empty but you still run the installer + validator and show their outputs.

## Memory commit / continue workflow
- When Daniel says “memorize this” (or similar), run the checklist in `references/MEMORY_COMMIT.md` (daily log, now, open-loops, topic file, MEMORY.md) and confirm which files changed.
- When he says “let’s continue” after a reset, reload `memory/now.md`, `open-loops`, and the relevant topic files so you can summarize where things left off before acting.

## Runtime modes and evidence contract
Every single task must follow the Runtime Evidence Checklist in `references/RUNTIME_CHECKLIST.md`.

The pipeline supports three runtime modes:
- `normal` — compact day-to-day operation
- `debug` — full pipeline artifacts for diagnosis
- `audit` — full artifacts plus Receipt Ledger for high-trust review

Default to `normal` unless the user explicitly asks for `debug`, `audit`, tracing, receipts, or a full evidence dump.

Mode rules:
- In **all** modes, the agent must actually perform the retrieval/compression/lint steps before claiming success.
- In **all** modes, if a required step cannot be completed, reply `NOT EXECUTED: <reason>` and stop.
- In **normal** mode, do not dump full Retrieval Bundle or Context Pack JSON into the transcript unless the user explicitly asks for it.
- In **debug** mode, emit the Retrieval Bundle JSON, Context Pack JSON, dropped-snippet reasons, and snippet pass-through summary.
- In **audit** mode, emit everything from debug mode and preserve a structured **Receipt Ledger** suitable for later review.

Required output by mode:
- **normal**:
  - compact answer
  - task type
  - snippet IDs passed forward
  - whether compression succeeded or fallback was used
  - internal artifact paths may be kept private unless troubleshooting requires them
- **debug**:
  - Retrieval Bundle JSON
  - Context Pack JSON
  - snippet summary
  - dropped reasons
  - run artifact paths
  - user-facing reasoning/result
- **audit**:
  - all debug artifacts
  - Receipt Ledger / proof of each completed step
  - user-facing reasoning/result

Casual prompts do **not** waive the requirement to do the work. They only keep the pipeline in `normal` mode unless the user explicitly asks for more evidence.

## Operating procedure (default)
1) Load the always-on policy + topic catalog (your `memory/always_on.md`).
2) Route the message deterministically (task type + caps) using `references/router.yml`.
3) Retrieve top relevant snippets from your memory store; build a **Retrieval Bundle** internally (see schema).
4) Compress Retrieval Bundle → **Context Pack** using `references/compressor_prompt.txt`.
   - **IMPORTANT:** Context Pack `sources` MUST be **snippet IDs only** (`S1`, `S2`, …).
5) Lint the Context Pack. If lint fails, **skip compression** and fall back to raw retrieved snippets.
6) Call the main reasoning model with: always-on policy header + Context Pack (+ raw snippets for high-stakes tasks) + user message.
7) For `debug` and `audit`, persist the run artifacts described in `references/RUNTIME_ARTIFACTS.md`.
8) Emit evidence according to the active runtime mode:
   - `normal`: compact evidence summary only
   - `debug`: full Retrieval Bundle + Context Pack + snippet summary
   - `audit`: debug artifacts plus a Receipt Ledger

## What to read / use
- Router + caps: `references/router.yml`
- Compressor prompt: `references/compressor_prompt.txt`
- Retrieval Bundle schema: `references/schemas/retrieval_bundle.schema.json`
- Context Pack schema: `references/schemas/context_pack.schema.json`
- Receipt Ledger schema: `references/schemas/receipt_ledger.schema.json`
- Runtime artifact layout: `references/RUNTIME_ARTIFACTS.md`
- Runtime checklist: `references/RUNTIME_CHECKLIST.md`
- Starter example file: `references/tests/golden.json`
- Authoritative positive-path harness fixtures: `references/tests/harness_cases.json`
- Authoritative anti-fabrication fixtures: `references/tests/anti_fabrication_cases.json`
- Installer/validator/watchdog scripts: `scripts/install_pipeline.py`, `scripts/validate_pipeline.py`, `scripts/memory_watchdog.py`
- Behavioral test runner: `scripts/run_pipeline_tests.py`

## Notes
- Keep “always-on policy header” tiny (invariants only). Put everything else behind retrieval.
- If you need deterministic snippet IDs, follow the stable ordering guidance in `references/deterministic_ids.md`.
- Receipt Ledger is an **audit-mode** structure first. `debug` may reuse it later, but `normal` mode should stay compact.
- Runtime artifacts are required for `debug` and `audit`. `normal` may keep artifacts internal and summarize only.
- Run `scripts/run_pipeline_tests.py` after changing routing, retrieval caps, snippet-ID behavior, runtime artifact behavior, derived-query behavior, daily-log-trigger behavior, or per-mode transcript evidence.
- Use `scripts/run_pipeline_tests.py --failure-fixtures references/tests/anti_fabrication_cases.json` when changing artifact, receipt, or transcript-proof behavior so anti-fabrication checks run alongside the positive harness.
- `references/tests/golden.json` is kept as a small starter/example file and validator sanity target, but the executable harness fixtures are the authoritative behavior checks.
- The harness should include canned compression success, dropped-snippet reporting, at least one lint-failure fallback case, and explicit overlap/precedence coverage for router behavior without live model calls.
