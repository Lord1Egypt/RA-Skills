---
name: clawhub-release-auditor
description: Validate, package, and verify ClawHub skills before and after publishing. Use when creating or updating a ClawHub skill, preparing a release, diagnosing repeated publish failures, checking metadata/frontmatter issues, comparing declared dependencies against scripts, or confirming that a published version and latest tag actually updated.
metadata:
  openclaw:
    requires:
      bins: [clawhub, openclaw]
    prePublishChecks:
      - clawhub-release-auditor
  homepage: https://clawhub.ai
---

# ClawHub Release Auditor

Run a strict preflight before any publish. Prefer stopping with a precise explanation over guessing. Treat repeated versions as a signal that the workflow needs diagnosis, not just another upload.

## Workflow

1. **Preflight**
   - Run `python3 scripts/preflight.py <skill-dir>`.
   - Fix all hard errors before continuing.
   - Read warnings carefully; they often explain why a skill ends up suspicious.

2. **Package locally**
   - Run `python3 ~/project/openclaw/skills/skill-creator/scripts/package_skill.py <skill-dir> [output-dir]`.
   - If packaging fails, stop and explain the exact validation error.

3. **Confirm before publish**
   - Show the skill path, intended version, and any remaining warnings.
   - Do not publish without explicit user confirmation.

4. **Publish**
   - Publish from the **skill folder**, not the `.skill` archive.
   - After publish, record the exact version that was attempted.

5. **Verify post-publish state**
   - Run `python3 scripts/verify_publish.py <skill-slug> --expected-version <version>`.
   - If latest/version visibility is inconsistent, say so clearly.
   - If scan results matter, check the web page separately and explain whether the issue is pending, version mismatch, or a likely metadata/code mismatch.

## What to check during preflight

- Frontmatter only uses supported keys.
- `name` and `description` are present and sane.
- Placeholder text is not leaking into examples.
- Declared `metadata.openclaw.requires` roughly matches real script usage.
- Homepage/source metadata exists when possible.
- Publish path points to the skill directory, not the packaged archive.
- Local package validation passes before any publish attempt.

## Common failure patterns

### Frontmatter mismatch
If validation complains about unsupported keys, trust the validator. Do not invent alternate formats from memory.

### Metadata drift
If scripts use env vars or binaries that the skill does not declare, expect suspicious scan results. Fix the declaration or the code.

### Placeholder leakage
If docs contain example paths like `/path/to/...`, make sure they are clearly examples and not presented as real files.

### Repeated publish loops
If many versions are being published quickly, pause and diagnose:
- Did packaging actually succeed?
- Did latest move?
- Is scan still reading an older version?
- Is the same metadata mismatch still present?

## Scripts

### `scripts/preflight.py`
Checks a skill directory for:
- frontmatter problems
- placeholder text
- likely undeclared env vars and binaries
- external execution hints
- package validation failures
- a simple verdict: `do-not-publish`, `review-before-publish`, or `ready-to-package`

### `scripts/verify_publish.py`
Checks published version state with `clawhub inspect` and compares it to an expected version.

### `scripts/analyze_history.py`
Inspects recent version history for a public skill and groups releases into rough categories such as docs, metadata, bugfix, and feature work. Use it to study repeated publish loops and sharpen the skill's heuristics.

### `scripts/failure_buckets.py`
Classifies likely publish problems into practical buckets such as `frontmatter-invalid`, `package-validation-failed`, `latest-not-updated`, or `no-hard-failure-detected`.

### `scripts/release_worthiness.py`
Compares a local skill directory against the latest published version and flags when there is no material diff. Use it to avoid unnecessary republish loops.

## Publishing tips

### SKILL.md body must have substantial content

ClawHub checks for "Skill content is too thin or templated." This evaluates the SKILL.md body text (markdown below frontmatter), not just the description field.

**Why this matters:**
- The `description` field is only used for UI/search summaries
- The SKILL.md body is what gets embedded and evaluated for the thin-content check
- If SKILL.md has only frontmatter and no body text, it will fail even with a perfect description

**How to avoid:**
- Always include substantive body content in SKILL.md (at least 300-500 words of meaningful guidance)
- Include real workflow guidance, usage examples, and operational notes in the body
- The more comprehensive the SKILL.md body, the less likely it triggers "templated" detection

### Other common pitfalls
- `homepage` field: Include a valid URL to avoid warnings
- Empty directories: Remove any empty `scripts/`, `references/`, or other directories before packaging
- Symlinks: These are rejected by the packager and cause failures

## References

- Read `references/checklist.md` for the release checklist.
- Read `references/research-notes.md` when designing heuristics for repeated publish loops and common failure modes.
- If the skill format or server behavior is unclear, read the official ClawHub skill format docs before guessing. Prefer current docs plus validator output over old habits.
