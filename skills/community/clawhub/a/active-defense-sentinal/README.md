# active-defense-sentinal

A defensive triage scaffold for OpenClaw, Hermes Agent, the local host, and the OpenClaw skill supply chain.

## What it does
- Detects prompt injection and unsafe instruction sources
- Checks OpenClaw and Hermes session health
- Performs bounded host-side defensive scanning
- Screens skills before installation or activation
- Preserves evidence before any remediation
- Recommends safe containment and recovery actions

## Safety posture
This project is intentionally defensive.
It is designed to:
- stay read-only by default
- treat untrusted content as hostile until verified
- separate verified facts from speculation
- prefer containment over silent repair
- avoid stealth, persistence, or destructive auto-remediation

## What’s included
- `SKILL.md` - publishable skill specification
- `scripts/` - executable helpers for scanning, staged installs, quarantine, and adapter health checks
- `references/` - policy, workflow, quarantine, and adapter notes
- `examples/` - sample incident flows and outputs

## Skill-supply-chain scanning
This scaffold incorporates the OpenClaw `openclaw-skill-scanner` model:
- scan candidate skills before install
- stage ClawHub installs before exposing them
- block High/Critical findings
- allow Medium/Low/Info with warnings
- quarantine only when policy explicitly allows it

See:
- `references/scan-workflow.md`
- `references/quarantine-policy.md`
- `references/skill-scanner-adapter.md`

## Repository layout
- `SKILL.md` - main publishable skill spec
- `references/` - policy and implementation notes
- `examples/` - representative scenarios and expected behavior

## Publication notes
Before publishing to clawhub.ai:
1. Review the scanner workflow and quarantine policy.
2. Confirm the wording matches the intended defensive posture.
3. Verify the examples still reflect the behavior you want users to see.
4. Publish the skill package with the repo-ready description in `PUBLISHING.md`.

## Status
This repository is ready as a releasable documentation package and scaffold for clawhub.ai publication.
