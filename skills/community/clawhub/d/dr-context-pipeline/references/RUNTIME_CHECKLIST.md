# Runtime Evidence Checklist — dr-context-pipeline

Agents **must** follow this checklist on every task once the context pipeline is installed.

## Runtime modes
The pipeline supports three modes:
- `normal` — compact operation for everyday use
- `debug` — full pipeline artifacts for diagnosis
- `audit` — full artifacts plus Receipt Ledger for high-trust review

Default to `normal` unless the user explicitly asks for debugging, tracing, receipts, or a full evidence dump.

## Rules that apply in all modes
1. Load `memory/always_on.md`.
2. Route + retrieve according to `context_pipeline/router.yml` caps.
   - When persistent memory is relevant, prefer semantic/hybrid memory search.
   - Record retrieval mode as `semantic`, `hybrid`, `file_fallback`, or `not_needed`.
   - If semantic memory is unavailable or not attempted, normal mode must say so compactly; debug/audit must include the reason.
3. Build a Retrieval Bundle object internally.
4. Compress to a Context Pack internally.
5. Lint the Context Pack.
6. If lint fails, use the documented fallback behavior.
7. If any required step cannot be completed, reply exactly `NOT EXECUTED: <reason>` and stop.
8. Do **not** claim a bundle, pack, or step was produced unless it actually was.

For `debug` and `audit`, persist runtime artifacts using `references/RUNTIME_ARTIFACTS.md` before emitting final evidence.

## Required transcript output by mode

### `normal`
Emit only:
- the user-facing reasoning/output
- a footer/footnote containing:
  - task type
  - snippet IDs passed into reasoning
  - retrieval mode: `semantic`, `hybrid`, `file_fallback`, or `not_needed`
  - whether compression succeeded or raw-snippet fallback was used
  - model used
  - files read
  - files updated

Do **not** emit the full Retrieval Bundle JSON or full Context Pack JSON unless the user explicitly asks for them.

### `debug`
Emit:
- full Retrieval Bundle JSON
- full Context Pack JSON
- dropped entries with reasons
- snippet summary + pass-through
- retrieval mode and fallback/degradation reason, if any
- runtime artifact paths
- the user-facing reasoning/output
- a footer/footnote containing model used, files read, and files updated

If lint fails, explicitly state `CONTEXT PACK LINT FAILED` and include the lint error before falling back.

### `audit`
Emit everything from `debug`, plus:
- a structured Receipt Ledger that matches `context_pipeline/schemas/receipt_ledger.schema.json`
- any command/tool proof needed to support claims of completion
- a footer/footnote containing model used, files read, and files updated

Receipt Ledger requirements:
- one entry per required pipeline step
- each entry must record whether the step `succeeded`, `failed`, or was `skipped`
- each successful entry must include enough proof to show what ran
- artifact-producing steps must include `proof.artifact_path` and `proof.artifact_sha256`
- if a required audit-mode receipt is missing, the task must fail with `NOT EXECUTED`

## Failure contract
If any required step above cannot be completed, reply exactly `NOT EXECUTED: <reason>` and stop. Do **not** invent bundles, packs, or receipts.
