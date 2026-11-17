# Changelog

## [2.3.0] - 2026-08-06

- Release to ClawHub (owner: timeaground, slug: figma-to-mobile)
- Version aligned with ClawHub release versioning

## [1.2.0] - 2026-08-06

- Slim SKILL.md via reference-loading protocol (AP-001): low-frequency details moved to `references/`
  - New `references/multi-frame.md` (multi-link relationship rules, from Step 1-C)
  - New `references/error-handling.md` (full error handling, from Error Handling)
  - New `references/feedback-log.md` (log format + rules, from Step 4)
  - `references/scan-usage.md` gained presenting-scan-results section (from Step 2.5)
  - SKILL.md keeps step skeleton + one-line pointers at each moved section

## [1.1.0] - 2026-08-06

- Add standard `requires` field to frontmatter (Bash, Read, Write, Grep, Glob)
- Add resource manifest declaration (cpu/memory/timeout/network)
- Add `## API Request Limits` section (30s timeout, 3 retries, rate-limit behavior, adaptive depth)
- Add `## Tips` section (token safety, rate limits, multi-frame reuse)
- Slim frontmatter `description` to ~260 chars (keeps all trigger signals)
- Add `eval/evals.json` self-test suite (12 P0 cases)

## [1.0.0] - 2026-08-06

Initial release.

- Add `version` field to SKILL.md frontmatter
- Add `## Not Applicable` section (screenshot input, non-conversion requests, pure design discussion)
- Add `## Deliverables` section (generated code files, scan-report.json, feedback-log.md)
- Clean up `__pycache__` build artifacts
