# gemini-smart-search v0.1.1

Artifact-policy and release-hygiene update for the Gemini-only, script-backed smart search skill for OpenClaw.

## What changed in v0.1.1

- Clarified and tightened the ClawHub artifact policy so the export is a deliberate runtime subset of the repo.
- Added `README.md` and `references/release-checklist.md` to the approved artifact ship list.
- Kept `LICENSE` in the GitHub repo while explicitly excluding it from the ClawHub artifact.
- Kept credential policy unchanged and explicit:
  1. `SMART_SEARCH_GEMINI_API_KEY`
  2. `GEMINI_API_KEY`
- Kept the Python entrypoint as the canonical agent entrypoint, with the shell wrapper documented as convenience-only.
- Added deterministic staged-artifact preparation and exclusion checks via `scripts/prepare_artifact.sh`.
- Reconciled release docs so the documented artifact contents match the actual staging script.

## Included files in the v0.1.1 ClawHub artifact

- `SKILL.md`
- `README.md`
- `scripts/gemini_smart_search.py`
- `scripts/gemini_smart_search.sh`
- `scripts/smoke_test.sh`
- `references/config.md`
- `references/release-checklist.md`
- `assets/example-output.json`

## Repo-only / excluded from the v0.1.1 ClawHub artifact

- `.git/`
- `.env.local`
- `.gitignore`
- `LICENSE`
- development, QA, review, and release-note working docs not needed at runtime, including:
  - `references/development-goals-v0.1.1.md`
  - `references/agent-qa-cases.md`
  - `references/escalation-design.md`
  - `references/model-id-recon.md`
  - `references/qa-results-2026-03-12.md`
  - `references/qa-test-plan.md`
  - `references/release-notes-v0.1.0.md`
  - `references/release-notes-v0.1.1.md`
  - `references/vnext-review-2026-03-12.md`

## Validated release behaviors

- Python entrypoint works for live queries.
- Shell wrapper works for live queries.
- `--json` returns structured JSON on success and supported runtime errors.
- Invalid CLI arguments with `--json` return structured JSON on stderr.
- Missing-key behavior is graceful and structured.
- Repo-local `.env.local` is ignored by git.
- Wrapper and Python entrypoints are behaviorally aligned.
- Fallback metadata is present and useful.
- `escalation` field is present on success and error responses.

## Known caveats retained in v0.1.1

- Citation URLs may still be Google/Vertex grounding redirect URLs rather than canonical publisher URLs.
- `model_used` is the actual probed API model id, not the human-facing display label.
- Live fallback means identical queries are not guaranteed to land on the same final model every time.
- Some Gemini 3 display labels map to preview-suffixed API ids in practice.

## Release scope

This release is intended as a clean skill artifact.

Before packaging/publishing the artifact:
- export from the clean staging helper (`scripts/prepare_artifact.sh`) instead of publishing a raw repo snapshot
- do not include `.git/`, `.env.local`, `.gitignore`, or `LICENSE`
- keep `LICENSE` in the GitHub repo; exclude it only from the ClawHub artifact

## Not included in v0.1.1

- canonical citation normalization
- deterministic fallback unit test harness
- automated model-recon refresh tooling
- richer GitHub issue prefill UX for escalations
