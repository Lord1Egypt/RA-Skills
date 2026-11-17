# AGENTS.md

> **Scope of this file**: This file is for coding agents that *maintain this
> repository*. The runtime entry point of the skill is `SKILL.md`; this file
> does not participate in skill routing or activation.

## What this repository is

`ai-company` is a standalone, micro-tier LLM Agent governance skill
package (version 1.0.0): 2 departments, 18 function blocks, 25 files total,
including its own self-contained generation spec `README-FOR-AI.md`. For a
human overview, read `README.md`. For skill runtime behavior, the *only* entry
point is `SKILL.md` — never duplicate or paraphrase its content in any other
file.

## Before you change anything

1. Read `CONTRIBUTING.md` for branch, commit, test, and PR rules.
2. `README-FOR-AI.md` (at the package root) is the self-contained, sole
   authoritative generation & maintenance spec of this standalone project —
   there is no upstream or external spec to consult. Its **§14** lists the red
   lines **P1–P55**; **§15** lists the acceptance checks. Check the relevant
   red-line rows before writing code or content.
3. The Project Structure tree in `README.md` must always match the disk
   exactly. If you add, rename, or remove any file, update that tree (and the
   file-count claims) in `README.md`, `README.en.md`, and `README.zh.md` in the
   same change.

## Commands to run

Run from the package root:

| Purpose | Command |
|---|---|
| Unit tests (authoritative-source validation) | `python tests/test-method-patterns.py` |
| Tier evaluation (read-only readiness check) | `powershell -File scripts/self-scale.ps1 -Action evaluate` |
| Key acceptance counts | See the acceptance section of `CONTRIBUTING.md` |

All tests must pass before you commit. Any tier action beyond `evaluate`
(upgrade/downgrade) is lossy and requires explicit human approval — never run
it on your own.

## Invariants — where to check them, not what they say

This section deliberately contains no content copied from `SKILL.md`. Each row
points to the single authoritative location.

| Invariant | Authoritative source |
|---|---|
| Skill routing, department index, error-code prefixes | `SKILL.md` (sole runtime entry) |
| Code templates and prompt frameworks | `references/method-patterns.md` (sole code authority; no file may inline-copy them — P10/P44) |
| Error codes (four-element table) | `references/error-codes.md` |
| Upgrade thresholds, gating, aliases | `references/scaling.md` |
| Self-upgrade safety (no changes to `tests/` or the `permissions` block in proposals) | `tests/test-method-patterns.py`; `README-FOR-AI.md` §9.5 / §12.3 |

## Hard rules for edits

- **Link, never inline.** Code templates live only in
  `references/method-patterns.md`; nothing may inline-copy them. (P10, P44)
- **Never modify `tests/` or the `permissions` block of `SKILL.md` as part of
  an upgrade proposal.** The test suite asserts this and will fail.
- **Never ignore `.scaling-state.json`** — it is package metadata and must be
  tracked. (See the note in `.gitignore`.)
- **No file names containing spaces**, and no misspelled variants such as
  `.gitingnore` or `changelog.md`. (P51)
- **Never tier-trim the governance files** — all 13 exist at every scale tier.
  (P50)
- **Never translate identifiers** (slugs, error codes, field names, enum
  values, file paths, function names), including in `README.zh.md`. (P48)
- Source files are English (except `README.zh.md`); output language follows the
  user. (P47)
- UTF-8 without BOM, LF line endings, 2-space indent (4 for Python), CRLF for
  `.ps1` — see `.editorconfig`.
- `.gitignore` uses wildcard patterns (`REVIEW-*.md`, `AUDIT-*.md`), never
  exact report file names. (P39)
- After generating or changing content, run the acceptance checks that the
  content claims to satisfy. (P39)

## When you are unsure

- Red lines: `README-FOR-AI.md` §14 (P1–P55).
- Acceptance: `README-FOR-AI.md` §15.
- Process and PR rules: `CONTRIBUTING.md`.

This file stays under 150 lines and never becomes a second skill entry point
(P55).
