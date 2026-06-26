# gemini-smart-search v0.1.0

Initial public artifact release of a Gemini-only, script-backed smart search skill for OpenClaw.

## What it does

- Uses the Gemini Developer API directly instead of relying on gateway-level `web_search` model switching.
- Supports Google Search grounding.
- Supports three routing modes:
  - `cheap`
  - `balanced`
  - `deep`
- Resolves API keys with the following precedence:
  1. `SMART_SEARCH_GEMINI_API_KEY`
  2. `GEMINI_API_KEY`
- Returns structured JSON suitable for orchestration.
- Includes fallback across configured Gemini model candidates for retryable upstream/model failures.
- Includes `escalation` metadata so agents can direct a human to file a GitHub issue for suspicious/systemic failures.

## Included files

- `SKILL.md`
- `scripts/gemini_smart_search.py`
- `scripts/gemini_smart_search.sh`
- `scripts/smoke_test.sh`
- `references/config.md`
- `references/qa-test-plan.md`
- `references/qa-results-2026-03-12.md`
- `references/agent-qa-cases.md`
- `references/model-id-recon.md`
- `references/escalation-design.md`
- `references/vnext-review-2026-03-12.md`
- `assets/example-output.json`

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

## Known caveats

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

## Not included in v0.1.0

- canonical citation normalization
- deterministic fallback unit test harness
- automated model-recon refresh tooling
- richer GitHub issue prefill UX for escalations
