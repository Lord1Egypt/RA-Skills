# Changelog

## 1.1.1

- Requires global `AGENTS.md` context by default before Geordi mission prompts.
- Adds `GEORDI_AGENTS_FILE` and `GEORDI_REQUIRE_AGENTS` controls for portable installs.
- Updates Codex/Droid examples and build-loop reference to document the global context step.

## 1.1.0

- Renames the public bundle and command to `geordi`.
- Merges the reusable geordi build-pipeline discipline into the installable mission runner.
- Adds sanitized references for the build loop and Geordi builder identity.
- Keeps Codex and Droid modes, goal/mission state, acceptance checks, receipts, and resumable logs.

## 1.0.0

- Initial public installable mission-runner bundle.
- Adds install script, CLI, Codex mode, Droid mode, goal/mission state, acceptance checks, and examples.
- Sanitized for public reuse: no private hostnames, private IPs, operator names, account-specific model IDs, or secrets.
