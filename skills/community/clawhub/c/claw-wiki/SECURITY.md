# Security Notes

`claw-wiki` is a documentation reference and snapshot-maintenance skill for OpenClaw. It is intentionally scoped to local documentation lookup plus bounded refresh of the bundled docs snapshot.

## Intended capability

- Answer OpenClaw questions from checked-in local docs under `openclaw_docs/`
- Verify snapshot freshness from `state/source-lock.json`
- Refresh the docs snapshot from the upstream OpenClaw documentation source when explicitly requested
- Rebuild derived metadata in `state/`

## Explicit non-goals

- General-purpose shell execution
- Arbitrary repository mirroring
- Secret discovery or credential extraction
- Uploading local files to external services
- Pushing changes to remotes, opening PRs, or mutating upstream repositories
- Running install commands copied from documentation examples

## Trust boundaries

- Upstream OpenClaw docs are treated as read-only source content
- Local writes are limited to this skill directory
- The skill should not inspect unrelated user files, credential stores, shell profiles, or environment secrets

## Data handling rules

- Documentation may contain example tokens, API key names, passwords, or bearer auth examples
- Those examples are documentation text, not credentials to use or extract
- The skill must not claim to have validated or used any credential value unless the user separately provides it for another task

## Operational constraints

- Refresh mode should only run after an explicit user request
- Sync scope should be limited to documentation files and `docs.json`
- Validation and diff generation should run after sync before claiming success
- If source contents fall outside the expected OpenClaw docs layout, the refresh should stop and report the mismatch

## Review guidance

When reviewing this skill for safety, focus on whether it remains:

- bounded to OpenClaw documentation sources
- bounded to local snapshot maintenance outputs
- unable to push, exfiltrate, or execute arbitrary downloaded content

That boundary is the intended safety model for this skill.
