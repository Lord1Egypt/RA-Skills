# Live Mode

Live verification is a **secondary follow-up workflow**.
Use it only after the static audit has already narrowed the risk area.

## When to use

Use live mode only when:
- the static audit already identified a narrow set of suspect endpoints
- runtime confirmation is needed in dev/staging
- side effects are acceptable
- test credentials and cleanup expectations are explicit

## When not to use

Do not use live mode for:
- production write tests
- guaranteed rollback workflows
- broad exploratory QA
- systems with sensitive external integrations unless those are isolated

## Current tool

```bash
python3 scripts/generate_tests.py --config config.json --read-only
```

This tool remains available, but it is not the primary entrypoint of the skill.
Treat it as an experimental helper for targeted dev/staging follow-up checks only.
If you need repeatable real API regression coverage, keep using your dedicated QA test suite such as `workspace-qa/tests/`.

## Operational stance

- static audit comes first
- live verification is opt-in
- write testing is risk-bearing
- cleanup is best-effort only
