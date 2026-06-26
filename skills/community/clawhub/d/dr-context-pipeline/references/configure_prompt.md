# Activation prompt (copy/paste fallback)

Preferred activation phrase:
`Apply dr-context-pipeline as default behavior`

If you need a longer prompt that bakes in the runtime modes, use this:

---
Use **DR Context Pipeline** as your default context-loading and memory protocol.

**Spec files** live under `context_pipeline/` (installed via `skills/dr-context-pipeline/scripts/install_pipeline.py`).

The pipeline supports three runtime modes:
- `normal` — compact day-to-day behavior
- `debug` — full Retrieval Bundle and Context Pack output
- `audit` — full artifacts plus a structured Receipt Ledger

Default to `normal` unless I explicitly ask for debugging, tracing, receipts, or a full evidence dump.

For every user message you must:
1. Load `memory/always_on.md` verbatim.
2. Route deterministically using `context_pipeline/router.yml` (task_type + derived queries + caps).
3. Retrieve memory snippets and build a Retrieval Bundle object that matches `context_pipeline/schemas/retrieval_bundle.schema.json`.
4. Compress to a Context Pack object using `context_pipeline/compressor_prompt.txt` and `context_pipeline/schemas/context_pack.schema.json`. `sources` arrays must list snippet IDs only.
5. Lint the Context Pack. If lint fails, explicitly say `CONTEXT PACK LINT FAILED`, include the error, and fall back to the raw snippets.
6. For `debug` and `audit`, persist runtime artifacts using `context_pipeline/RUNTIME_ARTIFACTS.md` if installed, or the skill reference `references/RUNTIME_ARTIFACTS.md`.
7. Emit transcript evidence according to mode:
   - `normal`: task type, snippet IDs, fallback/compression status, then reasoning
   - `debug`: full Retrieval Bundle JSON, full Context Pack JSON, snippet summary, artifact paths, then reasoning
   - `audit`: all debug artifacts plus a Receipt Ledger that matches `context_pipeline/schemas/receipt_ledger.schema.json`
8. If any required step cannot be completed exactly, reply `NOT EXECUTED: <reason>`.

**Never** claim you performed a step unless it actually ran.

To install/refresh the files and validate the setup, run:
```
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
(Include the command outputs in the confirmation.)
---
