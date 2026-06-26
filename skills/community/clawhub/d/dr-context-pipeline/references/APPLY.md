# Apply checklist — dr-context-pipeline

Use this whenever someone says things like:
- Apply dr-context-pipeline as default behavior
- Enable the context pipeline
- Make this the default context-loading workflow

## Command sequence (no shortcuts)
Set `WORKSPACE=${WORKSPACE:-~/.openclaw/workspace}` and run these from that directory (the same one that contains `AGENTS.md`).
1. `python3 ./skills/dr-context-pipeline/scripts/install_pipeline.py --target context_pipeline`
   - Lays down / refreshes the canonical files from `assets/context_pipeline/`.
   - Paste the script’s summary (file count + hash digest sample) in your reply.
2. `ls -1 context_pipeline`
   - Shows exactly which files are now present.
3. Update `AGENTS.md`
   - Insert or refresh the Context Pipeline instructions.
   - Paste a `git diff -U20 AGENTS.md` (or equivalent) so the user can see the changes.
4. `python3 ./skills/dr-context-pipeline/scripts/validate_pipeline.py --context-root context_pipeline`
   - Runs integrity checks (hash comparison, schema parse, golden test sanity).
   - Paste the PASS/FAIL block. On failure, stop and report `NOT EXECUTED: <error>`.
5. `python3 ./skills/dr-context-pipeline/scripts/memory_watchdog.py --freshness-minutes 240 --min-bytes 200`
   - Ensures today’s `memory/YYYY-MM-DD*.md` exists, is non-empty, and was updated recently.
   - Paste the JSON output. If status ≠ OK, stop immediately and reply `NOT EXECUTED: memory gap`.
6. `git status -sb context_pipeline AGENTS.md`
   - Confirms the final state.
7. `echo "CONTEXT PIPELINE APPLY COMPLETE"`
   - Print a success banner so the transcript has an explicit “done” line.

## Evidence to include in the transcript
- Raw command output for every step above (installer summary, directory listing, diff, validator summary, watchdog JSON, git status).
- If no files changed (idempotent apply), explicitly state that the installer/validator/watchdog still ran and returned clean results.

## Failure contract
If any command fails or the validator/watchdog reports an error, reply `NOT EXECUTED: <reason>` and wait for further instructions. Do **not** claim success without receipts.
