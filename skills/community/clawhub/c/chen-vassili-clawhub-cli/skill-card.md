## Description:

Help developers manage OpenClaw skills with the ClawHub CLI. Use when publishing, inspecting, installing, updating, syncing, or troubleshooting ClawHub skills. Also covers auth, workdir behavior, and exact command templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cs995279497-byte](https://clawhub.ai/user/cs995279497-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, skill authors, ClawHub publishers, and OpenClaw users use this skill to install, inspect, update, publish, sync, authenticate, and troubleshoot skills with the ClawHub CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Token login examples can expose credentials if users paste or store tokens carelessly.

Mitigation: Treat ClawHub tokens as secrets and prefer interactive login when available.

Risk: Bulk update and sync commands can change multiple local or published skills at once.

Mitigation: Review bulk commands before running them and use dry-run workflows where available.

## Reference(s):

- [ClawHub CLI documentation](https://docs.openclaw.ai/tools/clawhub)
- [ClawHub skill page](https://clawhub.ai/cs995279497-byte/skills/chen-vassili-clawhub-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Concise command-first guidance for ClawHub CLI workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
