# Active Defense Sentinal

Defensive triage helpers for OpenClaw, Hermes Agent, host telemetry, and skill
supply-chain screening. Read-only diagnostics are separate from explicitly
requested installation, replacement, and quarantine actions.

## Current OpenClaw integration

```bash
python3 scripts/sentinal.py openclaw-health
python3 scripts/sentinal.py openclaw-health --profile work --timeout 2500
python3 scripts/sentinal.py auto-scan
python3 scripts/sentinal.py scan-install-local /path/to/candidate
```

Gateway health uses `openclaw health --json`, not a hardcoded Chrome debugging
port. Browser checks remain available as `browser-health --endpoint URL`.
State/home/profile/workspace overrides are respected. Scanner errors and unknown
report formats fail closed, including under `--force`.

The helper reports observations, not a verdict that your clone, host, session,
or skills are clean. `ok: true` means the Gateway RPC returned a snapshot; it
does not establish channel health or security. CLI and scanner executables must
be separately reviewed and trusted before use.

See [SKILL.md](SKILL.md) for command semantics, environment overrides, policy,
coverage boundaries, and quarantine requirements. See
[COMPATIBILITY.md](COMPATIBILITY.md) for the exact upstream baseline and test
limits. `references/` and `examples/` provide additional triage guidance.

## Tests and packaging

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

The tests are offline with mocked scanner, OpenClaw, and ClawHub calls. They do
not install dependencies, contact a live Gateway, or execute candidate skills.
Runtime and current compatibility documentation are mirrored in
`dist/active-defense-sentinal-clawhub/`. This change is unreleased; it does not
publish to ClawHub or create a release. Review `PUBLISHING.md` before publication.
