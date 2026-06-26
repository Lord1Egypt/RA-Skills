# Release Checklist

Use this checklist before publishing a `gemini-smart-search` artifact.

Legend:
- `[x]` completed for the current release candidate
- `[ ]` still required before publishing

## A. Core functionality

- [x] Python entrypoint works for live queries.
- [x] Shell wrapper works for live queries.
- [x] Google Search grounding is enabled in the direct Gemini API call path.
- [x] `cheap`, `balanced`, and `deep` modes are implemented.
- [x] Fallback across configured candidate model IDs works for retryable failures.
- [x] Missing-key behavior is graceful.
- [x] `SMART_SEARCH_GEMINI_API_KEY` takes precedence over `GEMINI_API_KEY`.

## B. Contract / output stability

- [x] `--json` returns structured JSON on success.
- [x] `--json` returns structured JSON on supported runtime errors.
- [x] Invalid CLI arguments under `--json` return structured JSON on stderr.
- [x] Output includes `display_chain` and `fallback_chain`.
- [x] Output includes `escalation`.
- [x] `model_used` semantics are documented as actual API model ids.

## C. Documentation consistency

- [x] `SKILL.md` documents Python as the canonical entrypoint.
- [x] Wrapper is documented as convenience-only.
- [x] `python -m gemini_smart_search` is explicitly documented as unsupported for agents.
- [x] Citation redirect-link behavior is documented.
- [x] Escalation behavior is documented.
- [x] Model-ID recon notes are written down.
- [x] QA notes are aligned with current behavior.

## D. QA / validation

- [x] Non-destructive smoke tests pass.
- [x] Missing-key path validated.
- [x] Invalid-argument JSON behavior validated.
- [x] Live cheap-mode path validated.
- [x] Live wrapper path validated.
- [x] Live deep/fallback path validated.
- [x] Agent-style misuse review completed.
- [x] Release-readiness doc audit completed.

## E. Secret / repo hygiene

- [x] `.env.local` is gitignored.
- [x] No API key is stored in tracked files.
- [x] Artifact export policy explicitly excludes `.git/`, `.env.local`, and repo/dev-only files.
- [x] `LICENSE` is kept as a repo-only file and excluded from the ClawHub artifact.

## F. Release packaging

Artifact ship list for ClawHub export:
- `SKILL.md`
- `README.md`
- `scripts/gemini_smart_search.py`
- `scripts/gemini_smart_search.sh`
- `scripts/smoke_test.sh`
- `references/config.md`
- `references/release-checklist.md`
- `assets/example-output.json`

Repo-only / exclude from ClawHub export:
- `.git/`
- `.env.local`
- `.gitignore`
- `LICENSE`
- development, QA, review, and release-note working docs not needed at runtime

Required packaging checks:
- [x] `scripts/prepare_artifact.sh` stages only the approved artifact contents.
- [x] Artifact contents are reviewed after export.
- [x] Release note is published alongside the artifact (`references/release-notes-v0.1.1.md`).
- [x] Version tag/name is chosen for the artifact (`v0.1.1`).

## G. Known acceptable caveats for v0.1.1

These do **not** block the current artifact release:

- [x] Citation URLs are still grounding redirect URLs.
- [x] Canonical citation normalization is deferred.
- [x] Deterministic fallback unit tests are deferred.
- [x] Automated model-recon refresh is deferred.

## Release decision

For a publishable candidate, run `scripts/smoke_test.sh`, then `scripts/prepare_artifact.sh`, then inspect the staged artifact contents.

If every unchecked item in section F is completed, this release candidate is ready to publish as an artifact.
