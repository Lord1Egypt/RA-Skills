# Agent Slim

A reversible "checkup + diet" for agents that have been in use for a while: find what actually occupies every-turn context, move low-frequency material into on-demand storage, and prove key behaviour still works.

## Quick start (5 minutes)

1. Scope it: which agent, which skills, what must not be touched.
2. Read-only audit: `python3 scripts/agent_slim.py audit --json` (auto-detects CODEX_HOME, or pass `--home`). Nothing is modified.
3. Build a plan: `python3 scripts/agent_slim.py plan --audit audit.json`. Items without hash or confirmation evidence stay pending.
4. Reversible apply: `apply` is dry-run by default; `--apply` moves allowlisted files into a transaction directory outside the home, with manifest, SHA-256 and restore script.
5. Verify and restore: `verify` checks preserved files, references, frontmatter and optional test prompts; `restore --apply` is idempotent and stops on conflicts.

## Three layers

- **Hot** — resident rules, descriptions and tool docs. Shrinking them can cut per-turn tokens.
- **Warm** — skill bodies and references loaded only on trigger. Token savings count only when loading is actually avoided.
- **Cold** — archives, backups, old sessions. Disk savings only; never reported as token savings.

## Safety

Dry-run by default; three move actions only (quarantine redundant backup, archive verified old session, quarantine confirmed low-frequency skill file). No deletion, no VACUUM, no secret/provider changes, no upload of company data. Conflicts stop the run and never overwrite user content.

## Pre-publish injection gate

Before publishing any new or changed skill:

```sh
python3 scripts/injection_state.py --record
python3 scripts/injection_state.py --check      # must be overall: OK
python3 scripts/measure_prompt.py --gate 57344  # text blocks must PASS
python3 scripts/self_test.py                    # must be ALL PASS
```

Limits: description ≤45 characters, `SKILL.md` target ≤8 KB, text blocks ≤57,344 bytes, and both `check_integration` and `check_release` must pass. `UNMEASURED` is not PASS; `UNKNOWN` is not supported.

## Status

v0.3.0 is the public version. It keeps the 0.2.0 read-only injection measurement and pre-publish gate, and makes the host layer configurable: describe any agent with `layout.json` instead of shipping code for it. Codex is the first host with an audit/plan/apply/verify/restore implementation verified on a synthetic aging fixture; real-host trigger regression is still `PARTIAL` until executable test prompts are supplied. Other agents are supported through a layout description (see `schemas/layout.schema.json`) or the shared adapter interface. Install from GitHub Releases, `skillhub install agent-slim --namespace user_43faedd6`, or `clawhub install agent-slim`.

## Documentation

`docs/usage.md` (commands), `docs/execution-contract.md` and `docs/audit-json-contract.md` (contracts), `docs/architecture.md`, `docs/safety.md`, `docs/injection-measurement.md` (injection measurement), `docs/acceptance.md`, `references/routing-index.md` (routing), `CHANGELOG.md`.

License: MIT. Platforms: macOS, Windows, Linux (Python 3.9+, standard library only).
