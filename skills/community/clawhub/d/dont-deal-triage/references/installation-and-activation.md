# Installation and activation

This repository should be treated as a portable skill source, not as one host's exclusive format.

## Practical model

- installation: download or clone the skill bundle to local disk
- activation: depends on the host that is currently running
- packaging: this skill should remain runnable from inside its own folder without depending on repo-root source files

So yes, one local copy can back multiple hosts, but each host still decides when and how that skill becomes available.

## Host notes

- Codex:
  `SKILL.md` is the core unit. Codex-style skills can also include `agents/openai.yaml` for richer UI metadata, but the behavior should live in `SKILL.md` and references.

- Claude Code:
  treat this repository as the source bundle and wrap it with Claude Code's own skill or prompt registration mechanism. The reasoning instructions should stay host-neutral.

- OpenClaw:
  OpenClaw loads workspace `skills/` directories and its official docs describe skills as folders centered on `SKILL.md`. ClawHub is the hosted package index and uses the same general idea: a reusable skill bundle that can be installed locally, versioned, and discovered.

## npm vs skill install

OpenClaw skills are not primarily installed through `npm install <skill>`.

- `npm i -g clawhub` installs the ClawHub CLI
- `clawhub install <skill-slug>` installs the skill bundle into a local skills directory
- this skill bundle includes a local `package.json` only so its Node scripts run cleanly after installation

## Design implication

Keep one canonical source of truth:

- shared prompt and safety rules in `skills/dont-deal-triage/`
- bundled runtime scripts in `skills/dont-deal-triage/scripts/`
- repo-root `src/` can still exist for full-repo development, but ClawHub publication should not depend on it
