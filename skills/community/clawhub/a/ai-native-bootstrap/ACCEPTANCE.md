# ai-native-bootstrap v1.0.0 - bundle acceptance

Date: 2026-11-13 (UTC) - re-validated after the WorkBuddy migration fixes.

## Scope

Installable bootstrap Skill for WorkBuddy, also compatible with the Codex, Claude Code and OpenCode install paths documented in `references/adapters-and-safety.md`. Carries the source specification at `references/implementation-standard.md` and adds an executable opt-in implementation. No customer repository or live deployment was modified during bundle acceptance.

## Validation environment

- OS: macOS (Darwin); Python 3.13.12; no network, no model API, no secrets, no CI credentials.
- Python 3.9+ is the declared source target; the full minor-version matrix was NOT independently tested.
- Before the 2026-11-13 fix, this host reported 16 failures out of 21 tests: OS-level symlink ancestors (`/var` and `/tmp` are system links on macOS) were rejected as unsafe, and git canonicalised the repository root differently from the supplied path. Both defects are fixed and covered by a dedicated regression test. The earlier "0 failures" claim was not reproducible on this host and has been replaced by the results below.

## Executed checks

| Gate | Command / method | Observed result |
|---|---|---|
| A1 - static package validation | `python3 scripts/validate_bundle.py` | PASS - 26 required files, syntax, metadata, empty default checks |
| A2 - offline unit/integration suite | `python3 -m unittest discover -s tests -v` | PASS - 22 tests, 0 failures / 0 errors (also PASS when running the test file directly) |
| A3 - clean fixture repo bootstrap | `bootstrap.py init ... --apply` plus `bootstrap.py verify` (test suite) | PASS - generated files and SHA-256 manifest |
| A4 - existing repo rule preservation | Existing `AGENTS.md` and `CLAUDE.md` fixture cases | PASS - originals unchanged |
| A5 - fail closed | Dirty state, default branch, symlink, nested repo, non-Git existing project | PASS - blocked before mutation |
| A6 - checks and evals | Empty, successful, failing and unsafe launcher cases | PASS - empty => exit 2; failure => exit 1; real fixture success => exit 0 |
| A7 - installation and upgrade | Codex / Claude / OpenCode paths, repeated install, modified upgrade, backup | PASS - no silent overwrite; backup generated for valid upgrade |
| A8 - offline verification | No model API, network, secrets, CI credentials or production access | PASS - bundle tests do not require them |
| A9 - macOS symlink regression | `PlatformCompatibilityTests` | PASS - OS-level symlink ancestors no longer block a valid project root |

## State definitions

- **Skill bundle implementation:** PASS in local offline fixture tests on macOS / Python 3.13.12.
- **Actual project adoption:** NOT RUN; requires target repository evidence, real tests/CI and human decisions.
- **Live Agent skill discovery:** NOT RUN; paths follow documented conventions, but must be tested in actual Codex/Claude/OpenCode sessions.
- **WorkBuddy host behaviour (T1/T2/T3):** NOT RUN; only static simulation was performed, with `behavior_verification: not_run`.
- **Platform review:** NOT RUN; only a real upload can confirm. Local validators cannot prove platform acceptance.
- **Remote branch protection, production gate and deploy permissions:** UNVERIFIED; the Skill does not provision or approve any of them.
- **LLM-quality Evals:** NOT RUN; the generic deterministic runner is included but intentionally starts with zero cases, so it fails BLOCKED until genuine cases are approved.
- **Python compatibility:** source targets Python 3.9+; exercised here with Python 3.13, not independently matrix-tested across all minor versions.

## Rollback and isolation

For a new project bootstrap, remove **only the paths enumerated in the generated bootstrap manifest** (the ai-sdlc document directory of the target repository) after reviewing any subsequent edits. Do not delete pre-existing project files. A user-scope Skill installation can be removed from its documented destination. Installer upgrades preserve the previous installation under a timestamped backup. Restoration and production rollback were not performed on user systems.

## Evidence and upstream scope

Authoritative source: `references/implementation-standard.md` (its section 8 template prose is explanatory; the shipped templates under `templates/` are the single source of truth). See `references/adapters-and-safety.md` for cross-tool directory conventions and boundaries. **Passing this bundle's tests does not authorize a production release nor prove a repository meets D01-D08.**
