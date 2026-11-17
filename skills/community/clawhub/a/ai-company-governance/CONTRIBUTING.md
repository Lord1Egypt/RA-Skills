# Contributing to ai-company

Thanks for helping improve this skill package. This document covers branch
strategy, commit conventions, how to run the tests, how to run the acceptance
checks, and pull-request requirements.

The authoritative design specification for this project is `README-FOR-AI.md`,
which ships at the root of this repository and is fully self-contained: every
parameter, contract, red line, and acceptance check a contributor needs is
defined there, so no external or upstream document is required. Its **§14**
defines the red lines **P1–P55** — read at least the rows relevant to your
change before you start. The scale-tier ladder this package belongs to is
defined locally in **§1**.

## Branch strategy

- `main` is protected; never push directly to it.
- Branch from `main` using `feat/<slug>`, `fix/<slug>`, or `docs/<slug>`.
- One logical change per branch and per pull request.

## Commit conventions

Follow [Conventional Commits](https://www.conventionalcommits.org/): `feat:`,
`fix:`, `docs:`, `test:`, `refactor:`, `chore:`. Subject lines are imperative
and at most 72 characters, for example:

```text
fix: use wildcard pattern for review reports in .gitignore (P39)
```

## How to run the tests

From the package root:

```bash
python tests/test-method-patterns.py
```

The suite validates the real authoritative sources (it never relies on inline
copies of template code) and additionally guards self-upgrade proposals: a
proposal package that modifies `tests/` or the `permissions` block of
`SKILL.md` fails the tests. All tests must pass before you open a PR.

## How to run the acceptance checks

Key checks for the micro tier (the full list is in `README-FOR-AI.md` **§15**):

| Check | Expected |
|---|---|
| Total file count | 25 |
| Function blocks across the two department files | 18 (`governance-and-delivery.md`: 8; `engineering-and-safety.md`: 10) |
| `SKILL.md` frontmatter | ≤ 85 lines |
| `SKILL.md` body | ≤ 120 lines, no code implementations or full error-code tables |
| Governance and community files | 13/13 present (no tier trimming) |
| `README.md` / `README.en.md` / `README.zh.md` Project Structure tree | Matches the disk exactly |
| Internal links | No broken relative links; no orphan files under `prompts/` or `references/` |

Tier readiness can be checked read-only with:

```powershell
powershell -File scripts/self-scale.ps1 -Action evaluate
```

Any tier mutation (upgrade or downgrade) is lossy and requires explicit human
approval — contributors must never run it inside a PR.

## Red lines (where to find them)

All red lines are listed in `README-FOR-AI.md` **§14 (P1–P55)**. The most
frequently hit ones:

- **P10 / P44** — code templates live only in `references/method-patterns.md`;
  never inline-copy them anywhere else.
- **P17** — no bulk error-code tables inside `SKILL.md`.
- **P39** — after generating or changing content, run the acceptance checks the
  content claims to satisfy.
- **P47 / P48** — source files are English and output language follows the
  user; never translate identifiers (slugs, error codes, field names, enum
  values, file paths, function names).
- **P50** — never tier-trim the governance and community files.
- **P51** — no file names containing spaces and no misspelled variants.
- **P55** — `AGENTS.md` must not duplicate `SKILL.md` content or become a
  second skill entry point.

## Pull request requirements

- **Description**: what changed and why; link the relevant red line (`P##`) or
  the `README-FOR-AI.md` section (`§x.y`) when applicable.
- **Green**: `python tests/test-method-patterns.py` passes, and the acceptance
  table above is satisfied for the micro tier.
- **Structure sync**: if any file was added, removed, or renamed, update the
  Project Structure tree in `README.md`, `README.en.md`, and `README.zh.md` in
  the same PR.
- **Changelog**: add an entry under `[Unreleased]` in `CHANGELOG.md`
  (Keep a Changelog format). A version number must never appear twice, and
  dates must never go backwards (P12/P13).
- **No self-exemption**: PR content must not modify `tests/` or the
  `permissions` block of `SKILL.md` as part of upgrade-proposal payloads.
- **Encoding hygiene**: UTF-8 without BOM, LF line endings (CRLF for `.ps1`),
  no trailing whitespace — see `.editorconfig`.
