# gemini-smart-search vNext goals (target: v0.1.1)

## Goals

- Keep API-key requirements explicit and consistent across skill metadata, runtime behavior, and human-facing docs.
- Make ClawHub artifact packaging deterministic, minimal, and easy to audit.
- Keep repo-only files clearly separated from artifact-shipped files.
- Preserve current runtime behavior, including header-based Gemini auth and env fallback compatibility.

## Non-goals

- No provider expansion beyond Gemini.
- No major JSON contract redesign.
- No canonical citation normalization in this pass.
- No automated release publishing in this pass.

## Prioritized todo

### P0
- Add a concise artifact policy with explicit include/exclude decisions.
- Add a repeatable artifact-prep script that exports only approved files.
- Update release checklist so artifact validation is concrete instead of ad hoc.
- Ensure docs consistently declare `SMART_SEARCH_GEMINI_API_KEY` as primary and `GEMINI_API_KEY` as compatibility fallback.

### P1
- Tighten repo hygiene for generated packaging output.
- Document that `LICENSE` stays in the GitHub repo but is excluded from the ClawHub artifact.
- Add lightweight validation that the prepared artifact excludes `.git/`, `.env.local`, and other repo/dev noise.

### P2
- Consider a non-secret debug field for selected API-key source if future troubleshooting needs it.
- Consider a single-command release helper that can emit a tarball/zip once the artifact format is standardized.

## Artifact policy

### Ship in ClawHub artifact
- `SKILL.md`
- `README.md`
- `scripts/gemini_smart_search.py`
- `scripts/gemini_smart_search.sh`
- `scripts/smoke_test.sh`
- `references/config.md`
- `references/release-checklist.md`
- `assets/example-output.json`

### Keep in repo only
- `.git/`
- `.env.local`
- `.gitignore`
- `LICENSE`
- `references/development-goals-v0.1.1.md`
- QA working notes / release notes / review notes not needed at runtime, including:
  - `references/agent-qa-cases.md`
  - `references/escalation-design.md`
  - `references/model-id-recon.md`
  - `references/qa-results-2026-03-12.md`
  - `references/qa-test-plan.md`
  - `references/release-notes-v0.1.0.md`
  - `references/release-notes-v0.1.1.md`
  - `references/vnext-review-2026-03-12.md`

## Release validation checklist

- Confirm `SKILL.md` metadata still declares `SMART_SEARCH_GEMINI_API_KEY` as primary env.
- Confirm runtime still prefers `SMART_SEARCH_GEMINI_API_KEY` and falls back to `GEMINI_API_KEY`.
- Confirm request auth still uses `x-goog-api-key` header, not URL query params.
- Run `scripts/smoke_test.sh`.
- Run `scripts/prepare_artifact.sh`.
- Inspect exported artifact contents and verify excluded files are absent.
- Confirm no secret-bearing local files are tracked or exported.
- Confirm repo-only `LICENSE` remains present in GitHub source but absent from artifact export.
