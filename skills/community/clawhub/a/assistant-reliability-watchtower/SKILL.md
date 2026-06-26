---
name: assistant-reliability-watchtower
description: Deterministic reliability monitoring for OpenClaw assistant workflows. Use when you need to run ARW smoke probes, generate a daily digest, validate scorecard evidence, render a delivery preamble, inspect current probe/reporting coverage, or package ARW as an operator-facing reliability skill.
---

# Assistant Reliability Watchtower

Run ARW through the repo-backed wrapper instead of rediscovering commands by hand.

## Quick start

Use `scripts/arw_skill.py` from this skill for the common flows:

- `python3 scripts/arw_skill.py smoke`
- `python3 scripts/arw_skill.py digest`
- `python3 scripts/arw_skill.py verify-scorecard-evidence`
- `python3 scripts/arw_skill.py verify-scorecard-preamble`

The wrapper accepts `--repo-root` (or `ARW_REPO_ROOT`) so repo location stays explicit outside the skill contract, and it exports `PYTHONPATH` correctly.

## Workflow

1. Read `references/release-contract.md` for scope, release posture, and anti-goals.
2. Read `references/probe-catalog.md` when you need to explain what ARW currently watches.
3. Read `references/config-contract.md` when you need to set thresholds, artifact location, or delivery evidence values.
4. Point the wrapper at the checked-out ARW repo with `--repo-root /path/to/arw-watchtower` when autodetection is not enough.
5. Use `scripts/arw_skill.py` for the common operational paths.
6. Keep writes inside the configured ARW repo and `artifacts/arw/**`.

## Common tasks

### Run smoke probes

```bash
python3 scripts/arw_skill.py smoke
```

### Generate a digest

```bash
python3 scripts/arw_skill.py digest --window-hours 24
```

### Run the validation evidence drill

```bash
python3 scripts/arw_skill.py verify-scorecard-evidence
```

### Render the final operator preamble

```bash
python3 scripts/arw_skill.py verify-scorecard-preamble
```

## Notes

- This RC surface is intentionally repo-backed for now. It is an internal release candidate, not a marketplace-polished public release.
- `verify-scorecard-evidence` and `verify-scorecard-preamble` now use skill-level dry-run delivery values instead of inheriting repo-local recipient ids.
- Prefer RC1 work that improves packaging, operator clarity, portability, or high-value probe coverage.
- Avoid expanding the backlog with new micro-gates unless they directly unblock RC1.
