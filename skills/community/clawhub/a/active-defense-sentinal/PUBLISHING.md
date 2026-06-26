# clawhub.ai publication copy

## Listing title
Active Defense Sentinal

## Short description
Defensive triage for OpenClaw, Hermes Agent, the local host, and OpenClaw skill-supply-chain scanning.

## Long description
Active Defense Sentinal is a policy-first defensive skill scaffold for agent operators who want bounded, auditable protection across sessions, host integrity, and skill installation workflows.

It helps with:
- prompt injection and unsafe instruction detection
- OpenClaw UI, gateway, and session health checks
- Hermes profile, tool, cron, and MCP checks
- local host anomaly detection with read-only defaults
- OpenClaw skill-supply-chain scanning before install or activation
- quarantine handling for already-installed skills when policy allows it

The skill is designed to preserve evidence, avoid silent remediation, and separate verified facts from suspicion before recommending the safest next step. The package now includes executable helper scripts for local scanning, staged ClawHub installs, quarantine workflows, and adapter health checks.

## Suggested tags
openclaw, hermes, security, defense, triage, host, integrity, skill-scanner

## Security posture statement
This skill is read-only by default. It does not attempt stealth, persistence, or destructive remediation. High/Critical skill-scan findings are blocked by default, and quarantine is limited to already-installed skills in the active OpenClaw skill tree.

## Recommended install / usage note
Use this skill as a safety layer before acting on untrusted content, before changing the local host, and before installing new OpenClaw skills.

## One-line promotional copy
A defensive control plane for OpenClaw, Hermes, and the local host, with skill-supply-chain scanning built in.
